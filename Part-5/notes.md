# Part 5 — Your First Python Code

## The Python Interactive Shell (REPL)

Open your terminal and type:

```bash
python
```

(On Mac/Linux, use `python3`)

You will see:

```
>>>
```

This is the **REPL** — Read, Evaluate, Print, Loop.

- **Read** — Python reads what you type
- **Evaluate** — Python executes it
- **Print** — Python shows the result
- **Loop** — Python waits for the next input

The REPL is useful for quick experiments and testing small pieces of code. It is not meant for building applications.

Try this:

```python
>>> 2 + 3
5
>>> "hello"
'hello'
```

To exit the REPL:

```python
>>> exit()
```

---

## print() — Sending Output to the Screen

`print()` is the most basic way to send data from your program to the screen.

```python
print("Hello, World")
```

Output:

```
Hello, World
```

You can print numbers, text, or results of calculations:

```python
print(10)
print(2 + 3)
print("Python is powerful")
```

### Printing Multiple Values

```python
print("Score:", 95)
```

Output:

```
Score: 95
```

Python automatically adds a space between values when you separate them with commas.

### Printing Different Data Types

```python
print(42)            # Output: 42
print(3.14)          # Output: 3.14
print(True)          # Output: True
print(None)          # Output: None
print([1, 2, 3])     # Output: [1, 2, 3]
print({"a": 1})      # Output: {'a': 1}
```

### Why print() Matters Beyond Tutorials

`print()` is the simplest debugging tool. In real projects, when something behaves unexpectedly, developers add `print()` statements to check what values variables hold at different points.

Before learning advanced debugging tools, `print()` is your first line of investigation.

---

## The Full Power of print()

`print()` has four parameters most people never learn:

```python
print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)
```

### sep — Change What Goes Between Values

```python
print("Python", "Java", "C++")
# Output: Python Java C++

print("Python", "Java", "C++", sep=", ")
# Output: Python, Java, C++

print("Python", "Java", "C++", sep=" | ")
# Output: Python | Java | C++

print(2026, 3, 17, sep="-")
# Output: 2026-3-17
```

### end — Change What Goes After

By default, `print()` adds a newline. `end` changes that.

```python
print("Loading", end="...")
print(" Done!")
# Output: Loading... Done!

print("One", end=" → ")
print("Two", end=" → ")
print("Three")
# Output: One → Two → Three
```

### file — Print to a File Instead of Screen

```python
with open("log.txt", "w") as f:
    print("App started", file=f)
    print("User logged in", file=f)
```

Nothing appears in terminal — output goes to `log.txt`.

### flush — Force Output Immediately

Python sometimes holds output in a buffer. `flush=True` forces it out instantly.

```python
import time

print("Step 1...", flush=True)
time.sleep(1)
print("Step 2...", flush=True)
time.sleep(1)
print("Done!", flush=True)
```

Each line appears one by one, not all at once.

### Other Useful print() Tricks

```python
# Empty line for spacing
print()

# Visual separator
print("=" * 40)
# Output: ========================================

# String repetition
print("Ha" * 5)
# Output: HaHaHaHaHa

# Multi-line output
print("""
==========================
   Welcome to Python!
==========================
""")
```

### repr() — Reveal Hidden Characters

When a string "looks right" but behaves wrong, `repr()` shows what's really inside.

```python
text = "Hello\tWorld\n"

print(text)
# Output:
# Hello	World
#

print(repr(text))
# Output: 'Hello\tWorld\n'
```

Tabs (`\t`) and newlines (`\n`) become visible. Very useful for debugging.

### Quick Reference: All print() Combinations

| What You Want | Code | Output |
|---|---|---|
| Basic output | `print("hello")` | `hello` |
| Multiple values | `print("a", "b", "c")` | `a b c` |
| Custom separator | `print("a", "b", sep="-")` | `a-b` |
| No newline | `print("hi", end="")` | `hi` (no line break) |
| Custom ending | `print("hi", end="!")` | `hi!` |
| Print to file | `print("log", file=f)` | (writes to file) |
| Force instant output | `print("ok", flush=True)` | `ok` (immediately) |
| Empty line | `print()` | (blank line) |
| Visual separator | `print("=" * 30)` | `==============================` |
| Repeat string | `print("Ha" * 3)` | `HaHaHa` |
| Reveal hidden chars | `print(repr(text))` | Shows `\n`, `\t` etc. |

---

## print() Is Your First Debugger

`print()` is not just for displaying output. It is the **first debugging tool every developer uses**.

### Example: Finding a Bug

You write this:

```python
price = input("Enter price: ")
discount = 20
final = price - (price * discount / 100)
print(f"Final price: {final}")
```

You enter `500` and get:

```
TypeError: unsupported operand type(s) for -: 'str' and 'str'
```

### Debug with print()

Add prints to check what you actually have:

```python
price = input("Enter price: ")
print(f"DEBUG: price = {price}")
print(f"DEBUG: type = {type(price)}")
```

Output:

```
DEBUG: price = 500
DEBUG: type = <class 'str'>
```

`price` is a string, not a number. Fix it:

```python
price = int(input("Enter price: "))
```

### The Debugging Pattern

1. Something breaks or gives wrong output
2. Add `print()` before the broken line — check values and types
3. Compare what you expected vs what you see
4. Fix the root cause
5. Remove debug prints when done

Even senior developers do this daily. Before you learn advanced debuggers, `print()` is all you need.

### When print() Is Not Enough

| Situation | Better Tool |
|---|---|
| Need timestamps and severity levels | `logging` module |
| Want to pause and inspect variables | `pdb` debugger |
| Working in VS Code / PyCharm | IDE breakpoints |

We will cover these in later parts. For now, `print()` is your best friend.

---

## input() — Receiving Data from the User

`input()` pauses the program and waits for the user to type something.

```python
name = input("Enter your name: ")
print("Hello,", name)
```

When this runs:

```
Enter your name: OnePercentDev
Hello, OnePercentDev
```

The text inside `input()` is called a **prompt** — it tells the user what to type.

### Important: input() Always Returns a String

Everything that comes from `input()` is a **string** (text), even if the user types a number.

```python
age = input("Enter your age: ")
print(type(age))
```

Output:

```
<class 'str'>
```

Even if you type `25`, Python treats it as the text `"25"`, not the number `25`.

### Converting Input to a Number

To work with numbers from input, convert using `int()` or `float()`:

```python
age = int(input("Enter your age: "))
print(type(age))
```

Output:

```
<class 'int'>
```

Now `age` is an actual number and you can do math with it.

---

## The Truth About input() in Real Applications

### Do We Use input() in Real Applications?

**Honest answer: In web apps and APIs — no.**

In real applications, data comes from different sources:

| Source | Example |
|---|---|
| HTTP request | `request.json["name"]` in Flask/FastAPI |
| URL parameter | `/users?id=42` |
| Database | Query from PostgreSQL, MongoDB |
| Environment variable | `os.environ.get("API_KEY")` |
| Config file | `.env`, `settings.py` |
| Command-line argument | `sys.argv[1]` |

None of these use `input()`.

### So Why Learn input()?

Because `input()` teaches you the **concept** of receiving external data. The concept is the same everywhere — only the source changes:

```python
# Terminal input
name = input("Enter name: ")

# Web API input
name = request.json["name"]

# Command-line input
import sys
name = sys.argv[1]

# Environment variable input
import os
name = os.environ.get("APP_NAME")
```

Same idea: **data comes in from outside your program.** What you learn with `input()` applies to all of these.

### Where input() IS Actually Used

| Use Case | Why input() Works Here |
|---|---|
| CLI tools and scripts | Admin tools that ask "Are you sure? (y/n)" |
| Quick prototypes | Fastest way to test an idea |
| Competitive programming | LeetCode, HackerRank feed data via `input()` |
| Learning | Building fundamentals before frameworks |

### Preview: Other Ways to Receive Input

**Command-line arguments** — data comes with the command, no pausing:

```python
import sys
# Run as: python greet.py OnePercentDev
name = sys.argv[1]
print(f"Hello, {name}")
```

**Environment variables** — how real apps load secrets:

```python
import os
api_key = os.environ.get("API_KEY")
print("Key loaded" if api_key else "Warning: no API key")
```

---

## Your First Interactive Programs

### Program 1 — Greeting

```python
name = input("What is your name? ")
print("Welcome to OnePercentDev,", name)
```

### Program 2 — Simple Calculator

```python
a = int(input("Enter first number: "))
b = int(input("Enter second number: "))

print("Sum:", a + b)
print("Difference:", a - b)
print("Product:", a * b)
```

This program takes two numbers, performs basic math, and shows the results.

---

## f-strings — Clean Output Formatting

Python provides a clean way to embed values inside strings using **f-strings** (formatted string literals).

```python
name = "OnePercentDev"
age = 28
print(f"My name is {name} and I am {age} years old")
```

Output:

```
My name is OnePercentDev and I am 28 years old
```

The `f` before the quotes tells Python to look for `{}` placeholders and replace them with actual values.

f-strings are the modern, preferred way to format output in Python. You will use them constantly.

