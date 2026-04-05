# Part 11 — Booleans and Comparison Operators

## Connecting to Part 10

So far, we have learned how to **store** data — integers (Part 9), strings (Part 10). We can hold a user's name, their age, a price, a password. We know how Python keeps them in memory, how to manipulate them.

But think about this — **what have our programs actually done so far?**

They store values. They calculate. They print. That is it. Right now, our code is like a **warehouse full of raw materials** — wood, bricks, steel, all neatly organized, labeled, stacked. But nothing is being built. The materials are just sitting there.

A warehouse does not become a building by itself. Someone has to look at the materials and start asking questions: "Is this beam strong enough?" "Do we have enough bricks?" "Is this the right size?" — and then **decide** what to do based on the answers.

**Software works the exact same way.**

Every app you use — banking, Instagram, Google — is not just storing data. It is constantly **asking questions** about that data:

- "Is this password correct?" → let them in or block them
- "Is the balance sufficient?" → allow the transaction or decline it
- "Is this user old enough?" → show the content or restrict it
- "Has this item been purchased?" → ship it or keep it in the cart

Without these questions, your program is just a **notebook** — it writes things down but cannot act on them. It stores `age = 16` but cannot do anything different for a 16-year-old vs a 25-year-old. It holds `password = "abc123"` but cannot check if what the user typed matches.

**This is the moment your code goes from a calculator to actual software.**

From this part onward, your programs will start **thinking**. And it all begins with the simplest question a program can ask — **yes or no**. That is what a Boolean is.

---

## The Boolean Type

- Most used type in all of programming — every decision a program makes depends on a boolean
- Only **two possible values**: `True` and `False`
- These are **keywords** in Python — you cannot use them as variable names

```python
print(True)
print(False)
print(type(True))   # <class 'bool'>
```

### Booleans Are Objects in the Heap

- Same rule from Parts 7-8: **everything is an object**
- `True` is an object stored in the **heap**
- The variable on the **stack** holds a reference (arrow) pointing to it

```python
x = True
print(type(x))    # <class 'bool'>
print(id(x))      # some memory address — this is the object's location in the heap
```

```
STACK                    HEAP
┌──────────┐            ┌──────────────────┐
│ x  ──────│───────────▶│ type: bool       │
└──────────┘            │ value: True      │
                        │ id: 4345618736   │
                        └──────────────────┘
```

### True and False Are Singletons

- Python creates exactly **ONE** `True` object and **ONE** `False` object — ever
- Every variable holding `True` points to the **same object** in the heap
- Even comparison results point to the same singleton

```python
a = True
b = True

print(id(a))        # 4345618736
print(id(b))        # 4345618736  — same id!
print(a is b)       # True — same object in heap

c = (10 > 5)        # comparison produces True
print(id(c))        # 4345618736  — still the same object!
```

- This is called a **singleton** — only one instance exists
- Same concept as small integers (-5 to 256) from Part 9 — Python caches them
- Difference: integers have 262 cached objects, booleans have exactly **2** — ever

### bool Is a Subclass of int

**Why does bool even exist?**

