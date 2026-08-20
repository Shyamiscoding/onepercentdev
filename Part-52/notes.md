# Part 52 — Decorators

A decorator lets you add behaviour to a function *without touching the function's own code*. Timing, logging, authentication, caching, retries — all of these can be "wrapped" around a function from the outside. By the end of this episode you will read `@decorator` and know exactly what Python is doing under the hood.

We build up one idea at a time, then use a single running example — a web API endpoint — to see decorators solve real problems.

---

## Functions Are Objects (the foundation)

In Part 24 you learned that functions are **first-class objects**. That means a function is just another value, like an `int` or a `str`. Three consequences follow, and decorators are built on all three.

**1. A function can be stored in a variable**

```python
def greet(name):
    return f"Hello, {name}!"

say_hello = greet          # store the function OBJECT in another variable
                           # note: no () here — we are NOT calling greet, just referencing it
print(say_hello("Alice"))  # Hello, Alice!
```

`greet` and `say_hello` now point to the *same* function object.

**2. A function can be passed as an argument**

```python
def apply(func, value):
    return func(value)     # call whatever function was passed in

print(apply(greet, "Bob"))  # Hello, Bob!
```

**3. A function can be returned from another function**

This is the piece that makes decorators possible. A function can *define* another function inside itself and *return* it:

```python
def make_multiplier(factor):
    def multiply(number):        # inner function, defined INSIDE make_multiplier
        return number * factor   # it remembers `factor` from the outer function
    return multiply              # return the function object (no () — not calling it)

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))   # 10
print(triple(5))   # 15
```

`multiply` "remembers" the value of `factor` even after `make_multiplier` has already finished running. A function bundled together with the variables it remembers is called a **closure**.

### Closures — functions that remember

> **Closure:** an inner function that "captures" and keeps using variables from the outer function that created it, even after that outer function has returned.

Here is the smallest example that makes the idea click — a greeting builder:

```python
def make_greeter(greeting):      # outer function: takes the value to remember
    def greeter(name):           # inner function: uses that remembered value
        return f"{greeting}, {name}!"
    return greeter               # hand back the inner function

say_hello = make_greeter("Hello")
say_namaste = make_greeter("Namaste")

print(say_hello("Alice"))     # Hello, Alice!
print(say_namaste("Arjun"))   # Namaste, Arjun!
```

`make_greeter` has already finished by the time we call `say_hello`, yet `say_hello` still knows its `greeting` is `"Hello"`. Each closure keeps its **own** private copy of the remembered value — `say_hello` remembers `"Hello"`, `say_namaste` remembers `"Namaste"`. They never interfere with each other.

You can even peek at what a closure captured:

```python
print(say_hello.__closure__[0].cell_contents)   # Hello
```

Think of a closure as a function that carries a little backpack of remembered variables wherever it goes. That backpack is exactly what lets a decorator's `wrapper` remember the original `func` it is wrapping.

That third ability — a function that builds and returns another function, carrying remembered state — is the engine behind every decorator.

---



## What Is a Decorator?

A decorator is a function that:

1. takes a function as input,
2. defines a new function (the *wrapper*) that adds some behaviour, and
3. returns that wrapper.

```python
def loud(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)  # run the original function
        return result.upper()           # add behaviour: shout the result
    return wrapper                      # return the wrapper (same closure pattern as above)
```

`*args, **kwargs` let the wrapper accept *any* arguments and forward them to `func`, so `loud` works on functions with any signature.

### Applying it manually

```python
def greet(name):
    return f"Hello, {name}!"

greet = loud(greet)      # loud(greet) returns `wrapper`; we reassign greet to point at it
print(greet("Alice"))    # HELLO, ALICE!
```

`greet` now points to `wrapper`. Every call to `greet` runs the wrapper, which calls the original function and uppercases the result.

### The @ syntax (syntactic sugar)

Reassigning by hand is verbose. Python gives us the `@` symbol to do exactly the same thing:

```python
@loud
def greet(name):
    return f"Hello, {name}!"

print(greet("Alice"))    # HELLO, ALICE!
```

`@loud` written above `def greet` is **identical** to `greet = loud(greet)`. The decorator is applied once, at definition time.

---



## functools.wraps — Keep the Function's Identity

There is a hidden problem. After decorating, the original function is replaced by `wrapper`, so its identity (name, docstring, and other metadata) is lost:

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet(name):
    """Greet a user by name."""
    return f"Hello, {name}!"

print(greet.__name__)   # wrapper  <- wrong! it should say "greet"
print(greet.__doc__)    # None     <- the docstring is gone
```

`functools.wraps` fixes this by copying the original function's metadata onto the wrapper:

```python
import functools

def my_decorator(func):
    # `func` is the ORIGINAL function being decorated (here, greet).
    @functools.wraps(func)          # copy func's identity onto `wrapper`
    def wrapper(*args, **kwargs):
        # `wrapper` is the function that REPLACES greet after decoration.
        # Without @functools.wraps above, greet.__name__ would become "wrapper".
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet(name):
    """Greet a user by name."""
    return f"Hello, {name}!"

