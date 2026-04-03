# Part 9 — Numbers and Math

## What You Will Walk Away With

By the end of this part, you will:

- Know every data type Python offers — the complete mental map
- Understand how numbers are stored as  and why that mattebinary in the heap —rs
- Know why `0.1 + 0.2` is NOT `0.3` — and how this one fact has caused million-dollar bugs in production

---

## Try This Before We Start

Open your terminal and run this:

```python
print(0.1 + 0.2)
```

You expect `0.3`. You will not get `0.3`. Run it. See the result.

Now run this:

```python
print(0.1 + 0.2 == 0.3)
```

You expect `True`. You will get `False`.

Why? By the end of this part, you will understand exactly why — and it has everything to do with how the heap stores your data.

---

## Connecting to Part 8 — From Objects to Binary

In Part 7, we learned that when Python executes `x = 10`, a value is created in the **heap** and a label is registered on the **stack** with an arrow pointing to it.

In Part 8, we gave those proper names — the label is a **variable**, the value in the heap is an **object**, and the arrow is a **reference**. Every object has three properties: **type** (`int`), **value** (`10`), and **identity** (its memory address).

But here is a question we have not answered yet: **how is the object `10` actually stored inside the heap?**

Your computer's memory — the RAM, the heap — does not understand the number `10`. It does not understand "hello" or `True` either. At the hardware level, RAM only understands one thing: **binary — 0s and 1s.**

When the PVM executes the bytecode and creates the integer object `10` in the heap, it stores it as binary:

```
10 in decimal  →  1010 in binary  →  stored as 0s and 1s in RAM
```

### A Quick Binary Brush-Up

Binary is just another way to write numbers — using only two digits: **0** and **1**. You already know the decimal system (base 10), where each position is a power of 10. Binary (base 2) works the same way, but each position is a power of 2:

```
Position:    8    4    2    1     (powers of 2: 2³  2²  2¹  2⁰)
             ─    ─    ─    ─
Decimal 0:   0    0    0    0  →  0
Decimal 1:   0    0    0    1  →  1
Decimal 2:   0    0    1    0  →  2
Decimal 3:   0    0    1    1  →  2 + 1 = 3
Decimal 5:   0    1    0    1  →  4 + 1 = 5
Decimal 10:  1    0    1    0  →  8 + 2 = 10
```

That is all binary is — each slot is either ON (1) or OFF (0), and you add up the positions that are ON.

You can verify this in Python:

```python
print(bin(10))    # 0b1010
print(bin(255))   # 0b11111111
print(bin(1))     # 0b1
```

The `0b` prefix just means "this is a binary number."

### What About Text?

Text is also stored as 0s and 1s — but through an extra step. Every character has a number assigned to it (a character code). Python uses **Unicode**, where `'A'` is 65, `'B'` is 66, `'a'` is 97, and so on:

```python
print(ord('A'))         # 65
print(ord('a'))         # 97
print(bin(ord('A')))    # 0b1000001  — the binary of 65
```

So when Python stores the string `"Hi"` in the heap, it converts each character to its number, and each number to binary:

```
'H' → 72 → 1001000
'i' → 105 → 1101001
```

Every piece of data — integers, floats, strings, booleans — is ultimately stored as a pattern of 0s and 1s in the heap. The **type** of the object tells Python how to interpret those 0s and 1s. The same 0s and 1s could mean a number, a letter, or a True/False — the type decides.

### The Problem with Decimals

Integers convert cleanly into binary — `10` is `1010`, `255` is `11111111`, no problem. But decimal numbers like `0.1` **cannot be represented exactly in binary**. That is not a Python bug — it is a fundamental limitation of how computers store data. We will prove this later in this part.

---

## The Full Picture — Every Data Type at a Glance

Before we dive into numbers, here is the complete map of all data types in Python. This is your mental model — the big picture of everything you will learn in the coming parts.


