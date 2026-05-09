# Part 26 — Recursion Part 1 (Thinking in Stack Frames)

In Part 25, you learned how to make functions flexible with default arguments, `*args`, and `**kwargs`. Now we turn to a different kind of power: a function that calls itself.

---

## What Is Recursion?

Recursion is when a function calls itself to break a problem into a **smaller version of the same problem**.

You already know how to do a countdown with a loop:

```python
def countdown_loop(n):
    for i in range(n, 0, -1):
        print(i)
    print("Done!")

countdown_loop(5)
```

Here's the same thing with recursion:

```python
def countdown(n):
    if n == 0:
        print("Done!")
        return
    print(n)
    countdown(n - 1)

countdown(5)
```

Both produce the same output:

```
5
4
3
2
1
Done!
```

The loop does all the work in one place. The recursive version does one step (`print(n)`) and delegates the rest to itself (`countdown(n - 1)`).

Every recursive function has two parts:

| Part | Purpose |
|------|---------|
| **Base case** | The simplest version — stops calling itself and returns a known answer |
| **Recursive case** | Calls itself with a **smaller** input |

Without a base case, the function calls itself forever.

---

## Why Do We Need Recursion?

Loops work on **flat** data — one level deep, left to right.

```python
numbers = [1, 2, 3, 4, 5]
total = 0
for n in numbers:
    total += n
print(total)   # 15
```

But what if the data is **nested**?

```python
data = [1, [2, [3, [4, [5]]]]]
```

Try summing this with a loop:

```python
total = 0
for item in data:
    if isinstance(item, list):
        for sub_item in item:
            if isinstance(sub_item, list):
                for sub_sub_item in sub_item:
                    # ... how deep do we go?!
                    pass
    else:
        total += item
```

You **don't know** how deep the nesting goes. 1 level? 5 levels? 100 levels? You'd need infinite `for` loops.

With recursion — it just works:

```python
def nested_sum(data):
    total = 0
    for item in data:
        if isinstance(item, list):
            total += nested_sum(item)   # Recursive case — it's a list, go deeper
        else:
            total += item               # Base case — it's a number, just add it
    return total

print(nested_sum([1, [2, [3, [4, [5]]]]]))          # 15
print(nested_sum([1, 2, [3, 4], [5, [6, [7]]]]))    # 28
```

No matter how deep — 5 levels, 500 levels — this handles it.

### Folders on Your Computer

```
Downloads/
├── resume.pdf
├── photos/
│   ├── vacation/
│   │   ├── beach.jpg
│   │   └── sunset.jpg
│   └── selfie.png
└── projects/
    └── app/
        └── main.py
```

A folder contains **files** and **folders**. A folder inside a folder also contains files and folders. Same problem at every level — just smaller.

```python
import os

def list_files(path):
    for item in os.listdir(path):
        full = os.path.join(path, item)
        if os.path.isdir(full):
            list_files(full)       # folder? same problem, smaller.
        else:
            print(full)
```

Reads like English: "For each item — if it's a folder, list its files. If it's a file, print it."

### When to use recursion vs loops

**Reach for recursion when:**
1. The problem has a smaller version of **itself** inside it
2. You don't know how deep it goes
3. "Handle one piece, delegate the rest" fits naturally

**A loop is fine when:**
- Flat data, known number of steps, no nesting

Recursion is **not** a replacement for loops — it's a different tool for a different **shape** of problem.

---

## Base Case and Recursive Case — Factorial

Factorial of n: `n! = n × (n-1) × (n-2) × ... × 1`

- `5! = 5 × 4 × 3 × 2 × 1 = 120`
- `1! = 1`
- `0! = 1` (by definition — the base case)

```python
def factorial(n):
    if n == 0 or n == 1:           # Base case
        return 1
    return n * factorial(n - 1)    # Recursive case

print(factorial(5))   # 120
print(factorial(0))   # 1
```

### Step-by-Step Trace

