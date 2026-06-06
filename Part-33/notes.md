# Part 33 — Exceptions Part 1 (Error Handling Mindset)

Your `onepercentutils` package from Part 32 is live on PyPI. Strangers can install it. That is exciting — and a little terrifying. Because right now, the moment one of them passes a number instead of a string, or calls your function on an empty list, your code crashes loudly. No safety net.

You already know how to organize code into modules (Part 29), pull in third-party libraries (Part 30), isolate dependencies with virtual environments (Part 31), and publish packages to the world (Part 32). The missing skill is what professionals do *before* shipping anything: anticipate what can go wrong, and decide how the program should respond when it does.

## Errors Are Not Failure

Every beginner panics when they see a red error message. Every professional expects them.

Errors are not signs that you failed. They are signals that something needs handling. A program that never encounters errors is either trivially simple or not dealing with the real world.

Real-world programs face:
- Users entering invalid data
- Files that do not exist
- Network connections that drop
- APIs that return unexpected responses
- Databases that time out

The question is not "will errors happen?" — it is "how will your program respond when they do?"

---

## Common Python Exceptions

You have already encountered some of these:

| Exception | When It Happens |
|-----------|----------------|
| `ValueError` | Wrong value for a type: `int("abc")` |
| `TypeError` | Wrong type for an operation: `"5" + 3` |
| `KeyError` | Missing dictionary key: `d["missing"]` |
| `IndexError` | List index out of range: `[1,2][5]` |
| `FileNotFoundError` | File does not exist |
| `ZeroDivisionError` | Division by zero: `10 / 0` |
| `NameError` | Variable not defined |
| `AttributeError` | Object has no such attribute or method |

---

## try / except — Catching Exceptions

Instead of letting errors crash your program, catch them and respond:

```python
try:
    number = int(input("Enter a number: "))
    print(f"You entered: {number}")
except ValueError:
    print("That is not a valid number.")
```

If the user enters `"abc"`, `int()` raises a `ValueError`. The `except` block catches it and prints a friendly message instead of a crash.

### Catching Specific Exceptions

Always catch specific exceptions — not all of them:

```python
try:
    result = 10 / int(input("Divide 10 by: "))
except ValueError:
    print("Please enter a number.")
except ZeroDivisionError:
    print("Cannot divide by zero.")
```

Each `except` handles one type of error with an appropriate response.

### Catching Multiple Types in One Block

```python
try:
    value = int(input("Enter a number: "))
    result = 100 / value
except (ValueError, ZeroDivisionError) as e:
    print(f"Invalid input: {e}")
```

The `as e` captures the exception object, which contains the error message.

---

## The else Block

`else` runs only when **no exception** was raised in `try`:

```python
try:
    number = int(input("Enter a number: "))
except ValueError:
    print("Invalid input.")
else:
    print(f"Success! Double is {number * 2}")
```

Why use `else` instead of putting code inside `try`? Because code in `else` is protected only by its own exceptions — not lumped together with the risky code. It keeps the `try` block minimal.

---

## The finally Block

`finally` runs **no matter what** — whether an exception occurred or not:

```python
try:
    f = open("data.txt", "r")
    content = f.read()
except FileNotFoundError:
    print("File not found.")
finally:
    print("Cleanup complete.")
```

`finally` is used for cleanup: closing files, releasing resources, resetting state. It runs even if an exception is raised and not caught.

---

## The Full Pattern

```python
try:
    number = int(input("Enter a number: "))
    result = 100 / number
except ValueError:
    print("Not a number.")
except ZeroDivisionError:
    print("Cannot divide by zero.")
else:
    print(f"Result: {result}")
finally:
    print("Operation attempted.")
```

| Block | When It Runs |
|-------|-------------|
| `try` | Always — the code that might fail |
| `except` | Only if an exception matches |
| `else` | Only if NO exception occurred |
| `finally` | Always — regardless of what happened |

---

## raise — Raising Exceptions

You can raise exceptions intentionally to signal that something is wrong:

```python
def set_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative")
    if age > 150:
        raise ValueError("Age is unrealistically high")
    return age

try:
    user_age = set_age(-5)
except ValueError as e:
    print(f"Error: {e}")   # Error: Age cannot be negative
```

`raise` is how functions communicate errors to their callers. Instead of returning a special value or printing an error, the function raises an exception. The caller decides how to handle it.

### When to Raise

- Invalid input that your function cannot handle
- Business logic violations (negative price, age above 150)
- Conditions that should never happen in correct code

---

## assert — Developer Sanity Checks

`assert` tests a condition and raises `AssertionError` if it is `False`:

```python
def calculate_average(scores):
    assert len(scores) > 0, "Scores list cannot be empty"
    return sum(scores) / len(scores)

calculate_average([])   # AssertionError: Scores list cannot be empty
```

### assert vs raise

| Use | For |
|-----|-----|
| `assert` | Conditions that should never be false if the code is correct — developer-facing sanity checks |
| `raise` | Conditions caused by external input or runtime situations — user-facing validation |

Important: `assert` statements are removed when Python runs with the `-O` (optimize) flag. Never use `assert` for input validation or security checks.