| Type       | What It Stores                | Mutable? | Example               | When You Use It                       |
| ---------- | ----------------------------- | -------- | --------------------- | ------------------------------------- |
| `int`      | Whole numbers                 | No       | `10`, `-3`, `0`       | Counting, IDs, indexing               |
| `float`    | Decimal numbers               | No       | `3.14`, `-0.5`        | Prices, measurements, calculations    |
| `bool`     | True or False                 | No       | `True`, `False`       | Conditions, flags, comparisons        |
| `NoneType` | Absence of a value            | No       | `None`                | Default values, "nothing here"        |
| `str`      | Text (sequence of characters) | No       | `"hello"`, `"Python"` | Names, URLs, API data, file content   |
| `list`     | Items in sequence (any type)  | Yes      | `[1, 2, 3]`           | Shopping carts, user lists, logs      |
| `tuple`    | Ordered, fixed collection     | No       | `(12.97, 77.59)`      | Coordinates, config, RGB colors       |
| `set`      | Unique items (no order)       | Yes      | `{"Python", "SQL"}`   | Removing duplicates, permissions      |
| `dict`     | Key-value pairs               | Yes      | `{"name": "Dev"}`     | API responses, configs, database rows |


We will go deep into each one in its own part — all methods, patterns, real-time examples, interview questions, time complexity. Right now, this is your mental map. You know what exists. Now we go deep.

---

## Mutable vs Immutable — The One Rule

You already know this from Part 8 — but here is how it connects to the data types above:

- **Immutable** (`int`, `float`, `bool`, `str`, `tuple`, `NoneType`) — When you "change" an immutable object, Python creates a **new object** in the heap and repoints the variable. The original object is untouched.
- **Mutable** (`list`, `dict`, `set`) — When you change a mutable object, Python modifies the **same object** in the heap. The `id()` stays the same.

This is why `id()` is your proof tool — same ID means same object, different ID means new object was created.

---

## The Learning Roadmap

Here is the order we will cover all data types and tools:

1. **Numbers** (`int`, `float`) — this part (Part 9)
2. **Strings** (`str`) — Part 10
3. **Operators and Boolean** (`bool`) — Part 11
4. **Conditionals** — Part 11
5. **Loops** — Parts 12 and 13
6. **Lists** (`list`) — Parts 14 and 15 (deep dive with all methods, complexity, real-time examples)
7. **Tuples** (`tuple`) — Part 16 (with List vs Tuple differentiation)
8. **Sets** (`set`) — Part 17 (with Set vs List differentiation)
9. **Dictionaries** (`dict`) — Parts 18 and 19 (with Dict vs List differentiation)
10. **Comprehensions** — Part 20 (list, dict, and set comprehensions)

Now let us start with the first data type — numbers. And they are not as simple as you think.

---

## Why Python Integers Have No Size Limit

Integers are whole numbers without a decimal point.

```python
a = 10
b = -3
c = 0

print(type(a))  # <class 'int'>
```

In most programming languages — C, Java, JavaScript — integers have a limit. A 32-bit integer can only hold numbers up to about 2 billion. Go beyond that and the number overflows, wraps around, or crashes.

Python integers have **no size limit**. You can do this:

```python
big = 10 ** 100
print(big)
# 10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
print(type(big))  # <class 'int'>
```

This is a design choice by Python — it handles memory allocation for large integers automatically. The heap grows as needed.

Python also lets you use underscores in numbers for readability — they are completely ignored by the interpreter:

```python
population = 8_000_000_000
print(population)   # 8000000000

budget = 1_500_000.50
print(budget)       # 1500000.5
```

This is especially useful when working with large numbers where counting zeros is error-prone.

---

## Floats — The Type That Lies to You

Floats are numbers with a decimal point.

```python
price = 99.99
temperature = -3.5

print(type(price))  # <class 'float'>
```

They look simple. But floats are the most dangerous data type in Python — because they are **not exact**.

---

## Why 0.1 + 0.2 Is Not 0.3 — The Binary Truth

Remember the first thing we did in this part? You ran `print(0.1 + 0.2)` and got `0.30000000000000004`. Now let us understand exactly why.

Everything in the heap is stored as **binary (0s and 1s)**. Integers convert cleanly: `10` → `1010`, `255` → `11111111`. But `0.1` in decimal is a **repeating fraction** in binary, just like `1/3` is `0.3333...` in decimal — it never ends. The computer has limited bits (64 bits for a float), so it rounds the binary representation. That tiny rounding error is what you see.

