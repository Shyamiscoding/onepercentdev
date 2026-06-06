# Part 35 — Exceptions Part 3 (Hands-On Practice)

In Parts 33 and 34, you learned the *theory* of exceptions — `try/except/else/finally`, `raise`, the exception hierarchy, custom exceptions, chaining, retries, and the LBYL vs EAFP styles. That gave you the map. This chapter gives you the road.

Beginners learn exceptions best by **breaking code on purpose, reading the message, and then fixing it**. So in this part we go through every exception from the Quick Reference table in Part 34 — one at a time, one tiny example each — show the broken code, show the traceback, explain *why* it happened in plain words, then show the fix.

By the end, you will be able to look at any traceback and instantly know which kind of error it is and how to handle it.

---

## How To Use This Chapter

Every example follows the **same four-step format**, so you can move fast:

1. **Broken code** — copy-paste it into a file and run it.
2. **What you see** — the actual error message Python prints (the *traceback*).
3. **Why it happened** — one or two sentences in plain English.
4. **The fix** — either a code change (for bugs you fix) or a `try/except` (for runtime errors you handle).

> **How to run these examples:** save each snippet as `bug.py` and run `python bug.py` from your terminal. For the very short ones, you can also paste them straight into the Python REPL (`python` then Enter). Both work.
>
> **Faster option — use the bundled `example.py`:** every error in this chapter is also wrapped as a section in `Part-35/example.py`. You can run any section on its own by passing its number or letter:
>
> ```bash
> python3 example.py list      # see every section with its title
> python3 example.py 4         # run only #4 TypeError
> python3 example.py 12 13     # run multiple sections
> python3 example.py A         # run the Custom Exceptions demo
> ```
>
> Inside each section the **broken code is active by default and the fix is commented out**. The teaching flow is:
>
> 1. `python3 example.py 4` → students see the real `TypeError` traceback.
> 2. Explain what the error means and why it happened.
> 3. Open `example.py`, comment out the BROKEN block, uncomment the FIX block.
> 4. `python3 example.py 4` → students see the fixed code print correctly.
>
> Three sections need special handling: **#1 SyntaxError** and **#2 IndentationError** are parse-time errors — uncommenting them would prevent the whole file from loading, so copy those lines into a fresh `bug.py` to demo. **#26 MemoryError** can freeze your machine if uncommented and is left as read-only.

A reading order tip — **do not skip ahead**. The errors are arranged from the ones you will see on day one to the ones you will see in production. Each one teaches a small idea that the next one builds on.

---

## Mental Model — Fix vs Handle

Before the examples, remember this rule from Part 34:

| Group              | What it usually means                                | What you do                                      |
| ------------------ | ---------------------------------------------------- | ------------------------------------------------ |
| Group 1 — Everyday | A bug in *your* code — typo, wrong type, wrong value | **Fix it** by changing the code                  |
| Group 2 — File/Net | The outside world misbehaved — file gone, net down   | **Handle it** with `try/except` at runtime       |
| Group 3 — Behavior | Program ran into a runtime limit or a check failed   | **Handle it** if expected, **fix it** if not     |
| Group 4 — Rare     | Something unusual — encoding, memory, sys exit       | **Recognize it** in tracebacks; rarely catch it  |

Keep this table in your head. For every error below, ask: *"Is this a bug to fix, or a situation to handle?"*

---

## Group 1 — Everyday Errors

These are the errors you will see while writing your very first programs. Most of them are bugs in your own code. The cure is almost always **fix the code**, not catch the exception.

### 1. SyntaxError — Python cannot even read your code

**Broken code:**

```python
if x = 5:
    print("hello")
```

**What you see:**

```
  File "bug.py", line 1
    if x = 5:
         ^
SyntaxError: invalid syntax
```

**Why it happened:** `=` is *assignment* (give a name to a value). `==` is *comparison* (check if two things are equal). Python sees `if x = 5` and refuses to even start running the file because the grammar is wrong.

**The fix:**

```python
x = 5
if x == 5:
    print("hello")
```

> **Knowledge point:** `SyntaxError` is special — it is raised *before* your program runs, so you cannot catch it with `try/except`. The only fix is to read the line number Python points at and correct the grammar.

---

### 2. IndentationError — wrong spaces or tabs

**Broken code:**

```python
def greet():
print("hello")
```

**What you see:**

