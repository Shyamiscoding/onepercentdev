# Part 19 — Tuples and Unpacking

## Connecting to Parts 17 and 18

In Parts 17 and 18, we went deep into lists — mutable collections you can change freely. But sometimes you **want** a collection that cannot change: **one line on the printed bill**, a **fixed place in the shop** (row number, shelf number), or **price and quantity at checkout** — data that should stay exactly as it was recorded.

That is a tuple. Think of it as a list that is locked after creation. In the Part 9 overview table, you saw that tuples are **immutable** — just like `int`, `float`, and `str`. When you "change" a tuple, Python creates a new object in the heap. The original stays untouched.

---

## What Is a Tuple?

A tuple is an ordered, **immutable** collection that allows duplicates.

```python
shop_place = (5, 12)                   # row 5, position 12 — fixed spot in the store
sections = ("Grocery", "Dairy", "Home") # three section names, in order
one_line = ("Rice", 1, 450)             # one bill line: item name, qty, total rupees
```

Think of tuples as lists that cannot be changed after creation.


| Property          | List | Tuple  |
| ----------------- | ---- | ------ |
| Ordered           | Yes  | Yes    |
| Mutable           | Yes  | **No** |
| Allows duplicates | Yes  | Yes    |
| Syntax            | `[]` | `()`   |


---

## Creating Tuples

```python
# With parentheses
row = (3, 5)   # e.g. row 3, shelf 5 — two numbers together as one tuple

# Without parentheses (packing)
row = 3, 5
print(type(row))   # <class 'tuple'>

# Single element — the comma is what makes it a tuple, not the parentheses
one_code = (99012,)   # one product code in a tuple — note the comma
print(type(one_code))   # <class 'tuple'>

not_a_tuple = (99012)        # no trailing comma — this is just an int in parentheses
print(type(not_a_tuple))   # <class 'int'>

# Empty tuple
empty = ()
empty2 = tuple()

# From other iterables
letters = tuple("DMART")   # ('D', 'M', 'A', 'R', 'T')
nums = tuple([1, 2, 1])    # quantities from a cart row, e.g. (1, 2, 1)
```

The single-element comma rule trips up everyone the first time. `(99012)` is just the integer `99012`. `(99012,)` is a tuple because of the comma.

---

## Tuples Are Immutable

```python
receipt_line = ("Rice", 1, 450)
receipt_line[0] = "Dal"   # TypeError: 'tuple' object does not support item assignment
```

Once created, you cannot add, remove, or change items.

This is not a limitation — it is a **guarantee**. When you pass a tuple to a function or store it as a key, you know it will never change unexpectedly.

### Proving Immutability with id()

```python
price_qty = (450, 1)   # price in rupees, quantity — frozen snapshot
print(id(price_qty))    # e.g., 140234866357520

price_qty = (120, 2)    # you put a new snapshot in the name — new tuple
print(id(price_qty))    # different ID — a new tuple object was created
```

When you "change" a tuple, Python does not modify the original. It creates a brand new tuple. The old one is left for garbage collection. This is the same **rebinding / new object on the heap** story from **Part 7** (stack vs heap). `**str`** behaves the same way — **Part 10**.

Compare with a list (mutable):

```python
cart_prices = [450, 120]
print(id(cart_prices))    # e.g., 140234866123456

cart_prices.append(210)
print(id(cart_prices))    # same ID — same object, modified in place
```

---

## Indexing and Slicing

Same syntax as lists and strings:

```python
products = ("Rice", "Dal", "Oil", "Sugar")

print(products[0])      # Rice
print(products[-1])     # Sugar
print(products[1:3])    # ('Dal', 'Oil')
print(products[::-1])   # ('Sugar', 'Oil', 'Dal', 'Rice')
```

Slicing a tuple returns a new tuple.

**Sorting:** Tuples have **no** `.sort()` — there is nothing to mutate in place. Use `**sorted(my_tuple)`**; you get a **new `list`** (same rule as `**sorted()` on any iterable** in **Part 18**).

---

## Tuple Unpacking

Unpacking assigns each item in a tuple to a separate variable in one line:

```python
pair = (450, 1)   # price, quantity
price, qty = pair

print(price)   # 450
print(qty)     # 1
```

The number of variables on the left must match the number of items in the tuple.

### Swap Pattern

```python
first = "Rice"
second = "Dal"

first, second = second, first

print(first)   # Dal
print(second)  # Rice
```

No temporary variable needed. Python evaluates the right side first, builds a tuple `(second, first)`, then unpacks into `first` and `second`.

### Extended Unpacking with *

