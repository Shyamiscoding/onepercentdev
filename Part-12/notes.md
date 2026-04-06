# Part 12 — Logical Operators and Truthiness

## Connecting to Part 11

In Part 11, you learned to ask Python yes/no questions using comparison operators — `==`, `!=`, `>`, `<`. Each comparison returns `True` or `False`.

But real-world decisions are rarely based on a single question. "Is the user 18 or older **AND** do they have an ID?" — that is two questions combined. "Is the input empty **OR** is it invalid?" — another combination.

This part teaches you how to combine multiple conditions, and reveals a surprising fact: in Python, **every value is secretly True or False**.

---

## Logical Operators

Logical operators combine multiple conditions into one expression.

### and — Both must be True

```python
age = 25
has_id = True

print(age >= 18 and has_id)   # True
print(age >= 18 and not has_id)  # Would be False if has_id was False
```

`and` returns `True` only if **both** sides are `True`.

### or — At least one must be True

```python
is_student = False
is_employee = True

print(is_student or is_employee)   # True
```

`or` returns `True` if **at least one** side is `True`.

### not — Reverses the boolean

```python
is_active = True
print(not is_active)   # False
```

### The Critical Detail: and/or Return VALUES, Not True/False

Most tutorials teach that `and` returns `True` or `False`. That is **incomplete**. In Python, `and` and `or` return one of the **actual operands**, not a boolean:

```python
print("hello" and "world")   # "world"  — NOT True
print("" and "world")        # ""       — NOT False
print("hello" or "world")    # "hello"  — NOT True
print("" or "world")         # "world"  — NOT True
print(0 or 42)               # 42       — NOT True
print(None or "default")     # "default"
```

**The rule:**

- `and` returns the **first falsy value** it finds, or the **last value** if all are truthy
- `or` returns the **first truthy value** it finds, or the **last value** if all are falsy

This is not academic — senior developers use this for **default values**:

```python
username = input("Name: ") or "Anonymous"
```

If the user enters nothing (empty string = falsy), `or` skips it and returns `"Anonymous"`. If the user enters a name (truthy), `or` returns that name immediately. One line, clean, professional.

```python
config_port = user_config.get("port") or 8080
```

If the config has no port (`None` = falsy), use `8080` as the default.

### Short-Circuit Evaluation

Python stops evaluating as soon as the result is determined:

```python
# With 'and': if the first condition is False, Python skips the second
print(False and "This never gets checked")   # False — stopped at False

# With 'or': if the first condition is True, Python skips the second
print(True or "This never gets checked")     # True — stopped at True
```

This is not just a performance detail — it prevents errors:

```python
name = ""
print(name and name[0])   # "" — returned empty string, never tried name[0]
```

Without short-circuit, `name[0]` on an empty string would cause an `IndexError`. But `and` sees that `name` is falsy and returns it immediately — it never evaluates `name[0]`.

```python
name = "Python"
print(name and name[0])   # "P" — name is truthy, so and evaluates and returns name[0]
```

---

## Truthiness and Falsiness

In Python, every value has a boolean interpretation — it is either **truthy** or **falsy**. You do not need to write `== True` or `== False`. Python can evaluate any value as a boolean directly.

### The Complete Falsy List

These are ALL the values that evaluate to `False` in Python:

```python
print(bool(False))     # False  — the boolean itself
print(bool(0))         # False  — zero integer
print(bool(0.0))       # False  — zero float
print(bool(0j))        # False  — zero complex
print(bool(""))        # False  — empty string
print(bool([]))        # False  — empty list
print(bool(()))        # False  — empty tuple
print(bool({}))        # False  — empty dict
print(bool(set()))     # False  — empty set
print(bool(None))      # False  — None
```

The pattern: **zero, empty, and nothing are all falsy.** Memorize this — every other value in Python is truthy. There are no exceptions.

### Truthy Values

Everything else is truthy — even values that might surprise you:

```python
print(bool(1))         # True
print(bool(-5))        # True  — negative numbers are truthy
print(bool("hello"))   # True
print(bool(" "))       # True  — a space is NOT empty
print(bool([0]))       # True  — list with one element (even if that element is falsy)
print(bool({"key": ""}))  # True — dict with one entry
print(bool(3.14))      # True
print(bool("False"))   # True  — the STRING "False" is truthy! It's not empty.
```

That last one catches beginners: `bool("False")` is `True` because `"False"` is a non-empty string. Python does not read the word — it checks if the string has characters.

### How Python Determines Truthiness — Under the Hood

When Python needs to decide if a value is truthy or falsy (in `and`, `or`, `not`, or the `bool()` constructor), it checks two things in order:

1. Does the object have a `__bool__()` method? Call it.
2. If not, does it have a `__len__()` method? Call it — length 0 means falsy.
3. If neither exists, the object is truthy.

This is why empty strings and empty collections are falsy — they have `__len__()` which returns `0`:

```python
print(len(""))      # 0 → bool("") is False
print(len("hi"))    # 2 → bool("hi") is True
```

You do not need to write custom `__bool__()` methods yet — that comes with classes. But knowing this exists helps you understand that truthiness is not magic. It is a defined protocol.

### Why Truthiness Matters

Truthiness makes conditions cleaner. You already saw this with `and` and `or`:

```python
name = input("Enter your name: ")
greeting = name or "Anonymous"    # if name is empty (falsy), use "Anonymous"
print(f"Hello, {greeting}")
```

In Part 13 (Conditionals), you will use truthiness directly in `if` statements. For now, practice reading `bool()` results — when you see `bool("")` returns `False`, you know that an empty string will behave as `False` in any boolean context.

### None — The Absence of Value

`None` is Python's way of saying "no value" or "nothing." It is not `0`. It is not `""`. It is not `False`. It is **nothing at all**.

