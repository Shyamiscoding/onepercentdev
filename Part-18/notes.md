# Part 18 — Lists Part 2 (Advanced Patterns)

## Connecting to Part 17

Part 17 was **foundation**: what a list *means*, **stack vs heap**, why Python’s `list` is a **dynamic array** of references (not the same as a textbook **linked list**), indexing and slicing, **mutability** and stable `id()`, and **copy vs alias** (including shallow copies of nested lists). Part 17 deliberately stopped at a **small method set** (`append`, `remove`, `pop`, `len`) so the memory story could land first.

This part is **advanced patterns**: the **rest of the list API** (`extend`, `insert`, sort/reverse/search helpers), **sorting strategies** (`sort` vs `sorted`), **`enumerate()` and `zip()`**, and the **bugs** that still trip up experienced developers. We will continue using our DMart shopping cart examples from Part 17.

---

## Adding Items — append vs extend vs insert

### .append() — Add One Item to the End

```python
my_cart = ["Rice", "Dal", "Oil"]
my_cart.append("Sugar")
print(my_cart)   # ['Rice', 'Dal', 'Oil', 'Sugar']

# Appending a list adds it as a SINGLE nested item
my_cart.append(["Salt", "Tea"])
print(my_cart)   # ['Rice', 'Dal', 'Oil', 'Sugar', ['Salt', 'Tea']]
```

### .extend() — Add Multiple Items from Another Iterable

If you want to merge items from one cart directly into another without nesting:

```python
wife_cart = ["Rice", "Dal"]
wife_cart.extend(["Sugar", "Tea"])
print(wife_cart)   # ['Rice', 'Dal', 'Sugar', 'Tea']  — each item added individually
```

### .insert() — Add at a Specific Position

```python
friend_cart = ["Rice", "Oil", "Tea"]

# Oh wait, we forgot Dal! Let's insert it at position 1.
friend_cart.insert(1, "Dal")
print(friend_cart)   # ['Rice', 'Dal', 'Oil', 'Tea']
```

| Method | What It Does | Example |
|--------|-------------|---------|
| `.append(x)` | Adds `x` as one item at the end | `["Rice"].append("Dal")` → `["Rice", "Dal"]` |
| `.extend(iterable)` | Adds each element from iterable | `["Rice"].extend(["Dal", "Oil"])` → `["Rice", "Dal", "Oil"]` |
| `.insert(i, x)` | Inserts `x` at index `i` | `["Rice", "Oil"].insert(1, "Dal")` → `["Rice", "Dal", "Oil"]` |

**Details worth memorizing**

- **`.append(x)`** — takes **exactly one** object. That object can be anything (including another list), but it is always **one slot** at the end.
- **`.extend(iterable)`** — takes **one** iterable and adds **each element**. Because a **string** is iterable character-by-character, `cart.extend("Dal")` adds `'D'`, `'a'`, `'l'` as three items — usually you wanted `append("Dal")` or `extend(["Dal"])`.
- **`.insert(i, x)`** — takes **two** arguments **in this order**: index, then value. `cart.insert("Dal")` raises `TypeError` (missing index). If `i` is **greater than** `len(cart)`, Python inserts at the end (same effect as `append`). **Negative** `i` counts from the end (same idea as indexing).

---

## Sorting

### .sort() — Modify the List In-Place

```python
prices = [149, 45, 210, 30, 85]
prices.sort()
print(prices)   # [30, 45, 85, 149, 210]

prices.sort(reverse=True)
print(prices)   # [210, 149, 85, 45, 30]
```

`.sort()` changes the original list. It returns `None`.

### sorted() — Return a New Sorted List

```python
prices = [149, 45, 210, 30, 85]
ordered = sorted(prices)

print(ordered)    # [30, 45, 85, 149, 210]
print(prices)     # [149, 45, 210, 30, 85]  — original unchanged
```

`sorted()` creates a new list. The original remains untouched.

### Sorting Strings

`sorted()` can order **a list of strings** (whole words) or **one string** (character by character). These feel different — both use the same rule: compare characters using **Unicode code points** (for simple all-lowercase English words, that matches ordinary alphabetical order).

**List of words** — sorts the items as strings:

```python
dmart_cart = ["Rice", "Dal", "Oil", "Apple"]
print(sorted(dmart_cart))   # ['Apple', 'Dal', 'Oil', 'Rice']
```

**One string** — `sorted` walks the characters and returns a **new list** of one-character strings; the original string is unchanged. There is **no** `.sort()` on `str` (strings are immutable).

