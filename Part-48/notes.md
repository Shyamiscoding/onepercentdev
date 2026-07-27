# Part 48 — OOP 6 (SOLID Design Principles)

In Parts 42–47 you learned the four pillars — encapsulation, inheritance, polymorphism, and (in Part 47) abstraction. You now have every *tool* OOP offers. But here is the uncomfortable truth: **you can use every tool correctly and still write code that is painful to change.** Knowing the pillars is not the same as knowing how to arrange classes so a system survives years of new requirements.

SOLID is the missing layer. It is five design principles that turn "code that works today" into "code that keeps working as it grows."

---

## First — Is SOLID a Fifth Pillar? Is OOP Part of SOLID?

This confuses almost everyone, so let us settle it before any code.

- **OOP is the paradigm.** It gives you the raw tools: classes, objects, encapsulation, inheritance, polymorphism.
- **SOLID is a set of design principles that sit *on top of* OOP.** It adds no new language features — it tells you *how to use the pillars well* so your classes stay flexible.
- SOLID is **not** a fifth pillar. The pillars describe *what OOP is*; SOLID describes *how to design with it*.
- OOP is **not** "part of" SOLID either — it is the other way around. SOLID is built out of OOP features.

So the relationship is one-directional:

```text
SOLID  →  depends on OOP   (it uses classes, polymorphism, abstraction)
OOP    →  does NOT need SOLID to run
```

> **Analogy:** OOP is knowing **grammar and vocabulary**. SOLID is knowing how to **write clearly** so someone else can read your paragraph and safely edit it. You can be grammatically perfect and still write an unreadable mess — *that* is OOP without SOLID.

**Is OOP alone enough? No.** OOP lets you *create* classes; it does not stop you from writing a 2,000-line **"God class"** that does everything, or a rigid inheritance tree that breaks every time you touch it. SOLID is the **discipline** that prevents exactly those mistakes.

Picture bad code as having four **diseases**: **rigidity** (hard to change), **fragility** (a change breaks unrelated things), **immobility** (nothing can be reused), and **tight coupling** (everything depends on everything). SOLID is the cure — **each of the five principles is a targeted treatment** for one of them.

