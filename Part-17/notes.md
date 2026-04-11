# Part 17 — Lists Part 1 (Foundation)

## This part covers

- What a **list** is and how it lives in **memory** (stack / heap)
- **Why** Python has lists (limits of many separate variables)
- **Creating** lists; **indexing**; **slicing**
- **Mutability** vs strings; **`id()`**
- **Two names, one list** (alias) vs **`.copy()`**; shallow copy with **nested** lists
- **Core methods** (built-in operations on a list): **`.append`**, **`.remove`**, **`.pop`**, and **`len`**
- **`for`** over a list; **`in`** / **`not in`**; **empty list** and truthiness
- **Building** a list in a loop; **`sum`**, **`min`**, **`max`**; simple **filter**
- **Nested** lists (e.g. rows / departments)

*“Core methods”* = the built-in actions Python defines on lists (here: add/remove items and measure length). More list methods come in a later episode.

---

## Prerequisites — Parts 7–16 at a glance

| Part | Title (from series) | Key concepts to recall |
|------|---------------------|-------------------------|
| **7** | Memory: Stack and Heap | Stack vs heap; frames; names point into heap |
| **8** | Variables, Names, and Objects | Name; heap **object**; **reference**; **`id()`** |
| **9** | Numbers and Math | **`int`**, **`float`**; math; **type map** (includes `list` as a type) |
| **10** | Strings | **`str`**; **indexing** & **slicing**; **immutable** text |
| **11** | Booleans and Comparison Operators | **`bool`**; comparisons **`==` `!=` `<` `>` …** |
| **12** | Logical Operators and Truthiness | **`and` `or` `not`**; **truthiness** |
| **13** | Conditionals | **`if` / `elif` / `else`** |
| **14** | Professional Conditional Patterns | Guard clauses; cleaner conditional style |
| **15** | While Loops | **`while`**; **`break` / `continue`** |
| **16** | For Loops | **`for`**; **`range`**; iterate over a **sequence** |

---

## What is a list? — Definition

A **list** is an **ordered**, **mutable** collection. Each position has an index (`0`, `1`, `2`, …). You can change, add, and remove elements after the list is created. The same value may appear more than once.

```python
fruits = ["Mango", "Banana", "Apple"]
vegetables = ["Tomato", "Onion", "Potato"]
dmart_cart = ["Rice", "Dal", "Oil"]
mixed = [149, "DMart", 3.14, True]
```

| Property | Meaning |
|----------|---------|
| Ordered | First item is index `0`, then `1`, … |
| Mutable | Assign by index, append, remove, pop — the same list object is updated |
| Duplicates allowed | Same value can appear in multiple slots |

---

## List object in memory (stack / heap)

**Question:** When you write `dmart_cart = ["Rice", "Dal", "Oil"]`, where does Python put things?

(Reuse **Part 7–8**: names live in the **frame** (stack side of the model); values are **objects** in the **heap**.)

```python
dmart_cart = ["Rice", "Dal", "Oil"]
```

- **Heap:** One **list object**. Inside it: bookkeeping + a row of **slots**; each slot holds a **reference** to another object (here, three strings).
- **Frame:** The name `dmart_cart` holds a **reference** to that list object — not a copy of all the strings “inside” the stack.
- **`dmart_cart[k]`:** Python uses the index to pick a slot and follow the reference to the element.

Changing `dmart_cart[0]` or calling `.append(...)` usually keeps **`id(dmart_cart)`** the same: you are still using the **same list object**, only its slots change (internal storage may grow).

---

## Why lists exist

If you only use **separate variables** (`item1`, `item2`, `item3`, …):

- You **cannot** run **`for`** over “all items” as one thing — you would need one `print` (or block) per variable.
- You **cannot** ask **`len(...)`** for “how many items” in one expression.
- You **cannot** **index** by a variable position (`i`-th item) in a uniform way.
- Growing or shrinking the group (add/remove) does not scale — new variables or lots of repeated code.
- Passing “the whole group” to something else is awkward; a list is **one** object, one reference.

A **list** gives **one name** for many values, **fixed order**, **shared operations** (loop, length, index, slice, add/remove), and **one reference** to pass around. That is why languages provide a list (or array-like) type instead of leaving everything as separate names.

---

## Background (optional — how Python implements `list`)

- Older / low-level style: fixed **arrays** in memory.
- In **CPython**, `list` is usually a **dynamic array of references** (growing buffer), not a textbook **linked list**.
- In algorithms class, “list” sometimes means **linked list** — different from Python’s `list`.