```python
product = "sugar"                    # all lowercase — easy to read as A→Z
letters = sorted(product)
print(letters)   # ['a', 'g', 'r', 's', 'u']
print(product)   # "sugar" — unchanged

# product.sort()   # AttributeError — str has no .sort()
```

Mixed capitals (for example `"DMart"`) sort **uppercase before lowercase** in Unicode order, which can look odd until you use `key=str.lower` — we stick to one case here so the output matches what beginners expect.

### When to Use Which

| Use | When |
|-----|------|
| `.sort()` | You want to modify the original list and do not need the unsorted version |
| `sorted()` | You want a sorted copy while keeping the original order |

This is a mutability decision — the same thinking from Part 17.

### The Memory Proof: `id()`

To prove that `sorted()` creates a new object while `.sort()` modifies the existing one in place, we can check their memory IDs directly without even assigning them to variables.

```python
dmart_cart = ["Rice", "Oil", "Dal"]

# 1. Print the original ID
print("Original ID:   ", id(dmart_cart))

# 2. Print the ID of the sorted() result directly (without storing it)
print("sorted() ID:   ", id(sorted(dmart_cart)))  # BRAND NEW ID!

# 3. Print the original ID again to prove it hasn't changed
print("Original ID:   ", id(dmart_cart))
```

If we try to print `id(dmart_cart.sort())`, it will print the ID for Python's built-in `None` object, because `.sort()` modifies the list in place and returns `None`.

### Advanced Sorting: The `key` Parameter

Both `.sort()` and `sorted()` accept a `key` parameter. This lets you provide a function that transforms each item *just for the purpose of comparison*.

```python
dmart_cart = ["Strawberry", "Fig", "Apple"]

# Sort by length of the string, not alphabetically!
dmart_cart.sort(key=len)
print(dmart_cart)   # ['Fig', 'Apple', 'Strawberry']
```

**Sorting variants**

- **`.sort(*, key=None, reverse=False)`** and **`sorted(iterable, /, *, key=None, reverse=False)`** — optional `key` and `reverse` work the same way on both.
- If items **cannot be compared** with each other (for example mixing numbers and strings with no `key`), Python raises **`TypeError`**.
- Sorting is **stable**: items that compare equal keep their **relative order** (matters when using `key=`).

---

## Reversing

```python
checkout_items = ["Rice", "Dal", "Oil", "Sugar"]

# In-place reversal
checkout_items.reverse()
print(checkout_items)   # ['Sugar', 'Oil', 'Dal', 'Rice']

# New reversed list via slicing
original = ["Rice", "Dal", "Oil", "Sugar"]
rev = original[::-1]
print(rev)        # ['Sugar', 'Oil', 'Dal', 'Rice']
print(original)   # ['Rice', 'Dal', 'Oil', 'Sugar']  — unchanged
```

**Three ways to reverse — pick by need**

| Approach | Mutates original? | What you get |
|----------|-------------------|--------------|
| **`.reverse()`** | Yes | `None` (list reversed in place) |
| **`reversed(lst)`** | No | An **iterator**; wrap with `list(...)` if you need a list |
| **`lst[::-1]`** | No | A **new list** (shallow copy with reversed order) |

---

## Removing Items (Advanced)

While Part 17 introduced `.remove()` and `.pop()`, here are two more powerful ways to delete data from lists:

### .clear() — Empty the List
Empties the entire list in-place, leaving it as `[]`. It keeps the same list object in memory, just wiping its contents.

```python
friend_cart = ["Rice", "Dal", "Oil"]
friend_cart.clear()
print(friend_cart)   # []
```

### The `del` Statement
`del` is not a list method, but a built-in Python keyword. It is extremely powerful because it can delete items by index or even delete **entire slices**.

```python
my_cart = ["Rice", "Dal", "Oil", "Sugar", "Tea"]

del my_cart[1]      # Removes "Dal"
print(my_cart)      # ['Rice', 'Oil', 'Sugar', 'Tea']

del my_cart[1:3]    # Removes "Oil" and "Sugar" (slice deletion)
print(my_cart)      # ['Rice', 'Tea']
```

**`del` vs `.clear()` vs deleting the variable**

- **`lst.clear()`** or **`del lst[:]`** — empties the list; the **name** `lst` still refers to the **same** list object (`id` unchanged).
- **`del lst`** — removes the **variable name** from scope; you must not use `lst` afterward (unless you assign it again).
- **`del lst[i]`** / **`del lst[a:b]`** — removes **elements** (or a slice), list may still be non-empty.

---

## Searching

### .index() — Find Position of a Value

