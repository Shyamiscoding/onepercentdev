# Part 46 — OOP 4 (Polymorphism and Modern Patterns)

In Part 45, you built class hierarchies with inheritance and composition. Now we explore polymorphism — the reason those hierarchies are powerful: different objects, same interface, different behavior.

## Polymorphism — Same Interface, Different Behavior

Polymorphism means different objects respond to the same method call in their own way:

```python
class Dog:
    def speak(self):
        return "Woof!"

class Cat:
    def speak(self):
        return "Meow!"

class Parrot:
    def speak(self):
        return "Squawk!"
```

```python
animals = [Dog(), Cat(), Parrot()]

for animal in animals:
    print(animal.speak())
```

Output:

```
Woof!
Meow!
Squawk!
```

The `for` loop does not know or care what type each `animal` is. It just calls `.speak()`. Each object responds with its own behavior. This is polymorphism.

---

## Why Polymorphism Matters

Without polymorphism:

```python
def make_sound(animal):
    if isinstance(animal, Dog):
        return "Woof!"
    elif isinstance(animal, Cat):
        return "Meow!"
    elif isinstance(animal, Parrot):
        return "Squawk!"
```

Every time you add a new animal, you modify this function. With polymorphism:

```python
def make_sound(animal):
    return animal.speak()
```

Add 100 new animal types — this function never changes. Each type implements its own `.speak()`. This is the power of polymorphism: **open for extension, closed for modification**.

---

## A Real-World Example — Payment Processing

```python
class CreditCard:
    def __init__(self, number):
        self.number = number

    def charge(self, amount):
        print(f"Charging ₹{amount} to credit card ending {self.number[-4:]}")
        return True

class UPI:
    def __init__(self, upi_id):
        self.upi_id = upi_id

    def charge(self, amount):
        print(f"Requesting ₹{amount} via UPI to {self.upi_id}")
        return True

class NetBanking:
    def __init__(self, bank_name):
        self.bank_name = bank_name

    def charge(self, amount):
        print(f"Redirecting to {self.bank_name} for ₹{amount}")
        return True
```

```python
def checkout(processor, amount):
    """Works with any object that has a charge() method."""
    if processor.charge(amount):
        print("Payment successful!")
    else:
        print("Payment failed.")

checkout(CreditCard("4111111111112222"), 999)
checkout(UPI("shyam@upi"), 500)
checkout(NetBanking("SBI"), 2000)
```

`checkout()` does not care how the payment happens. It calls `.charge()` and the specific processor handles the rest.

---

## Duck Typing

"If it walks like a duck and quacks like a duck, it is a duck."

Python does not check types — it checks behavior. If an object has the method you are calling, it works:

```python
class FileLogger:
    def write(self, message):
        print(f"[FILE] {message}")

class ConsoleLogger:
    def write(self, message):
        print(f"[CONSOLE] {message}")

class APILogger:
    def write(self, message):
        print(f"[API] {message}")

def log_event(logger, event):
    logger.write(event)   # Works with ANY object that has .write()
```

```python
log_event(FileLogger(), "User logged in")
log_event(ConsoleLogger(), "Server started")
log_event(APILogger(), "Request received")
```

No inheritance. No shared base class. Each logger is independent. But they all have `.write()`, so they all work with `log_event()`. This is duck typing in action.

---

## The Weakness of Duck Typing — A Bridge to Abstraction

Duck typing is flexible, but it has a gap: if someone passes an object that is *missing* the required method, nothing complains until that method is finally called — possibly deep inside a long-running job.

```python
def make_sound(animal):
    return animal.speak()

make_sound("not an animal")   # AttributeError — but only when it actually runs
```

The fix is to define the interface *explicitly* and enforce it — with **Abstract Base Classes** (`ABC`, `@abstractmethod`) and **Protocols**. That is precisely the fourth pillar, **abstraction**, and it is the whole subject of the next part.

---

## Polymorphism with Built-in Functions

Python's built-in functions use polymorphism. `len()` works with strings, lists, dicts, and any object that defines `__len__()`:

```python
print(len("hello"))      # 5
print(len([1, 2, 3]))    # 3
print(len({"a": 1}))     # 1
```

`+` works differently for numbers and strings:

```python
print(3 + 5)             # 8 — addition
print("hello" + " world") # hello world — concatenation
```

This is operator polymorphism. Different types respond to the same operation in their own way. In Part 49, you will learn how to make your own classes work with `len()`, `+`, `in`, and more.

---

## Where This Applies in Real Work

- **API routing:** FastAPI and Flask route handlers are polymorphic — each endpoint function has different behavior but the framework calls them the same way.
- **AI model serving:** A prediction service accepts any model object that implements `.predict()`. Swap models without changing the serving infrastructure.
- **Plugin architectures:** IDEs, CI/CD tools, and monitoring systems define ABCs for plugins. Each plugin implements the required methods.
- **Payment gateways:** Real payment integrations (Razorpay, Stripe, PayPal) all implement a common interface. The application code is gateway-agnostic.
- **Data sources:** A data pipeline reads from databases, CSV files, or APIs. Each source implements `.fetch_data()`. The pipeline does not care where data comes from.

---

## Practice Assignment

Build a payment system using polymorphism and duck typing (no shared base class):

1. Create three independent classes — `CreditCard(card_number)`, `UPI(upi_id)`, and `Cash()` — each with its own `charge(amount) -> bool`:
   - `CreditCard` / `UPI` — print a charging message, return `True`
   - `Cash` — print cash received, return `True` only if `amount <= 10000`

2. Create a `checkout(processor, items)` function:
   - `items` is a list of dicts with `"name"` and `"price"` keys
   - Calculate the total
   - Call `processor.charge(total)` — it does not care which class it received
   - Print success or failure

3. Test with all three processors and the same item list.

4. Now pass an object that has **no** `charge()` method and notice *when* the error appears — at call time, not before. Keep this in mind: Part 47 shows how abstraction turns that late failure into an early, safe one.

Save as `src/payment_system.py`.

---

> **Next:** Part 47 — OOP 5 (Abstraction and Interfaces). Duck typing trusts that a method exists; abstraction *guarantees* it. Abstract base classes, `@abstractmethod`, and `Protocol` — the contracts that make polymorphism safe.
