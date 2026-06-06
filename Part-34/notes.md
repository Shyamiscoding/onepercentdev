# Part 34 — Exceptions Part 2 (Professional Error Design)

In Part 33, you learned `try/except/else/finally`, how to `raise` exceptions, and the exception hierarchy. Those are the mechanics. Now we go deeper — designing your own exception types, avoiding common anti-patterns, and writing error handling that professionals trust in production.

---

## Quick Reference — Common Python Exceptions

Before we dive in, here is the complete list of Python's built-in exceptions you should recognize. Group 1 are everyday errors you have already seen. Groups 2-4 appear less often, but you will hit them in real-world projects — especially when working with files, networks, and APIs. You do not need to memorize all of them — just glance through so you recognize them when they show up in tracebacks.

### Group 1 — Everyday Errors


| Exception             | When It Happens                                                                                               |
| --------------------- | ------------------------------------------------------------------------------------------------------------- |
| `SyntaxError`         | You wrote code Python cannot even read — like `if x = 5:` (used `=` instead of `==`)                          |
| `IndentationError`    | Your indentation is wrong — usually mixing tabs and spaces, or missing indentation inside a function/loop     |
| `NameError`           | You used a variable that was never defined — often just a typo like `prnit(x)`                                |
| `TypeError`           | You did an operation on the wrong type — like `"5" + 3` or `len(5)`                                           |
| `ValueError`          | Right type, but the value is invalid — like `int("hello")`                                                    |
| `KeyError`            | Asked for a dictionary key that does not exist — `d["missing"]`                                               |
| `IndexError`          | Asked for a list position that does not exist — `[1, 2][5]`                                                   |
| `AttributeError`      | Tried to use a method or attribute an object does not have — `"hello".append(...)` (strings have no `append`) |
| `ZeroDivisionError`   | Divided by zero — `10 / 0`                                                                                    |
| `ModuleNotFoundError` | Tried to `import` a package you have not installed — `import requests` without `pip install requests`         |
| `ImportError`         | The package exists, but the specific thing inside does not — `from math import xyz`                           |


### Group 2 — File & Network Errors


| Exception           | When It Happens                                                                                                                                          |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `FileNotFoundError` | Tried to open a file that does not exist on disk                                                                                                         |
| `PermissionError`   | The file exists, but the OS will not let you read or write it (no permission)                                                                            |
| `OSError`           | Generic OS-level error and parent of `FileNotFoundError`, `PermissionError`, etc. — use when you are not sure which specific file/system error to expect |
| `ConnectionError`   | Network failed — server unreachable, internet dropped, DNS failed. Very common with API calls                                                            |
| `TimeoutError`      | Operation took too long — common when an API, database, or external service does not respond in time                                                     |


### Group 3 — Program Behavior Errors


| Exception           | When It Happens                                                                                                                                                           |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `KeyboardInterrupt` | The user pressed **Ctrl+C** to stop your program. **Never silently catch this** — always let the user kill the program if they want to                                    |
| `RecursionError`    | A function called itself too many times (over ~1000 by default). Usually means you forgot the stopping condition in a recursive function                                  |
| `UnboundLocalError` | You tried to use a local variable before assigning a value to it — often a typo where you wrote `count = count + 1` but `count` was never initialized inside the function |
| `StopIteration`     | You called `next()` on an iterator that has no more values left — usually happens internally when a `for` loop finishes                                                   |
| `RuntimeError`      | Generic runtime problem when no other exception type fits — rare to use directly, you will see it occasionally in libraries                                               |
| `AssertionError`    | An `assert` statement failed — means a developer's sanity check caught a bug in their own code                                                                            |


### Group 4 — Less Common (Good to Recognize)


| Exception             | When It Happens                                                                                                                                                                                                                                  |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `SystemExit`          | Raised when `sys.exit()` is called. For example: your script checks if a command-line argument is missing and calls `sys.exit(1)` to quit immediately. Python also uses this internally to shut down cleanly. You almost never catch it manually |
| `OverflowError`       | A math result is too large for the data type — happens with floats (e.g. `math.exp(1000)`). Rare with regular Python `int` (which has no size limit)                                                                                             |
| `UnicodeDecodeError`  | Tried to read bytes as text but the encoding does not match — common when opening files written in a different encoding (e.g. trying to read a Windows-1252 file as UTF-8)                                                                       |
| `MemoryError`         | The program ran out of RAM — happens when you create very large data structures or have an infinite loop that keeps creating new objects                                                                                                         |
| `NotImplementedError` | A method exists in the code but the developer has not actually written what it should do yet — you will see this in abstract classes (Part 41) and unfinished libraries                                                                          |


A useful rule of thumb: **Group 1 you fix by changing your code. Groups 2-3 you fix by handling at runtime with `try/except`. Group 4 is mostly informational** — you rarely catch them yourself, but you should know what they mean when you see them in a traceback.

