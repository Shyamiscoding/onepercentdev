# Part 29 — Modules and Imports

In Part 28, you used `from functools import reduce` — you pulled a function from another file and used it in yours. That's importing a module. Now let's properly understand how modules work and how to create your own.

## What Is a Module?

A **module** is simply a `.py` file. Any `.py` file you create is a module. It contains functions, variables, and classes that other files can import and use.

## Why Modules Exist

When your program grows beyond a couple of hundred lines, one file becomes unmanageable — you can't find functions, you can't reuse code across projects, and collaborating with others becomes chaotic. Modules solve this by letting you split code into separate files organized by purpose.

```
Before modules:
  main.py → 800 lines of everything mixed together

After modules:
  main.py → orchestration logic
  utils.py → helper functions
  data.py → data processing
  config.py → settings
```

---

## Module vs Package

| Term | What It Is | Example |
|------|-----------|---------|
| Module | A single `.py` file | `utils.py` |
| Package | A folder containing modules | `utils/` folder with `__init__.py` |

### Package Structure

```
project/
├── main.py
└── utils/
    ├── __init__.py
    ├── helpers.py
    └── formatters.py
```

`__init__.py` tells Python that the folder is a package. It can be empty or contain initialization code. In modern Python (3.3+), `__init__.py` is technically optional, but including it is still the professional convention.

---

## Import Patterns

### import module

```python
import math

print(math.sqrt(16))    # 4.0
print(math.pi)          # 3.141592653589793
```

You access everything through the module name. This is the safest form — it keeps the namespace clean.

### from module import name

```python
from math import sqrt, pi

print(sqrt(16))   # 4.0
print(pi)         # 3.141592653589793
```

Imports specific names directly. No need for the `math.` prefix.

### import module as alias

```python
import datetime as dt

now = dt.datetime.now()
print(now)   # 2026-05-12 11:30:00.123456 (current date/time)
```

Aliases are useful for modules with long names. Common conventions:

```python
import datetime as dt
import collections as col
```

### from module import * (Avoid This)

```python
from math import *

print(sqrt(16))   # Works, but...
```

This imports everything from the module into your namespace. Problems:

- You do not know where `sqrt` came from when reading the code
- If two modules define the same name, one silently overrides the other
- Debugging becomes harder

**Never use `import *` in production code.** Explicit imports make code traceable.

---

## Creating Your Own Module

Any `.py` file is a module. Create a file called `utils.py`:

```python
# utils.py

def clean_text(text):
    """Remove extra whitespace and convert to lowercase."""
    return text.strip().lower()

def format_currency(amount):
    """Format a number as currency."""
    return f"₹{amount:,.2f}"

def is_valid_email(email):
    """Basic email validation."""
    return "@" in email and "." in email
```

Now import and use it in `main.py`:

```python
# main.py

from utils import clean_text, format_currency, is_valid_email

user_input = "  Hello World  "
print(clean_text(user_input))    # hello world

price = 150000
print(format_currency(price))    # ₹150,000.00

email = "alice@example.com"
print(is_valid_email(email))     # True
```