```
  File "bug.py", line 2
    print("hello")
    ^
IndentationError: expected an indented block
```

**Why it happened:** Python uses indentation to know what is *inside* a function or loop. The body of `greet()` must be indented (usually 4 spaces).

**The fix:**

```python
def greet():
    print("hello")
```

> **Knowledge point:** Pick spaces *or* tabs and stick with one — never mix. Most editors (VS Code, Cursor, PyCharm) auto-convert tabs to 4 spaces if you turn that setting on. Do it once and forget about it forever.

---

### 3. NameError — variable was never defined

**Broken code:**

```python
prnit("hello")
```

**What you see:**

```
NameError: name 'prnit' is not defined. Did you mean: 'print'?
```

**Why it happened:** Python looked up the name `prnit` in its dictionary of known names and did not find it. It is almost always a typo or a missing `import`.

**The fix:**

```python
print("hello")
```

> **Knowledge point:** Python 3.10+ shows the famous *"Did you mean: ..."* hint. When you see it, trust it — it is almost always right. If you see `NameError` for something you wrote yourself, check spelling first, then check whether the variable was defined *before* this line.

---

### 4. TypeError — wrong type for the operation

**Broken code:**

```python
age = "25"
next_year = age + 1
print(next_year)
```

**What you see:**

```
TypeError: can only concatenate str (not "int") to str
```

**Why it happened:** `age` is a string `"25"` (notice the quotes), not the number `25`. Python does not silently mix strings and numbers — `"25" + 1` is meaningless to it.

**The fix — change the type:**

```python
age = int("25")
next_year = age + 1
print(next_year)   # 26
```

**The fix — handle at runtime:**

```python
try:
    age = "25"
    next_year = age + 1
except TypeError:
    print("Cannot add a number to a string. Convert first with int().")
```

> **Knowledge point:** Whenever data comes from `input()`, a file, or an API, it is almost always a *string*. The first thing you do is convert it: `int(...)`, `float(...)`, `bool(...)`. If you forget, you will see `TypeError`.

---

### 5. ValueError — right type, wrong value

**Broken code:**

```python
number = int("hello")
```

**What you see:**

```
ValueError: invalid literal for int() with base 10: 'hello'
```

**Why it happened:** `int()` accepts a string (right type), but only if that string actually looks like a number. `"hello"` does not.

**The fix — handle at runtime:**

```python
raw = input("Enter a number: ")
try:
    number = int(raw)
    print(f"You entered {number}")
except ValueError:
    print(f"'{raw}' is not a valid number. Please type digits only.")
```

> **Knowledge point:** `TypeError` vs `ValueError` is a constant beginner confusion. Memorize it like this — *"wrong **type** of thing" is `TypeError`, "right type but bad **value**" is `ValueError`*.

---

### 6. KeyError — dictionary key does not exist

**Broken code:**

```python
user = {"name": "Alice", "age": 30}
print(user["email"])
```

**What you see:**

```
KeyError: 'email'
```

**Why it happened:** The dictionary `user` has only two keys — `name` and `age`. Asking for `"email"` returns nothing, so Python raises `KeyError`.

**The fix — use `.get()` (cleanest):**

```python
email = user.get("email", "no email on file")
print(email)
```

**The fix — handle at runtime:**

```python
try:
    print(user["email"])
except KeyError:
    print("Email not found for this user.")
```

> **Knowledge point:** `dict.get(key, default)` is the Pythonic way to read a key that *might* be missing. Use it whenever you are not 100% sure the key exists. Save `try/except KeyError` for cases where a missing key is genuinely an error worth reporting.

---

### 7. IndexError — list position does not exist

**Broken code:**

```python
numbers = [10, 20, 30]
print(numbers[5])
```

**What you see:**

```
IndexError: list index out of range
```

**Why it happened:** The list has 3 items, at positions `0`, `1`, and `2`. Position `5` does not exist.

**The fix — check length first (LBYL):**

```python
if len(numbers) > 5:
    print(numbers[5])
else:
    print("List is too short.")
```

**The fix — handle at runtime (EAFP):**

```python
try:
    print(numbers[5])
except IndexError:
    print("That position does not exist in the list.")
```

> **Knowledge point:** Off-by-one errors are the most common cause of `IndexError`. A list of `n` items has valid indexes `0` to `n-1`, *not* `1` to `n`. The last item is always `numbers[-1]` — that is the safe way to get it without counting.