```python
# Imagine you picked up multiple packets of Dal
dmart_cart = ["Rice", "Dal", "Oil", "Dal", "Sugar"]

print(dmart_cart.index("Dal"))   # 1 (finds the first occurrence)

# Optional start and stop (same slice-style bounds as slicing):
print(dmart_cart.index("Dal", 2))      # 3 — search from index 2 onward
print(dmart_cart.index("Dal", 0, 2))   # 1 — search only in [0, 2)
```

Raises `ValueError` if the value is not in the list (or not in the searched range).

### .count() — Count Occurrences

```python
print(dmart_cart.count("Dal"))   # 2
print(dmart_cart.count("Milk"))  # 0 — no error; missing means zero
```

---

## enumerate() — Iterate with Index

A common beginner pattern:

```python
my_cart = ["Rice", "Dal", "Oil"]

for i in range(len(my_cart)):
    print(i, my_cart[i])
```

The Pythonic way:

```python
for index, item in enumerate(my_cart):
    print(index, item)
```

Output:

```
0 Rice
1 Dal
2 Oil
```

`enumerate()` returns pairs of (index, value) on each iteration.

### Custom Start Index

```python
for rank, item in enumerate(my_cart, start=1):
    print(f"Item {rank}: {item}")
```

Output:

```
Item 1: Rice
Item 2: Dal
Item 3: Oil
```

`enumerate()` is the professional way to iterate when you need both the index and the value. Never use `range(len())` when `enumerate()` works.

**Signature:** `enumerate(iterable, start=0)` — only `start` is named; the iterable is the first argument.

---

## zip() — Parallel Iteration

`zip()` combines two or more sequences element by element. This is perfect when you have related data spread across multiple lists:

```python
items = ["Rice", "Dal", "Oil"]
prices = [450, 120, 210]

for item, price in zip(items, prices):
    print(f"{item}: ₹{price}")
```

Output:

```
Rice: ₹450
Dal: ₹120
Oil: ₹210
```

`zip()` stops at the shortest sequence:

```python
items = ["Rice", "Dal", "Oil"]
prices = [450, 120]  # Missing the price for Oil!

for item, price in zip(items, prices):
    print(item, price)
# Only prints 2 pairs: (Rice, 450) and (Dal, 120)
```

With **three or more** lists, `zip(a, b, c, ...)` yields triples (or longer tuples) per step. In **Python 3.10+**, `zip(..., strict=True)` raises if lengths differ — handy when mismatch should be a bug, not silent truncation.

### Combining enumerate and zip

```python
items = ["Rice", "Dal", "Oil"]
prices = [450, 120, 210]

for rank, (item, price) in enumerate(zip(items, prices), start=1):
    print(f"{rank}. {item} — ₹{price}")
```

Output:

```
1. Rice — ₹450
2. Dal — ₹120
3. Oil — ₹210
```

---

## List Slicing Creates New Lists

```python
original_cart = ["Rice", "Dal", "Oil", "Sugar", "Tea"]
checkout_chunk = original_cart[1:4]

checkout_chunk[0] = "Premium Dal"
print(checkout_chunk)      # ['Premium Dal', 'Oil', 'Sugar']
print(original_cart)       # ['Rice', 'Dal', 'Oil', 'Sugar', 'Tea']  — unchanged
```

Slicing creates a shallow copy. Modifying the slice does not affect the original.

---

## Stack Pattern

A stack follows **Last In, First Out (LIFO)** — the last item added is the first one removed. Imagine taking items out of your physical shopping cart to put them on the checkout counter.

```python
checkout_stack = []

checkout_stack.append("Rice")
checkout_stack.append("Dal")
checkout_stack.append("Oil")

print(checkout_stack.pop())   # Oil (last in, first out)
print(checkout_stack.pop())   # Dal
print(checkout_stack)         # ['Rice']
```

Stacks are used for undo operations, function call tracking, and expression evaluation. The Python call stack (Part 6) works this way.

---

## Common List Bugs

### 1. Modifying a List While Iterating

```python
prices = [149, 45, 30, 210, 85, 120]

# Bad! We want to remove prices under 100
for p in prices:
    if p < 100:
        prices.remove(p)   # Dangerous — skips elements!

print(prices)   # [149, 30, 210, 120] — Notice how 30 was missed!
```

The safe approach — iterate over a copy:

```python
prices = [149, 45, 30, 210, 85, 120]

for p in prices.copy():
    if p < 100:
        prices.remove(p)

print(prices)   # [149, 210, 120]
```

### 2. Confusing .sort() Return Value

```python
prices = [149, 45, 210]
result = prices.sort()
print(result)    # None  — .sort() returns None, not the sorted list
```