Both files must be in the same directory for this to work (or the module must be on Python's search path).

---

## \_\_name\_\_ == "\_\_main\_\_"

Every Python file has a built-in variable called `__name__`. You don't create it — Python sets it automatically. But its value changes based on **how** the file is being used.

### Step 1: See what `__name__` actually is

```python
# utils.py

print(f"__name__ is: {__name__}")
```

Run it directly:

```
$ python utils.py
__name__ is: __main__
```

Python set `__name__` to `"__main__"` because this file is the one being executed.

### Step 2: Now import this same file from another file

```python
# main.py

import utils
```

```
$ python main.py
__name__ is: utils
```

Same file, but now `__name__` is `"utils"` (the module name) — because it's being imported, not run directly.

### Step 3: The problem — code runs during import

```python
# utils.py

def clean_text(text):
    return text.strip().lower()

print("Testing: ", clean_text("  HELLO  "))   # test print
```

```python
# main.py

import utils   # you just wanted the function...
```

```
$ python main.py
Testing:  hello       ← unwanted! This ran just because you imported
```

When Python imports a file, it **executes all top-level code** in that file. Your test prints pollute the other file's output.

### Step 4: The guard — protect code from running during import

```python
# utils.py

def clean_text(text):
    return text.strip().lower()

if __name__ == "__main__":
    print("Testing: ", clean_text("  HELLO  "))
```

Now run directly:

```
$ python utils.py
Testing:  hello       ← runs! because __name__ is "__main__"
```

Import from another file:

```
$ python main.py
                      ← nothing prints! the guard blocked it
```

The guard asks: "Am I the file being run directly?" If yes → run the code inside. If no (being imported) → skip it.

### Step 5: This works in ANY file, not just main.py

```
project/
├── utils.py         ← can have if __name__ == "__main__"
├── database.py      ← can have if __name__ == "__main__"
├── main.py          ← can have if __name__ == "__main__"
```

```
$ python utils.py      → utils.py's __name__ is "__main__"
$ python database.py   → database.py's __name__ is "__main__"
$ python main.py       → main.py's __name__ is "__main__"
```

Whichever file you run with `python filename.py` — that file gets `__name__ = "__main__"`. All other imported files get their actual module name. Every file can have this guard independently.

---

## sys.path — Where Python Looks for Modules

When you write `import utils`, Python searches for `utils.py` in this order:

1. The current directory (where the script is running)
2. Directories listed in the `PYTHONPATH` environment variable
3. The standard library
4. Installed packages (site-packages)

```python
import sys
print(sys.path)
```

This prints the list of directories Python searches. If your import fails with `ModuleNotFoundError`, the module is not in any of these directories.

---

## Standard Library Highlights

Python comes with a large standard library — modules that are installed with Python and ready to use:

| Module | Purpose | Example |
|--------|---------|---------|
| `math` | Mathematical functions | `math.sqrt(16)` |
| `random` | Random number generation | `random.randint(1, 100)` |
| `datetime` | Date and time handling | `datetime.datetime.now()` |
| `os` | Operating system interaction | `os.listdir(".")` |
| `sys` | System-specific parameters | `sys.argv`, `sys.path` |
| `json` | JSON encoding/decoding | `json.dumps()`, `json.loads()` |
| `collections` | Specialized containers | `Counter`, `defaultdict` |
| `functools` | Higher-order functions | `lru_cache`, `reduce` |
| `pathlib` | Object-oriented file paths | `Path("data/file.txt")` |

You have already used some of these — `functools.reduce` in Part 28, `functools.lru_cache` in Part 27.

---

## Organizing a Real Project

```
my_project/
├── main.py              # Entry point
├── config.py             # Settings and constants
├── models/
│   ├── __init__.py
│   ├── user.py           # User-related logic
│   └── product.py        # Product-related logic
├── utils/
│   ├── __init__.py
│   ├── validation.py     # Input validation helpers
│   └── formatting.py     # Output formatting helpers
├── tests/
│   ├── test_user.py
│   └── test_product.py
├── requirements.txt
├── README.md
└── .gitignore
```

Every professional project follows a structure like this. Functions are grouped by purpose into modules. Related modules are grouped into packages. The entry point imports from these modules.

> **Note:** In this series, assignments use `src/` as the code folder. When running your scripts, run from the **project root** (the folder containing `src/`). In later parts (Part 59), we will learn the professional `src/` layout with proper packaging — for now, just keep your code organized in `src/` and run from the parent directory.

---

## Where This Applies in Real Work

- **Every framework (Django, FastAPI, Flask)** splits code into modules — `models.py`, `views.py`, `urls.py`, etc. Each is imported where needed.
- **Testing** — test files import the functions they test. Without modules, automated testing is impossible.
- **Collaboration** — each developer works on different modules. Prevents merge conflicts and keeps responsibilities clear.

---

## Practice Assignment

1. Create a file `utils.py` with three functions:
   - `clean_text(text)` — strips whitespace and lowercases
   - `count_words(text)` — returns the number of words in a string
   - `reverse_words(text)` — reverses the order of words ("hello world" → "world hello")

2. Add an `if __name__ == "__main__":` block to `utils.py` that tests all three functions with sample input

3. Create a file `main.py` that:
   - Imports the three functions from `utils`
   - Asks the user for a sentence
   - Prints the cleaned text, word count, and reversed words

4. Run `utils.py` directly — verify the tests run
5. Run `main.py` — verify the tests from `utils.py` do NOT run (only the imports happen)

Save both files in your `src/` directory.

---

> **Next:** Part 30 — Third-Party Packages & APIs. You know how to import local files. Now let's download code from the internet and write a script that talks to ChatGPT!
