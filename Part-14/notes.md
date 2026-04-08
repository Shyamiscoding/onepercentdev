# Part 14 — Professional Conditional Patterns

## Connecting to Part 13

In Part 13, you learned the core conditional structures — `if`, `if-else`, `if-elif-else`, and nested conditionals. You also learned the guard clause pattern — how senior developers flatten deeply nested code. You can now make any decision in code.

But here is the difference between a beginner and a professional: they both know `if-elif-else`. The professional writes it **differently** — shorter syntax, cleaner patterns, and features that combine truthiness (Part 12), comparisons (Part 11), and conditionals (Part 13) into code that other developers actually enjoy reading.

This part teaches those professional patterns. By the end, you will write conditionals the way experienced Python developers do — and you will see the feature that Python's creator rejected for 20 years, until the right version of it finally arrived.

---

## The pass Statement

Sometimes you need an empty block — a placeholder for code you will write later. Python does not allow empty blocks:

```python
if True:
    # nothing here — SyntaxError!
```

`pass` is the solution:

```python
age = 20

if age >= 18:
    pass   # TODO: implement adult logic later
else:
    print("Minor")
```

`pass` does nothing — it is a "no-operation" statement. It tells Python "I intentionally left this blank."

### Where You Use pass

```python
age = 20

if age >= 18:
    pass   # TODO: handle adult case
elif age >= 13:
    pass   # TODO: handle teen case
else:
    print("Child")
```

`pass` is common during development — you write the structure first, then fill in the logic. Later, when you learn functions and classes, you will use `pass` there too as a placeholder while building your code structure.

---

## Using Truthiness in Conditionals

From Part 12, you know that empty strings, `0`, `None`, and `False` are all falsy. Everything else is truthy. This lets you write cleaner conditionals:

```python
name = input("Enter your name: ")

# Non-Pythonic (works, but verbose):
if name != "":
    print(f"Hello, {name}")

# Pythonic (uses truthiness):
if name:
    print(f"Hello, {name}")
```

Both do the same thing. The second version is what professional Python developers write.

More examples:

```python
items = []

# Non-Pythonic:
if len(items) > 0:
    print("Has items")

# Pythonic:
if items:
    print("Has items")
```

```python
result = None

# Non-Pythonic:
if result != None:
    print(result)

# Pythonic (for None specifically, use 'is'):
if result is not None:
    print(result)
```

**The principle:** Use the value's truthiness directly. Do not compare against empty strings, zero, or `None` unless you need to distinguish between different falsy values.

---

## Ternary Operator (Conditional Expression)

A one-line way to write `if-else`:

```python
age = 20

# Standard if-else:
if age >= 18:
    status = "adult"
else:
    status = "minor"

# Ternary (same logic, one line):
status = "adult" if age >= 18 else "minor"
```

The syntax:

```
value_if_true if condition else value_if_false
```

More examples:

```python
score = 85
grade = "Pass" if score >= 60 else "Fail"

temperature = 35
feeling = "hot" if temperature > 30 else "comfortable"

x = 10
result = "even" if x % 2 == 0 else "odd"
```

### When to Use vs When to Avoid

Use ternary for simple assignments:

```python
is_active = True
label = "active" if is_active else "inactive"
```

Avoid ternary when the logic is complex — readability drops fast:

```python
# Hard to read — use regular if-elif-else instead
result = "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "F"
```

**Rule:** If you cannot understand the ternary in 2 seconds, use a regular `if` block.

---

## match-case (Python 3.10+)

### The History — Why Python Had No match for 30 Years

Python was born in **1991**. Every major language around it — C (1972), Java (1995), JavaScript (1995) — had a `switch` statement from the start. For **30 years**, Python did not. Developers asked for it repeatedly. Guido van Rossum rejected it — **twice**:

- **[PEP 275 (2001)](https://peps.python.org/pep-0275/)** — proposed adding a `switch` statement to Python. Rejected.
- **[PEP 3103 (2006)](https://peps.python.org/pep-3103/)** — Guido himself authored this PEP, exploring multiple implementation options for a `switch`. He then put it to a vote at PyCon 2007. The community showed no strong support. He rejected his own proposal.

That is **20 years of switch proposals** (2001–2021), all rejected. And **30 years of Python's existence** (1991–2021) without anything resembling one. Both numbers are measuring different things — the proposals started 10 years after Python was born.

### Why Guido Kept Saying No — The Real Reason

The reason was not stubbornness. It was a genuine technical argument. Guido wrote this in PEP 3103:

> *"There isn't a lot of readability or performance to be gained by writing this differently."*

Here is why. Look at what `switch` does in C or JavaScript:

```
switch (command) {
    case "start": doStart(); break;
    case "stop": doStop(); break;
    default: doError(); break;
}
```

Now look at the Python equivalent:

```python
if command == "start":
    print("Starting...")
elif command == "stop":
    print("Stopping...")
else:
    print("Error: unknown command")
```

A `switch` statement just compares **one value against a list of constants**. That is it. `if-elif-else` already does exactly the same thing, and everyone already knows how to use it. Adding `switch` would mean two ways to do the same thing — violating The Zen of Python: *"There should be one — and preferably only one — obvious way to do it."*

A traditional `switch` is essentially **syntactic sugar** — different syntax for the same logic. Not worth complicating the language.

### What Changed in 2020 — Why Guido Finally Said Yes

During COVID lockdowns in 2020, Guido van Rossum sent what Brandt Bucher (a CPython core developer) called "a nerd sniping email on a Wednesday" — inviting him to collaborate on something entirely different from a `switch`.

The result was not a `switch` statement. It was **[PEP 634 — Structural Pattern Matching](https://peps.python.org/pep-0634/)**, co-authored by Guido himself. Python 3.10 (released October 2021) included it as `match-case`.

Guido did not compromise his principles. He accepted it because this proposal was **genuinely different** from every previous `switch` proposal. It earned its place in the language.

### match vs switch — The Difference Nobody Teaches You

This is what most tutorials on the internet get wrong. They show you `match-case` and say: *"It is Python's version of switch."* This is **misleading**. Let us put them side by side — using JavaScript's `switch` as the comparison — and see where `switch` breaks down.

> You do not need to know JavaScript. Just read the structure — it is close enough to Python that you will follow along. `console.log()` is JavaScript's version of `print()`. `break` tells `switch` to stop — without it, execution falls into the next case (more on that in Round 4).

**Round 1 — Simple value matching (switch CAN do this):**

```javascript
// JavaScript — switch
switch (command) {
    case "start":
        console.log("Starting...");
        break;
    case "stop":
        console.log("Stopping...");
        break;
    case "restart":
        console.log("Restarting...");
        break;
    default:
        console.log("Unknown command: " + command);
}
```

```python
# Python — match
match command:
    case "start":
        print("Starting...")
    case "stop":
        print("Stopping...")
    case "restart":
        print("Restarting...")
    case _:
        print(f"Unknown command: {command}")
```

At this level, they look almost identical. Both compare one value against constants. If this were all `match` could do, Guido would have rejected it too — `if-elif-else` already handles this. But watch what happens next.

**Round 2 — Matching multiple values at once (switch needs a hack):**

Suppose you want to check if a day is a weekday or weekend:

```javascript
// JavaScript — switch uses "fall-through" to group values.
// You intentionally leave out "break" so execution falls
// from one case into the next. This is confusing and error-prone:
switch (day) {
    case "Saturday":
    case "Sunday":
        console.log("Weekend");
        break;
    case "Monday":
    case "Tuesday":
    case "Wednesday":
    case "Thursday":
    case "Friday":
        console.log("Weekday");
        break;
}
```

```python
# Python — match uses the | (OR) operator. Clean and obvious:
match day:
    case "Saturday" | "Sunday":
        print("Weekend")
    case "Monday" | "Tuesday" | "Wednesday" | "Thursday" | "Friday":
        print("Weekday")
```

In `switch`, grouping multiple values requires you to stack empty cases on top of each other and rely on fall-through — a feature that causes bugs when you forget `break` (more on that in Round 4). In `match`, you use `|` — read it as "or." Simple, readable, no tricks.

**Round 3 — Capturing and testing values (switch CANNOT do this):**

Suppose you want to categorize an age — but you also want to use the age value inside each case:

```javascript
// JavaScript — switch CANNOT capture the value and test it.
// switch only compares against exact constants.
// You cannot write: case age > 65
// You are forced to fall back to if-else:
if (age < 0) {
    console.log("Invalid age");
} else if (age < 18) {
    console.log("Minor, age " + age);
} else if (age < 65) {
    console.log("Adult, age " + age);
} else {
    console.log("Senior, age " + age);
}
```

```python
# Python — match can capture the value into a variable
# AND test it with a guard (the "if" after the pattern):
match age:
    case n if n < 0:
        print("Invalid age")
    case n if n < 18:
        print(f"Minor, age {n}")
    case n if n < 65:
        print(f"Adult, age {n}")
    case n:
        print(f"Senior, age {n}")
```

Look at `case n if n < 0:` — this does two things at once. First, `n` **captures** the value of `age` (now you can use `n` inside the block). Then `if n < 0` is a **guard** — an extra condition that must be true for this case to match. `switch` has no syntax for either of these. You cannot capture values, and you cannot add conditions. You are forced back to `if-else`.

**Round 4 — No fall-through (switch's oldest bug):**

In C/Java/JavaScript, forgetting a `break` in a `switch` causes "fall-through" — execution drops into the next case accidentally:

```javascript
// JavaScript — forgot the break. Bug!
switch (role) {
    case "admin":
        console.log("Admin access");
        // forgot break here — falls through into the next case!
    case "user":
        console.log("User access");
        break;
}
// If role is "admin", BOTH lines print. Silent bug.
```

This is one of the most common bugs in those languages. Python's `match` has no fall-through. Each `case` is self-contained. If it matches, its block runs, and the match is done. No `break` needed, no accidental bugs.

**The core difference:**

| | **switch** (C / Java / JavaScript) | **match** (Python) |
|---|---|---|
| Compare value against constants | Yes | Yes |
| Group multiple values (`\|`) | Needs fall-through hack | Built-in with `\|` |
| Capture value into a variable | No | Yes (`case n:`) |
| Add conditions (guards) | No | Yes (`case n if n > 0:`) |
| Fall-through bugs | Yes (forget `break` = bug) | No (each case is independent) |
| Inspect data structures | No | Yes (you will see this in Parts 19 and 21) |

`switch` is a value comparator — it can only check `==` against constants. `match` is a pattern matcher — it can check equality, combine patterns with `|`, capture values, and add conditions with guards. They happen to look similar in the simplest case, but they are fundamentally different tools.

**What you will see later — the real power:**

Everything above uses strings and numbers — concepts you already know. But `match` can do even more. When you learn **tuples** (Part 19) and **dictionaries** (Part 21), you will see that `match` can inspect the **shape** of complex data — checking how many elements something has, what keys a dictionary contains, and pulling out values from inside structures, all in a single pattern. No `switch` in any language can do that. You will come back to `match` then and see why Guido considered it worthy of Python.

### Why Not Performance?

A common assumption: *"match must be faster than if-elif, right?"* No. Python's `match` does **not** use a jump table internally (like C's `switch` can). For simple value comparisons, `if-elif` is actually slightly faster. Benchmarks on Python 3.13 show `if-elif` beating `match-case` by about 10% for simple constant matching.

The advantage of `match` is not speed — it is **expressiveness**. It lets you write cleaner, more readable code when you are matching patterns — and as you progress through this course, you will see just how powerful that becomes.

### Using match-case

`match-case` is most useful when comparing one value against many specific options — menu selections, command parsers, status codes:

```python
status_code = 404

match status_code:
    case 200:
        print("OK")
    case 301:
        print("Redirect")
    case 404:
        print("Not Found")
    case 500:
        print("Server Error")
    case _:
        print(f"Status: {status_code}")
```

- `match` evaluates the expression once
- `case` checks against each pattern
- `_` is the wildcard — it matches anything (like `else`)

For conditions with ranges or complex logic (`>=`, `and`, etc.), stick with `if-elif-else`.

### match-case with Guards

You can add conditions to cases using `if`:

```python
age = 25

match age:
    case n if n < 0:
        print("Invalid age")
    case n if n < 18:
        print(f"Minor, age {n}")
    case n if n < 65:
        print(f"Adult, age {n}")
    case n:
        print(f"Senior, age {n}")
```

The variable `n` captures the value, and the `if` guard adds a condition. This is more readable than a long if-elif chain when the logic is pattern-based.

### The Big Picture

Python went 30 years without a `switch` because Guido refused to add something that `if-elif-else` already handled. When `match` was finally added, it was not a compromise — it was a fundamentally different tool. A `switch` compares values. `match` **matches patterns**. That distinction is why Guido co-authored PEP 634 himself — the same person who rejected every `switch` proposal for 20 years. He was not against the feature. He was waiting for the right version of it.

---

## The Walrus Operator := (Python 3.8+)

The walrus operator lets you **assign and use a value in the same expression**. It solves a common annoyance: computing a value, checking it, then using it.

```python
# Without walrus — compute twice or use a temporary variable:
data = input("Enter data: ")
if len(data) > 10:
    print(f"Too long: {len(data)} characters")   # len() called twice

# With temporary variable — works but clunky:
data = input("Enter data: ")
length = len(data)
if length > 10:
    print(f"Too long: {length} characters")

# With walrus — assign and check in one line:
data = input("Enter data: ")
if (length := len(data)) > 10:
    print(f"Too long: {length} characters")
```

`length := len(data)` assigns the result to `length` AND returns it for the comparison, all in one expression.

**More examples:**

```python
# Assign and test user input in one step:
if (name := input("Enter name: ")):
    print(f"Hello, {name}!")
else:
    print("No name entered")

# Assign and check length:
text = "Hello, World!"
if (n := len(text)) > 10:
    print(f"Text is long: {n} characters")
else:
    print(f"Text is short: {n} characters")
```

When you learn loops later, the walrus operator becomes even more useful — reading input inside a loop condition, for example. For now, use it when you need to compute a value, test it, and use it — all in one place.

**Rule:** Do not use it everywhere. If it makes the code harder to read, use a regular variable.

---

## Input Validation Pattern — Putting It All Together

This capstone example combines comparison operators (Part 11), truthiness (Part 12), and conditionals (Part 13) into a real-world pattern:

```python
username = input("Enter username: ")

if not username:
    print("Username cannot be empty")
elif len(username) < 3:
    print("Username must be at least 3 characters")
elif len(username) > 20:
    print("Username must be 20 characters or less")
elif not username.isalnum():
    print("Username can only contain letters and numbers")
else:
    print(f"Welcome, {username}!")
```

What is happening:
1. `not username` — truthiness check (Part 12): empty string is falsy, `not falsy` is `True`
2. `len(username) < 3` — comparison operator (Part 11)
3. `not username.isalnum()` — string method (Part 10) combined with `not` (Part 12)
4. `if-elif-else` chain (Part 13) — checks conditions in order, stops at the first match

This is how professional developers validate input. Each condition catches a specific problem. The `else` only runs when all checks pass.

---

## Where This Applies in Real Work

- **Form validation:** Every web form validates input with this exact pattern — check empty, check length, check format, then accept.
- **API endpoints:** Server-side code validates request data using the same pattern before processing.
- **CLI tools:** Command-line tools use `match-case` for subcommands (`git push`, `git pull`, `git commit`).
- **Configuration parsing:** Reading config files and acting on different settings is a classic conditional pattern.
- **Error handling:** Different error types get different responses — pattern matching maps perfectly.

---

## Practice Assignments

### Assignment 1: Grade Calculator

Write a program that:
1. Takes a score (0–100) as input
2. Prints the grade based on this scale: A (90+), B (80–89), C (70–79), D (60–69), F (below 60)
3. Validates the input — reject scores outside 0–100 and non-numeric input

Use: `input()`, `int()`, comparison operators, `if-elif-else`, input validation pattern.

### Assignment 2: Login System

Write a simple login system that:
1. Has a stored username and password (hardcoded)
2. Asks the user for their username and password
3. Checks: Is the username empty? Does it match? Is the password empty? Does it match?
4. Prints appropriate messages for each failure case and a welcome message on success

Use: truthiness, `==`, `and`, `if-elif-else`, input validation pattern.

### Assignment 3: Command Parser

Write a program that:
1. Accepts a command from the user (`help`, `status`, `quit`, or anything else)
2. Uses `match-case` to handle each command
3. For `status`, additionally asks if the user wants "brief" or "detailed" output (nested conditional or ternary)

Use: `match-case`, ternary operator, nested conditionals.

---

> **Next:** Part 15 — While Loops. You have mastered operators and conditionals. Your programs can now think. But they still run once and stop. Next: loops — making your code repeat.
