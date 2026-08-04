# Part 49 — Dunder Methods (Pythonic Objects)

Through Parts 42-48, you built classes with encapsulation, inheritance, polymorphism, and abstraction, then learned the SOLID principles that keep them clean. Now we unlock how Python's built-in operations — `len()`, `print()`, `==`, `for` — can work with *your* objects.

## What Are Dunder Methods?

Dunder methods (double underscore) are special methods that hook your objects into Python's built-in operations:


| You Write      | Python Calls                        |
| -------------- | ----------------------------------- |
| `len(obj)`     | `obj.__len__()`                     |
| `print(obj)`   | `obj.__str__()` or `obj.__repr__()` |
| `obj[key]`     | `obj.__getitem__(key)`              |
| `item in obj`  | `obj.__contains__(item)`            |
| `obj1 == obj2` | `obj1.__eq__(obj2)`                 |
| `for x in obj` | `obj.__iter__()`                    |
| `obj1 + obj2`  | `obj1.__add__(obj2)`                |


You have already seen `__init__`. Every dunder method makes your object integrate with a Python feature.

---

## **repr** vs **str**

### **repr** — Developer View

`__repr__` returns a string useful for debugging. It should be unambiguous and ideally valid Python:

```python
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"User(name='{self.name}', age={self.age})"
```

```python
u = User("Alice", 25)
print(repr(u))   # User(name='Alice', age=25)
print(u)         # User(name='Alice', age=25) — falls back to __repr__ if no __str__
```



### **str** — User View

`__str__` returns a human-friendly string:

```python
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"User(name='{self.name}', age={self.age})"

    def __str__(self):
        return f"{self.name} (age {self.age})"
```

```python
u = User("Alice", 25)
print(str(u))    # Alice (age 25)       — __str__
print(repr(u))   # User(name='Alice', age=25) — __repr__
print(u)         # Alice (age 25)       — print() uses __str__
```


| Function     | Uses                                      | Purpose                 |
| ------------ | ----------------------------------------- | ----------------------- |
| `repr(obj)`  | `__repr__`                                | Debugging — unambiguous |
| `str(obj)`   | `__str__`                                 | Display — readable      |
| `print(obj)` | `__str__` first, falls back to `__repr__` | Display                 |


**Rule:** Always implement `__repr__`. Implement `__str__` when you want a different, friendlier display.

---



## **len** — Making len() Work

```python
class Playlist:
    def __init__(self, name):
        self.name = name
        self._songs = []

    def add(self, song):
        self._songs.append(song)

    def __len__(self):
        return len(self._songs)

    def __repr__(self):
        return f"Playlist('{self.name}', {len(self)} songs)"
```

```python
p = Playlist("Workout Mix")
p.add("Eye of the Tiger")
p.add("Lose Yourself")

print(len(p))   # 2
print(p)        # Playlist('Workout Mix', 2 songs)
```

Without `__len__`, calling `len(p)` raises `TypeError`. With it, your object works like any built-in collection.

---



## **eq** and **lt** — Comparison Operators



### **eq** — Equality

```python
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __eq__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return self.name == other.name and self.price == other.price

    def __repr__(self):
        return f"Product('{self.name}', ₹{self.price})"
```

```python
p1 = Product("Laptop", 50000)
p2 = Product("Laptop", 50000)
p3 = Product("Phone", 20000)

print(p1 == p2)   # True — compares field values
print(p1 == p3)   # False
print(p1 is p2)   # False — different objects
```

Without `__eq__`, `==` compares identity (same as `is`). With `__eq__`, it compares values.

### **lt** — Less Than (Enables Sorting)

```python
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __lt__(self, other):
        return self.price < other.price

    def __repr__(self):
        return f"Product('{self.name}', ₹{self.price})"
```

```python
products = [Product("Laptop", 50000), Product("Phone", 20000), Product("Tablet", 35000)]
products.sort()   # Uses __lt__ for comparison
print(products)   # [Product('Phone', ₹20000), Product('Tablet', ₹35000), Product('Laptop', ₹50000)]
```

Implementing `__lt__` enables `sort()`, `sorted()`, `min()`, and `max()` to work with your objects.

---



## **getitem** — Bracket Access

```python
class Playlist:
    def __init__(self, name):
        self.name = name
        self._songs = []

    def add(self, song):
        self._songs.append(song)

    def __getitem__(self, index):
        return self._songs[index]

    def __len__(self):
        return len(self._songs)
```

```python
p = Playlist("Road Trip")
p.add("Bohemian Rhapsody")
p.add("Hotel California")
p.add("Stairway to Heaven")

print(p[0])       # Bohemian Rhapsody
print(p[-1])      # Stairway to Heaven
print(p[1:3])     # ['Hotel California', 'Stairway to Heaven'] — slicing works too
```

`__getitem__` makes your object support bracket notation and slicing, just like lists and dictionaries.

---

`__contains__` enables the `in` operator — demonstrated in the `Inventory` class below.

`__iter__` makes `for` loops work with your object — also shown in the `Inventory` class below. We explore the iterator protocol in depth in Part 50.

---



## **add** — Operator Overloading

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"
```

```python
v1 = Vector(1, 2)
v2 = Vector(3, 4)
v3 = v1 + v2

print(v3)   # Vector(4, 6)
```

`+` on your objects calls `__add__`. This is operator overloading — giving operators custom behavior for your types.

---



## A Complete Pythonic Class

Combining multiple dunder methods into one cohesive class:

```python
class Inventory:
    def __init__(self):
        self._items = {}

    def add(self, item, quantity=1):
        self._items[item] = self._items.get(item, 0) + quantity

    def __len__(self):
        return len(self._items)

    def __contains__(self, item):
        return item in self._items

    def __getitem__(self, item):
        return self._items[item]

    def __iter__(self):
        return iter(self._items)

    def __repr__(self):
        items_str = ", ".join(f"{k}: {v}" for k, v in self._items.items())
        return f"Inventory({{{items_str}}})"
```

```python
inv = Inventory()
inv.add("apple", 10)
inv.add("banana", 5)
inv.add("apple", 3)

print(len(inv))              # 2
print("apple" in inv)        # True
print(inv["apple"])          # 13
print(inv)                   # Inventory({apple: 13, banana: 5})

for item in inv:
    print(f"{item}: {inv[item]}")
```

This object feels native. It behaves like Python's built-in types because it implements the same interfaces.

---



## Where This Applies in Real Work

- **ORM models:** Django and SQLAlchemy models use `__repr__` for debugging, `__eq__` for comparisons, and `__str__` for display.
- **NumPy arrays:** `+`, `-`, `*`, `/` all work on arrays because of dunder methods. `len()`, indexing, slicing — all powered by dunders.
- **Data classes:** `@dataclass` auto-generates `__init__`, `__repr__`, `__eq__` — all dunder methods.

---



## Practice Assignment

Build a `Playlist` class with full Pythonic behavior:

1. Attributes: `name`, `_songs` (list of dicts with `"title"` and `"artist"`)
2. Methods:
  - `add(title, artist)` — adds a song
  - `remove(title)` — removes a song by title
3. Dunder methods:
  - `__len__` — number of songs
  - `__getitem__` — access by index (`playlist[0]`)
  - `__contains__` — check by title (`"Song Name" in playlist`)
  - `__iter__` — iterate over songs
  - `__repr__` — `"Playlist('name', 5 songs)"`
  - `__str__` — formatted list of all songs
  - `__add__` — merge two playlists into a new one (`playlist1 + playlist2`)
4. Create two playlists, add songs, merge them, iterate, and test all operations

Save as `src/playlist.py`.

---

