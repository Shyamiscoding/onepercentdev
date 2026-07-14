# Part 45 — OOP 3 (Inheritance and Composition)

In Part 44, you learned to protect an object's internals with encapsulation and properties. Now we look at how to build new classes on top of existing ones — reusing code without rewriting it.

## Inheritance — Building on Existing Classes

Inheritance lets you create a new class that reuses and extends an existing one:

```python
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def display(self):
        return f"{self.name} ({self.email})"

class Admin(User):
    pass
```

`Admin` inherits everything from `User` without writing any code:

```python
admin = Admin("Shyam", "shyam@example.com")
print(admin.display())   # Shyam (shyam@example.com)
print(isinstance(admin, User))    # True — Admin IS-A User
print(isinstance(admin, Admin))   # True
```

---

## super() — Calling the Parent

When a child class needs its own `__init__` but also wants the parent's initialization:

```python
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class Admin(User):
    def __init__(self, name, email, permissions):
        super().__init__(name, email)   # Call parent's __init__
        self.permissions = permissions

    def display(self):
        perms = ", ".join(self.permissions)
        return f"Admin {self.name} — permissions: {perms}"
```

```python
admin = Admin("Shyam", "shyam@example.com", ["create", "delete", "manage_users"])
print(admin.display())   # Admin Shyam — permissions: create, delete, manage_users
print(admin.email)       # shyam@example.com — inherited from User
```

`super().__init__(name, email)` calls `User.__init__`, ensuring the parent class is properly initialized. Without it, `self.name` and `self.email` would not exist.

---

## Method Overriding

A child class can replace a parent method with its own version:

```python
class User:
    def __init__(self, name):
        self.name = name

    def get_role(self):
        return "member"

class Admin(User):
    def get_role(self):
        return "admin"

class SuperAdmin(Admin):
    def get_role(self):
        return "super_admin"
```

```python
users = [User("Alice"), Admin("Bob"), SuperAdmin("Charlie")]

for user in users:
    print(f"{user.name}: {user.get_role()}")
```

Output:

```
Alice: member
Bob: admin
Charlie: super_admin
```

Each class provides its own version of `get_role()`. Python calls the version belonging to the actual object type.

---

## When Inheritance Makes Sense — The IS-A Test

Inheritance models an **IS-A** relationship:

- Admin **IS-A** User (makes sense)
- Rectangle **IS-A** Shape (makes sense)
- Car **IS-A** Engine (does not make sense — a car has an engine)

If the IS-A relationship feels natural, inheritance is appropriate. If it feels forced, use composition instead.

---

## Composition — The Preferred Alternative

Composition models a **HAS-A** relationship. Instead of inheriting, an object contains other objects:

```python
class Engine:
    def __init__(self, horsepower):
        self.horsepower = horsepower

    def start(self):
        return f"Engine with {self.horsepower}HP started"

class Car:
    def __init__(self, brand, engine):
        self.brand = brand
        self.engine = engine   # Car HAS-A Engine

    def start(self):
        return f"{self.brand}: {self.engine.start()}"
```

```python
engine = Engine(150)
car = Car("Toyota", engine)
print(car.start())   # Toyota: Engine with 150HP started
```

The `Car` does not inherit from `Engine`. It contains an `Engine` object. This is more flexible — you can swap engines, have multiple engines, or change the engine type without modifying the `Car` class.

### Why Prefer Composition

```python
class Car:
    def __init__(self, brand):
        self.brand = brand

# Inheritance — tightly coupled
class ElectricCar(Car):      # What if Car changes? ElectricCar might break.
    pass

# Composition — loosely coupled
class ElectricCar:
    def __init__(self, brand, battery, motor):
        self.brand = brand
        self.battery = battery   # HAS-A Battery
        self.motor = motor       # HAS-A Motor
```

Composition allows mixing and matching components. Inheritance forces a rigid hierarchy. The engineering principle is: **prefer composition over inheritance** unless there is a clear IS-A relationship.

---

## A Real-World Example — Notification System

```python
class EmailSender:
    def send(self, to, message):
        print(f"Email to {to}: {message}")

class SMSSender:
    def send(self, to, message):
        print(f"SMS to {to}: {message}")

class NotificationService:
    def __init__(self, sender):
        self.sender = sender   # HAS-A sender (composition)

    def notify(self, user, message):
        self.sender.send(user, message)
```

```python
email_service = NotificationService(EmailSender())
sms_service = NotificationService(SMSSender())

email_service.notify("alice@example.com", "Your order shipped")
sms_service.notify("+91-9876543210", "Your OTP is 4523")
```

The `NotificationService` does not know or care whether it is sending an email or SMS. It just calls `self.sender.send()`. You can add `PushNotificationSender`, `WhatsAppSender`, or any other sender without changing `NotificationService`.

---

## Multiple Inheritance (Awareness)

Python supports inheriting from multiple classes:

```python
class Loggable:
    def log(self, message):
        print(f"[LOG] {message}")

class Serializable:
    def to_dict(self):
        return self.__dict__

class User(Loggable, Serializable):
    def __init__(self, name, email):
        self.name = name
        self.email = email
```

```python
u = User("Alice", "alice@example.com")
u.log("User created")            # [LOG] User created
print(u.to_dict())                # {'name': 'Alice', 'email': 'alice@example.com'}
```

### Method Resolution Order (MRO)

When multiple parent classes define the same method, Python follows the **MRO** to decide which one to call:

```python
print(User.mro())
# [User, Loggable, Serializable, object]
```

Python searches left to right through the MRO chain. Be aware of this, but avoid complex multiple inheritance hierarchies — they create confusion. Composition is usually a better solution.

---

## Inheritance You Have Already Used

The exception hierarchy from Part 34:

```
Exception
├── ValueError
├── TypeError
├── KeyError
└── FileNotFoundError
```

Every exception inherits from `Exception`. When you wrote `class InvalidAgeError(Exception):` in Part 35, you used inheritance — `InvalidAgeError` IS-A `Exception`.

---

## Where This Applies in Real Work

- **Django class-based views:** Views inherit from base classes (`ListView`, `CreateView`) and override methods like `get_queryset()` to customize behavior.
- **Exception hierarchies:** Custom exception trees use inheritance. `class PaymentError(Exception)`, `class InsufficientFundsError(PaymentError)`.
- **AI model architectures:** PyTorch models inherit from `nn.Module`. You override `forward()` to define how data flows through the model.
- **Plugin systems:** A base `Plugin` class defines the interface. Each plugin inherits and implements its behavior.
- **Composition in microservices:** Services compose database clients, cache clients, and API clients instead of inheriting from them.

---

## Practice Assignment

Build a shape system using both inheritance and composition:

1. Create a `Shape` base class with:
   - Method `area()` that returns 0 (default)
   - Method `describe()` that returns `"Shape: area = {area}"`

2. Create child classes:
   - `Rectangle(width, height)` — overrides `area()`
   - `Circle(radius)` — overrides `area()` (use `3.14159 * radius ** 2`)
   - `Triangle(base, height)` — overrides `area()`

3. Create a `Canvas` class (composition):
   - `_shapes` list
   - Method `add_shape(shape)`
   - Method `total_area()` — sum of all shapes' areas
   - Method `largest_shape()` — returns the shape with the biggest area
   - Method `summary()` — prints each shape's description and the total area

4. Add various shapes to a canvas and print the summary

Save as `src/shape_system.py`.

---

> **Next:** Part 46 — OOP 4. Polymorphism, duck typing, and abstract base classes — designing flexible systems that work with any object that has the right behavior.
