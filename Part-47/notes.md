# Part 47 — OOP 5 (Abstraction and Interfaces)

In Part 46, you saw polymorphism and duck typing — many objects, one interface, different behavior. That raises a question we skipped: *how do you define and guarantee that "one interface" in the first place?* That is the fourth and final pillar — **abstraction**: hiding complexity behind a simple surface, and defining the contracts that make polymorphism safe.

## What Abstraction Really Means

Abstraction is focusing on **what** something does, while hiding **how** it does it.

You met the idea back in Part 42 with the restaurant menu: you order *"Paneer Butter Masala"* and it arrives — you never see the kitchen. The menu is the abstraction. The cooking is the hidden implementation.

You already *use* abstraction constantly without thinking about it:

```python
len("hello")           # You call it. You have no idea how CPython counts characters.
sorted([3, 1, 2])      # Timsort runs inside. You just get a sorted list.
requests.get(url)      # Sockets, TLS, HTTP parsing — all hidden behind one call.
```

Each of these exposes a **simple surface** and hides a **complex interior**. That is abstraction from the *user's* side. The other half of this pillar is designing that surface yourself — deciding what your class promises to the outside world.

---



## Abstraction vs Encapsulation — The Classic Confusion

These two pillars are constantly mixed up. They are related but not the same:


|              | Encapsulation (Part 44)               | Abstraction (this part)                    |
| ------------ | ------------------------------------- | ------------------------------------------ |
| **Hides**    | the **data** / internal state         | the **complexity** / implementation        |
| **Question** | "Who can touch this variable?"        | "What is the essential interface?"         |
| **Tool**     | `private`, name-mangling, `@property` | methods, abstract base classes, interfaces |
| **Goal**     | protect internal state from misuse    | expose only what matters, hide the rest    |


Think of a car. **Encapsulation** is the sealed engine bay — you cannot reach in and change the fuel mixture. **Abstraction** is the steering wheel and pedals — a simple interface that hides the enormous complexity underneath. Encapsulation is one of the *tools* you use to *achieve* abstraction.

---



## A Simple Abstraction — Hide the Mess Behind a Method

Before contracts, the everyday form: wrap messy steps behind a clean method so callers never see the details.

Take the `BankAccount` from Part 44. Withdrawing money is really several steps — check the amount, check the balance, update it, log the transaction. The caller should not have to juggle all that; they just want to *withdraw*:

```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self._balance = balance

    def withdraw(self, amount):
        # The caller sees only .withdraw(). All of these steps stay hidden:
        self._check_amount(amount)
        self._check_funds(amount)
        self._balance -= amount
        self._record(amount)
        return self._balance

    def _check_amount(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")

    def _check_funds(self, amount):
        if amount > self._balance:
            raise ValueError("Insufficient funds")

    def _record(self, amount):
        print(f"Logged: {self.owner} withdrew ₹{amount}")
```

```python
acc = BankAccount("Ada", 1000)
print(acc.withdraw(300))
# Logged: Ada withdrew ₹300
# 700
```

The caller writes one line — `acc.withdraw(300)`. The amount check, the balance check, the update, and the logging are all abstracted away behind `withdraw()`. The three `_helper` methods are the hidden "how"; `withdraw()` is the simple "what."

This is also where the two pillars meet: in Part 44 you used **encapsulation** to guard `_balance` from being changed directly; here you use **abstraction** to hide the *steps* of changing it behind one clean method. Same class — two different jobs.

---



## Abstract Base Classes (ABC) — Defining a Contract

Remember the cliffhanger from Part 46? `make_sound("not an animal")` did not complain until `animal.speak()` actually ran — the rule *"every animal must have* `.speak()`*"* lived only in our heads. Abstraction fixes that by defining an **interface**: a promise of *what methods must exist*, without saying how. Python does this with **Abstract Base Classes** from the `abc` module.

