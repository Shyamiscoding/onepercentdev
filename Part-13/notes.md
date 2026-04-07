# Part 13 — Conditionals

## Connecting to Part 12

Let us trace the journey so far:

- **Parts 9–10:** We learned to **store data** — integers and strings. We could hold a user's age, their name, a price. We performed calculations, formatted text, sliced strings. But all our programs did was store and compute. They were **calculators** — not software.
- **Part 11:** We made the shift from calculator to software. Real software does not just store data — it **asks questions** about that data. "Is the password correct?" "Is the user old enough?" We learned comparison operators (`==`, `!=`, `>`, `<`, `>=`, `<=`) that ask a single yes/no question and produce `True` or `False`.
- **Part 12:** A single question is not enough to build real software. An ATM does not just ask "Is the PIN correct?" — it asks "Is the PIN correct **AND** is the account active **AND** is the card not expired?" We learned logical operators (`and`, `or`, `not`) to combine multiple questions into one decision. We also discovered truthiness — every value in Python is secretly `True` or `False`.

**But here is the problem** — we can ask questions, we can combine them, we get answers (`True` or `False`). And then... **nothing happens.** The program still runs every single line of code regardless. `age >= 18` returns `True`, but the program does not actually do anything different for an adult versus a minor. The answer just sits there, unused.

Think of it this way: you have built a complete security system with sensors, cameras, and alarms. The sensors detect motion. The cameras capture footage. But there is no one watching the monitors. No one deciding "intruder detected → lock the doors." The system collects information but never **acts** on it.

Conditionals are the person watching the monitors. They take the `True` or `False` answers from Parts 11 and 12 and **make decisions** — if this is true, do one thing; otherwise, do something else. This is the moment your programs stop being calculators and start **thinking**.

---

## How Conditionals Work — What Python Actually Does

Before we write any `if` statement, understand what happens under the hood. When Python encounters `if something:`, it calls `bool()` on `something`. That is it. The result is `True` → run the block. `False` → skip the block.

This connects to Part 12's truthiness rules:

```python
if "hello":         # bool("hello") → True → runs
    print("truthy")

if 0:               # bool(0) → False → skipped
    print("never")

if [1, 2, 3]:       # bool([1,2,3]) → True (non-empty) → runs
    print("has items")
```

Every `if` statement is a `bool()` call. That is why we covered truthiness in Part 12 **before** conditionals — it was not a separate topic. It was preparation for this moment. When you see `if name:`, you already know Python calls `bool(name)`, checks `__bool__()` or `__len__()`, and gets `True` or `False`. No mystery. No magic. You understand the full chain.

---

## The if Statement

The simplest conditional — execute a block of code only if a condition is `True`:

```python
age = 20

if age >= 18:
    print("You are an adult")
    print("You can vote")

print("Program continues")
```

Output:

```
You are an adult
You can vote
Program continues
```

### The Structure

```python
if condition:
    # code that runs only if condition is True
    # (indented by 4 spaces)
```

Three critical rules:

1. The condition can be **any expression** — Python calls `bool()` on it to get True or False
2. The line ends with a **colon** `:`
3. The body is **indented** (4 spaces or 1 tab) — Python uses indentation instead of curly braces `{}` to define blocks

```python
age = 15

if age >= 18:
    print("You are an adult")   # Skipped — condition is False

print("This always runs")       # Not indented — outside the if block
```

Output:

```
This always runs
```

### Indentation Is Not Optional

In Python, indentation defines what belongs inside the `if` block. Unlike other languages that use `{}`, Python uses whitespace:

```python
if True:
    print("Inside the block")
    print("Still inside")
print("Outside the block")
```

If you mix tabs and spaces, or indent inconsistently, Python raises an `IndentationError`. Use 4 spaces per level — this is the Python standard.

**Why indentation and not curly braces?** Most languages — C, Java, JavaScript — use `{}` to define blocks. Guido van Rossum chose indentation because developers already indent their code for readability anyway. Python just makes it a rule instead of a suggestion. The result: Python code looks clean by force. You cannot write messy Python — the language will not let you.

