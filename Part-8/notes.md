# Part 8 — Variables, Names, and Objects

## Connecting to Part 7

In Part 7, we learned how memory works. We used simple, everyday words to understand the model:

- **Labels** live on the stack (reception desk) — like `x`, `y`, `total`
- **Values** live in the heap (office workspace) — like `10`, `20`
- Labels hold **arrows** pointing to values

We kept the language simple on purpose — "labels" and "values." Now it is time to use the **real technical terms** that the Python world uses.

What we called a **"value"** in the heap — Python calls it an **object**. It is not just a raw value sitting there. Python wraps it into something more (we will see what exactly in a moment).

What we called a **"label"** on the stack — Python calls it a **variable**. But it does not work like a box holding a value. It is a **name** that points to a value — like a name tag attached to something.

What we called an **"arrow"** connecting them — Python calls it a **reference**. The label does not contain the value. It holds a reference (an arrow) pointing to where the value lives in the heap.

```
Part 7 language            →    Python's real terms
─────────────────                ─────────────────
"label" on the stack       →    variable (a name tag, not a box)
"value" in the heap        →    value is wrapped into an object
"arrow" connecting them    →    reference
```

---

## What Is an Object?

In Part 7, we said that when Python executes `x = 10`, the value `10` is created in the heap. But Python does not just throw a raw `10` into the heap. It wraps it into something more — an **object**.

Think of it using our IT company analogy. In Part 7, we said an employee sits at a desk in the office. But an employee is not just a body sitting in a chair. Every employee has:

- A **role** — developer, designer, manager. This tells you what kind of employee they are.
- Their **work** — the actual code they write, the designs they create. This is what they hold.
- An **employee ID** — a unique number. No two employees share the same ID.

Every object in Python works the same way. Every object — no matter what it is — has exactly **three properties**:

| Property | What It Tells You | Employee Analogy | How to Check |
|----------|------------------|------------------|--------------|
| **Type** | What kind of object it is | Role (developer, designer) | `type(x)` |
| **Value** | The actual data it holds | The work they do | `print(x)` |
| **Identity** | Unique ID — where it lives in memory | Employee ID number | `id(x)` |

```python
x = 42
print(type(x))   # <class 'int'>   ← Type: this is an integer
print(x)          # 42              ← Value: the actual data
print(id(x))      # 4392513824     ← Identity: unique desk number in the heap
```

So when we write `x = 10`, Python does not just store a raw `10` in the heap. It creates an **integer object** with:
- Type = `int`
- Value = `10`
- Identity = some unique address (the desk number)

```
  STACK                     HEAP
 ┌──────┐                ┌─────────────────────────┐
 │  x  ────────────────▶ │  Object                 │
 └──────┘                │    Type:     int         │
 (variable)              │    Value:    10          │
                         │    Identity: 4392513792  │
                         └─────────────────────────┘
```

This is what it means when people say **"everything in Python is an object."** Every piece of data — numbers, text, True/False, even `None` — is wrapped into an object with these three properties.

---

## Why These Three Properties Matter

These are not just trivia. They show up everywhere in real Python code:

- When you compare with `==`, Python is comparing **values** — "do these objects hold the same data?"
- When you compare with `is`, Python is comparing **identities** — "are these the exact same object in memory?"
- When you get a `TypeError`, Python is telling you the **type** is wrong — "this object is not the right kind for this operation"

Every error message, every comparison, every operation in Python connects back to these three properties. You will see this again and again.

---

## The "Variable Is a Box" Myth

Most programming tutorials teach this:

> "A variable is a box. When you write `x = 10`, the value 10 is stored inside the box called x."

That mental model is **wrong** in Python.

You already know why — from Part 7. You saw it yourself:

- The value `10` lives in the **heap** (office workspace)
- The name `x` lives on the **stack** (reception desk)
- `x` holds an **arrow** (reference) pointing to the value — not the value itself