```
factorial(5)
  → 5 * factorial(4)
       → 4 * factorial(3)
            → 3 * factorial(2)
                 → 2 * factorial(1)
                      → 1          (base case)
                 → 2 * 1 = 2
            → 3 * 2 = 6
       → 4 * 6 = 24
  → 5 * 24 = 120
```

Dives deeper until it hits the base case, then unwinds back up building the result.

---

## The Call Stack

When you call a function, Python creates a **frame** on the stack. A frame holds the function's local variables. When the function returns, that frame is removed.

When `factorial(5)` runs, five frames stack up:

```
┌─────────────────────────┐
│ Frame: factorial(5)      │  n=5, waiting for factorial(4)
├─────────────────────────┤
│ Frame: factorial(4)      │  n=4, waiting for factorial(3)
├─────────────────────────┤
│ Frame: factorial(3)      │  n=3, waiting for factorial(2)
├─────────────────────────┤
│ Frame: factorial(2)      │  n=2, waiting for factorial(1)
├─────────────────────────┤
│ Frame: factorial(1)      │  n=1, returns 1 → starts unwinding
└─────────────────────────┘
```

Each frame has its **own** `n`. They don't share variables. When `factorial(1)` returns, its frame is removed, then `factorial(2)` computes its result, and so on — the stack **unwinds** back up.

### Visualizing with Print Tracing

```python
def factorial(n, depth=0):
    indent = "  " * depth
    print(f"{indent}factorial({n}) called")

    if n == 0 or n == 1:
        print(f"{indent}factorial({n}) returns 1")
        return 1

    result = n * factorial(n - 1, depth + 1)
    print(f"{indent}factorial({n}) returns {result}")
    return result

factorial(5)
```

Output:

```
factorial(5) called
  factorial(4) called
    factorial(3) called
      factorial(2) called
        factorial(1) called
        factorial(1) returns 1
      factorial(2) returns 2
    factorial(3) returns 6
  factorial(4) returns 24
factorial(5) returns 120
```

Goes DOWN (calling) then comes back UP (returning) — the call stack in action.

---

## Common Mistakes

### 1. Missing Base Case

```python
def infinite(n):
    return n * infinite(n - 1)   # Never stops

infinite(5)   # RecursionError: maximum recursion depth exceeded
```

### 2. Base Case Never Reached

```python
def broken(n):
    if n == 0:
        return 1
    return n * broken(n + 1)   # n grows instead of shrinking

broken(5)   # RecursionError
```

Each call must move **closer** to the base case, not farther.

### 3. Wrong Base Case Value

```python
def bad_factorial(n):
    if n == 0:
        return 0   # Should return 1
    return n * bad_factorial(n - 1)

print(bad_factorial(5))   # 0 — everything multiplied by 0
```

---

## RecursionError and Python's Limit

Python has a default recursion limit of 1000:

```python
import sys
print(sys.getrecursionlimit())   # 1000
```

Go deeper than this and Python raises `RecursionError` to prevent a stack overflow.

You can increase it with `sys.setrecursionlimit()`, but if your recursion goes that deep, a loop is probably the better tool.

---

## Practice Assignment

1. Write a recursive function `sum_digits(n)` that calculates the sum of digits of a positive integer:
   - `sum_digits(1234)` → `10` (1+2+3+4)
   - Hint: `n % 10` gives the last digit, `n // 10` removes the last digit
   - Base case: when `n` is a single digit (less than 10)

2. Add print tracing to `sum_digits` (like the factorial example) to visualize each call

3. Write a recursive function `reverse_string(s)` that reverses a string:
   - `reverse_string("Python")` → `"nohtyP"`
   - Hint: last character + reverse of the rest
   - Base case: empty string or single character

Save as `src/recursion_basics.py`.

---

> **Next:** Part 27 — Recursion Part 2. Fibonacci, why naive recursion is slow, and memoization — the technique that turns exponential time into instant results.