print(greet.__name__)   # greet                 <- preserved
print(greet.__doc__)    # Greet a user by name. <- preserved
```

`@functools.wraps(func)` copies across the original's `__name__`, `__doc__`, `__module__`, and `__qualname__`, and updates `__dict__`. It also sets a bonus attribute, `__wrapped__`, that points back to the untouched original function:

```python
print(greet.__wrapped__)   # <function greet ...> — the original, undecorated function
```

Why this matters in practice:

- `help(greet)` and IDE tooltips show the *real* function, not "wrapper".
- Debuggers and error tracebacks show the real name, which makes bugs far easier to find.
- Documentation generators (like Sphinx) and many frameworks read `__name__` — for example, Flask uses the function's name to register routes, so silently losing it can break your app.

**Rule: always put** `@functools.wraps(func)` **on your wrapper.**

---



## The Standard Decorator Template

Almost every decorator you write follows this shape. Keep it as a mental template:

```python
import functools

def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # --- code here runs BEFORE the original function ---
        result = func(*args, **kwargs)   # call the original function
        # --- code here runs AFTER the original function ---
        return result                    # return its result (don't forget this!)
    return wrapper
```

---



## Decorators That Take Arguments

Sometimes a decorator needs its own configuration, e.g. `@retry(max_attempts=3)`. That requires **three layers** instead of two:

```python
def repeat(times):                       # 1. takes the decorator's ARGUMENTS
    def decorator(func):                 # 2. takes the FUNCTION
        @functools.wraps(func)
        def wrapper(*args, **kwargs):    # 3. wraps the CALL
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def ping():
    print("ping")

ping()   # prints "ping" three times
```

Read `@repeat(times=3)` as two steps: `repeat(times=3)` runs first and *returns* `decorator`; then that `decorator` is applied to `ping` like any normal decorator. We use this exact pattern for `@retry` and `@require_role` below.

---



## A Running Example: Protecting a Web API Endpoint

From here on we use **one example** and layer real-world behaviour onto it with decorators. Imagine a web framework that calls your function with a `request` object (we'll use a simple dictionary). Here is the bare endpoint:

```python
def get_dashboard(request):
    return {"widgets": ["sales", "traffic", "alerts"]}
```

We will now add timing, logging, retries, authentication, and authorization — **without ever changing this function's body.**

### 1. Timing — how long did it take?

```python
import functools
import time

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()          # perf_counter is the right clock for durations
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timer
def get_dashboard(request):
    time.sleep(0.1)          # pretend we queried a database
    return {"widgets": ["sales", "traffic", "alerts"]}

get_dashboard({})            # get_dashboard took 0.1003s
```



### 2. Logging — record every call

```python
import functools

def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"-> calling {func.__name__}(args={args}, kwargs={kwargs})")
        result = func(*args, **kwargs)
        print(f"<- {func.__name__} returned {result}")
        return result
    return wrapper
```

We use `print` here for clarity; in production you would use the `logging` module. And never log raw secrets such as tokens — redact them first.

### 3. Retry — survive a flaky dependency

Our endpoint depends on a database call that sometimes fails. `@retry` (a decorator with arguments) retries it automatically:

```python
import functools
import time

def retry(max_attempts=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise                     # out of attempts — re-raise the error
                    print(f"attempt {attempt} failed: {e}. retrying in {delay}s...")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=1)
def fetch_orders_from_db(user_id):
    import random
    if random.random() < 0.7:
        raise ConnectionError("database timeout")
    return [{"id": 1, "total": 99.0}]
```



### 4. Authentication — decode a JWT before the endpoint runs

This is the classic real-world decorator. The caller sends a **JWT** (JSON Web Token) in the `Authorization` header. The decorator extracts it, verifies and decodes it, and only then lets the request reach your endpoint — with the decoded user already attached.

```python
import functools
import jwt        # pip install pyjwt

SECRET_KEY = "super-secret-signing-key"