A box **contains** something inside it. But `x` does not contain `10`. `x` is on the stack, `10` is on the heap — they are in completely different places. `x` just knows where `10` is, like a name tag attached to an object.

```
WRONG mental model (box):

  ┌─────────────┐
  │  x  =  10   │    ← value is "inside" the box
  └─────────────┘

CORRECT mental model (name tag):

  STACK                     HEAP
 ┌──────┐                ┌────────────────┐
 │  x  ────────────────▶ │  int object: 10│    ← value is in the heap
 └──────┘                └────────────────┘
 (name tag)              (object)
```

A variable in Python is a **name tag** — a label attached to an object. Not a box containing a value.

Understanding this distinction prevents the most common Python bugs and is one of the most frequently asked interview questions.

---

## How Assignment Actually Works

When you write:

```python
x = 10
```

Here is what Python does (using the proper terms now):

1. Creates an **integer object** with value `10` in the **heap**
2. Creates the **variable** `x` on the **stack**
3. The variable `x` now holds a **reference** (arrow) pointing to that object

Now try this:

```python
x = 10
y = x
```

What happens:

1. Python creates the integer object `10` in the heap
2. `x` points to it
3. `y` also points to the **same object** — no new object is created

```
  STACK                     HEAP
 ┌──────┐                ┌────────────────┐
 │  x  ────────────────▶ │  int object: 10│
 │  y  ────────────────▶ │                │
 └──────┘                └────────────────┘
 Two variables            One object
```

There is only one object `10` in memory. Both `x` and `y` are name tags pointing to it.

---

## Proving It: id() and type()

```python
x = 10
y = x

print(f"x = {x},  type = {type(x)},  id = {id(x)}")
print(f"y = {y},  type = {type(y)},  id = {id(y)}")
print(f"Same object? {id(x) == id(y)}")
```

Output:

```
x = 10,  type = <class 'int'>,  id = 4392513792
y = 10,  type = <class 'int'>,  id = 4392513792
Same object? True
```

Same `id()` — same desk number — proves both variables point to the same object in the heap.

---

## Reassignment — What Really Happens

```python
x = 10
print(f"x = {x}, id = {id(x)}")

x = 20
print(f"x = {x}, id = {id(x)}")
```

Output:

```
x = 10, id = 4392513792
x = 20, id = 4392514112
```

The IDs are **different**. When you write `x = 20`:

1. Python creates a **new** integer object with value `20` in the heap
2. The variable `x` is detached from the old object (`10`)
3. `x` now points to the new object (`20`)
4. If nothing else points to the old object (`10`), the garbage collector cleans it up

```
BEFORE: x = 10                    AFTER: x = 20

  STACK         HEAP               STACK         HEAP
 ┌──────┐     ┌────────┐         ┌──────┐     ┌────────┐
 │  x  ──────▶│ int: 10│         │  x  ──────▶│ int: 20│ ← new object
 └──────┘     └────────┘         └──────┘     └────────┘
                                               ┌────────┐
                                    nobody ──▶ │ int: 10│ ← orphan
                                               └────────┘
```

**Reassignment does not change the original object.** It creates a new object and repoints the variable.

This is the IT company analogy — the employee at desk 10 did not change. The receptionist just updated the register to point `x` to a different employee at a different desk. The old employee is still sitting there unchanged (until the cleanup crew removes them if nobody references them).

---

## Dynamic Typing — Variables Are Not Locked to a Type

Because variables are name tags (not boxes), a variable can point to **any type of object** — and you can change it anytime:

```python
x = 10
print(type(x))   # <class 'int'>

x = "hello"
print(type(x))   # <class 'str'>

x = 3.14
print(type(x))   # <class 'float'>

x = True
print(type(x))   # <class 'bool'>
```

Python does not complain. The variable `x` is just a name tag — first it pointed to an integer object, then a string object, then a float, then a boolean. The name tag moved. That is **dynamic typing**.

