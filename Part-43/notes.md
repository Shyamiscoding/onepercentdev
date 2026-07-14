# Part 43 — OOP Intro (2): Why We Need Classes → What "OOP" Is

In Part 42 we drew the big picture: a **class is a job role**, an **object is an employee**, and a class is your **own data type**. Now the concrete **why**, then the mechanics — proven in code, exactly as in the master deck.

---

## Why We Need Classes

Functions are great — but they have one big pain.

### Problem 1 — A function forgets

A function is a machine: input → output → then it **forgets everything**. It keeps no memory between calls.

```python
def deposit(amount):
    balance = 0            # re-made as 0 EVERY call
    balance += amount
    return balance

print(deposit(500))   # 500
print(deposit(500))   # 500  ← forgot the last one!
```

An object **remembers**:

```python
class Account:
    def __init__(self):
        self.balance = 0   # runs ONCE, at creation

    def deposit(self, amount):
        self.balance += amount
        return self.balance

acc = Account()
print(acc.deposit(500))   # 500
print(acc.deposit(500))   # 1000  ← remembered!
```

The secret is *where* `= 0` runs. In the function it re-runs every call (reset). In the object, `__init__` runs **once**; after that the balance lives inside `acc` and survives.

### Problem 2 — Data, actions, and rules get scattered

Every real thing = **DATA + ACTIONS + RULES**, kept together. With loose functions they drift apart, and nothing enforces the rule:

```python
balance = 1000

def deposit(bal, amount):
    return bal + amount

balance = -9999      # allowed
balance = "oops"     # allowed! nothing protects the data
```

A class bundles all three into one safe unit, and the rule is enforced:

```python
class BankAccount:
    def __init__(self, balance):
        self.balance = balance          # DATA inside

    def deposit(self, amount):          # ACTION with data
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:       # RULE built in
            raise ValueError("Not enough money")
        self.balance -= amount
```

### The pain of functions, in one line

A function only ever **acts on** types that already exist — `int`, `str`, `list`. It can never **add a new one**. A function gives you a **verb** (an action); only a **class** gives you a new **noun** — a brand-new data type. Let us prove that now.

---

## First — Object vs Type vs Data Type

This is the exact spot most learners get lost. Let us settle three words for good.

Every object is **exactly three things**: an **identity**, a **type**, and a **value**. The **methods are not a fourth part** — they live *inside the type*, written once and shared by every object of that type.

```python
nums = [1, 2, 3]
print(type(nums))   # <class 'list'>   ← (1) TYPE      what kind
print(id(nums))     # 140412...        ← (2) IDENTITY  which one / where
print(nums)         # [1, 2, 3]        ← (3) VALUE     the contents

# append, sort, pop ... do NOT live in THIS list —
# they live in the type `list`, shared by every list.
```

A `str` has the same three things but a **different type**, so a **different set of methods** (`upper`, `split`, `replace` ...).

- **Object** = one real thing in memory = identity + type + value.
- **Type** = the "what kind?" answer — the category that holds the shared methods.
- **Data type** = just another name for type. So `type = "what kind" = data type`.

> `dir(x)` prints the full menu a type offers.

---

## Build One — in 4 Tiny Steps

1. **Name it:** `class BankAccount:` — tell Python "a new type is coming."
2. **`__init__`:** gives each object its starting data; runs automatically when an object is made.
3. **`self`:** means "this particular object" — so each account keeps its own data.
4. **Methods:** the actions, with the rule inside.

```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Not enough money")
        self.balance -= amount

acc = BankAccount("Alice", 5000)   # __init__ runs automatically
acc.deposit(500)
print(acc.owner, acc.balance)      # Alice 5500
```

---

## The Reveal: You Just Made Your Own Data Type

```python
print(type([1, 2, 3]))   # <class 'list'>
print(type(acc))         # <class 'BankAccount'>  ← YOUR type, equally real
```