---

### 8. AttributeError — object has no such method or attribute

**Broken code:**

```python
name = "alice"
name.append(" smith")
```

**What you see:**

```
AttributeError: 'str' object has no attribute 'append'
```

**Why it happened:** `append` is a *list* method, not a string method. Strings are immutable — you cannot add to them in place.

**The fix:**

```python
name = "alice"
full_name = name + " smith"
print(full_name)
```

> **Knowledge point:** When you see `AttributeError`, ask *"what type is this object actually?"*. A quick `print(type(name))` answers it immediately. Often you thought you had a list but you actually have a string, or you thought you had an object but you have `None`.

---

### 9. ZeroDivisionError — divided by zero

**Broken code:**

```python
total = 100
people = 0
average = total / people
```

**What you see:**

```
ZeroDivisionError: division by zero
```

**Why it happened:** Math itself does not allow division by zero, so Python refuses too.

**The fix — check first:**

```python
if people == 0:
    average = 0
else:
    average = total / people
```

**The fix — handle at runtime:**

```python
try:
    average = total / people
except ZeroDivisionError:
    average = 0
    print("No people to divide by — defaulting to 0.")
```

> **Knowledge point:** `ZeroDivisionError` shows up most often when computing averages, percentages, or ratios from user-supplied data. Always ask: *"can the denominator be zero in real input?"* If yes, guard against it.

---

### 10. ModuleNotFoundError — package is not installed

**Broken code:**

```python
import requests
```

**What you see:**

```
ModuleNotFoundError: No module named 'requests'
```

**Why it happened:** `requests` is a third-party library. It is not part of Python by default — you have to install it separately.

**The fix — install it:**

```bash
pip install requests
```

> **Knowledge point:** Always install third-party packages *inside an active virtual environment* (Part 31), never globally. If `pip install` succeeds but Python still cannot find the module, you almost certainly installed it into the wrong environment.

---

### 11. ImportError — package is there, but the thing inside is not

**Broken code:**

```python
from math import xyz
```

**What you see:**

```
ImportError: cannot import name 'xyz' from 'math'
```

**Why it happened:** `math` exists, but it does not contain anything called `xyz`. Maybe a typo, maybe wrong module.

**The fix:**

```python
from math import sqrt
print(sqrt(16))   # 4.0
```

> **Knowledge point:** `ModuleNotFoundError` = the package itself is missing. `ImportError` = the package is fine but the specific name inside is wrong. The fix is different for each — install vs. correct the name.

---

## Group 2 — File and Network Errors

These come from the *outside world*. Files get deleted, permissions change, networks drop. Your code did nothing wrong — the environment did. This is exactly where `try/except` shines: you cannot prevent these, but you can respond gracefully.

### 12. FileNotFoundError — the file is not there

**Broken code:**

```python
with open("config.txt") as f:
    print(f.read())
```

**What you see:**

```
FileNotFoundError: [Errno 2] No such file or directory: 'config.txt'
```

**Why it happened:** The file does not exist at the path Python is looking. Either the file was never created, the name is wrong, or the program is running from a different directory than you think.

**The fix — handle at runtime:**

```python
try:
    with open("config.txt") as f:
        config = f.read()
except FileNotFoundError:
    print("config.txt missing — using default settings.")
    config = "default"
```

> **Knowledge point:** When you see `FileNotFoundError`, run `import os; print(os.getcwd())` first. Nine times out of ten, your script is running from a different folder than the file lives in. Always prefer absolute paths or `pathlib` (covered in Part 37).

---

### 13. PermissionError — file exists but the OS says no

**Broken code:**

```python
with open("/etc/passwd", "w") as f:
    f.write("hacked")
```

**What you see:**

```
PermissionError: [Errno 13] Permission denied: '/etc/passwd'
```

**Why it happened:** The file is real, but the operating system will not let your user write to it. Common with system files, read-only files, or files owned by another user.

**The fix — handle at runtime:**

```python
try:
    with open("report.txt", "w") as f:
        f.write("done")
except PermissionError:
    print("Cannot write here. Try a different folder, like your home directory.")
```

> **Knowledge point:** On macOS and Linux, you can check permissions with `ls -l filename`. On Windows, right-click the file → Properties → Security. If you genuinely need to write somewhere protected, that is a signal to choose a different location, not to use `sudo`.