In the IT company — it is like the receptionist updating the register. "x" was pointing to a developer on the 4th floor. Now "x" points to a designer on the 2nd floor. The register (stack) just updated the arrow. The receptionist does not care what type of employee it is.

Dynamic typing makes Python fast to write and experiment with — no type declarations, no restrictions.

But it also means **Python will not warn you** if a variable changes type unexpectedly:

```python
count = 10
count = input("Enter count: ")  # Now count is a string, not an int
print(count + 1)                # TypeError!
```

The fix is always the same — be aware of your types. Use `type()` to check when debugging.

---

## is vs == (Identity vs Equality)

Python has two ways to compare:

### `==` checks if **values** are equal

```python
a = 1000
b = 1000
print(a == b)   # True — same value
```

Both objects hold the same value (`1000`), so `==` returns `True`.

### `is` checks if they are the **same object**

```python
a = 1000
b = 1000
print(a is b)   # may be False — different objects
```

Even though `a` and `b` have the same value, they might be different objects in memory (different IDs, different desks).

```
  STACK                     HEAP
 ┌──────┐                ┌──────────────┐
 │  a  ────────────────▶ │  int: 1000   │  desk 140700001
 │  b  ──────────┐       └──────────────┘
 └──────┘        │       ┌──────────────┐
                 └──────▶│  int: 1000   │  desk 140700002
                         └──────────────┘
 Same value, different objects, different desks
```

| Comparison | What It Asks | Checks |
|-----------|-------------|--------|
| `==` | "Do these have the same **value**?" | Value property |
| `is` | "Are these the **same object** in memory?" | Identity property |

---

## Integer Caching

Python optimizes small integers. Integers from **-5 to 256** are cached — Python creates them once at startup and reuses them.

```python
a = 100
b = 100
print(a is b)   # True — same cached object
```

```python
a = 1000
b = 1000
print(a is b)   # may be False — not cached, separate objects
```

### How This Actually Works

When CPython starts — before your code even runs — it pre-creates **262 integer objects** in the heap:

```
-5, -4, -3, -2, -1, 0, 1, 2, 3, ... 254, 255, 256
```

These objects sit in the heap permanently. They are never destroyed during the program's lifetime.

When you write `a = 100`, Python checks: "Is 100 between -5 and 256?" Yes — so instead of creating a new object, it points `a` to the **already existing** `100` object. When you write `b = 100`, the same thing happens. Both variables point to the same pre-created object.

When you write `a = 1000`, Python checks: "Is 1000 between -5 and 256?" No — so it creates a **new** object. `b = 1000` creates **another new** object. Two separate objects, same value, different desks.

In the IT company — it is like having 262 permanent employees who were hired before the company even opened. They always sit at their desks. When anyone asks for employee "100", the receptionist points to the already-seated permanent employee. No new hiring needed.

### But Wait — "I Tried It and Everything Shows True!"

If you write this in a `.py` file and run it:

```python
a = 1000
b = 1000
print(a is b)   # True?! But 1000 is outside -5 to 256!
```

You will get `True` — even though 1000 is outside the cache range. **This is not the cache doing it.** This is a different optimization.

When CPython **compiles** your `.py` file, it scans the source code and notices: "There are two identical constant values `1000` and `1000` in the same file." So the compiler creates **one** object and reuses it for both. This happens at **compile time**, before the code even runs. The compiler is being smart — why create two identical constants when one will do?

This is called **constant folding**. It applies to any values the compiler can see directly in the source code — integers, strings, floats, anything hardcoded.

### When Does Integer Caching Actually Matter?

The real issue shows up when values come from **different sources at runtime** — user input, calculations, APIs, databases. The compiler cannot optimize these because it does not know what value will arrive:

```python
a = 1000
b = int(input("Enter a number: "))   # user types 1000

print(a == b)    # True  — same value
print(a is b)    # False — different objects in the heap!
```