---

## Exception Hierarchy

All exceptions in Python form a hierarchy:

```
BaseException
├── KeyboardInterrupt
├── SystemExit
└── Exception
    ├── ValueError
    ├── TypeError
    ├── KeyError
    ├── IndexError
    ├── FileNotFoundError
    ├── ZeroDivisionError
    └── ... many more
```

`except Exception` catches almost everything (except `KeyboardInterrupt` and `SystemExit`). `except ValueError` catches only `ValueError`. Always prefer catching specific exceptions.

Notice that `KeyboardInterrupt` and `SystemExit` sit **above** `Exception` in the tree — they inherit directly from `BaseException`. This is deliberate: when a user presses Ctrl+C, Python wants that signal to escape almost everything. So a casual `except Exception` will *not* stop Ctrl+C — you must catch `KeyboardInterrupt` explicitly if you want graceful shutdown.

---

## Bringing It Back to Your Code

So far the examples have been generic. Let's apply exception handling to the actual code you wrote in earlier parts.

### Hardening `format_currency` from your published package

Remember `format_currency` from Part 30, which is now sitting inside your published `onepercentutils` package on PyPI? Right now it crashes if a user passes a string:

```python
def format_currency(amount):
    return f"₹{amount:,.2f}"

format_currency("abc")   # TypeError: unsupported format string passed to str.__format__
```

A stranger installing your package would see an ugly traceback and think your library is broken. A professional version raises a clear, intentional error:

```python
def format_currency(amount):
    """Format a number as Indian Rupee currency."""
    if not isinstance(amount, (int, float)):
        raise TypeError(f"format_currency expected int or float, got {type(amount).__name__}")
    return f"₹{amount:,.2f}"
```

Now the caller gets a message they understand — and they can wrap it in `try/except` themselves if they want to recover.

### Wrapping the OpenAI call from Part 30

In Part 30 you wrote a `chat.py` that calls the OpenAI API. That call can fail for many real reasons: the network drops, the API key is wrong, you hit your rate limit. Without exception handling, your script crashes mid-conversation:

```python
import os
from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, RateLimitError, APIConnectionError

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hello!"}],
    )
    print(response.choices[0].message.content)
except AuthenticationError:
    print("Your API key is invalid. Check your .env file.")
except RateLimitError:
    print("You have hit your rate limit. Wait a moment and try again.")
except APIConnectionError:
    print("Cannot reach OpenAI servers. Check your internet connection.")
```

Same script — but now every failure mode produces a calm, useful message instead of a wall of red text. This is what *production-ready* means.

---

## Practical Pattern — Safe Input

```python
def get_integer(prompt, min_val=None, max_val=None):
    """Keep asking until the user enters a valid integer within range."""
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Please enter a valid integer.")
            continue

        if min_val is not None and value < min_val:
            print(f"Value must be at least {min_val}.")
            continue
        if max_val is not None and value > max_val:
            print(f"Value must be at most {max_val}.")
            continue

        return value

age = get_integer("Enter your age (1-120): ", min_val=1, max_val=120)
print(f"Your age: {age}")
```

This function combines exception handling with input validation — a reusable pattern for any CLI application.

---

## Where This Applies in Real Work

- **API endpoints:** Every request handler wraps its logic in try/except. If a database query fails, the API returns a 500 error instead of crashing the entire server.
- **Data pipelines:** When processing millions of records, one bad record should not stop the entire pipeline. Catch the error, log it, and continue.
- **User input:** Any data from a user or external system can be invalid. Exception handling prevents crashes from unexpected input.
- **Network operations:** API calls, database connections, and file downloads can fail due to timeouts, disconnections, or server errors. These are handled with try/except.
- **AI model inference:** When feeding data to a model, malformed input should be caught and reported, not allowed to crash the prediction service.
- **Published libraries:** When you publish a package (like you did in Part 32), other developers pass it inputs you never tested. Raising clear exceptions with helpful messages is how professional libraries communicate "you used me wrong" — instead of crashing with a confusing internal traceback.

---

## Practice Assignment

Build a robust number input system:

1. Create a function `get_valid_number(prompt)` that:
   - Asks for input using the prompt
   - Returns an integer if valid
   - Catches `ValueError` and asks again

2. Create a function `divide_numbers()` that:
   - Uses `get_valid_number` for both numerator and denominator
   - Catches `ZeroDivisionError`
   - Uses `else` to print the result only on success
   - Uses `finally` to print "Calculation attempted"

3. Wrap everything in a `while True` loop so the user can perform multiple divisions
4. Handle `KeyboardInterrupt` (Ctrl+C) to exit gracefully with a message

Example session:

```
Enter numerator: abc
Please enter a valid integer.
Enter numerator: 10
Enter denominator: 0
Cannot divide by zero.
Calculation attempted.
Enter numerator: 10
Enter denominator: 3
Result: 3.33
Calculation attempted.
```

Save as `safe_calculator.py` inside a fresh project folder (use `uv` from Part 31 to set up the virtual environment).

---

> **Next:** Part 34 — Exceptions Part 2. Custom exceptions, error design principles, and the patterns that make production code resilient.