---

### 14. OSError — the generic operating-system error

**Broken code:**

```python
import os
os.rmdir("folder_with_files_inside")
```

**What you see:**

```
OSError: [Errno 66] Directory not empty: 'folder_with_files_inside'
```

**Why it happened:** `os.rmdir` only removes *empty* directories. The OS rejected the operation. `OSError` is the parent class for many file-system errors — including `FileNotFoundError` and `PermissionError`.

**The fix — handle at runtime:**

```python
import os
try:
    os.rmdir("folder_with_files_inside")
except OSError as e:
    print(f"Could not remove folder: {e}")
```

> **Knowledge point:** Catch `OSError` when you are not sure *which* specific file/system error to expect — it covers the whole family. Catch `FileNotFoundError` or `PermissionError` specifically when you know exactly what you want to handle.

---

### 15. ConnectionError — the network failed

**Broken code:**

```python
import urllib.request
urllib.request.urlopen("http://this-domain-does-not-exist-12345.com")
```

**What you see:**

```
urllib.error.URLError: <urlopen error [Errno 8] nodename nor servname provided>
```

(The exact message varies — but the cause inherits from `ConnectionError` / `OSError`.)

**Why it happened:** The DNS lookup or TCP connection failed. The server is unreachable, the domain is wrong, or your internet is down.

**The fix — handle at runtime:**

```python
import urllib.request
try:
    response = urllib.request.urlopen("http://example.com", timeout=5)
    print(response.status)
except (ConnectionError, OSError) as e:
    print(f"Network problem: {e}")
```

> **Knowledge point:** Network code should *always* be wrapped in `try/except`. Networks are unreliable by nature. Pair this with the retry pattern from Part 34 — try, fail, wait, try again — and your program becomes resilient instead of fragile.

---

### 16. TimeoutError — operation took too long

**Broken code:**

```python
import socket
sock = socket.create_connection(("example.com", 80), timeout=0.001)
```

**What you see:**

```
TimeoutError: timed out
```

**Why it happened:** You set a 1-millisecond timeout. The server cannot respond that fast. Real networks take tens or hundreds of milliseconds.

**The fix — handle at runtime:**

```python
import socket
try:
    sock = socket.create_connection(("example.com", 80), timeout=5)
    print("Connected.")
except TimeoutError:
    print("Server is too slow. Try again later.")
```

## Group 3 — Program Behavior Errors

These come from how your program *runs* — runtime limits, wrong sequencing, or your own checks failing. Some you fix, some you handle.

### 17. KeyboardInterrupt — the user pressed Ctrl+C

**Broken code:**

```python
import time
print("Press Ctrl+C to stop...")
while True:
    time.sleep(1)
```

**What you see (after pressing Ctrl+C):**

```
^CTraceback (most recent call last):
  ...
KeyboardInterrupt
```

**Why it happened:** The user pressed Ctrl+C to stop your program. Python turns that into a `KeyboardInterrupt` exception so any cleanup code can run before exit.

**The fix — clean up, do not silence:**

```python
import time
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopped by user. Saving progress and exiting.")
```

> **Knowledge point:** Catching `KeyboardInterrupt` is fine *only* to do final cleanup (close files, save state, log out) — and then let the program exit. **Never** swallow it silently in a `try/except: pass`. Your user must always be able to kill a program with Ctrl+C.

---

### 18. RecursionError — function called itself too many times

**Broken code:**

```python
def countdown(n):
    print(n)
    countdown(n - 1)

countdown(5)
```

**What you see:**

```
RecursionError: maximum recursion depth exceeded
```

**Why it happened:** `countdown` calls itself forever — there is no stop condition. Python kills it after about 1000 calls.

**The fix — add a base case:**

```python
def countdown(n):
    if n <= 0:
        print("Done.")
        return
    print(n)
    countdown(n - 1)

countdown(5)
```

> **Knowledge point:** Every recursive function needs a *base case* that does **not** call itself — otherwise it runs forever. If your recursion needs to go very deep (thousands of levels), prefer a `while` loop instead.

---

### 19. UnboundLocalError — used a local variable before assigning it

**Broken code:**

```python
def add_one():
    count = count + 1
    return count

add_one()
```

**What you see:**

```
UnboundLocalError: local variable 'count' referenced before assignment
```