Why? `a = 1000` was created at compile time. `b = int(input(...))` was created at **runtime** from user input. The compiler could not know they would be the same value. So Python created two separate objects in the heap — same value, different desks.

```
  STACK                     HEAP
 ┌──────┐                ┌──────────────┐
 │  a  ────────────────▶ │  int: 1000   │  desk 140700001 (from source code)
 │  b  ──────────┐       └──────────────┘
 └──────┘        │       ┌──────────────┐
                 └──────▶│  int: 1000   │  desk 140700002 (from user input)
                         └──────────────┘
 Same value, different objects — a is b → False
```

Now try the same thing with a small number:

```python
a = 100
b = int(input("Enter a number: "))   # user types 100

print(a == b)    # True  — same value
print(a is b)    # True  — SAME cached object!
```

This time `a is b` is `True` even though `b` came from user input. Why? Because `100` is in the cache range (-5 to 256). Python did not create a new object — it pointed `b` to the **already existing** cached `100` object. The cache works across all sources — compile time, runtime, user input, everywhere.

**That is the difference:**

| Scenario | Small int (-5 to 256) | Large int (outside range) |
|---|---|---|
| Both hardcoded in same `.py` file | `is` → True (compiler optimization) | `is` → True (compiler optimization) |
| One hardcoded, one from input/API/calculation | `is` → True (runtime cache) | `is` → **False** (separate objects) |

### Verify the Boundaries Yourself

Try this in the **Python REPL** (interactive mode), typing each line separately:

```
>>> a = 256
>>> b = 256
>>> a is b
True          ← 256 is the last cached number

>>> a = 257
>>> b = 257
>>> a is b
False         ← 257 is outside the cache range

>>> a = -5
>>> b = -5
>>> a is b
True          ← -5 is the first cached negative number

>>> a = -6
>>> b = -6
>>> a is b
False         ← -6 is outside the cache range
```

Each line in the REPL is compiled separately — so the compiler constant folding does not apply. You see the **pure caching behavior** here.

### Quick Reference

| Question | Answer |
|---|---|
| Which integers are cached? | Exactly -5 to 256 |
| When are they created? | At CPython startup, before your code runs |
| Where do they live? | In the heap, permanently |
| Based on your RAM size? | No, same on every system |
| Does this apply to floats? | No, only integers |
| Can you change the range? | Not without modifying CPython's source code |
| Why does `is` return True for 1000 in a `.py` file? | Compiler optimization (constant folding), not caching |

### The Rule

**Always use `==` to compare values.** Never use `is` to check if two values are equal — it might work sometimes (because of caching or compiler optimization) and silently fail other times (when values come from different sources).

The only common use of `is` in real Python code: **`if x is None`**. That is it.

---

## Everything in Python Is an Object

This is not a metaphor. In Python, literally everything is an object — it has a type, a value, and an identity:

```python
print(type(42))          # <class 'int'>
print(type("hello"))     # <class 'str'>
print(type(3.14))        # <class 'float'>
print(type(True))        # <class 'bool'>
print(type(None))        # <class 'NoneType'>
print(type(print))       # <class 'builtin_function_or_method'>
```

Even the `print` function itself is an object. It has a type, an identity, and a value.

```python
print(id(print))         # some number — print is an object sitting in the heap
```

This is a design decision in Python. It makes the language consistent — the same three rules (type, identity, value) apply to everything. Numbers, text, True/False, None, functions — all objects, all in the heap, all with the same three properties.

---

## Types You Know So Far

| Type | What It Represents | Example |
|------|-------------------|---------|
| `int` | Whole numbers | `10`, `-3`, `0` |
| `float` | Decimal numbers | `3.14`, `-0.5` |
| `str` | Text (strings) | `"hello"`, `"Python"` |
| `bool` | True or False | `True`, `False` |
| `NoneType` | Absence of a value | `None` |

Every one of these is an object. Every one has type, value, and identity. We will explore each data type deeply in the upcoming parts.

---

## Naming Rules and Conventions