---

## Custom Exceptions

Built-in exceptions cover generic errors. But real applications have domain-specific errors that deserve their own names.

```python
# No import needed — Exception is a Python built-in (like print, len, int).
# Every exception in the Quick Reference table above is also built-in.

class InvalidAgeError(Exception):
    """Raised when an age value is outside the valid range."""
    pass

class InvalidEmailError(Exception):
    """Raised when an email format is invalid."""
    pass
```

> **Where does `Exception` come from?** `Exception` is a built-in Python class — part of the `builtins` module that Python automatically loads into every file. The same is true for `ValueError`, `TypeError`, `KeyError`, and every other exception in the reference table above. You never need to `import` them. The only time you import an exception is when it lives inside a library — for example, `from requests.exceptions import ConnectionError` or `from json import JSONDecodeError`.

This uses the `class` keyword, which we cover in depth in Part 41. For now, treat it as a copy-paste recipe: `class YourErrorName(Exception): pass`. You do not need to understand classes yet — just follow this pattern, and it will make full sense when you reach Part 41.

### Using Custom Exceptions

```python
def validate_age(age):
    if not isinstance(age, int):
        raise InvalidAgeError(f"Age must be an integer, got {type(age).__name__}")
    if age < 0 or age > 150:
        raise InvalidAgeError(f"Age must be between 0 and 150, got {age}")
    return age

def validate_email(email):
    if "@" not in email or "." not in email:
        raise InvalidEmailError(f"Invalid email format: {email}")
    return email
```

```python
try:
    validate_age(-5)
except InvalidAgeError as e:
    print(f"Age error: {e}")   # Age error: Age must be between 0 and 150, got -5

try:
    validate_email("shyam")
except InvalidEmailError as e:
    print(f"Email error: {e}")   # Email error: Invalid email format: shyam
```

### When to Create Custom Exceptions


| Use Custom Exceptions                                          | Use Built-in Exceptions                                 |
| -------------------------------------------------------------- | ------------------------------------------------------- |
| Domain-specific errors (InvalidAgeError, PaymentFailedError)   | Generic type/value problems                             |
| When callers need to distinguish between different error types | When the built-in name accurately describes the problem |
| In libraries and frameworks used by other developers           | In simple scripts                                       |


---

## The except: pass Anti-Pattern

This is the worst thing you can write in Python:

```python
try:
    result = dangerous_operation()
except:
    pass
```

This catches **every** exception — including `KeyboardInterrupt` (Ctrl+C) — and silently ignores it. Bugs hide. Data corrupts. You spend hours debugging an issue that was already signaled by an exception you swallowed.

```python
# Never do this
try:
    user = get_user(user_id)
except:
    pass   # User is now undefined. Code below will crash mysteriously.
```

### The Correct Approach

```python
try:
    user = get_user(user_id)
except KeyError:
    print(f"User {user_id} not found")
    user = None
```

Catch specific exceptions. Handle them explicitly. Never swallow errors silently.

---

## Catching Too Broadly

```python
# Too broad — hides real bugs
try:
    result = complex_calculation(data)
except Exception:
    print("Something went wrong")
```

If `complex_calculation` has a bug that raises `TypeError`, this code hides it. You see "Something went wrong" instead of the actual error.

```python
# Better — catch what you expect
try:
    result = complex_calculation(data)
except ValueError as e:
    print(f"Invalid data: {e}")
except ZeroDivisionError:
    print("Division by zero in calculation")
```

Catch only what you expect and know how to handle. Let unexpected errors propagate — they reveal bugs.

---

## Exception Chaining

When catching one exception and raising another, preserve the original context:

```python
class DataProcessingError(Exception):
    pass

def process_record(record):
    try:
        age = int(record["age"])
    except (ValueError, KeyError) as e:
        raise DataProcessingError(f"Failed to process record: {record}") from e
```

```python
try:
    process_record({"name": "Alice", "age": "abc"})
except DataProcessingError as e:
    print(e)
    print(f"Caused by: {e.__cause__}")
```

`from e` chains the exceptions together. When debugging, you see both the high-level error and the original cause.

---

## Re-Raising Exceptions

Sometimes you want to catch an exception, do something (like logging), and then let it propagate:

```python
def process_data(data):
    try:
        result = transform(data)
    except ValueError:
        print(f"Warning: bad data encountered: {data}")
        raise   # Re-raises the same exception

try:
    process_data("bad input")
except ValueError as e:
    print(f"Caught at top level: {e}")
```

`raise` without arguments re-raises the current exception with its original traceback intact.

---

## LBYL vs EAFP

Two philosophies for dealing with potential errors. Both terms are **officially defined in the Python language documentation** — they are not community slang, but canonical Python terminology.