**Why it happened:** Inside the function, Python sees `count = ...` and decides `count` is a *local* variable. But on the right side, `count` has not been given a value yet — so it cannot be read.

**The fix — give it a starting value:**

```python
def add_one(count):
    count = count + 1
    return count

print(add_one(0))   # 1
```

> **Knowledge point:** If the variable is meant to be *outside* the function (a global counter, for example), use the `global` keyword inside the function. But honestly, passing values in as arguments and returning them is almost always cleaner.

---

### 20. StopIteration — no more values left in an iterator

**Broken code:**

```python
nums = iter([1, 2, 3])
print(next(nums))   # 1
print(next(nums))   # 2
print(next(nums))   # 3
print(next(nums))   # boom
```

**What you see:**

```
StopIteration
```

**Why it happened:** `next()` pulled all three values, then asked for a fourth. There is no fourth, so the iterator signals that it is done by raising `StopIteration`.

**The fix — let `for` handle it (the normal way):**

```python
for n in [1, 2, 3]:
    print(n)
```

**The fix — handle manually if you really need `next()`:**

```python
nums = iter([1, 2, 3])
while True:
    try:
        print(next(nums))
    except StopIteration:
        print("Done.")
        break
```

> **Knowledge point:** You almost never raise or catch `StopIteration` yourself — `for` loops do it for you behind the scenes. If you ever see one in a traceback, it usually means someone called `next()` one time too many.

---

### 21. RuntimeError — a generic runtime problem

**Broken code:**

```python
data = [1, 2, 3]
for item in data:
    if item == 2:
        data.remove(item)   # mutating while iterating
```

(In some versions this raises `RuntimeError: dictionary changed size during iteration` for dicts — for lists you may instead get silently-wrong behavior, but the *type* of bug is the same family.)

**What you see (with a dict):**

```python
d = {"a": 1, "b": 2}
for key in d:
    del d[key]
```

```
RuntimeError: dictionary changed size during iteration
```

**Why it happened:** You changed the size of a collection while looping over it. Python cannot keep its place.

**The fix — loop over a copy:**

```python
d = {"a": 1, "b": 2}
for key in list(d):
    del d[key]
print(d)   # {}
```

> **Knowledge point:** `RuntimeError` is the catch-all "something went wrong at runtime, and no other type fits". Library authors raise it for unusual situations. You will rarely raise it yourself — if you can, raise something more specific.

---

### 22. AssertionError — your own sanity check failed

**Broken code:**

```python
def withdraw(balance, amount):
    assert amount > 0, "amount must be positive"
    return balance - amount

withdraw(100, -50)
```

**What you see:**

```
AssertionError: amount must be positive
```

**Why it happened:** The `assert` statement says *"if this is not true, crash with this message."* `-50` is not greater than `0`, so the assertion failed.

**The fix — use `assert` for *developer* checks, `raise` for *user* errors:**

```python
def withdraw(balance, amount):
    if amount <= 0:
        raise ValueError(f"amount must be positive, got {amount}")
    return balance - amount
```

## Group 4 — Less Common (Recognize, Rarely Catch)

You will rarely catch these yourself, but you should *recognize* them when they show up in tracebacks.

### 23. SystemExit — `sys.exit()` was called

```python
import sys

if len(sys.argv) < 2:
    print("Usage: python script.py <name>")
    sys.exit(1)
```

`sys.exit()` raises `SystemExit` internally. Python uses it to shut the program down cleanly. **Do not** catch it — let the program exit.

> **Knowledge point:** `sys.exit(0)` means "quit successfully", `sys.exit(1)` (or any non-zero) means "quit with an error". Other programs and CI systems read that exit code to decide if your script worked.

---

### 24. OverflowError — number too big for the type

```python
import math
print(math.exp(1000))
```

```
OverflowError: math range error
```

**Why it happened:** `e^1000` is bigger than the largest float Python can hold. Notice — regular `int` in Python has no size limit, so you only see this with floats and certain math functions.

**Fix:** use a smaller input, or work with logarithms instead of raw exponentials.

---

### 25. UnicodeDecodeError — file uses a different encoding

```python
with open("notes.txt") as f:
    text = f.read()
```

```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0x... in position ...
```

**Why it happened:** Python tried to read the file as UTF-8, but the file was actually saved in a different encoding (often Windows-1252 from older Windows tools).