```python
item1, *others = ["Rice", "Dal", "Oil", "Sugar", "Tea"]

print(item1)   # Rice
print(others)  # ['Dal', 'Oil', 'Sugar', 'Tea']
```

```python
item1, *middle, last = ["Rice", "Dal", "Oil", "Sugar", "Tea"]

print(item1)    # Rice
print(middle)   # ['Dal', 'Oil', 'Sugar']
print(last)     # Tea
```

The `*` variable collects all remaining items into a list. The right-hand side can be a **tuple** instead of a list — the syntax is identical; only the `*name` bucket is always a `**list`**.

---

## Unpacking in Loops

You already used this in Part 18 without knowing it:

```python
my_cart = ["Rice", "Dal", "Oil"]

for index, item in enumerate(my_cart):
    print(index, item)
```

`enumerate()` yields tuples like `(0, "Rice")`, `(1, "Dal")`, etc. Writing `index, item` unpacks each tuple automatically.

Same with `zip()`:

```python
items = ["Rice", "Dal"]
prices = [450, 120]

for item, price in zip(items, prices):
    print(f"{item}: ₹{price}")
```

**Part 18 (nested unpacking)** — `zip` yields `(item, price)` tuples; `enumerate` wraps each step as `(rank, that_tuple)`. You can unpack **both** levels in the `for` line:

```python
items = ["Rice", "Dal", "Oil"]
prices = [450, 120, 210]

for rank, (item, price) in enumerate(zip(items, prices), start=1):
    print(f"{rank}. {item} — ₹{price}")
```

This is the same receipt idea as **Part 18**; here you see it as **tuple unpacking** end to end.

---

## Functions That Return Tuples

Some built-in functions return tuples. You can unpack the result:

```python
# How many full ₹100 notes fit in ₹450, and what is left?
result = divmod(450, 100)
print(result)       # (4, 50)
print(type(result)) # <class 'tuple'>

hundreds, leftover = divmod(450, 100)
print(hundreds)     # 4
print(leftover)     # 50
```

`divmod(a, b)` returns `(a // b, a % b)` — the quotient and remainder as a tuple.

This pattern is used extensively in Python. Functions return multiple values by packing them into a tuple, and callers unpack them.

---

## Tuple Methods

Tuples have only two methods (because they are immutable):

```python
# Same rupee amounts can repeat on a bill — tuples allow duplicates
amounts = (450, 120, 210, 120, 450)

print(amounts.count(120))    # 2
print(amounts.index(210))  # 2 (position of first 210)
print(amounts.index(120, 2)) # 3 — optional start (and stop), same idea as list `.index` in Part 18
```

---

## Tuples as Dictionary Keys

Tuples are **hashable** (because they are immutable), which means they can be used as dictionary keys. Lists cannot.

```python
# Map: (latitude, longitude) → store name. Lists cannot be dict keys; tuples can.
stores_map = {}
stores_map[(12.97, 77.59)] = "DMart Bangalore"
stores_map[(19.08, 72.88)] = "DMart Mumbai"

print(stores_map[(12.97, 77.59)])   # DMart Bangalore
```

This becomes important in Part 21 when we cover dictionaries in detail.

---

## Complete Tuple Operations ReferencePART

Tuples have only two methods (because they are immutable), but support several built-in operations:


| Operation / Method           | What It Does                                                             | Returns            |
| ---------------------------- | ------------------------------------------------------------------------ | ------------------ |
| `tuple[i]`                   | Access item at index `i`                                                 | The item           |
| `tuple[start:end]`           | Slice — returns a portion of the tuple                                   | New `tuple`        |
| `.count(x)`                  | Number of times `x` appears                                              | `int`              |
| `.index(x[, start[, stop]])` | First index of `x`; optional bounds like **list** `.index` (**Part 18**) | `int`              |
| `len(tuple)`                 | Number of items                                                          | `int`              |
| `x in tuple`                 | Check if `x` exists in the tuple                                         | `bool`             |
| `tuple1 + tuple2`            | Concatenation — combines into a new tuple                                | New `tuple`        |
| `tuple * n`                  | Repetition — repeats `n` times                                           | New `tuple`        |
| `a, b, c = tuple`            | Unpacking — assigns each item to a variable                              | Individual values  |
| `a, *rest = tuple`           | Extended unpacking — collects remaining items                            | `list` for `*rest` |


---

## When to Use Tuples vs Lists