---

## Creating lists

```python
vegetables = ["Tomato", "Onion", "Potato"]
fruits = ["Mango", "Banana", "Apple"]
dmart_cart = ["Rice", "Dal", "Oil"]
empty_cart = []

letters = list("DMart")        # ['D', 'M', 'a', 'r', 't']
aisles = list(range(1, 6))     # [1, 2, 3, 4, 5]
```

---

## Indexing

Same rules as **Part 10** (strings).

```python
vegetables = ["Tomato", "Onion", "Potato", "Carrot"]
vegetables[0]    # Tomato
vegetables[2]    # Potato
vegetables[-1]   # Carrot
vegetables[-2]   # Potato
# vegetables[10]  # IndexError
```

---

## Slicing

Syntax **`[start:end:step]`**. Result is a **new** list.

```python
prices = [149, 45, 30, 210, 85, 120, 199]
prices[:3]
prices[2:5]
prices[4:]
prices[::-1]
```

---

## Mutability (vs string)

Strings cannot be changed in place; lists can.

```python
store = "DMart"
# store[0] = "E"   # TypeError
```

```python
dmart_cart = ["Rice", "Dal", "Oil"]
dmart_cart[0] = "Basmati Rice"
```

### `id()` — list vs rebinding a name

```python
dmart_cart = ["Rice", "Dal", "Oil"]
id(dmart_cart)
dmart_cart[0] = "Basmati Rice"
id(dmart_cart)       # same — in-place mutation
dmart_cart.append("Sugar")
id(dmart_cart)       # same
```

```python
store = "DMart"
id(store)
store = "DMart Hyper"   # name points to a new str object
id(store)               # different

price = 149
id(price)
price = 199
id(price)               # typically different (implementation detail: small-int cache)
```

---

## Aliasing — two names, one list

`b = a` copies the **reference**, not the list.

```python
my_cart = ["Rice", "Dal", "Oil"]
wife_cart = my_cart
wife_cart.append("Ghee")
# my_cart and wife_cart both show Ghee
id(my_cart) == id(wife_cart)   # True
```

### Shallow copy

```python
my_cart = ["Rice", "Dal", "Oil"]
friend_cart = my_cart.copy()
friend_cart.append("Butter")
# my_cart unchanged at top level
id(my_cart) == id(friend_cart)   # False
```

Nested lists: **`.copy()`** copies the **outer** list only; **inner** lists are still shared.

```python
dmart = [
    ["Rice", "Dal", "Oil"],
    ["Tomato", "Onion", "Potato"],
]
branch_copy = dmart.copy()
branch_copy[0][0] = "Wheat"
# dmart[0][0] is also Wheat
```

Deep copy (later): `import copy; copy.deepcopy(dmart)`.

---

## Core list methods (this part)

Each method below is a **built-in operation** on a list object.

### 1. `.append(x)`

Adds **one** element **at the end**. Mutates the list. Returns `None`.

```python
cart = ["Rice", "Dal"]
cart.append("Oil")
```

### 2. `.remove(x)`

Removes the **first** element equal to `x`. Mutates the list. **`ValueError`** if `x` is not in the list.

```python
cart.remove("Dal")
```

### 3. `.pop()` or `.pop(i)`

Removes and **returns** the item at index `i`; default `i` is **last**.

```python
cart = ["Rice", "Dal", "Oil"]
cart.pop()     # 'Oil'
cart.pop(0)    # 'Rice'
```

### 4. `len(list)`

Built-in function: number of elements (not a method on the list, but always used with lists).

```python
len([149, 45, 30])   # 3
```

---

## Iteration

```python
for item in ["Mango", "Banana", "Apple"]:
    print(item)
```

---

## Membership: `in` / `not in`

```python
cart = ["Rice", "Dal", "Oil"]
"Rice" in cart
"Milk" in cart
"Bread" not in cart
```

---

## Empty list — truthiness

`[]` is **falsy**; a non-empty list is **truthy**.

```python
if cart:
    ...
else:
    ...
```

Prefer `if cart:` over `if len(cart) > 0:` (Python style).

---

## Build a list in a loop; `sum`, `min`, `max`

```python
prices = []
for i in range(3):
    p = int(input(f"Price {i + 1} (₹): "))
    prices.append(p)
total = sum(prices)
avg = total / len(prices)
```

```python
prices = [149, 45, 30, 210, 85]
sum(prices)
min(prices)
max(prices)
len(prices)
```