Python treats your `BankAccount` exactly like its built-in `list`. So when you see `class`, do not think "blueprint" — think: **"I am teaching Python a new data type."** This is true even for an empty class (`class Empty: pass` still produces real objects with type + identity + value).

---

## Class vs Object

- **Class** = the design, written once.
- **Object** = a real thing built from it, made many times.

```python
acc1 = BankAccount("Alice", 5000)   # object 1 — its own data
acc2 = BankAccount("Ravi", 2000)    # object 2 — its own data
print(acc1.owner, acc2.owner)       # Alice Ravi — never mixed up
```

One design → many objects: separate data, shared actions. (Same as `list` being the idea and `[1, 2, 3]` being one real list.)

---

## What Really Happens When You Write `class`

`class` is **live code that builds an object**. When Python reaches a `class` block, it runs the body, gathers what you defined into a dictionary, and hands it to a built-in factory called **`type`**, which manufactures the class and stores it under your name.

```python
class Dog:
    legs = 4

# is really shorthand for:
Dog = type("Dog", (), {"legs": 4})
```

So a class is **itself an object**:

```python
print(type(Dog))   # <class 'type'>
```

Two floors: **`type` makes classes, and classes make objects.** (`int`, `str`, `list` were all made by `type` too.)

---

## `__init__` vs `__new__` — Initializer, Not Constructor

People call `__init__` the "constructor." Not quite:

- **`__new__`** → the real **constructor**: it *creates* the empty object and returns it. Runs first.
- **`__init__`** → the **initializer**: it *fills* the object that already exists. Runs second, returns `None`.

`__new__` builds the empty box; `__init__` puts things in it. You almost always write only `__init__` — which is exactly why everyone mistakes it for the constructor.

---

## `self` Is Not Magic (and Not a Keyword)

When you write `acc.deposit(500)`, Python rewrites it as:

```python
BankAccount.deposit(acc, 500)   # the object before the dot becomes the first argument
```

We *name* that first argument `self` — by convention, not law. Whatever sits **before the dot** becomes `self`. So `self` is *this account* (`acc`), **not** the class.

---

## Instance Data vs Class Data (a Famous Trap)

- `self.x = ...` → lives on **that one object**.
- A name in the class body → **shared by all** objects.

```python
class Dog:
    species = "Canis"        # class data — shared by all dogs
    def __init__(self, name):
        self.name = name     # instance data — one per dog
```

**Trap:** a *mutable* class attribute is shared. `tricks = []` in the class body → every dog shares ONE list. Fix: put per-object state in `__init__` → `self.tricks = []`.

---

## Three Kinds of Methods

A **function** stands alone; a **method** is a function inside a class, called on an object. There are exactly **three kinds**, chosen by one question — *what does this job need?*

```python
class BankAccount:
    bank_name = "OnePercent Bank"   # class data — shared by every account
    interest_rate = 5               # class data — shared by every account
    count = 0                       # class data — how many exist so far

    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance
        BankAccount.count += 1

    # INSTANCE · needs THIS account (self)
    def deposit(self, amount):
        self.balance += amount

    # CLASS · needs the class (cls), not one account
    @classmethod
    def savings(cls, owner):            # reason 1: another DOOR to create one
        return cls(owner, 0)            # cls(...) == BankAccount(...) -> new object

    @classmethod
    def set_interest_rate(cls, rate):   # reason 2: a setting shared by ALL accounts
        cls.interest_rate = rate

    @classmethod
    def total_accounts(cls):            # reason 3: a fact about the WHOLE class
        return cls.count

    # STATIC · needs neither self nor cls
    @staticmethod
    def is_valid_amount(amount):        # just numbers in -> answer out
        return amount > 0
```