---

## if-else — Two Paths

When you need exactly two paths — do this OR do that:

```python
age = 15

if age >= 18:
    print("You are an adult")
else:
    print("You are a minor")
```

One of the two blocks always runs. There is no scenario where neither executes.

```
if condition:
    # path A (when True)
else:
    # path B (when False)
```

**Important:** `else` is always optional. A standalone `if` without `else` is perfectly valid — it means "do this if true, otherwise do nothing and move on." You add `else` only when you need a specific action for the `False` case.

---

## if-elif-else — Multiple Paths

When you need more than two paths:

```python
score = 85

if score >= 90:
    print("Grade: A")
elif score >= 80:
    print("Grade: B")
elif score >= 70:
    print("Grade: C")
elif score >= 60:
    print("Grade: D")
else:
    print("Grade: F")
```

Output: `Grade: B`

**Note:** Both `elif` and `else` are optional. You can have `if` alone, `if-else`, `if-elif`, or `if-elif-else`. You build only the paths your logic needs.

### How Execution Flows

Python checks conditions **from top to bottom**. The moment it finds a `True` condition, it runs that block and **skips all the rest**.

For `score = 85`:

1. `score >= 90` → `85 >= 90` → `False` → skip
2. `score >= 80` → `85 >= 80` → `True` → **run this block, skip everything below**

This is why the order matters. If you write the conditions in the wrong order, you get wrong results:

```python
# WRONG ORDER:
score = 95
if score >= 60:
    print("Grade: D")   # This runs! 95 >= 60 is True
elif score >= 90:
    print("Grade: A")   # Never reached
```

### Common Mistake: Multiple if vs elif

```python
score = 95

# Multiple if — checks ALL conditions independently
if score >= 90:
    print("Grade: A")   # Runs
if score >= 80:
    print("Grade: B")   # Also runs! (95 >= 80)
if score >= 70:
    print("Grade: C")   # Also runs! (95 >= 70)

# elif — stops at the first True
if score >= 90:
    print("Grade: A")   # Runs
elif score >= 80:
    print("Grade: B")   # Skipped — already found a match
elif score >= 70:
    print("Grade: C")   # Skipped
```

Multiple `if` statements are **independent checks**. `elif` is **one chain** where only the first match executes.

### Why Condition Order Matters — Beyond Correctness

Order is not just about getting the right answer. In production code, **condition order affects performance**.

Consider a login system that checks three things:

```python
# Non-optimal order:
if account_not_banned and password_correct and user_exists:
    print("Login successful")
```

This works — it gives the correct answer. But think about what happens in production: 90% of failed logins are because the user typed the wrong password. Only 1% are banned accounts. Yet this code checks ban status **first** for every single request — wasting time on a check that almost never fails.

```python
# Optimal order — cheapest and most likely to fail check first:
if user_exists and password_correct and account_not_banned:
    print("Login successful")
```

Python's short-circuit evaluation (from Part 12) means: if `user_exists` is `False`, it never checks the other two. If `password_correct` is `False`, it never checks ban status. The most common failure (`password_correct`) is checked early, so most requests exit fast.

Professional developers think about this when writing APIs that handle thousands of requests per second — every unnecessary check adds up.

### What Your CPU Does When It Hits an If Statement

Here is something most developers never learn — even in computer science classes.

When your CPU reaches an `if` statement, it does **not** wait for the condition to be evaluated. It **guesses** which path will be taken and starts executing that path **before it knows the answer**. This is called **branch prediction**.

- If the CPU guesses **right** → no time wasted, execution continues at full speed
- If the CPU guesses **wrong** → it throws away all the speculative work and starts over on the correct path. This is called a **pipeline flush** — and it is expensive

Modern CPUs (Intel, AMD, Apple Silicon) have sophisticated prediction algorithms. They look at patterns: "The last 100 times this condition was checked, it was `True` 95 times — so I will guess `True` again."