- Before Python 2.3 (year 2002) — there was **no boolean type** in Python
- Programmers used `1` for true and `0` for false — just like C language
- Problem: `return 1` — is that "yes/true" or the actual number one? You cannot tell by reading the code
- **Guido van Rossum** (Python's creator) wrote **PEP 285** to fix this — introduced `bool` with `True` and `False`
- Goal: **readability and intent** — `is_active = True` says what it means, `is_active = 1` does not

**Why subclass of int and not a separate type?**

- By 2002, thousands of Python programs already used `1` and `0` as booleans
- If `bool` was a completely new type, all that existing code would **break**
- Making `bool` inherit from `int` = backward compatibility — old code using `1`/`0` keeps working, new code can use `True`/`False`
- Guido's words: *"inheriting bool from int eases the implementation enormously"*
- Read it yourself: [PEP 285 — Adding a bool type](https://peps.python.org/pep-0285/)

**So `True` IS `1` and `False` IS `0` — by design, not by accident:**

```python
print(True + True)     # 2
print(False + 1)       # 1
print(True * 10)       # 10
```

**Real-world use case 1 — Counting matches:**

```python
print(sum([True, True, False, True]))  # 3
```

- `sum()` adds up the list — `True` is 1, `False` is 0, total is 3
- In data processing and ML, this is how you count how many items passed a condition
- Example: "How many students scored above 70?" → count the `True` values

**Real-world use case 2 — Indexing with booleans:**

```python
names = ["Alice", "Bob"]
has_permission = True

print(names[True])     # "Bob"  — True is 1, so index 1
print(names[False])    # "Alice" — False is 0, so index 0
```

- You can use a boolean as an index because it IS an integer
- Useful for picking between two options based on a condition

**Real-world use case 3 — Arithmetic with conditions:**

```python
price = 100
is_member = True

discount = price * 0.1 * is_member    # 10.0 if member, 0.0 if not
final_price = price - discount
print(final_price)    # 90.0
```

- `is_member` is `True` (= 1), so `0.1 * 1 = 0.1` → 10% discount applied
- If `is_member` were `False` (= 0), `0.1 * 0 = 0` → no discount
- No need to write a conditional — the math handles it

### The bool() Constructor

- Explicitly convert any value to a boolean

```python
print(bool(1))       # True
print(bool(0))       # False
print(bool("hello")) # True
print(bool(""))      # False
print(bool())        # False — no argument defaults to False
```

- **Rule:** zero and empty → `False`, everything else → `True`
- Full rules of truthiness come in Part 12 — for now, this is the mental model

**Gotcha — `bool("False")` is `True`:**

```python
print(bool("False"))   # True — surprise!
print(bool("0"))       # True — also surprise!
```

- `"False"` is a **non-empty string** → truthy
- Python does not read the text and interpret it — it checks if the string is empty or not
- Only `bool("")` is `False` — any other string, even `"False"` or `"0"`, is `True`
- This catches beginners who read data from files or user input as strings

---

## Comparison Operators

- Compare two values → produce a boolean result (`True` or `False`)
- These are how your program asks yes/no questions about data

```python
a = 10
b = 20

print(a == b)    # False  (equal to)
print(a != b)    # True   (not equal to)
print(a > b)     # False  (greater than)
print(a < b)     # True   (less than)
print(a >= 10)   # True   (greater than or equal to)
print(a <= 5)    # False  (less than or equal to)
```

| Operator | What It Asks | Example | Result |
|----------|-------------|---------|--------|
| `==` | Are they equal? | `10 == 10` | `True` |
| `!=` | Are they different? | `10 != 5` | `True` |
| `>` | Is left bigger? | `10 > 5` | `True` |
| `<` | Is left smaller? | `10 < 5` | `False` |
| `>=` | Is left bigger or equal? | `10 >= 10` | `True` |
| `<=` | Is left smaller or equal? | `5 <= 10` | `True` |

### What Happens in Memory When You Compare

- Every comparison produces a boolean **object**
- But since `True`/`False` are singletons → no new object is created
- Result just points to the existing `True` or `False` in the heap

```python
result = (10 > 5)
print(result)       # True
print(id(result))   # same id as every other True
```

- Millions of comparisons, but only two boolean objects ever exist
- This is efficient — Python does not waste memory on repeated `True`/`False` objects

### Comparing Strings

- Compared **character by character** using Unicode values
- From Part 9: `'A'` = 65, `'B'` = 66, `'a'` = 97, `'b'` = 98

```python
print("apple" < "banana")   # True — a(97) < b(98)
print("abc" == "abc")       # True
print("A" < "a")            # True — A(65) < a(97), uppercase is "smaller"
```

- First position where characters differ determines the result
- If one string is a prefix of the other → shorter one is "less than"

```python
print("app" < "apple")    # True — "app" is shorter
```

- **Real-world use:** Sorting names alphabetically, dictionary ordering, search algorithms

### == vs is — Value vs Identity

- `==` checks **value** — do they hold the same data?
- `is` checks **identity** — are they the exact same object in the heap (same `id()`)?

```python
a = 256
b = 256
print(a == b)    # True  — same value
print(a is b)    # True  — same object (256 is a cached singleton from Part 9)

a = 1000
b = 1000
print(a == b)    # True  — same value
print(a is b)    # False — different objects in heap (1000 is outside cache range)
```

- For booleans: `==` and `is` always agree (because singletons)
- For other types: they can disagree — this matters with `None` (Part 12)
- **Rule:** Use `==` to check values. Use `is` only for `None`, `True`, `False`

### Comparing Different Types

- `==` works between any types — checks if values are equal

```python
print(10 == 10.0)     # True  — int and float, same mathematical value
print(10 == "10")     # False — int and str, different types = not equal
print(True == 1)      # True  — bool is subclass of int
print(False == 0)     # True
print(True == 1.0)    # True  — 1.0 equals 1 equals True
```

- `<`, `>`, `<=`, `>=` raise **TypeError** when types are incompatible

```python
print(10 > 5)         # True  — both int, works
print(10 > 5.0)       # True  — int vs float, Python can compare these
print("10" > 5)       # TypeError: '>' not supported between 'str' and 'int'
```

- Python does **not** guess what you meant — `"10"` is a string, `5` is an integer
- Other languages silently convert and give surprising results
- Python raises an error → you catch the bug immediately
- **This is a safety feature, not a limitation**

### Common Confusion: = vs ==

```python
x = 10     # Assignment — puts value 10 into x
x == 10    # Comparison — asks "is x equal to 10?", returns True
```

- `=` puts a value into a variable
- `==` asks a question and returns True/False
- Using `=` when you mean `==` is one of the most common beginner bugs
- Python gives a syntax error if you use `=` inside a condition → catches it for you

---

## Where This Applies in Real Work

- **Authentication:** `entered_password == stored_password` — comparison is the foundation of every login
- **E-commerce:** `price > budget` — every filter, sort, and search uses comparisons
- **API validation:** `status_code == 200` — checking if a request succeeded
- **Data processing:** `age >= 18` — every rule and filter starts with a comparison
- **ML/Analytics:** `sum()` on boolean results counts how many items match — accuracy, precision, recall all use this
- **Feature flags:** Booleans toggle entire features on/off in production without deploying new code
- **Discount logic:** Multiplying by a boolean (True=1, False=0) applies or skips a calculation without needing a conditional

---

> **Next:** Part 12 — Logical Operators and Truthiness. You can now ask one question at a time. But what if you need to check two things at once? And what if every value in Python is secretly True or False?
