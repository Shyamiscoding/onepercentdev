# Part 44 — OOP 2 (Encapsulation and Properties)

In Part 43, you created your first classes — bundling data and behavior into objects. But right now, anyone can reach into your objects and change their internals. Encapsulation fixes that.

## Encapsulation

Encapsulation means hiding internal details and exposing a clean interface. Users of your class should not need to know — or touch — the internals.

Without encapsulation:

```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

acc = BankAccount("Alice", 5000)
acc.balance = -9999   # Nothing stops this — data is now corrupted
```

Anyone can set `balance` to anything. In a real banking system, this is a catastrophe.

---

## Naming Conventions for Privacy

Python does not have strict private/public keywords like Java or C++. Instead, it uses naming conventions:

### Single Underscore: _private (Convention)

```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self._balance = balance   # "private" by convention

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self._balance += amount

    def get_balance(self):
        return self._balance
```

`_balance` signals to other developers: "Do not access this directly. Use the provided methods." Python does not enforce it — it is a professional convention that everyone follows.

### Double Underscore: __mangled (Name Mangling)

```python
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance

acc = BankAccount(5000)
# print(acc.__balance)           # AttributeError
print(acc._BankAccount__balance)  # 5000 — still accessible, just mangled
```

Python renames `__balance` to `_BankAccount__balance` internally. This prevents accidental name collisions in inheritance, but it is not true security. In practice, single underscore `_` is used far more often than double underscore `__`.

---

## @property — Controlled Attribute Access

`@property` lets you define methods that behave like attributes:

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance

    @property
    def balance(self):
        return self._balance
```

```python
acc = BankAccount("Alice", 5000)
print(acc.balance)   # 5000 — looks like an attribute, but calls the method
# acc.balance = 100  # AttributeError — cannot set (read-only by default)
```

### Property with Setter — Validation on Assignment

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = value
```

```python
acc = BankAccount("Alice", 5000)
acc.balance = 3000    # Works — goes through the setter
print(acc.balance)    # 3000

acc.balance = -100    # ValueError: Balance cannot be negative
```

The caller writes `acc.balance = 3000` — clean, simple syntax. But behind the scenes, the setter validates the value. This is encapsulation in action: a clean interface with protection underneath.

---

## Dataclasses — Reducing Boilerplate

Writing `__init__` for every class gets repetitive:

```python
class User:
    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age
```

Every attribute is written three times. For a class with 10 attributes, this is tedious and error-prone.

### The dataclass Solution

```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    email: str
    age: int
```

That is it. `@dataclass` automatically generates:
- `__init__` — takes `name`, `email`, `age` as parameters
- `__repr__` — gives a readable string representation
- `__eq__` — compares objects by their field values

```python
u1 = User("Alice", "alice@example.com", 25)
u2 = User("Alice", "alice@example.com", 25)

print(u1)          # User(name='Alice', email='alice@example.com', age=25)
print(u1 == u2)    # True — compares field values, not identity
```

### Default Values

```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    email: str
    age: int = 18          # default value
    active: bool = True    # default value
```

```python
u = User("Bob", "bob@example.com")
print(u.age)       # 18
print(u.active)    # True
```

Fields with defaults must come after fields without defaults — same rule as function parameters.

### Mutable Default Fields

Remember the mutable default argument pitfall from Part 25? The same problem exists with dataclasses:

```python
from dataclasses import dataclass, field

@dataclass
class Student:
    name: str
    scores: list = field(default_factory=list)   # Safe — creates a new list for each instance
```

```python
s1 = Student("Alice")
s2 = Student("Bob")
s1.scores.append(95)

print(s1.scores)   # [95]
print(s2.scores)   # [] — independent, not shared
```

`field(default_factory=list)` creates a new list for each object. Without it, all students would share the same list — exactly the bug from Part 25.

### __post_init__ — Validation After Initialization

```python
from dataclasses import dataclass

@dataclass
class Student:
    name: str
    age: int
    email: str

    def __post_init__(self):
        if self.age < 13 or self.age > 120:
            raise ValueError(f"Age must be between 13 and 120, got {self.age}")
        if "@" not in self.email:
            raise ValueError(f"Invalid email: {self.email}")
```

```python
s = Student("Alice", 20, "alice@example.com")   # Works
s = Student("Bob", 5, "bob@example.com")         # ValueError: Age must be between 13 and 120, got 5
```

`__post_init__` runs after `__init__` completes. It is the place for validation logic in dataclasses.

---

## Combining Properties with Dataclasses

```python
from dataclasses import dataclass, field

@dataclass
class Student:
    name: str
    age: int
    scores: list = field(default_factory=list)

    @property
    def average_score(self):
        if not self.scores:
            return 0.0
        return sum(self.scores) / len(self.scores)

    @property
    def grade(self):
        avg = self.average_score
        if avg >= 90:
            return "A"
        elif avg >= 80:
            return "B"
        elif avg >= 70:
            return "C"
        elif avg >= 60:
            return "D"
        return "F"
```

```python
s = Student("Alice", 20, [85, 92, 78, 90])
print(s.average_score)   # 86.25
print(s.grade)           # B
```

Properties let you compute values on demand without storing them. The `average_score` is always calculated from the current `scores` list — it never goes stale.

---

## Where This Applies in Real Work

- **Pydantic models in FastAPI:** Pydantic models are similar to dataclasses but with automatic validation. `class UserCreate(BaseModel): name: str; age: int` — the framework validates incoming API data using these definitions.
- **Configuration objects:** Application config is stored as a dataclass or class with properties. `config.database_url`, `config.debug_mode` — clean access with validation.
- **AI model parameters:** Model configurations (learning rate, batch size, epochs) are encapsulated in config classes with validation.
- **Django model fields:** Django uses properties and descriptors (advanced properties) to validate data before saving to the database.
- **Immutable data:** Use `@dataclass(frozen=True)` to create immutable objects — useful for configuration that should never change after creation.

---

## Practice Assignment

Build a student records system:

1. Create a `Student` dataclass with:
   - `name: str`
   - `age: int`
   - `scores: list` (use `field(default_factory=list)`)
   - `__post_init__` validation: age between 13 and 120
   - `@property average_score` — returns the average of scores (0.0 if empty)
   - `@property grade` — returns A/B/C/D/F based on average
   - Method `add_score(score)` — validates score is 0-100, then appends

2. Create a `Classroom` class with:
   - `_students` list (use the `_` convention)
   - Method `add_student(student)` — adds a Student
   - `@property` `top_student` — returns the student with the highest average
   - Method `class_average()` — returns the average of all students' averages

3. Add 4 students with different scores, find the top student, and print the class average

Save as `src/student_records.py`.

---

> **Next:** Part 45 — OOP 3. Inheritance, composition, and the engineering principle that says "prefer composition over inheritance."