```python
result = None

print(type(result))     # <class 'NoneType'>
print(bool(result))     # False — None is falsy
print(result is None)   # True
```

#### None Is a Singleton

Just like `True` and `False` (from Part 11), there is exactly ONE `None` object in all of Python:

```python
a = None
b = None
print(id(a) == id(b))   # True — same object in the heap
print(a is b)            # True
```

#### is vs == for None

```python
x = None

print(x == None)     # True — works, but NOT recommended
print(x is None)     # True — correct way
```

Why `is`? Because `==` can be overridden by custom classes to return `True` for things that are not actually `None`. `is` checks identity — is this the exact same object in the heap? Since `None` is a singleton, `is None` is guaranteed to be correct.

**PEP 8** (Python's official style guide) explicitly says: "Comparisons to singletons like `None` should always be done with `is` or `is not`, never the equality operators."

#### Where You Will See None

- `print()` itself returns `None` — you just never notice:

```python
result = print("hello")    # Prints "hello"
print(result)               # None
print(type(result))         # <class 'NoneType'>
```

- Variables you want to declare but fill in later:

```python
user_data = None    # Will be populated after API call
```

- When we learn functions later, you will see that functions without an explicit `return` give back `None`. And when we learn dictionaries, `.get()` returns `None` when a key does not exist. `None` is everywhere in Python.

---

## The in Operator (Membership)

`in` checks if a value exists inside a sequence. It is one of the most commonly used operators with strings:

```python
print("P" in "Python")        # True
print("java" in "Python")     # False
print("thon" in "Python")     # True
```

### not in — The Opposite

`not in` checks if a value does **not** exist:

```python
print("Java" not in "Python is great")   # True
print("Python" not in "Python is great") # False
```

This reads like English: "Is Java not in this string?" — Yes, True.

With numbers in a `range()`:

```python
print(5 in range(10))    # True
print(15 in range(10))   # False
print(15 not in range(10))  # True
```

`in` and `not in` are used extensively with strings, lists, dictionaries, and other collections. For now, we use them with strings.

---

## Chained Comparisons

Python allows you to chain comparisons — something most languages cannot do:

```python
age = 25

# Instead of this:
print(age >= 18 and age <= 65)   # True

# Python lets you write this:
print(18 <= age <= 65)           # True
```

More examples:

```python
x = 5
print(1 < x < 10)     # True — x is between 1 and 10
print(1 < x < 3)      # False — x is not between 1 and 3

score = 85
print(80 <= score <= 100)  # True — score is in the A range
```

This reads naturally: "Is 1 less than x and x less than 10?" Python checks both conditions for you. Cleaner, shorter, more Pythonic.

---

## Operator Precedence

When multiple operators appear in one expression, Python follows a priority order. Here is the complete table:


| Priority | Operators                                                        | Description                                      |
| -------- | ---------------------------------------------------------------- | ------------------------------------------------ |
| Highest  | `()`                                                             | Parentheses (always evaluated first)             |
|          | `**`                                                             | Exponentiation                                   |
|          | `+x`, `-x`, `~x`                                                 | Unary plus, minus, bitwise NOT                   |
|          | `*`, `/`, `//`, `%`                                              | Multiplication, division, floor division, modulo |
|          | `+`, `-`                                                         | Addition, subtraction                            |
|          | `==`, `!=`, `>`, `<`, `>=`, `<=`, `is`, `is not`, `in`, `not in` | All comparisons (same level)                     |
|          | `not`                                                            | Logical NOT                                      |
|          | `and`                                                            | Logical AND                                      |
| Lowest   | `or`                                                             | Logical OR                                       |


Note: Bitwise operators (`&`, `^`, `|`, `<<`, `>>`) exist between arithmetic and comparisons, but we will not use them in this series.

Example:

```python
print(3 + 4 * 2)        # 11 (not 14, because * runs before +)
print((3 + 4) * 2)      # 14 (parentheses override precedence)
print(True or False and False)  # True (and runs before or)
```

**Rule:** When in doubt, use parentheses. They make your intent explicit and prevent bugs. Professional developers use parentheses even when they know the precedence — it makes the code readable for everyone.

---

## Complete Operators Reference

Here is every operator covered in Parts 11 and 12, in one place:


| Operator | Type       | What It Does                               | Example                     |
| -------- | ---------- | ------------------------------------------ | --------------------------- |
| `==`     | Comparison | Equal to                                   | `10 == 10` → `True`         |
| `!=`     | Comparison | Not equal to                               | `10 != 5` → `True`          |
| `>`      | Comparison | Greater than                               | `10 > 5` → `True`           |
| `<`      | Comparison | Less than                                  | `10 < 5` → `False`          |
| `>=`     | Comparison | Greater than or equal                      | `10 >= 10` → `True`         |
| `<=`     | Comparison | Less than or equal                         | `5 <= 10` → `True`          |
| `and`    | Logical    | `True` only if both sides are `True`       | `True and False` → `False`  |
| `or`     | Logical    | `True` if at least one side is `True`      | `True or False` → `True`    |
| `not`    | Logical    | Reverses the boolean                       | `not True` → `False`        |
| `in`     | Membership | `True` if value is found in collection     | `"a" in "abc"` → `True`     |
| `not in` | Membership | `True` if value is NOT found in collection | `"z" not in "abc"` → `True` |
| `is`     | Identity   | `True` if both refer to the same object    | `x is None` → `True`        |
| `is not` | Identity   | `True` if they refer to different objects  | `x is not None` → `True`    |


---

> **Next:** Part 13 — Conditionals. You now have the complete operator toolkit. But operators just produce True or False — they do not control what your program does. Next: using these results to make decisions with if, elif, and else.