```python
from abc import ABC, abstractmethod


class Animal(ABC):
    @abstractmethod
    def speak(self):
        """Every animal must be able to speak — each in its own way."""
```

`Animal` writes the contract down — every animal *must* have `speak()` — but gives no implementation. Two rules now apply:

**1. You cannot instantiate an abstract class:**

```python
a = Animal()
# TypeError: Can't instantiate abstract class Animal with abstract method speak
```

There is no such thing as a generic "animal" — only concrete ones. The ABC enforces exactly that.

**2. A subclass must implement every abstract method — or it stays abstract too:**

```python
class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"


print(Dog().speak())   # Woof!
print(Cat().speak())   # Meow!
```

These are the same `Dog` and `Cat` from Part 46 — but now they are *guaranteed* to have `speak()`, because the base class refuses to let them exist without it.

If a subclass forgets the method:

```python
class Snake(Animal):
    def __init__(self, length):
        self.length = length
    # Forgot speak()!

s = Snake(120)
# TypeError: Can't instantiate abstract class Snake with abstract method speak
```

This is the payoff. In Part 46, a missing `speak()` stayed silent until the line `animal.speak()` finally ran — perhaps hours into a job. Here the error fires the **moment you try to create the object** — right next to the mistake, before any real work begins. That early failure is the whole point of abstraction.

---



## Why ABCs Beat Plain Duck Typing

That `Snake` demo captured the whole shift — from *trusting* an interface to *guaranteeing* it. Written down as an ABC, the interface gives you three things plain duck typing cannot:

- **Enforced contract** — a subclass literally cannot exist without implementing the interface.
- **Self-documenting** — reading the ABC tells you exactly what any implementation must provide.
- **Fails fast** — the error appears at object creation, next to the bug, not in a stack trace three files away.

---



## Side by Side — Without vs With Abstraction

Here is the *same* `Dog` and `Cat` in both worlds. Read the commented block first (the old, trusting way), then the live code below it (the enforced way):

```python
# ---------- WITHOUT abstraction (plain duck typing) ----------
# Nothing forces speak() to exist — we just TRUST every animal has it.
#
# class Dog:
#     def speak(self): return "Woof!"
#
# class Cat:
#     def speak(self): return "Meow!"
#
# class Snake:                 # forgot speak() — but nobody stops us
#     pass
#
# def make_it_speak(animal):
#     return animal.speak()    # Snake has no speak(): explodes only
#                              # when make_it_speak(Snake()) actually runs (late)


# ---------- WITH abstraction (the interface, enforced) ----------
from abc import ABC, abstractmethod

class Animal(ABC):             # the interface: "every animal MUST have speak()"
    @abstractmethod
    def speak(self): ...

class Dog(Animal):
    def speak(self): return "Woof!"

class Cat(Animal):
    def speak(self): return "Meow!"

class Snake(Animal):           # forgot speak()
    pass

def make_it_speak(animal):
    return animal.speak()

print(make_it_speak(Dog()))    # Woof!
print(make_it_speak(Cat()))    # Meow!
# Snake()  ->  TypeError at CREATION: must implement speak()  (caught early)
```

Same animals, same `speak()`. The only thing added is the **interface** — written down as `Animal(ABC)`. That one change moves the `Snake` failure from *late* (when `speak()` is finally called) to *early* (the moment you try to build it).

---



## Concrete Methods in an ABC — The Template Method

An abstract class can also contain **fully implemented** methods that build on the abstract ones. The base class defines the *skeleton* of a workflow; subclasses fill in the *steps*.

Recall the payment processors from Part 46 — `CreditCard`, `UPI`, `NetBanking` — each carried its own `charge()`, but nothing *guaranteed* it and every one had to repeat its own validation. Turn that loose duck-typed group into an enforced contract, and the shared work can live in the base class:

```python
from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    @abstractmethod
    def charge(self, amount):
        """Subclasses define HOW money is charged."""

    def process(self, amount):
        # Concrete workflow shared by ALL processors:
        print(f"Validating amount ₹{amount}")
        if amount <= 0:
            raise ValueError("Amount must be positive")
        result = self.charge(amount)      # the abstract step
        print(f"Logging transaction: ₹{amount}")
        return result


class UPIProcessor(PaymentProcessor):
    def charge(self, amount):
        print(f"Charging ₹{amount} via UPI")
        return True
```

```python
UPIProcessor().process(500)
# Validating amount ₹500
# Charging ₹500 via UPI
# Logging transaction: ₹500
```

Every processor gets the same validation and logging for free and only supplies the one part that differs. This is the **Template Method** pattern — a direct payoff of abstraction.

---



## Protocol — Structural Typing (Static Duck Typing)

ABCs are **nominal**: a class must *explicitly inherit* to satisfy the contract. Python 3.8+ adds `Protocol`, which is **structural**: any class that simply *has* the right methods qualifies — no inheritance required. It is duck typing that a type checker can verify.

```python
from typing import Protocol


class Drawable(Protocol):
    def draw(self) -> str:
        ...


def render(item: Drawable) -> None:
    print(item.draw())


class Button:                 # note: does NOT inherit Drawable
    def draw(self) -> str:
        return "[ Button ]"


render(Button())              # [ Button ] — it just needs a draw() method
```

`Button` never mentions `Drawable`, yet it satisfies it because it has a matching `draw()`. Type checkers like **mypy** and **pyright** verify this at check-time; at runtime it behaves like normal duck typing.

---



## Choosing Your Abstraction Tool


| Approach        | Enforcement               | Use When                                                                 |
| --------------- | ------------------------- | ------------------------------------------------------------------------ |
| **Duck typing** | none (trust)              | small scripts, quick internal code                                       |
| **ABC**         | runtime, on instantiation | frameworks/libraries where subclasses must obey a contract               |
| **Protocol**    | static, at type-check     | large typed codebases; you want the contract without forcing inheritance |


All three deliver abstraction. Pick the weakest one that still gives you the safety you need.

---



## Where This Applies in Real Work

- `collections.abc`**:** Python's own `Iterable`, `Iterator`, `Sequence`, and `Mapping` are ABCs. When you implemented `__iter__` or `__len__`, you were satisfying these abstract interfaces.
- **PyTorch / Keras:** `nn.Module` is effectively an abstract base — you must implement `forward()`. The framework calls your method through the abstraction.
- **Django & DB drivers:** The DB-API (PEP 249) defines an abstract interface every database driver implements, so your code works the same against SQLite, Postgres, or MySQL.
- **File-like objects:** Anything with `.read()` / `.write()` satisfies the "file" abstraction — real files, `io.StringIO`, network sockets — all interchangeable.
- **Plugin systems:** A base `Plugin` ABC declares the required methods; every plugin implements them and the host program depends only on the abstraction.

---



## Practice Assignment

Build a small notification framework driven by abstraction.

1. Create an ABC `Notifier` with:
  - An abstract method `send(self, message) -> bool`
  - A concrete method `notify(self, message)` that prints `"Sending..."`, calls `send()`, and prints `"Sent"` or `"Failed"` based on the returned bool (Template Method).
2. Implement three subclasses — `EmailNotifier`, `SMSNotifier`, `SlackNotifier` — each defining its own `send()`.
3. Prove the contract:
  - Try to instantiate `Notifier()` directly and observe the `TypeError`.
  - Write a subclass that forgets `send()` and observe it cannot be instantiated.
4. Now do it the structural way: define a `Sender` **Protocol** with `send(self, message) -> bool`, and a `WebhookSender` class that satisfies it **without inheriting**. Write a function `broadcast(sender: Sender, messages)` that works with it.
5. In `main()`, loop over a list of different notifiers and broadcast the same message — one interface, many implementations.

Save as `src/notification_framework.py`.

---