> **Official sources** (read straight from python.org):
>
> - [LBYL — Python Glossary](https://docs.python.org/3/glossary.html#term-LBYL)
> - [EAFP — Python Glossary](https://docs.python.org/3/glossary.html#term-EAFP)
>
> The phrase "easier to ask forgiveness than permission" itself dates back to **Rear Admiral Grace Hopper**, one of the pioneers of computer science. The Python community adopted it as a coding philosophy and formally added it to the language's glossary.

### LBYL — Look Before You Leap

Check conditions before acting:

```python
if "name" in user_data:
    name = user_data["name"]
else:
    name = "Unknown"
```

### EAFP — Easier to Ask Forgiveness than Permission

Try and handle failure:

```python
try:
    name = user_data["name"]
except KeyError:
    name = "Unknown"
```

Python favors EAFP. The official Python glossary explicitly describes it as the "clean and fast" Pythonic style. It is often faster (avoids double lookups) and handles race conditions better. But the best solution here is:

```python
name = user_data.get("name", "Unknown")
```

Use whatever is clearest for the situation.

---

## Safe Failure Patterns

### Retry Logic

```python
import time

def fetch_with_retry(url, max_retries=3, delay=1):
    """Attempt to fetch a URL with retries on failure."""
    for attempt in range(1, max_retries + 1):
        try:
            print(f"Attempt {attempt}...")
            response = make_request(url)   # hypothetical function
            return response
        except ConnectionError:
            if attempt == max_retries:
                raise
            print(f"Failed. Retrying in {delay}s...")
            time.sleep(delay)
            delay *= 2   # exponential backoff
```

Each retry waits longer than the last. After the final attempt, the exception propagates.

### Fallback Values

```python
def get_config_value(config, key, default=None):
    try:
        return config[key]
    except KeyError:
        return default

timeout = get_config_value(settings, "timeout", default=30)
```

### Graceful Degradation

```python
def get_user_display_name(user_id):
    try:
        user = fetch_user(user_id)
        return user["display_name"]
    except (KeyError, ConnectionError):
        return f"User #{user_id}"
```

If the full data is unavailable, return a reasonable alternative instead of crashing.

---

## Error Design Principles

1. **Validate early** — check inputs at the boundary (function entry, API request, user input). Do not let bad data travel deep into your system.
2. **Fail clearly** — error messages should say what went wrong and what was expected. `"Invalid email format: shyam"` is better than `"Error"`.
3. **Provide context** — include the problematic value in the error message. `f"Age must be positive, got {age}"` helps debugging.
4. **Catch narrowly** — catch the most specific exception possible. `except ValueError` is better than `except Exception`.
5. **Never silence errors** — if you catch an exception, log it, handle it, or re-raise it. Never `except: pass`.

---

## Where This Applies in Real Work

- **FastAPI / Django:** Custom exceptions map to HTTP error codes. `raise HTTPException(status_code=404, detail="User not found")` returns a proper API error response.
- **Retry logic:** API clients, message queues, and database connections all use retry patterns with exponential backoff.
- **Data pipelines:** When processing a million records, custom exceptions categorize failures (InvalidFormatError, MissingFieldError). The pipeline logs each failure and continues.
- **AI inference:** Model serving systems catch prediction errors, return fallback responses, and alert monitoring systems.
- **Error boundaries:** Microservices isolate failures so that one service crashing does not take down the entire system.

---

## Practice Assignment

Build a user registration system:

1. Create two custom exceptions:
  - `InvalidAgeError` — for ages outside 13-120
  - `InvalidEmailError` — for emails missing `@` or `.`
2. Create a function `register_user(name, age, email)`:
  - Validate `name` is not empty (raise `ValueError`)
  - Validate `age` is between 13 and 120 (raise `InvalidAgeError`)
  - Validate `email` contains `@` and `.` (raise `InvalidEmailError`)
  - If all valid, return a dictionary with the user data
3. Create a main loop that:
  - Asks for name, age, and email
  - Calls `register_user` inside a try/except
  - Catches each custom exception with a specific message
  - On success, prints the registered user
  - Loops until the user types "quit"

Example session:

```
Name: Alice
Age: 10
Email: alice@example.com
Error: Age must be between 13 and 120, got 10

Name: Bob
Age: 25
Email: bob-email
Error: Invalid email format: bob-email

Name: Charlie
Age: 30
Email: charlie@example.com
Registered: {'name': 'Charlie', 'age': 30, 'email': 'charlie@example.com'}
```

Save as `src/user_registration.py`.

---

> **Next:** Part 35 — Exceptions Part 3 (Hands-On Practice). You now have the theory of professional error design. Next, we put every exception type from this chapter on the workbench — one tiny example each — so the patterns become muscle memory before we move on to file handling.