### Rules (Python enforces these)

- Names can contain letters, numbers, and underscores
- Names cannot start with a number
- Names are case-sensitive (`age` and `Age` are different)
- Reserved keywords cannot be used as names (`if`, `for`, `while`, `class`, etc.)

```python
# Valid
user_name = "Dev"
age_2 = 28
_private = "internal"

# Invalid
2name = "error"      # cannot start with number
my-name = "error"    # hyphens not allowed
class = "error"      # 'class' is a reserved keyword
```

### Conventions (Python community follows these — PEP 8)

| Convention | Usage | Example |
|-----------|-------|---------|
| snake_case | Variables and functions | `user_name`, `calculate_age` |
| UPPER_CASE | Constants | `MAX_RETRIES`, `API_KEY` |
| PascalCase | Classes | `UserProfile`, `DataPipeline` |

Following these conventions makes your code readable and consistent with the Python ecosystem.

---

## Mutability Preview

Objects in Python fall into two categories:

**Immutable** — cannot be changed after creation:

- `int`, `float`, `str`, `bool`, `tuple`, `frozenset`, `range`, `bytes`, `NoneType`

**Mutable** — can be changed after creation:

- `list`, `dict`, `set`

We have not covered all of these yet. In the next part, you will see the full data types overview.

For now, the important thing to understand:

```python
name = "Python"
name = "C"
```

This does **not** change the original string object `"Python"`. It creates a **new** string object `"C"` in the heap and repoints the variable `name` to it. The original `"Python"` object is untouched. That is what immutability means.

```
BEFORE: name = "Python"           AFTER: name = "C"

  STACK         HEAP               STACK         HEAP
 ┌──────┐     ┌───────────┐      ┌──────┐     ┌───────────┐
 │ name ─────▶│str: Python│      │ name ─────▶│str: C     │ ← new object
 └──────┘     └───────────┘      └──────┘     └───────────┘
                                               ┌───────────┐
                                    nobody ──▶ │str: Python│ ← orphan
                                               └───────────┘
```

Why this matters: when you pass variables to functions or assign them to new variables, the behavior is different for mutable vs immutable objects. Understanding this prevents a major category of bugs. We will explore this deeply when we cover lists and dictionaries.

---

## Where This Applies in Real Work

- **Function arguments** — when you pass a variable to a function, you pass a reference. If the object is mutable, the function can change it, and the caller sees the change. This surprises developers who think variables are boxes.
- **Configuration management** — in Django and FastAPI, settings are stored as variables pointing to string and integer objects. Understanding references helps when debugging configuration issues.
- **API data handling** — when JSON data comes from an API, it gets parsed into Python objects. Understanding types and references helps you process and validate data correctly.
- **Memory efficiency** — Python reuses small integer objects (caching). Understanding this explains why certain optimizations work.

---

## Practice Assignment

1. Open the Python REPL and run:

```python
x = 42
print(f"Type:     {type(x)}")
print(f"Value:    {x}")
print(f"Identity: {id(x)}")
```

2. Verify: every object has exactly three properties — type, value, identity.

3. Now try:

```python
a = 256
b = 256
print(f"a is b: {a is b}")    # True — cached

c = 257
d = 257
print(f"c is d: {c is d}")    # may be False — not cached
```

4. Explain to yourself why the results are different using what you know about integer caching and the heap.

5. Try this:

```python
name = "Python"
greeting = name
print(f"id(name)     = {id(name)}")
print(f"id(greeting) = {id(greeting)}")

name = "C"
print(f"id(name)     = {id(name)}")
print(f"id(greeting) = {id(greeting)}")
print(f"greeting     = {greeting}")
```

6. Answer: After `name = "C"`, does `greeting` also change to `"C"`? Why or why not? Use the stack/heap model to explain.

---

> **Next:** Part 9 — Data Types and Numbers. Now that you understand objects, it is time to learn the different types of objects Python provides — and numbers are not as simple as you think.