**Fix — declare the right encoding:**

```python
with open("notes.txt", encoding="utf-8", errors="replace") as f:
    text = f.read()
```

> **Knowledge point:** Always pass `encoding="utf-8"` when opening text files. UTF-8 is the modern standard. If you cannot avoid a legacy file, `errors="replace"` swaps unreadable bytes with `?` instead of crashing.

---

### 26. MemoryError — out of RAM

```python
big = [0] * (10 ** 12)   # try to make a trillion-item list
```

```
MemoryError
```

**Why it happened:** You asked for more memory than your computer has.

**Fix:** process data in chunks (a *generator*, Part 39) instead of loading everything into one giant list.

---

### 27. NotImplementedError — placeholder, not yet written

```python
class PaymentGateway:
    def charge(self, amount):
        raise NotImplementedError("Subclasses must implement charge()")
```

**Why it happened:** A developer left a placeholder. The method is meant to be filled in by a subclass.

> **Knowledge point:** You will see this often in libraries and frameworks (especially abstract base classes — Part 41). It is a *signal* to the caller: "you need to provide your own version of this method."

---

## Hands-On — Custom Exceptions End-to-End

Time to take everything from Part 34 and build a tiny but realistic example. Save this as `bank.py` and run it.

```python
class InsufficientFundsError(Exception):
    """Raised when a withdrawal exceeds the account balance."""
    pass

class NegativeAmountError(Exception):
    """Raised when amount is zero or negative."""
    pass

class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def withdraw(self, amount):
        if amount <= 0:
            raise NegativeAmountError(f"amount must be positive, got {amount}")
        if amount > self.balance:
            raise InsufficientFundsError(
                f"{self.owner} tried to withdraw {amount} but balance is {self.balance}"
            )
        self.balance -= amount
        return self.balance


account = Account("Alice", balance=100)

for attempt in [50, -10, 200, 25]:
    try:
        new_balance = account.withdraw(attempt)
        print(f"OK — withdrew {attempt}, balance now {new_balance}")
    except NegativeAmountError as e:
        print(f"Bad amount: {e}")
    except InsufficientFundsError as e:
        print(f"Refused: {e}")
```

**Expected output:**

```
OK — withdrew 50, balance now 50
Bad amount: amount must be positive, got -10
Refused: Alice tried to withdraw 200 but balance is 50
OK — withdrew 25, balance now 25
```

> **Knowledge point:** Notice each `except` block reacts *differently* depending on the error type. That is the whole reason you create custom exceptions in the first place — so the caller can tell the difference between *"the caller made a mistake"* (negative amount) and *"the system rules said no"* (insufficient funds).

---

## Hands-On — try / except / else / finally Together

A single example that uses all four blocks so you see when each one runs.

```python
def divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Cannot divide by zero.")
        return None
    else:
        print("Division succeeded.")
        return result
    finally:
        print("Done with divide().")

print(divide(10, 2))
print("---")
print(divide(10, 0))
```

**Expected output:**

```
Division succeeded.
Done with divide().
5.0
---
Cannot divide by zero.
Done with divide().
None
```

| Block     | When it runs                                  | What you put in it                |
| --------- | --------------------------------------------- | --------------------------------- |
| `try`     | Always — this is the risky code               | Operations that might fail        |
| `except`  | Only if the matching exception was raised     | The recovery / error message      |
| `else`    | Only if **no** exception was raised in `try`  | Success-path code                 |
| `finally` | Always — even if you `return` or re-raise     | Cleanup (close files, free locks) |

> **Knowledge point:** Use `else` to keep the `try` block as small as possible. The smaller the `try`, the less likely you are to accidentally catch an exception from code that was not supposed to be guarded.

---

## Hands-On — Exception Chaining with `raise ... from ...`

```python
class ConfigError(Exception):
    pass

def load_timeout(config):
    try:
        return int(config["timeout"])
    except KeyError as e:
        raise ConfigError("config is missing the 'timeout' key") from e
    except ValueError as e:
        raise ConfigError(f"timeout must be a number, got {config['timeout']!r}") from e


try:
    load_timeout({"retries": 3})
except ConfigError as e:
    print(f"High-level: {e}")
    print(f"Caused by:  {type(e.__cause__).__name__}: {e.__cause__}")
```

**Expected output:**