### Filter into a new list

```python
expensive = []
for p in prices:
    if p > 50:
        expensive.append(p)
```

---

## Nested lists

```python
dmart = [
    ["Rice", "Dal", "Oil"],
    ["Tomato", "Onion", "Potato"],
    ["Mango", "Banana", "Apple"],
]
dmart[0]
dmart[1][0]
dmart[2][2]
```

---

## Two parallel lists (same length, no dict)

When you have two lists aligned by index (e.g. item name and price), use the same index for both:

```python
items = ["Rice", "Dal", "Oil"]
prices = [450, 120, 210]
for i in range(len(items)):
    print(items[i], prices[i])
```

(Dictionaries are a later topic; this pattern only needs lists and a loop.)

---

## List operations — time cost (reference only)

What **O(1)**, **O(n)**, etc. **mean** is taught in your **time-complexity** topic (e.g. Part 56). Until then, treat this table as a **bookmark**.

| Operation | Time (usual) |
|-----------|----------------|
| `lst[i]` | O(1) |
| `append` | O(1) amortized |
| `insert(0, x)`, `pop(0)` | O(n) |
| `remove(x)`, `x in lst` | O(n) |
| `pop()` (end) | O(1) |
| `sort` | O(n log n) |
| `len` | O(1) |

---

## Practice (simple → harder)

Do these in order; use **one file per question** or clearly separated sections.

1. **Create and print** — Build `dmart_cart = ["Rice", "Dal", "Oil"]`. Print each item on its own line with a `for` loop. Print `len(dmart_cart)`.

2. **Indexing** — `vegetables = ["Tomato", "Onion", "Potato", "Carrot"]`. Print the first item, the last item, and the second-from-last using indices.

3. **Slicing** — `prices = [149, 45, 30, 210, 85, 120, 199]`. Produce: first three; middle slice from index `2` through `5` (exclusive); from index `4` to the end; full list reversed.

4. **Mutate** — Start with `["Rice", "Dal", "Oil"]`. Replace `"Rice"` with `"Basmati Rice"`. Append `"Sugar"`. Print the final list.

5. **`id()`** — For a list, print `id` before and after changing `list[0]` and after `.append`. For a string variable, print `id` before and after assigning a **new** string to the **same** name. Summarize the difference in one sentence.

6. **Alias** — `a = ["Rice", "Dal"]`, `b = a`, `b.append("Oil")`. Print `a` and `b` and whether `id(a) == id(b)`. Then repeat with `b = a.copy()` and explain why `a` differs from the alias case.

7. **Shallow nested** — Build `rows = [["Rice", "Dal"], ["Tomato", "Onion"]]`. `copy = rows.copy()`, then change `copy[0][0]` to `"Wheat"`. Print `rows` and `copy`. Explain why both first rows changed.

8. **Methods** — From `["Rice", "Dal", "Oil"]`, pop the last item and print what was returned; remove `"Dal"`; append `"Ghee"`; print final list and `len`.

9. **`in` and empty** — Write `if` logic: if `cart` is empty, print `"Empty"`; else if `"Rice" in cart`, print `"Has rice"`; else print `"No rice"`. Test with `[]`, `["Dal"]`, `["Rice", "Oil"]`.

10. **Menu cart** — Empty list. `while True`: prompt for `add` / `view` / `remove` / `quit`. On `remove`, catch missing item (no crash). Match behavior to the small I/O example: add Rice, add Dal, view, remove Rice, quit → `['Dal']`. Save as `src/shopping_list.py`.

11. **Prices from input** — Read **three** prices with `input`, build a list with `.append`, print list, **total**, and **average**.

12. **Filter** — Given `prices = [149, 45, 30, 210, 85]`, build a new list of all values **strictly greater than 50** using a `for` and `if` (no list comprehension required).

13. **Nested access** — Use the three-department `dmart` nested list from the notes. Print all staples on one line (join with commas or spaces). Print the vegetable at index `1` of the vegetable row.

14. **Parallel lists** — `items = ["Rice", "Dal", "Oil"]`, `prices = [450, 120, 210]`. Loop with index `i` and print each line as `Item: …  Price: …`. Compute total price in the loop and print total at the end.

15. **Squares** — With `for i in range(1, n+1)` and `input` for `n`, build a list of squares `[1, 4, 9, …]` using `.append` only.

---

> **Next:** More list methods and iteration patterns in the following part on lists.