The acronym comes from **[Robert C. Martin ("Uncle Bob")](https://en.wikipedia.org/wiki/Robert_C._Martin)** — a veteran engineer and co-author of the *Agile Manifesto* — who gathered these principles around 2000; **Michael Feathers** (author of *Working Effectively with Legacy Code*) later rearranged them into the memorable word *SOLID*:


| Letter | Principle                       |
| ------ | ------------------------------- |
| **S**  | Single Responsibility Principle |
| **O**  | Open/Closed Principle           |
| **L**  | Liskov Substitution Principle   |
| **I**  | Interface Segregation Principle |
| **D**  | Dependency Inversion Principle  |


> **Who came up with these? (worth a click)**
>
> - **L — Liskov** is named after **[Barbara Liskov](https://en.wikipedia.org/wiki/Barbara_Liskov)**, an MIT professor and winner of the **2008 [Turing Award](https://en.wikipedia.org/wiki/Turing_Award)**, who stated this rule in a landmark 1987 talk.
> - **What is the Turing Award?** Computer science's highest honour — the **"Nobel Prize of Computing"** (a $1 million prize, awarded every year since 1966 by the ACM). It is named after **[Alan Turing](https://en.wikipedia.org/wiki/Alan_Turing)** (1912–1954), the father of computer science and AI — the man who cracked Nazi Germany's *Enigma* code in WWII and invented the *Turing Machine*, the theoretical blueprint behind every modern computer.
> - **O — Open/Closed** was first described by **[Bertrand Meyer](https://en.wikipedia.org/wiki/Bertrand_Meyer)** in 1988 (creator of the Eiffel language).
> - **S, I, D** were formulated by Uncle Bob himself.

> **One cast, five lessons.** Every principle below is shown with the **same characters** from Part 47 — the `Animal` classes with a `speak()` method (`Dog` → "Woof!", `Cat` → "Meow!"). Each principle gets one tiny **❌ Without** example and one **✅ With** example, so you can see the *exact* line where the principle matters.

---

## S — Single Responsibility Principle (SRP)

> **A class should have only one reason to change.**

**❌ Without SRP** — one `Dog` doing two unrelated jobs (being a dog *and* talking to a database):

```python
class Dog:
    def speak(self):
        return "Woof!"

    def save_to_db(self):          # why does a dog know about databases?
        print("Saving dog to database")
```

Change the database → you edit the `Dog`. Change the sound → you edit the *same* class. Two reasons to change = two responsibilities.

**✅ With SRP** — one job per class:

```python
class Dog:
    def speak(self):
        return "Woof!"

class AnimalRepository:            # its only job is saving
    def save(self, animal):
        print("Saving animal to database")
```

**Conclusion:** one *reason to change* per class. If describing a class makes you say "and", split it.

---

## O — Open/Closed Principle (OCP)

> **Open for extension, closed for modification.** Add new behaviour with *new code*, not by *editing working code*.

**❌ Without OCP** — every new animal forces you to reopen and edit `make_sound()`:

```python
class SoundMaker:
    def make_sound(self, species):
        if species == "dog":
            return "Woof!"
        elif species == "cat":
            return "Meow!"
        # new animal? edit this method AGAIN...
```

**✅ With OCP** — lean on the `Animal` abstraction; add a subclass, touch nothing old:

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self): ...

class Dog(Animal):
    def speak(self): return "Woof!"

class Cow(Animal):                 # NEW animal — SoundMaker never changes
    def speak(self): return "Moo!"

def make_sound(animal: Animal):
    return animal.speak()
```

**Conclusion:** a growing `if/elif` chain is OCP asking for a new subclass.

---

## L — Liskov Substitution Principle (LSP)

> **A subclass must be usable anywhere its parent is expected — without surprising the caller.** IS-A must be *behaviourally* true, not just structurally.

> **Who was Liskov?** [Barbara Liskov](https://en.wikipedia.org/wiki/Barbara_Liskov) — MIT computer scientist and 2008 [Turing Award](https://en.wikipedia.org/wiki/Turing_Award) winner. Her 1987 rule, in plain words: *if `S` is a subtype of `T`, you must be able to use an `S` wherever a `T` is expected — and nothing should break.*

**❌ Without LSP** — `Fish` IS-A `Animal` on paper, but breaks the `speak()` promise:

```python
class Animal:
    def speak(self):
        return "Some sound"

class Fish(Animal):
    def speak(self):
        raise NotImplementedError("Fish can't speak!")   # 💥 any caller of .speak() crashes
```

**✅ With LSP** — only animals that *can* speak inherit `speak()`:

```python
class Animal:
    def move(self):
        return "Moving"

class SpeakingAnimal(Animal):
    def speak(self):
        return "Some sound"

class Dog(SpeakingAnimal):         # speaks — safe to substitute
    def speak(self): return "Woof!"

class Fish(Animal):                # an Animal, but never promises speak()
    def swim(self): return "Swimming"
```

**Conclusion:** if a subclass has to disable or throw on an inherited method, the IS-A is wrong. (Same trap as the textbook `Square` inheriting `Rectangle`.)

---

## I — Interface Segregation Principle (ISP)

> **No class should be forced to implement methods it does not use.** Prefer many small interfaces over one fat one.

**❌ Without ISP** — one fat `Animal` interface forces a `Dog` to fake `fly()`:

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self): ...
    @abstractmethod
    def fly(self): ...

class Dog(Animal):
    def speak(self): return "Woof!"
    def fly(self):
        raise NotImplementedError("Dogs can't fly")   # forced, useless
```

**✅ With ISP** — small, capability-based interfaces; implement only what you can do:

```python
class Speaker(ABC):
    @abstractmethod
    def speak(self): ...

class Flyer(ABC):
    @abstractmethod
    def fly(self): ...

class Dog(Speaker):                # only speaks
    def speak(self): return "Woof!"

class Duck(Speaker, Flyer):        # speaks AND flies
    def speak(self): return "Quack!"
    def fly(self):   return "Flying"
```

**Conclusion:** a fat interface makes classes lie with empty/throwing methods. Split by capability.

---

## D — Dependency Inversion Principle (DIP)

> **Depend on abstractions, not on concrete details.** High-level code should not be nailed to a specific low-level class.

**❌ Without DIP** — `AnimalShow` builds its own `Dog`, so it is locked to dogs forever:

```python
class Dog:
    def speak(self): return "Woof!"

class AnimalShow:
    def __init__(self):
        self.performer = Dog()     # can never be anything but a Dog

    def start(self):
        return self.performer.speak()
```

**✅ With DIP** — depend on `Animal` and *inject* the performer from outside:

```python
# Animal, Dog, Cat as defined in the OCP example above
class AnimalShow:
    def __init__(self, performer: Animal):   # abstraction, injected
        self.performer = performer

    def start(self):
        return self.performer.speak()

AnimalShow(Dog()).start()   # Woof!
AnimalShow(Cat()).start()   # Meow!
```

Passing the dependency in through `__init__` is called **dependency injection**.

**Conclusion:** point dependencies at *abstractions* ("any object with `speak()`"), not concrete classes — that is how real systems swap Stripe for Razorpay without a rewrite.

---

## The Whole Picture — Without vs With, at a Glance


| Principle   | ❌ Without                                  | ✅ With                                      |
| ----------- | ------------------------------------------ | ------------------------------------------- |
| **S** — SRP | `Dog` also saves to the database           | `Dog` speaks · `AnimalRepository` saves     |
| **O** — OCP | `if/elif` on species inside `make_sound()` | `Animal` ABC · add a subclass, edit nothing |
| **L** — LSP | `Fish.speak()` throws                      | only `SpeakingAnimal` has `speak()`         |
| **I** — ISP | one fat `Animal` (speak + fly)             | small `Speaker` / `Flyer` interfaces        |
| **D** — DIP | `AnimalShow` builds `Dog()` inside         | inject any `Animal` through `__init__`      |


Read the left column and you can feel the pain; read the right and you see the cure. That is the entire job of SOLID: **isolate change so tomorrow's requirement touches one small class, not your whole system.**

---

## How SOLID Connects to the Other Design Rules

SOLID does not live alone. It is the backbone of a wider set of design wisdom you have already met:


| Rule                             | Where you saw it       | Relationship                      |
| -------------------------------- | ---------------------- | --------------------------------- |
| **Composition over inheritance** | Part 45                | Makes LSP and DIP practical       |
| **DRY** (Don't Repeat Yourself)  | throughout             | SRP naturally removes duplication |
| **Program to an interface**      | Part 47 (ABC/Protocol) | The heart of OCP and DIP          |
| **Encapsulate what varies**      | Part 44                | Isolate change → OCP              |


### Principle vs pattern 

SOLID is not the only principle, and design patterns are a *different* layer:

- A **principle** is a *rule* for good design. SOLID is the famous set, but not the only one:
  - **DRY** (Don't Repeat Yourself) — every piece of knowledge lives in exactly one place.
  - **KISS** (Keep It Simple) — pick the simplest thing that works; don't over-engineer.
  - **YAGNI** (You Aren't Gonna Need It) — don't build a feature until you actually need it.
  - **Composition over inheritance** — prefer "has-a" (build from parts) over deep "is-a" trees.
- A **pattern** is a *ready-made solution* to a recurring problem — the 23 classic **"Gang of Four"** patterns. Four common ones, each a one-liner + a tiny taste:

**Singleton** — guarantee exactly one instance ever (one config / DB connection).

```python
class Database:
    _instance = None

    @classmethod
    def get(cls):
        if cls._instance is None:      # first time → create it
            cls._instance = Database()
        return cls._instance           # after that → same one

print(Database.get() is Database.get())   # True
```

**Factory** — one helper builds the right object for you.

```python
def make_animal(species):
    if species == "dog": return Dog()
    if species == "cat": return Cat()

make_animal("dog").speak()    # Woof!
```

**Strategy** — swap a behaviour at runtime by injecting a different object.

```python
class AnimalShow:
    def __init__(self, performer):
        self.performer = performer

    def start(self):
        return self.performer.speak()

AnimalShow(Dog()).start()     # Woof!
AnimalShow(Cat()).start()     # Meow!
```

**Observer** — when one object changes, its subscribers are notified automatically.

```python
class Zoo:
    def __init__(self):
        self.watchers = []

    def add_animal(self, name):
        for notify in self.watchers:
            notify(name)

zoo = Zoo()
zoo.watchers.append(lambda n: print(f"New animal: {n}"))
zoo.add_animal("Dog")         # New animal: Dog
```

Principles tell you *what* good design looks like; patterns are proven *recipes* that follow those principles. Both are **language-agnostic** — not Python-only.

---

## Where This Applies in Real Work

- **Django / FastAPI:** dependency injection (DIP) is everywhere — you pass in databases, auth backends, and settings rather than hard-coding them. FastAPI's `Depends()` is DIP as a language feature.
- **Payment & notification systems:** Strategy + DIP let a company support Stripe, Razorpay, UPI, and PayPal behind one interface — the real-world twin of swapping `Dog` for `Cat` in `AnimalShow`.
- **AI / ML pipelines:** a pipeline depends on an abstract `Model` with `.fit()` / `.predict()` (scikit-learn's estimator interface). Swap models without rewriting the pipeline — OCP and LSP in action.
- **Plugin architectures:** ISP + OCP — each plugin implements a small interface; the host grows by adding plugins, never by editing the core.
- **Testing:** DIP is what makes code testable — inject a fake/mock collaborator instead of the real database (you will use this constantly in the Testing parts).

---

## Practice Assignment

Take the animal cast and fix one violation per principle. Keep each example tiny.

1. **SRP** — start with a `Dog` that both `speak()`s and `save_to_db()`s. Split the saving into an `AnimalRepository`.
2. **OCP** — replace a `make_sound()` `if/elif` with an `Animal` ABC and `Dog`, `Cat`, `Cow` subclasses. Adding `Cow` must not edit any existing class.
3. **LSP** — show a `Fish(Animal)` that breaks `speak()`, then fix it with a `SpeakingAnimal` layer so `Fish` never promises `speak()`.
4. **ISP** — show a fat `Animal(speak, fly)` that forces a `Dog` to fake `fly()`, then split into `Speaker` / `Flyer`; give a `Duck` both.
5. **DIP** — make an `AnimalShow` that injects its performer, and run it once with a `Dog` and once with a `Cat` — changing only the object you pass in.

Save as `src/solid_zoo.py`, with a short comment above each pair labelling it `# without` / `# with`.

---