### f-string Formatting Tricks

```python
print(f"{1400000000:,}")
# Output: 1,400,000,000

print(f"{0.9534:.1%}")
# Output: 95.3%

print(f"{0.85:.0%}")
# Output: 85%

print(f"{'Python':*^20}")
# Output: *******Python*******
```

| Format | What It Does | Example Output |
|---|---|---|
| `:,` | Add commas to numbers | `1,000,000` |
| `:.1%` | Percentage with 1 decimal | `95.3%` |
| `:.0%` | Percentage, no decimal | `85%` |
| `:*^20` | Center, fill with `*` | `*******Python*******` |
| `:<20` | Left-align in 20 chars | `Python              ` |
| `:>20` | Right-align in 20 chars | `              Python` |

---

## The Fundamental Program Model

Every program — from a simple calculator to a complex AI system — follows the same core model:

```
Input → Process → Output
```

| Step    | What Happens                         | Example             |
| ------- | ------------------------------------ | ------------------- |
| Input   | Data comes in                        | User types a number |
| Process | Program does something with the data | Calculate the sum   |
| Output  | Result goes out                      | Print the answer    |

This model applies everywhere:

- A web API receives a request (input), processes it, and returns a response (output)
- An AI model receives text (input), processes it through the model, and generates a response (output)
- A data pipeline reads raw data (input), cleans and transforms it (process), and stores the result (output)

Every system you will ever build follows this pattern.

---

## REPL vs Script File

There are two ways to run Python code:

### REPL (Interactive Shell)

- Type `python` in terminal
- Execute code line by line
- Results appear immediately
- Good for quick experiments and testing

### Script File (.py)

- Write code in a file (e.g., `main.py`)
- Run with `python main.py`
- Executes the entire file top to bottom
- Used for real programs and projects

**When to use which:**

| Use Case                      | REPL or Script? |
| ----------------------------- | --------------- |
| Testing a quick calculation   | REPL            |
| Checking how a function works | REPL            |
| Building an actual program    | Script          |
| Working on a project          | Script          |
| Saving your work              | Script          |

In professional work, scripts are the standard. The REPL is a tool for exploration.

---

## Comments

Comments are lines that Python ignores. They are notes for humans reading the code.

```python
# This calculates the user's age
birth_year = int(input("Enter your birth year: "))
current_year = 2026
age = current_year - birth_year
print(f"You are {age} years old")
```

The `#` symbol marks a comment. Everything after `#` on that line is ignored by Python.

Use comments to explain **why** something is done, not **what** is done. The code itself should show what is happening. Comments should explain the reasoning behind decisions.

---

## Fun Things to Try

```python
# Emoji — Python 3 supports Unicode natively
print("Python is fun! 🐍🔥")
print("Status: ✅ Complete")

# Walrus operator (Python 3.8+) — assign and print in one line
print(length := len("OnePercentDev"))
# Output: 13
print(f"The name has {length} characters")
# Output: The name has 13 characters
```

---

## Where This Applies in Real Work

| What You Learned | Where It Shows Up |
|---|---|
| `print()` basics | Daily debugging in development |
| `sep`, `end`, `file`, `flush` | CLI tools, logging, formatted output |
| `repr()` | Debugging invisible characters in data |
| `print()` debugging | Every developer's first instinct when something breaks |
| `input()` concept | Receiving data from any source — HTTP, CLI, env vars |
| f-strings | Log messages, API responses, reports, dashboards |
| Input → Process → Output | Architecture of every backend, pipeline, and AI system |

---

## Practice Assignments

### Assignment 1 — About Me

Build a program in a file called `about_me.py` that:

1. Asks for the user's name
2. Asks for their birth year
3. Calculates their age (use 2026 as the current year)
4. Prints a formatted message using an f-string:

```
Hello [name], you are [age] years old. Welcome to your 1% developer journey!
```

### Assignment 2 — Unit Converter

Build a program in a file called `converter.py` that:

1. Asks for a temperature in Celsius
2. Converts to Fahrenheit: `F = C * 9/5 + 32`
3. Converts to Kelvin: `K = C + 273.15`
4. Prints a clean formatted output:

```
=============================
  Temperature Converter
=============================
  Celsius:    37.0
  Fahrenheit: 98.6
  Kelvin:     310.15
=============================
```

Use `float()` for conversion, f-strings with `:.1f` for formatting, and `"=" * 29` for the separator.

Save both in your `src/` folder and run with `python src/about_me.py` and `python src/converter.py`.

---

> **Next:** Part 6 — How Python actually runs your code. What happens between typing `python main.py` and seeing the output.