| Use Tuples When                                                                | Use Lists When                    |
| ------------------------------------------------------------------------------ | --------------------------------- |
| Data should not change (one bill line, fixed price row, map location as a key) | Data will grow, shrink, or change |
| Returning multiple values from a function                                      | Collecting items dynamically      |
| Dictionary keys                                                                | Processing collections of items   |
| Unpacking values into variables                                                | Sorting, filtering, transforming  |


A simple rule: if the data is fixed at creation time and should not change, use a tuple. If it will be modified, use a list.

### Real Examples — DMart: basket (list) and receipt (list of tuples)

**While shopping**, the customer keeps changing what they carry. That is a **list** — add and remove freely:

```python
basket = ["Rice", "Dal", "Oil"]
basket.append("Sugar")
basket.remove("Dal")
```

**After checkout**, each **line on the bill** is a fixed snapshot: item name, quantity, line total. That row is not “another basket” — you do not `append` into the middle of a printed line. Model each line as a **tuple** `(item, qty, line_total_in_rupees)`. The **whole receipt** is still a **list**, because it has **many lines**:

```python
receipt_lines = [
    ("Rice", 1, 450),
    ("Dal", 1, 120),
    ("Oil", 1, 210),
]
# receipt_lines.append(("Sugar", 1, 50))  # new line after another item — OK (the list grows)
# receipt_lines[0][1] = 2                 # TypeError — you cannot rewrite inside one tuple like a basket
```

**Idea:** **List** = the thing that **grows or changes** (basket, or the collection of lines). **Tuple** = **one sealed row** with a fixed shape (this bill line).

### More simple DMart examples

```python
offer = ("Rice", "Oil")              # two items on one offer poster — fixed pair
where = (7, 3)                       # row 7, shelf 3 in the shop
staff = ("Priya", "Night", 2)        # name, shift, floor — one fixed row of data
```

---

## Time and Space Complexity


| Operation                  | Time Complexity | Notes                   |
| -------------------------- | --------------- | ----------------------- |
| Access by index `tuple[i]` | O(1)            | Same as lists — instant |
| Search `x in tuple`        | O(n)            | Checks items one by one |
| Count `.count(x)`          | O(n)            | Scans entire tuple      |
| Index `.index(x)`          | O(n)            | Scans until found       |
| Length `len(tuple)`        | O(1)            | Tracked internally      |


Tuples have the same time complexity as lists for read operations. But because tuples are immutable, they have no insert, delete, or sort operations.

### Tuples Use Less Memory Than Lists

```python
import sys

my_list = [450, 120, 210, 50, 150]   # same five prices as a list
my_tuple = (450, 120, 210, 50, 150)  # same five prices fixed as a tuple

print(sys.getsizeof(my_list))    # e.g., 104 bytes
print(sys.getsizeof(my_tuple))   # e.g., 80 bytes
```

Tuples are smaller because they do not need the extra memory that lists allocate for potential growth (resizing). If your data is fixed and you are storing millions of records, tuples save memory.

---

## Where This Applies in Real Work

- **Checkout:** Each line on the bill is often a fixed row: item, quantity, rupees — tuple-shaped in memory or from a database.
- **Function returns:** Functions that compute multiple results return tuples. `divmod()`, `enumerate()`, and database rows often work the same way.
- **Stores:** Inventory or sales reports are often rows of columns; map keys like `(lat, long)` use tuples because lists are not allowed as keys.
- **Unpacking:** Used everywhere in professional Python — loop iteration, function arguments, configuration parsing. Clean unpacking is a sign of Pythonic code.
- **Data integrity:** When you want a basket line or audit snapshot to stay unchanged, tuples provide that safety — same DMart story as **receipt lines** above.

---

## Practice Assignment

Create a **DMart cold-chain tracker** (store name + cold-room temperature °C):

1. Define a list of tuples, each containing a **store label** and its **temperature**:

```python
stores = [
    ("DMart Bangalore", 4),
    ("DMart Delhi", 6),
    ("DMart Mumbai", 5),
    ("DMart Shimla", 2),
    ("DMart Chennai", 7),
]
```

1. Use unpacking in a `for` loop to print each store and temperature
2. Find the **warmest** and **coldest** cold room using a loop (do not use `max()`/`min()` with `key` — we have not covered that yet; use a simple comparison loop)
3. Try to modify a temperature inside one of the tuples — observe and understand the error
4. Use `divmod()` on the **warmest** temperature (integer division by `5`). Unpack the result and print quotient and remainder

Save as `src/temp_tracker.py`.

---

> **Next:** Part 20 — Sets. A collection that guarantees uniqueness and performs lightning-fast lookups. You will learn why "is this item already in my collection?" is a question that sets answer better than lists.