This is why **predictable conditions are faster than random ones**. If your `if` statement follows a pattern (many `True`s in a row, then many `False`s), the CPU predicts correctly almost every time. If the condition flips randomly between `True` and `False`, the CPU guesses wrong constantly and wastes cycles.

This exact phenomenon is behind one of the most famous Stack Overflow questions of all time — *"Why is processing a sorted array faster than an unsorted array?"* — with **35,000+ upvotes**. The answer: with sorted data, the `if` condition follows a pattern the CPU can predict. With unsorted data, it cannot.

Read it yourself: [Why is processing a sorted array faster than an unsorted array?](https://stackoverflow.com/questions/11227809/why-is-processing-a-sorted-array-faster-than-processing-an-unsorted-array)

You do not need to optimize for branch prediction in everyday Python code. But knowing this exists separates developers who understand the machine from those who just write code on top of it.

---

## Nested Conditionals

You can put an `if` inside another `if`:

```python
age = 25
has_id = True

if age >= 18:
    if has_id:
        print("Entry allowed")
    else:
        print("Show ID first")
else:
    print("Too young")
```

Each nesting level adds one more indentation. The inner `if` only runs if the outer `if` is `True`.

### When Nesting Becomes a Problem

Deeply nested code is hard to read — developers call this the "arrow problem" or "pyramid of doom":

```python
if user_exists:
    if password_correct:
        if account_active:
            if not banned:
                print("Login successful")
            else:
                print("Account banned")
        else:
            print("Account inactive")
    else:
        print("Wrong password")
else:
    print("User not found")
```

### Refactoring with Logical Operators

You can flatten nested conditionals using `and` from Part 12:

```python
# Nested version:
if age >= 18:
    if has_id:
        print("Entry allowed")

# Flattened version (same logic):
if age >= 18 and has_id:
    print("Entry allowed")
```

The flattened version is cleaner and easier to read. This is one of the reasons you learned logical operators first.

For the login example:

```python
if user_exists and password_correct and account_active and not banned:
    print("Login successful")
```

One line, same logic, much easier to understand at a glance.

### The Mindset: Flatten, Don't Nest

Senior developers avoid deep nesting whenever possible. Compare these approaches:

```python
# Deeply nested — hard to read:
username = input("Username: ")
password = input("Password: ")

if username != "":
    if password != "":
        if username == "admin":
            if password == "secret123":
                print("Login successful")
            else:
                print("Wrong password")
        else:
            print("Unknown user")
    else:
        print("Password cannot be empty")
else:
    print("Username cannot be empty")
```

```python
# Flattened with elif — same logic, much easier to read:
username = input("Username: ")
password = input("Password: ")

if not username:
    print("Username cannot be empty")
elif not password:
    print("Password cannot be empty")
elif username != "admin":
    print("Unknown user")
elif password != "secret123":
    print("Wrong password")
else:
    print("Login successful")
```

The flattened version checks failure conditions first and handles them immediately. The "happy path" (success) is at the bottom. No nesting. This is called the **guard clause** pattern — check for problems first, handle them, then proceed with the real logic.

When you learn functions later, this pattern becomes even more powerful with early `return`. For now, practice flattening nested conditionals using `elif` and logical operators.

---

## Where This Applies in Real Work

- **Authentication:** Every login system is an if-elif-else chain — check credentials, check account status, check permissions.
- **API routing:** Web servers use conditionals to decide which code handles a request.
- **Form validation:** Every field check is a conditional — is the email valid? Is the password strong enough?
- **Game logic:** Every game loop is built on conditionals — did the player collide? Is health zero?
- **Data processing:** Filter records, categorize data, handle edge cases — all conditionals.

### Machine Learning Is Just If-Elif-Else

You might think machine learning is some magical, complex technology far beyond what you are learning. Here is the truth:

A **Decision Tree** — one of the most widely used ML algorithms — is literally a tree of if-elif-else statements:

```python
if petal_length < 2.5:
    species = "setosa"
elif petal_width < 1.7:
    species = "versicolor"
else:
    species = "virginica"
```

That is a Decision Tree. The ML algorithm figures out the best conditions and thresholds automatically by analyzing data — but the final output is just nested conditionals. The same `if-elif-else` you are learning right now.

**Random Forest** — one of the most powerful ML models used in production at companies like Netflix and Amazon — is just **hundreds of Decision Trees voting together**. Each tree is an if-elif-else chain. Each tree gives an answer. The majority wins.

When someone says *"I built a machine learning model"* — in many cases, what they really built is a giant if-elif-else tree that the computer wrote for them. The concept you are learning right now is the same concept powering ML models in production.

Read more: [Decision Trees — scikit-learn documentation](https://scikit-learn.org/stable/modules/tree.html) | [Random Forest — scikit-learn documentation](https://scikit-learn.org/stable/modules/ensemble.html#forests-of-randomized-trees)

---

## Practice Assignments

### Assignment 1: Age Gatekeeper

Write a program that:

1. Takes the user's age as input
2. If the age is negative or above 150, print "Invalid age"
3. If the user is under 13, print "Child — no access"
4. If the user is 13–17, print "Teenager — limited access"
5. If the user is 18–64, print "Adult — full access"
6. If the user is 65 or above, print "Senior — full access with discount"

Use: `input()`, `int()`, `if-elif-else`, comparison operators, chained comparisons (Part 12).

### Assignment 2: ATM Withdrawal

Write a program that:

1. Has a hardcoded `balance = 10000` and `pin = "1234"`
2. Asks the user for their PIN
3. If the PIN is wrong, print "Incorrect PIN" and stop (do not ask for amount)
4. If correct, ask for the withdrawal amount
5. Check: Is the amount zero or negative? Is the amount greater than the balance? Otherwise, print the new balance after withdrawal

Use: `if-elif-else`, guard clause pattern, truthiness, comparison operators.

### Assignment 3: Flatten the Nest

You are given this deeply nested code. **Rewrite it** using the guard clause pattern with `if-elif-else` — no nesting deeper than one level:

```python
age = int(input("Age: "))
has_ticket = input("Have ticket? (yes/no): ")
has_id = input("Have ID? (yes/no): ")

if age >= 18:
    if has_ticket == "yes":
        if has_id == "yes":
            print("Welcome to the event!")
        else:
            print("ID required for entry")
    else:
        print("You need a ticket")
else:
    print("Must be 18 or older")
```

Use: `if-elif-else`, `and` (Part 12), guard clause pattern.

---

## Why Python Had No switch-case for 30 Years

Every major language — C (1972), Java (1995), JavaScript (1995) — has had a `switch` statement from the beginning. Developers asked for it in Python repeatedly. Guido van Rossum rejected it — **twice**:

- **[PEP 275 (2001)](https://peps.python.org/pep-0275/)** — proposed adding a `switch` statement. Rejected.
- **[PEP 3103 (2006)](https://peps.python.org/pep-3103/)** — proposed it again with multiple implementation options. Rejected.

Guido's argument: `if-elif-else` is clear enough. Adding `switch` would add complexity to the language without meaningful benefit. He believed Python should have **one obvious way to do things** (The Zen of Python: *"There should be one — and preferably only one — obvious way to do it."*).

Python finally got `match-case` in **Python 3.10 (2021)** — but it was not a simple `switch`. It was **[PEP 634 — Structural Pattern Matching](https://peps.python.org/pep-0634/)** — a much more powerful concept that goes far beyond comparing values. Guido would not add it until the proposal was genuinely better than what `if-elif-else` already provided.

Python's creator believed so strongly in `if-elif-else` that he defended it for **20 years**. The tool you just learned is not "basic." It is the decision-making tool that Python's designer considered sufficient for two decades of professional software development.

---

> **Next:** Part 14 — Professional Conditional Patterns. You can now make any decision in code. But there are cleaner, more professional ways to write these — the ternary operator, match-case (the feature Guido resisted for 20 years), and real-world patterns that experienced developers use daily.

