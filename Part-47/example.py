"""
Part 47 — Abstraction
=====================
The SAME Dog / Cat / Cow example carried across all four OOP pillars.
This mirrors the visual walkthrough in `four-pillars-walkthrough.html`.

Run it:   python example.py
"""

from abc import ABC, abstractmethod


# ============================================================
# 1) ENCAPSULATION  —  data + behavior in one capsule; internals protected
# ============================================================
def encapsulation():
    class Dog:
        def __init__(self, name):
            self.name = name          # data the object carries
            self._energy = 100        # internal data — the "_" means "private"

        def speak(self):              # behavior bundled WITH the data
            self._energy -= 10        # only the dog changes its own energy
            return "Woof"

    d = Dog("Rex")
    print(d.speak())                  # Woof
    print(d.name)                     # Rex   (public — safe to read)


# ============================================================
# 2) INHERITANCE  —  hierarchical: one parent, many children
# ============================================================
def inheritance():
    class Animal:                     # the parent — the shared type / family
        def speak(self) -> str:
            return "(some sound)"     # a default

    class Dog(Animal):                # Dog IS-A Animal
        def speak(self):
            return "Woof"

    class Cat(Animal):                # Cat IS-A Animal
        def speak(self):
            return "Meow"

    class Cow(Animal):                # Cow IS-A Animal
        def speak(self):
            return "Moo"

    print(Dog().speak())              # Woof


# ============================================================
# 3) POLYMORPHISM  —  one call, many forms (no if/elif type ladder)
# ============================================================
def polymorphism():
    class Animal:
        def speak(self) -> str:
            return "(some sound)"

    class Dog(Animal):
        def speak(self):
            return "Woof"

    class Cat(Animal):
        def speak(self):
            return "Meow"

    class Cow(Animal):
        def speak(self):
            return "Moo"

    for animal in [Dog(), Cat(), Cow()]:
        print(animal.speak())         # Woof, then Meow, then Moo


# ============================================================
# 4a) ABSTRACTION — WITHOUT it (plain duck typing)
#     Nothing forces speak(). A missing one fails LATE, at call time.
# ============================================================
def without_abstraction():
    class Animal:                     # normal parent — NOTHING forces speak()
        pass

    class Dog(Animal):
        def speak(self):
            return "Woof"

    class Cat(Animal):
        def speak(self):
            return "Meow"

    class Cow(Animal):
        def speak(self):
            return "Moo"

    class Snake(Animal):              # forgot speak() — but nobody stops us!
        pass

    def make_sound(animal):           # no type hint on purpose — this IS duck typing
        return animal.speak()

    for animal in [Dog(), Cat(), Cow()]:
        print(make_sound(animal))     # Woof, Meow, Moo

    # Snake was built with no complaint. The crash only happens HERE, at call time:
    try:
        make_sound(Snake())           # AttributeError — LATE, only when it runs
    except AttributeError as e:
        print("Snake built fine, but crashed LATE ->", e)


# ============================================================
# 4b) ABSTRACTION — WITH it (ABC + @abstractmethod = enforced contract)
#     A missing speak() is caught EARLY — so early the editor flags it too.
# ============================================================
def with_abstraction():
    class Animal(ABC):                # ABC parent — speak() is now REQUIRED
        @abstractmethod
        def speak(self) -> str:       # the contract (return type included)
            ...

    class Dog(Animal):
        def speak(self):
            return "Woof"

    class Cat(Animal):
        def speak(self):
            return "Meow"

    class Cow(Animal):
        def speak(self):
            return "Moo"

    class Snake(Animal):              # forgot speak()
        pass

    for animal in [Dog(), Cat(), Cow()]:
        print(animal.speak())         # Woof, Meow, Moo

    # Snake()  #->  TypeError at CREATION: "Can't instantiate abstract class Snake".
    # We leave it commented because the error is caught SO early that even your
    # editor / type-checker underlines Snake() before you ever run the program.


if __name__ == "__main__":
    steps = [
        ("1) Encapsulation", encapsulation),
        ("2) Inheritance (hierarchical)", inheritance),
        ("3) Polymorphism", polymorphism),
        ("4a) Abstraction — WITHOUT", without_abstraction),
        ("4b) Abstraction — WITH", with_abstraction),
    ]
    for title, demo in steps:
        print(f"\n=== {title} ===")
        demo()