Use `sorted()` if you need the sorted list as a value.

### 3. Forgetting .copy()

Covered in Part 17 — always use `.copy()` when you need an independent list.

### 4. `.pop()` with a bad index

```python
cart = ["Rice"]
cart.pop(5)   # IndexError — nothing at index 5
```

**`.pop()`** with **no argument** removes and returns the **last** item. **`.pop(i)`** removes and returns the item at index `i`. Empty list: **`cart.pop()`** raises **`IndexError`**.

### 5. `.remove()` when the value is missing

```python
cart = ["Rice", "Dal"]
cart.remove("Milk")   # ValueError — not in list
```

---

## Complete List Methods Reference

Here is every built-in list method in one place:

| Method | What It Does | Returns |
|--------|-------------|---------|
| `.append(x)` | Adds `x` to the end | `None` |
| `.extend(iterable)` | Adds each item from iterable to the end | `None` |
| `.insert(i, x)` | Inserts `x` at index `i` | `None` |
| `.remove(x)` | Removes first occurrence of `x` (raises `ValueError` if missing) | `None` |
| `.pop(i)` | Removes and returns item at index `i` (default: last) | The removed item |
| `.clear()` | Removes all items | `None` |
| `.index(x)` | Returns index of first occurrence of `x` (raises `ValueError` if missing) | `int` |
| `.count(x)` | Returns number of times `x` appears | `int` |
| `.sort()` | Sorts in place (ascending by default) | `None` |
| `.reverse()` | Reverses in place | `None` |
| `.copy()` | Returns a shallow copy | New `list` |

**Returns:** Most methods that **mutate** the list return **`None`** (by design — you are not meant to chain them for a new list). **`.pop()`** is the exception: it returns the **removed element**. **`.index`** and **`.count()`** return an **`int`**.

---

## Method vs built-in (how this part fits together)

| Kind | Examples in this part | Mental model |
|------|------------------------|--------------|
| **List method** | `.append`, `.extend`, `.insert`, `.sort`, `.reverse`, … | “Do this **to this list**” — call with **`.`** on the list. |
| **Built-in function** | `sorted()`, `reversed()`, `len()`, `enumerate()`, `zip()` | “Do this **to whatever you pass**” — first argument is the data (or main input). |
| **Statement / syntax** | `del`, slicing `[start:stop:step]` | Not functions; part of Python grammar. |

**Why `sorted` but `.sort`?** `sorted(any_iterable)` works on **any** iterable without turning it into a list first; **`.sort()`** only exists on **lists** and sorts **in place**. Same split for **`reversed()`** vs **`.reverse()`**.

---

## Where This Applies in Real Work

- **enumerate()** — generating numbered lists in reports, tracking position while processing records, displaying ranked results in dashboards.
- **zip()** — matching parallel data from different sources (item names + prices, dates + values, IDs + labels), common in data science when combining columns.
- **sorted()** — displaying leaderboards, sorting API results, ordering data before display.
- **Stack pattern** — undo/redo functionality, browser back button, expression parsers, function call management.
- **Modifying while iterating** — one of the top 5 Python bugs in production. Code reviews flag this immediately.

---

## Practice Assignment

Create a DMart checkout receipt:

1. Define two lists:

```python
cart_items = ["Rice", "Dal", "Oil", "Sugar", "Tea"]
cart_prices = [450, 120, 210, 50, 150]
```

2. Use `zip()` to combine the two lists. Use **`zip(cart_prices, cart_items)`** so each row is a **`(price, item)`** tuple — with the price **first**, Python’s default tuple ordering sorts by **price** when you call `sorted(..., reverse=True)`, and you do **not** need a `key=` function (no `lambda` yet — that lands in **Part 28**; **list comprehensions** in **Part 23**).
3. Use `sorted()` (or `.sort()` on a list you built) so the **most expensive** line appears first.
4. Use `enumerate()` with `start=1` to print a numbered receipt:

```
1. Rice — ₹450
2. Oil — ₹210
3. Tea — ₹150
4. Dal — ₹120
5. Sugar — ₹50
```

Save as `src/receipt.py`.

**If you are stuck** — try the steps above first; the whole script is only a few lines after the two lists. Core loop:

```python
rows = list(zip(cart_prices, cart_items))
ordered = sorted(rows, reverse=True)
for rank, (price, item) in enumerate(ordered, start=1):
    print(f"{rank}. {item} — ₹{price}")
```

---

> **Next:** Part 19 — Tuples and Unpacking. The immutable sibling of lists. Tuples are simpler but play a crucial role in Python — from function returns to dictionary keys.