```python
print(0.1 + 0.2)
```

Output:

```
0.30000000000000004
```

This is **not** a Python bug. This is not a mistake. This is how every computer on earth works — C, Java, JavaScript, Rust — all of them have this same behavior. Because all of them store floats as binary.

Now try this:

```python
print(0.1 + 0.2 == 0.3)
```

Output:

```
False
```

The comparison fails because of that tiny precision difference. The hook from the beginning — now you know the answer.

### Why This Matters in Real Work

- **Financial systems:** A rounding error of 0.0000000001 across millions of transactions adds up to real money lost or gained incorrectly.
- **AI model training:** Loss values and gradient calculations involve floats. Accumulated precision errors can affect model convergence.
- **Data pipelines:** Comparing float values directly causes silent failures in data validation.

### How to Handle It

Use `round()` for controlled precision:

```python
result = 0.1 + 0.2
print(round(result, 2))  # 0.3
```

For financial or high-precision work, Python provides the `decimal` module:

```python
from decimal import Decimal
print(Decimal("0.1") + Decimal("0.2"))  # 0.3
```

The `decimal` module avoids binary representation issues by working with decimal arithmetic directly.

**Rule:** Never compare floats directly with `==`. Use `round()` or a tolerance value.

---

## Your First Toolkit — Arithmetic Operators

You already know `=` from Part 8 — it assigns a value to a variable. Now let us learn what you can do with those values.

Python gives you the standard math operators, and they work on both `int` and `float`:

```python
a = 15
b = 4

print(a + b)    # 19   (addition)
print(a - b)    # 11   (subtraction)
print(a * b)    # 60   (multiplication)
```

These work with floats too:

```python
price = 49.99
quantity = 3

total = price * quantity
print(total)    # 149.97
```


| Operator | What It Does   | Example | Result |
| -------- | -------------- | ------- | ------ |
| `+`      | Addition       | `7 + 3` | `10`   |
| `-`      | Subtraction    | `7 - 3` | `4`    |
| `*`      | Multiplication | `7 * 3` | `21`   |


These three are straightforward. But division in Python has three different operators — each with different behavior. That is where things get interesting.

---

## Three Ways to Divide — And Why Each Exists

Python has three division-related operators. Each behaves differently.

```python
print(10 / 3)    # 3.3333333333333335  (float division)
print(10 // 3)   # 3                   (floor division)
print(10 % 3)    # 1                   (modulus - remainder)
```

### `/` — Float Division

Always returns a float, even if the result is a whole number:

```python
print(10 / 2)    # 5.0 (not 5)
print(type(10 / 2))  # <class 'float'>
```

### `//` — Floor Division

Returns the integer part, discarding the decimal. Always rounds down:

```python
print(7 // 2)    # 3
print(-7 // 2)   # -4 (rounds toward negative infinity, not toward zero)
```

### `%` — Modulus (Remainder)

Returns the remainder after division:

```python
print(10 % 3)    # 1
print(15 % 5)    # 0
```

### Real-World Uses of These Operators


| Operator | Real-World Use Case                                           |
| -------- | ------------------------------------------------------------- |
| `/`      | Calculating averages, percentages                             |
| `//`     | Pagination: `total_items // items_per_page` gives total pages |
| `%`      | Checking even/odd: `number % 2 == 0`, cycling through options |


**Pagination example:**

```python
total_items = 47
items_per_page = 10

full_pages = total_items // items_per_page      # 4
remaining_items = total_items % items_per_page   # 7

print(f"Full pages: {full_pages}")
print(f"Items on last page: {remaining_items}")
```

This pattern appears in every web application that displays data in pages.

---

## Exponent Operator

```python
print(2 ** 3)     # 8  (2 raised to the power of 3)
print(10 ** 2)    # 100
print(9 ** 0.5)   # 3.0 (square root)
```

The exponent operator is used in:

- **Machine learning:** Squared error calculation (`(predicted - actual) ** 2`)
- **Cryptography:** Large number exponentiation
- **Data scaling:** Power transformations on datasets

---

## Shorthand That Saves You Time — Assignment Operators

You already know the basic assignment operator from Part 8:

```python
x = 10   # = assigns the value 10 to the variable x
```

The `=` operator is the most fundamental one — it creates a variable and points it to an object in the heap. Every program starts here.

But what if you want to update `x`? Writing `x = x + 1` works, but Python gives you a shorter way:

```python
x = 10

x += 3     # same as x = x + 3  → x is now 13
x -= 2     # same as x = x - 2  → x is now 11
x *= 4     # same as x = x * 4  → x is now 44
x /= 2     # same as x = x / 2  → x is now 22.0
```

These are called **augmented assignment operators**. They combine an arithmetic operation with assignment into one step.

Here is every assignment operator:


| Operator  | What It Does             | Equivalent To |
| --------- | ------------------------ | ------------- |
| `x = n`   | Assign value to variable | —             |
| `x += n`  | Add and assign           | `x = x + n`   |
| `x -= n`  | Subtract and assign      | `x = x - n`   |
| `x *= n`  | Multiply and assign      | `x = x * n`   |
| `x /= n`  | Divide and assign        | `x = x / n`   |
| `x //= n` | Floor divide and assign  | `x = x // n`  |
| `x %= n`  | Modulus and assign       | `x = x % n`   |
| `x **= n` | Exponent and assign      | `x = x ** n`  |


You will use `+=` constantly — in every loop counter, every running total, every accumulator pattern. When you see `i += 1` in Parts 12 and 13, you will know exactly what it means.

---

## abs() — Absolute Value

`abs()` returns the distance of a number from zero — always positive.

```python
print(abs(-10))    # 10
print(abs(10))     # 10
print(abs(-3.5))   # 3.5
print(abs(0))      # 0
```

You will see `abs()` used later in this part for comparing floats with a tolerance. It is also used in:

- **Distance calculations:** Difference between two values regardless of direction
- **Error measurement:** How far a prediction is from the actual value

---

## Built-In Numeric Functions — min, max, sum

Python provides three built-in functions that work on any collection of numbers:

```python
scores = [85, 92, 78, 95, 88]

print(min(scores))   # 78
print(max(scores))   # 95
print(sum(scores))   # 438
```

They also work with individual arguments:

```python
print(min(10, 3, 7))   # 3
print(max(10, 3, 7))   # 10
```

`sum()` only works on iterables (lists, tuples, etc.), not individual arguments.

A common pattern — calculating an average:

```python
scores = [85, 92, 78, 95, 88]
average = sum(scores) / len(scores)
print(f"Average: {average:.2f}")   # Average: 87.60
```

---

## When Python Secretly Changes Your Types

Python can convert between int and float:

```python
# int to float
x = float(10)
print(x)        # 10.0

# float to int (truncates, does not round)
y = int(3.9)
print(y)        # 3

# string to int
age = int("25")
print(age)      # 25

# string to float
price = float("99.99")
print(price)    # 99.99
```

**Important:** `int()` truncates — it removes the decimal part without rounding. `int(3.9)` is `3`, not `4`.

To round properly, use `round()` first:

```python
print(round(3.9))     # 4
print(int(round(3.9)))  # 4
```

### Why round(0.5) Is 0, Not 1

Python 3 uses **banker's rounding** (round half to even). When a number is exactly halfway, it rounds to the nearest **even** number:

```python
print(round(0.5))   # 0  (not 1!)
print(round(1.5))   # 2
print(round(2.5))   # 2  (not 3!)
print(round(3.5))   # 4
```

Most people expect `round(0.5)` to give `1`. Python rounds it to `0` because `0` is even.

This is not a bug — it is a deliberate choice to reduce rounding bias in large datasets. If you always round 0.5 up, the total will drift upward over thousands of calculations. Banker's rounding keeps the overall average balanced.

---

## Four Bugs That Will Bite You (and How to Avoid Them)

### 1. Division by Zero

```python
result = 10 / 0  # ZeroDivisionError
```

Always validate the divisor before dividing. This is one of the most common runtime errors.

### 2. Float Equality Comparison

```python
if 0.1 + 0.2 == 0.3:  # This will NOT execute
    print("Equal")
```

Never compare floats with `==`. Use `round()` or a tolerance:

```python
if abs((0.1 + 0.2) - 0.3) < 0.0001:
    print("Close enough")
```

### 3. Integer Division Surprise

```python
print(10 / 2)  # 5.0, not 5
```

If you expect an integer, use `//` or `int()`.

### 4. Mixing Types Unknowingly

```python
age = input("Enter age: ")  # This is a string
print(age + 1)  # TypeError: can't add str and int
```

Always convert input before doing math: `age = int(input("Enter age: "))`.

---

## Complete Numeric Operations Reference

Here is every arithmetic operator and numeric function covered in this part, in one place:


| Operation / Function | What It Does                                    | Example             | Result      |
| -------------------- | ----------------------------------------------- | ------------------- | ----------- |
| `=`                  | Assign value to variable                        | `x = 10`            | `x` is `10` |
| `+`                  | Addition                                        | `7 + 3`             | `10`        |
| `-`                  | Subtraction                                     | `7 - 3`             | `4`         |
| `*`                  | Multiplication                                  | `7 * 3`             | `21`        |
| `/`                  | True division (always returns float)            | `7 / 2`             | `3.5`       |
| `//`                 | Floor division (rounds down to int)             | `7 // 2`            | `3`         |
| `%`                  | Modulus (remainder)                             | `7 % 3`             | `1`         |
| `**`                 | Exponentiation                                  | `2 ** 10`           | `1024`      |
| `abs(x)`             | Absolute value                                  | `abs(-5)`           | `5`         |
| `round(x, n)`        | Round to `n` decimal places (banker's rounding) | `round(3.14159, 2)` | `3.14`      |
| `int(x)`             | Convert to integer (truncates toward zero)      | `int(3.9)`          | `3`         |
| `float(x)`           | Convert to float                                | `float(10)`         | `10.0`      |
| `pow(x, y)`          | Same as `x ** y`                                | `pow(2, 10)`        | `1024`      |
| `divmod(x, y)`       | Returns `(x // y, x % y)` as a tuple            | `divmod(17, 5)`     | `(3, 2)`    |
| `min(...)`           | Returns the smallest value                      | `min(3, 1, 7)`      | `1`         |
| `max(...)`           | Returns the largest value                       | `max(3, 1, 7)`      | `7`         |
| `sum(iterable)`      | Returns the total of all values                 | `sum([1, 2, 3])`    | `6`         |
| `x += n`             | Add and assign (shorthand for `x = x + n`)      | `x = 10; x += 3`    | `13`        |
| `x -= n`             | Subtract and assign                             | `x = 10; x -= 3`    | `7`         |
| `x *= n`             | Multiply and assign                             | `x = 10; x *= 3`    | `30`        |
| `x /= n`             | Divide and assign                               | `x = 10; x /= 4`    | `2.5`       |
| `x //= n`            | Floor divide and assign                         | `x = 10; x //= 3`   | `3`         |
| `x %= n`             | Modulus and assign                              | `x = 10; x %= 3`    | `1`         |
| `x **= n`            | Exponent and assign                             | `x = 2; x **= 10`   | `1024`      |


---

## Where This Applies in Real Work

- **API responses** often contain numeric data as strings. Converting and validating them is a daily task.
- **Database queries** return floats for averages and aggregations. Understanding precision prevents incorrect reports.
- **AI training loops** compute loss values using float arithmetic. Precision issues can mask real training progress.
- **Batch processing** uses `//` and `%` constantly — splitting data into chunks, calculating offsets, managing pagination.
- **Financial applications** never use float for money. They use `Decimal` or integer cents to avoid precision loss.

---

## Practice Assignment

Build a bill splitter program:

1. Ask the user for the total bill amount
2. Ask for the number of people
3. Calculate the exact split using `/`
4. Calculate the rounded-down split using `//`
5. Calculate the remainder using `%`
6. Print all three results with f-strings

Example output:

```
Total bill: 157
Number of people: 4
Exact split: 39.25
Rounded split: 39
Remainder: 1
```

Save it as `src/bill_splitter.py` and run it.

---

> **Next:** Part 10 — Strings. Strings are not just text — they are the foundation of AI, APIs, and data processing. Understanding their structure, immutability, and methods changes how you think about data.