| The job is about… | Example | Use | First word |
|---|---|---|---|
| one specific object | `alice.deposit(500)` | instance method | `self` |
| creating an object (a new "door") | `BankAccount.savings("Alice")` | class method | `cls` |
| a setting shared by all | `BankAccount.set_interest_rate(7)` | class method | `cls` |
| a fact about the whole class | `BankAccount.total_accounts()` | class method | `cls` |
| numbers in → answer out | `BankAccount.is_valid_amount(500)` | static method | *none* |

Four ideas that make it click:

- **Create first, then use.** You cannot deposit into an account that does not exist — `deposit` needs `self` (a real account). A class method is the "open the account" step: it uses `cls`, so it needs no account yet.
- **`self` / `cls` are written but never passed** — they come from *before the dot*. `BankAccount.savings("Alice")` runs as `savings(BankAccount, "Alice")`.
- **`()` = make a new one · `.` = reach into an existing one.** `cls(owner, 0)` *builds* an account; `cls.interest_rate = rate` *changes shared data* (the twin of `self.balance += amount`).
- **Three kinds, not more.** Dunder methods (`__str__` ...), `@property`, `@abstractmethod` are not a fourth kind — they are *flavors* layered on top, covered in later parts.

Memory hook: `self` → **this one** account · `cls` → **the whole bank** · no first word → **a calculator** inside the class.

---

## So… What Is "OOP"?

When you build your program around such objects — things that carry their own data and actions — you are doing **Object-Oriented Programming**. The order settles the common doubt "class first, or OOP first?":

**class (the tool) → object (the real thing) → apply 4 ideas → = OOP.**

OOP is a **formula: four pillars** applied on top of classes and objects to keep code clean as it scales:

- **Encapsulation** — a wall around the data; touch it only through methods.
- **Abstraction** — hide the messy inside behind a simple surface.
- **Inheritance** — build a new type from an existing one, no copy-paste.
- **Polymorphism** — many types answer the same call their own way (like `len()` on a str, list, or dict).

You have already met all four in Python's own types — OOP is not new magic; it is what Python already does, now in your hands.

---

## Connecting to What You Already Know

You did not start OOP today — you have used objects since Part 5. Every `str`, `list`, and `dict` is an object. Every exception you have ever caught is an object.

In Part 35 you even wrote your own class without thinking of it that way:

```python
class InvalidAgeError(Exception):
    pass
```

`InvalidAgeError` is a **class** built on `Exception`; each `raise InvalidAgeError("...")` makes an **object** of that class. Python has been object-oriented the whole time — the only new thing is that the tools are now in your hands.

---

## Where This Applies in Real Work

- **Django models:** every database table is a class — `class User(models.Model):` — and each row becomes an object.
- **FastAPI request bodies:** incoming JSON is validated into a Python object (a Pydantic model) with attributes.
- **AI agents:** an agent is a class with state (history, model config) and behavior (process input, update memory).
- **Alternative constructors** (`@classmethod`): `datetime.now()`, `dict.fromkeys()`, Django's `Model.objects.create()`.
- **Shared config / counters** (class attributes + class methods): app-wide settings, instance counting, registries.
- **Your own data types**: Pydantic / dataclass models, ORM rows, AI-agent state — all "your own types" that Python treats as first-class.

---

## Practice Assignment

Extend the `BankAccount` class:

1. Add class data `bank_name` and `count` (total accounts created).
2. Add a `@classmethod` `premium(owner)` that opens an account with a starting balance of `1000`.
3. Add a `@staticmethod` `is_valid_amount(amount)` returning whether an amount is positive.
4. Add an instance method `deposit(amount)` that checks `is_valid_amount` before adding.
5. Create 3 accounts (mixing the normal constructor and `premium`), deposit into each, and print `BankAccount.count`.

In a comment, label each method as instance / class / static and write its "first word" (`self` / `cls` / none).

Save as `src/methods_three_kinds.py`.

---

> **Next:** the four pillars of OOP — Encapsulation, Inheritance, Polymorphism, and Abstraction — each with a diagram and runnable code.