```
High-level: config is missing the 'timeout' key
Caused by:  KeyError: 'timeout'
```

> **Knowledge point:** `raise ... from e` keeps the *original* error attached as `__cause__`. The high-level message tells the *user* what went wrong; the cause helps the *developer* find the root reason. Both matter.

---

## Hands-On — Re-Raising After Logging

Sometimes you want to log and then keep propagating:

```python
def process(data):
    try:
        return int(data)
    except ValueError:
        print(f"[log] bad data seen: {data!r}")
        raise   # let the caller deal with it

try:
    process("not a number")
except ValueError as e:
    print(f"Top level handler caught: {e}")
```

**Expected output:**

```
[log] bad data seen: 'not a number'
Top level handler caught: invalid literal for int() with base 10: 'not a number'
```

## Hands-On — Retry Pattern

A function that retries on failure, with exponential backoff. Save as `retry_demo.py`.

```python
import random
import time

class TemporaryError(Exception):
    pass

def flaky_operation():
    """Fails 70% of the time, succeeds 30% of the time."""
    if random.random() < 0.7:
        raise TemporaryError("network glitch")
    return "got the data"

def with_retry(func, max_retries=4, delay=1):
    for attempt in range(1, max_retries + 1):
        try:
            print(f"Attempt {attempt}...")
            return func()
        except TemporaryError as e:
            if attempt == max_retries:
                print("Out of retries — giving up.")
                raise
            print(f"  failed ({e}), retrying in {delay}s")
            time.sleep(delay)
            delay *= 2

print(with_retry(flaky_operation))
```

> **Knowledge point:** Two rules of retry. **First**, only retry errors that are *temporary* (network, timeout). Never retry things like `ValueError` — they will fail every time. **Second**, always use *exponential backoff* (double the delay each time). It avoids hammering a struggling server.

---

## Hands-On — Fallback and Graceful Degradation

```python
def fetch_user_name(user_id):
    """Pretend this hits a remote API that may fail."""
    raise ConnectionError("API down")

def display_name(user_id):
    try:
        return fetch_user_name(user_id)
    except ConnectionError:
        return f"User #{user_id}"

print(display_name(42))   # User #42
```

**Expected output:**

```
User #42
```

> **Knowledge point:** A great app degrades *gracefully* — when something is broken, it shows a less-good but still useful result. A bad app crashes. The whole skill of error handling is choosing what the *less-good but still useful* thing should be.

---

## Hands-On — LBYL vs EAFP Side-by-Side

Same task, two styles:

```python
data = {"name": "Alice"}

# LBYL — Look Before You Leap
if "age" in data:
    age = data["age"]
else:
    age = 0
print(age)

# EAFP — Easier to Ask Forgiveness than Permission
try:
    age = data["age"]
except KeyError:
    age = 0
print(age)

# Pythonic shortcut
age = data.get("age", 0)
print(age)
```

All three print `0`. The third is the cleanest. Use whichever reads most naturally for the job in front of you.

> **Knowledge point:** Python's culture leans EAFP because of *race conditions* — between checking that a file exists and opening it, another process could delete it. With EAFP, your check and your action are the same step.

---

## Mini-Project — Robust Calculator

A small calculator that uses *every* concept from this chapter. Save as `safe_calc.py`.

```python
class CalculatorError(Exception):
    """Base class for all calculator errors."""
    pass

class InvalidNumberError(CalculatorError):
    pass

class InvalidOperatorError(CalculatorError):
    pass

VALID_OPERATORS = {"+", "-", "*", "/"}

def parse_number(text, label):
    try:
        return float(text)
    except ValueError as e:
        raise InvalidNumberError(f"{label} must be a number, got {text!r}") from e

def calculate(a_text, op, b_text):
    a = parse_number(a_text, "first number")
    b = parse_number(b_text, "second number")
    if op not in VALID_OPERATORS:
        raise InvalidOperatorError(f"operator must be one of {VALID_OPERATORS}, got {op!r}")
    try:
        if op == "+": return a + b
        if op == "-": return a - b
        if op == "*": return a * b
        if op == "/": return a / b
    except ZeroDivisionError:
        raise CalculatorError("cannot divide by zero")


print("Type 'quit' as the first input to exit.")
while True:
    a_text = input("First number: ")
    if a_text.strip().lower() == "quit":
        print("Goodbye.")
        break
    op = input("Operator (+, -, *, /): ")
    b_text = input("Second number: ")

    try:
        result = calculate(a_text, op, b_text)
    except InvalidNumberError as e:
        print(f"Number error: {e}")
    except InvalidOperatorError as e:
        print(f"Operator error: {e}")
    except CalculatorError as e:
        print(f"Calculation error: {e}")
    except KeyboardInterrupt:
        print("\nInterrupted — exiting.")
        break
    else:
        print(f"Result: {result}")
    finally:
        print("---")
```