def jwt_required(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        # 1. Pull the token out of the Authorization header ("Bearer <token>").
        auth_header = request.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise PermissionError("missing or malformed Authorization header")
        token = auth_header.split(" ", 1)[1]

        # 2. Verify the signature and expiry, then decode the payload.
        #    jwt.decode raises if the token was tampered with or has expired,
        #    so a forged token can never reach the endpoint below.
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise PermissionError("token has expired")
        except jwt.InvalidTokenError:
            raise PermissionError("invalid token")

        # 3. Attach the decoded user to the request, then call the REAL endpoint.
        request["user"] = payload
        return func(request, *args, **kwargs)
    return wrapper
```

Creating a token and calling the protected endpoint:

```python
import datetime

def create_token(name, role):
    payload = {
        "name": name,
        "role": role,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

@jwt_required
def get_dashboard(request):
    user = request["user"]          # placed here by the decorator after decoding
    return f"Dashboard for {user['name']} (role: {user['role']})"

token = create_token("Alice", "admin")
request = {"Authorization": f"Bearer {token}"}

print(get_dashboard(request))       # Dashboard for Alice (role: admin)
print(get_dashboard({}))            # PermissionError: missing or malformed Authorization header
```

The endpoint never sees a raw token — by the time it runs, authentication is finished and `request["user"]` is ready to use. Keeping that plumbing out of the endpoint is the whole point of decorators.

### 5. Authorization — check the user's role

Authentication answers *"who are you?"*; authorization answers *"are you allowed?"*. Now that `jwt_required` has decoded the user, a second decorator can check their role:

```python
import functools

def require_role(role):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            user = request.get("user", {})           # set earlier by jwt_required
            if user.get("role") != role:
                raise PermissionError(
                    f"requires '{role}' role, but user is '{user.get('role')}'"
                )
            return func(request, *args, **kwargs)
        return wrapper
    return decorator
```

---



## Stacking Decorators

Because each decorator simply returns a function, you can apply several at once. Here is the full production-style endpoint:

```python
@timer                       # outermost: measures the whole request
@log_calls                   # logs the call
@jwt_required                # authenticates: decodes the JWT, sets request["user"]
@require_role("admin")       # authorizes: checks request["user"]["role"]
def get_dashboard(request):
    return {"widgets": ["sales", "traffic", "alerts"]}
```

Decorators are applied **bottom-up**, so the block above is equivalent to:

```python
get_dashboard = timer(log_calls(jwt_required(require_role("admin")(get_dashboard))))
```

At call time they run **top-down**: `timer` starts the clock, `log_calls` logs, `jwt_required` decodes the token and sets `request["user"]`, `require_role` reads that user and checks the role, and finally the real `get_dashboard` runs. The order matters — `jwt_required` must sit *above* `require_role`, because the role check depends on the user that authentication decoded.

```python
admin_request  = {"Authorization": f"Bearer {create_token('Alice', 'admin')}"}
member_request = {"Authorization": f"Bearer {create_token('Bob', 'member')}"}

print(get_dashboard(admin_request))   # runs — Alice is an admin
print(get_dashboard(member_request))  # PermissionError: requires 'admin' role, but user is 'member'
```

---



## Decorators You Already Use

You have been using decorators since long before this episode:


| Decorator              | Where You Learned It | What It Does                                    |
| ---------------------- | -------------------- | ----------------------------------------------- |
| `@property`            | Part 44              | Makes a method behave like an attribute         |
| `@dataclass`           | Part 44              | Auto-generates `__init__`, `__repr__`, `__eq__` |
| `@abstractmethod`      | Part 46              | Marks a method as abstract in an ABC            |
| `@functools.lru_cache` | Part 27              | Caches function results (memoization)           |
| `@contextmanager`      | Part 51              | Turns a generator into a context manager        |


Every `@something` above a function or class is a decorator. Now you understand the mechanism behind all of them.

### How @property works, demystified

```python
class User:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name
```

`@property` wraps the `name` method and turns it into a *descriptor* — a special object that intercepts attribute access. When you write `user.name`, Python calls the wrapped method instead of doing a plain attribute lookup. Same decorator mechanism, applied to a method.

---



## Where Else This Shows Up

- **Web routing:** `@app.get("/users")` in FastAPI / Flask registers a function as a route handler.
- **Caching:** `@functools.lru_cache` / `@cache` store results to skip repeated work — common in AI inference and database access.
- **Rate limiting & validation:** decorators reject too-frequent or invalid requests before your code runs.
- **Database transactions:** `@transactional`-style decorators commit on success and roll back on error.

The pattern is always the same: *wrap the function to add cross-cutting behaviour without editing the function itself.*

---



## Practice Assignment

1. Create a `@log_calls` decorator that:
  - Prints the function name, arguments, and keyword arguments before the call
  - Prints the return value after the call
  - Uses `@functools.wraps`
2. Create a `@timer` decorator that prints how long a function took (use `time.perf_counter`).
3. Create a `@validate_positive` decorator that:
  - Checks that all positional arguments are positive numbers
  - Raises `ValueError` if any argument is negative or zero
4. Create a `@retry(max_attempts=3, delay=0.5)` decorator with arguments:
  - Retries the function up to `max_attempts` times
  - Waits `delay` seconds between retries
  - Re-raises the last exception if all attempts fail
5. Apply and stack decorators:
  - Create a `divide(a, b)` function with `@log_calls` and `@validate_positive`
  - Create a `fetch_data()` function with `@timer` and `@retry(max_attempts=3)`
6. Stretch — authentication: create a `@require_auth` decorator that:
  - Reads a `request` dict and checks `request["token"]`
  - Rejects a missing/invalid token with `PermissionError`
  - On success, attaches the user to `request["user"]` and calls the endpoint
  - (Bonus: if you `pip install pyjwt`, decode a real JWT as in the lesson.)
  - Stack it with `@log_calls` on a `get_profile(request)` endpoint.
7. Test all decorators and verify they work correctly when stacked.

Save as `src/decorators.py`.

