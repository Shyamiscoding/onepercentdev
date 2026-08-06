# Part 51 — Context Managers

> **A bit of history:** The `with` statement and the context manager protocol (`__enter__` / `__exit__`) were introduced **together** in **Python 2.5 (2006)** by Guido van Rossum and Nick Coghlan — to replace the repetitive, easy-to-forget `try/finally` cleanup pattern. Reference: [PEP 343 — The "with" Statement](https://peps.python.org/pep-0343/).

## What with Really Does

You have been writing `with open(...)` since Part 36:

```python
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()
```

**Before** `with`**, you had to close the file yourself using** `try` **/** `finally`**:**

```python
f = open("data.txt", "r", encoding="utf-8")
try:
    content = f.read()
finally:
    f.close()   # you must remember this — and it must run even if read() crashes
```

Both do the same job — but the `try` / `finally` version is longer and easy to forget (forget `f.close()` and the file leaks). `with` does exactly this cleanup for you, automatically.

You know it automatically closes the file. But what is `with` actually doing?

`with` calls two special methods on the object:

1. `__enter__()` — runs at the start, returns the resource
2. `__exit__()` — runs at the end, handles cleanup

```python
# What 'with' does behind the scenes:
manager = open("data.txt", "r", encoding="utf-8")
f = manager.__enter__()       # Opens the file, returns it
try:
    content = f.read()
finally:
    manager.__exit__(None, None, None)   # Closes the file — always
```

The `finally` block guarantees cleanup even if an error occurs inside the `with` block. This is the context manager protocol.

---



## Building a Custom Context Manager



### A Timer

```python
import time

class Timer:
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.time() - self.start
        print(f"Elapsed: {self.elapsed:.4f} seconds")
        return False   # Do not suppress exceptions
```

```python
with Timer():
    total = sum(range(1_000_000))
    print(f"Sum: {total}")
```

Output:

```
Sum: 499999500000
Elapsed: 0.0312 seconds
```

`__enter__` records the start time. `__exit__` calculates the elapsed time and prints it.

### Using the Return Value

```python
with Timer() as t:
    data = [x ** 2 for x in range(100_000)]

print(f"The operation took {t.elapsed:.4f}s")
```

The `as t` captures whatever `__enter__` returns. Since our `__enter__` returns `self`, `t` is the Timer object, and we can access `t.elapsed` after the block.

---



## **exit** Parameters

`__exit__` receives three arguments about any exception that occurred:


| Parameter  | Value If No Exception | Value If Exception                       |
| ---------- | --------------------- | ---------------------------------------- |
| `exc_type` | `None`                | The exception class (e.g., `ValueError`) |
| `exc_val`  | `None`                | The exception instance                   |
| `exc_tb`   | `None`                | The traceback object                     |




### Suppressing Exceptions

If `__exit__` returns `True`, the exception is suppressed (swallowed):

```python
class SafeBlock:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f"Caught and suppressed: {exc_type.__name__}: {exc_val}")
            return True   # Suppress the exception
        return False
```

```python
with SafeBlock():
    print(1 / 0)   # ZeroDivisionError — caught and suppressed

print("Program continues")   # This runs because the exception was suppressed
```

Use exception suppression carefully. In most cases, return `False` to let exceptions propagate normally.

---



## contextlib.contextmanager — The Simple Way

Writing a class with `__enter__` and `__exit__` is verbose for simple cases. `contextlib.contextmanager` lets you write context managers as generator functions:

```python
from contextlib import contextmanager
import time

@contextmanager
def timer(label="Operation"):
    start = time.time()
    yield   # Everything before yield is __enter__, everything after is __exit__
    elapsed = time.time() - start
    print(f"{label}: {elapsed:.4f} seconds")
```

```python
with timer("Data processing"):
    data = [x ** 2 for x in range(100_000)]
```

Output:

```
Data processing: 0.0089 seconds
```

The pattern:

1. Code **before** `yield` runs on entry (setup)
2. `yield` gives control to the `with` block
3. Code **after** `yield` runs on exit (cleanup)

The single `yield` splits the function into the two halves of a context manager:

```python
@contextmanager
def timer(label="Operation"):
    start = time.time()               # ┐
    # ... setup ...                    # ├─ everything BEFORE yield = __enter__
                                       # ┘
    yield                              # ← hands control to the `with` block
                                       #   (a yielded value becomes the `as` variable)
    elapsed = time.time() - start     # ┐
    print(f"{label}: {elapsed:.4f}s") # ├─ everything AFTER yield = __exit__
                                       # ┘
```



### Yielding a Value

```python
@contextmanager
def timer(label="Operation"):
    start = time.time()
    result = {"label": label}
    yield result   # This becomes the 'as' variable
    result["elapsed"] = time.time() - start
    print(f"{label}: {result['elapsed']:.4f}s")
```

```python
with timer("Calculation") as t:
    total = sum(range(1_000_000))

print(t)   # {'label': 'Calculation', 'elapsed': 0.0312}
```



### Handling Exceptions in contextmanager

```python
@contextmanager
def managed_resource(name):
    print(f"Acquiring {name}")
    try:
        yield name
    except Exception as e:
        print(f"Error in {name}: {e}")
        raise   # Re-raise after logging
    finally:
        print(f"Releasing {name}")
```

```python
with managed_resource("database"):
    print("Working with database")
    raise ValueError("Something went wrong")
```

Output:

```
Acquiring database
Working with database
Error in database: Something went wrong
Releasing database
```

The `finally` block ensures cleanup runs even if an exception occurs. The `except` block logs the error, and `raise` re-raises it.

---



## Practical Context Managers



### Database Transaction

A **transaction** is a group of database changes that must **all succeed or all fail together** — never halfway. The classic example is a **bank transfer**: money leaves one account and must arrive in the other. If anything fails in between, we must **undo everything** so money is never lost.

This full example uses `sqlite3` from the standard library, so it runs as-is — no install, no server. Here `connection` is a real database connection returned by `sqlite3.connect(...)`.

```python
import sqlite3
from contextlib import contextmanager

@contextmanager
def transaction(connection):
    """Commit on success, roll back on any error."""
    try:
        yield connection
        connection.commit()          # all statements succeeded -> save them
        print("Transaction committed")
    except Exception:
        connection.rollback()        # something failed -> undo everything
        print("Transaction rolled back")
        raise

# A real (in-memory) database
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE accounts (name TEXT, balance INTEGER)")
conn.execute("INSERT INTO accounts VALUES ('Alice', 100)")
conn.execute("INSERT INTO accounts VALUES ('Bob', 0)")
conn.commit()

def show(msg):
    rows = conn.execute("SELECT name, balance FROM accounts ORDER BY name").fetchall()
    print(msg, dict(rows))

show("Start:      ")

# 1) A transfer that SUCCEEDS -> committed
with transaction(conn):
    conn.execute("UPDATE accounts SET balance = balance - 50 WHERE name='Alice'")
    conn.execute("UPDATE accounts SET balance = balance + 50 WHERE name='Bob'")
show("After OK:   ")

# 2) A transfer that FAILS midway -> rolled back (Alice is NOT charged)
try:
    with transaction(conn):
        conn.execute("UPDATE accounts SET balance = balance - 30 WHERE name='Alice'")
        raise ValueError("network dropped mid-transfer!")   # something breaks
        conn.execute("UPDATE accounts SET balance = balance + 30 WHERE name='Bob'")
except ValueError as e:
    print("Error:", e)
show("After fail: ")
```

Output:

```
Start:       {'Alice': 100, 'Bob': 0}
Transaction committed
After OK:    {'Alice': 50, 'Bob': 50}
Transaction rolled back
Error: network dropped mid-transfer!
After fail:  {'Alice': 50, 'Bob': 50}
```

Look at the last line: the failed transfer's `-30` was **undone** — Alice stays at 50. That is the whole point of a transaction: **commit on success, roll back on failure**, and the caller never has to remember to handle either case.

### Temporary Working Directory

```python
import os
from contextlib import contextmanager

@contextmanager
def working_directory(path):
    """Temporarily change the working directory."""
    original = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(original)
```

```python
with working_directory("/tmp"):
    print(os.getcwd())   # /tmp

print(os.getcwd())       # Back to original directory
```

**Takeaway:** This is the *restore-state* pattern — `__enter__` switches into the new folder and `__exit__` **always** switches back, so your program is never left stranded in the wrong directory, even if the block crashes.

### Logging Context

```python
import logging
from contextlib import contextmanager

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

@contextmanager
def log_operation(operation_name):
    """Log the start and end of an operation."""
    logger.info(f"Starting: {operation_name}")
    try:
        yield
        logger.info(f"Completed: {operation_name}")
    except Exception as e:
        logger.error(f"Failed: {operation_name} - {e}")
        raise

# 1) success
with log_operation("data import"):
    total = sum(range(1000))

# 2) failure
try:
    with log_operation("risky step"):
        raise ValueError("bad data")
except ValueError:
    pass
```

Output:

```
INFO: Starting: data import
INFO: Completed: data import
INFO: Starting: risky step
ERROR: Failed: risky step - bad data
```

**Takeaway:** `log_operation` wraps any block so it automatically logs *Starting* on entry and either *Completed* on success or *Failed* on error at exit — consistent start/end logging without repeating those lines at every call site.

Note the `logging.basicConfig(...)` line — without it, `logger.info(...)` prints nothing, because logging defaults to only showing warnings and errors.

---



## Nesting Context Managers

```python
with open("input.txt", "r", encoding="utf-8") as infile, \
     open("output.txt", "w", encoding="utf-8") as outfile:
    for line in infile:
        outfile.write(line.upper())
```

Multiple context managers on one `with` statement. Both files are guaranteed to close properly.

---



## Where This Applies in Real Work

- **Database connections:** Every database operation in Django and SQLAlchemy uses context managers. The connection is opened, queries execute, and the connection is closed — even if an error occurs.
- **File locks:** When multiple processes access the same file, a lock context manager acquires the lock on entry and releases it on exit.
- **API sessions:** HTTP client sessions (`requests.Session()`) are context managers that manage connection pooling.
- **AI model loading:** Loading a large ML model into GPU memory, using it for predictions, and releasing the memory — a perfect context manager use case.
- **Testing:** Test fixtures that set up and tear down test environments use context managers.
- **Resource monitoring:** Timing, memory tracking, and profiling are implemented as context managers that measure the resource usage of a code block.

---



## Practice Assignment

1. Build a `Timer` context manager class (using `__enter__` and `__exit__`) that:
  - Records start time on entry
  - Prints elapsed time on exit
  - Stores elapsed time as an attribute
2. Rewrite the same `Timer` using `@contextmanager` from contextlib
3. Build a `FileBackup` context manager using `@contextmanager`:
  - Before the `with` block: copies the file to `filename.bak`
  - If the `with` block succeeds: deletes the backup
  - If the `with` block fails: restores from the backup
  - (Use `pathlib` for file operations)
4. Test the `FileBackup`:
  - Create a file, modify it inside `with FileBackup("data.txt"):`
  - Verify it works on success
  - Raise an exception inside the block and verify the backup is restored

Save as `src/context_managers.py`.

---