**What this project teaches you in one place:**

- A **base custom exception** (`CalculatorError`) and **subclasses** for each specific failure
- **Exception chaining** with `raise ... from e`
- **Multiple `except` blocks**, ordered from most specific to most general
- **`else` and `finally`** working alongside `except`
- **Graceful exit** on `KeyboardInterrupt`
- **Validating early** at the function boundary, before doing the real work

Try it with: `5 + 3`, `abc + 3`, `5 ? 3`, `5 / 0`, then Ctrl+C.

---

## Quick Cheat Sheet — Pick the Right Tool

When you face an error in your code, ask these three questions in order:

1. **Can I prevent it?** (typo → fix code, missing key → use `dict.get()`)
2. **Can I expect it at runtime?** (file may be missing, network may drop) → wrap in `try/except`.
3. **Is it a bug I should learn about?** Then **let it crash** in development. Crashes are how you find bugs.

| Situation                              | Best tool                              |
| -------------------------------------- | -------------------------------------- |
| Reading a maybe-missing dict key       | `dict.get(key, default)`               |
| Accessing the last list item           | `lst[-1]` and check `if lst` first     |
| Converting user input to a number      | `try/except ValueError`                |
| Opening a maybe-missing file           | `try/except FileNotFoundError`         |
| Calling a network or API               | `try/except (ConnectionError, TimeoutError)` + retry |
| Validating function arguments          | `if ...: raise ValueError(...)`        |
| Domain-specific error in your library  | Custom exception class                 |
| Catching and propagating with context  | `raise YourError(...) from e`          |
| Cleanup that must always happen        | `finally:` (or use `with`)             |

---

## Practice Assignment

Build a **temperature converter CLI** that uses everything you learned in Parts 33–35.

Requirements:

1. Define two custom exceptions: `InvalidTemperatureError` and `InvalidUnitError` (both inheriting from a common `ConverterError`).
2. Function `convert(value, from_unit, to_unit)`:
   - `from_unit` and `to_unit` must each be one of `"C"`, `"F"`, `"K"` (case-insensitive). Raise `InvalidUnitError` otherwise.
   - `value` must be a number. If a string is passed, try `float(...)` and raise `InvalidTemperatureError` (chained from the original `ValueError` using `from e`) if conversion fails.
   - Reject physically impossible temperatures (below absolute zero — `-273.15°C`, `-459.67°F`, or `0K`) with `InvalidTemperatureError`.
3. A loop that asks the user for a value and two units, calls `convert`, and:
   - Prints the converted value on success.
   - Catches each custom exception with a *specific* friendly message.
   - Catches `KeyboardInterrupt` to exit cleanly.
   - Uses `finally` to print a separator after each round.

Bonus:

- Add a retry wrapper (max 3 attempts) for invalid input — re-prompt instead of exiting.
- Log every error to a file `errors.log` *and* re-raise (`raise`), so the user still sees the message.

Save as `src/temperature_cli.py`.

---

## Where This Applies in Real Work

- **Web frameworks:** every input validator in FastAPI / Django raises a custom exception that maps to a specific HTTP status code. Same pattern as the calculator above.
- **Data engineering:** ETL pipelines processing millions of rows wrap each row in `try/except`, log the bad ones to a "dead letter" file, and keep going. Without this, one bad row kills a 10-hour job.
- **AI inference:** model servers wrap predictions in `try/except` to catch malformed inputs, return a default response, and alert monitoring — exactly the *graceful degradation* pattern.
- **Reliability engineering:** retry-with-backoff is built into every production-grade library (`tenacity`, `urllib3`, `requests-toolbelt`). The handcrafted version you saw above is what those libraries do under the hood.

---

> **Next:** Part 36 — File Handling Part 1. Now that your programs handle errors gracefully, the next missing skill is *persistence* — reading and writing files so your data survives after the program exits.
