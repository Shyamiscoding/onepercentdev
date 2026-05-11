# Part 27 — Memoization: Don't Compute What You Already Know

In Part 26, you learned what recursion is, why we need it, and how the call stack works. Now we discover a hidden danger — recursion can be **dangerously slow** — and learn how to fix it.

---

## Fibonacci — A Recursive Trap

The Fibonacci sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55 ...

0, 1, 1, 2, 3, 5, 8, 13, 21, 34

0, 1, 1, 2, 3, 5, 8, 13, 21

Each number is the sum of the two before it.

```python
def fibonacci(n):
    if n == 0:                                  # Base case 1
        return 0
    if n == 1:                                  # Base case 2
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)  # Recursive case — two calls!

print(fibonacci(10))   # 55
```

This works. But try `fibonacci(35)` — it takes several seconds. Try `fibonacci(50)` — it might hang your computer. Why?

---

## Why It Explodes

`fibonacci(5)` generates this call tree:

```
                    fib(5)
                   /      \
              fib(4)       fib(3)
             /     \       /    \
         fib(3)  fib(2)  fib(2) fib(1)
        /    \    /   \   /   \
    fib(2) fib(1) fib(1) fib(0) fib(1) fib(0)
    /   \
fib(1) fib(0)
```

`fib(3)` is computed **twice**. `fib(2)` is computed **three times**. The same work is done over and over.

Let's prove it by counting calls:

```python
call_count = 0

def fibonacci(n):
    global call_count
    call_count += 1
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)

fibonacci(30)
print(f"Calls: {call_count}")   # Calls: 2692537
```

**2.7 million calls** for `n=30`. For `n=50`, over **40 billion**. The calls grow exponentially because of **redundant computation** — solving the same subproblem again and again.

---

## Memoization — Remember What You Already Computed

The fix: before computing, check if you've already solved this. If yes, return the cached result.

### Manual Memoization with a Dictionary

```python
cache = {}
call_count = 0

def fibonacci(n):
    global call_count
    call_count += 1
    if n in cache:
        return cache[n]
    if n == 0:
        return 0
    if n == 1:
        return 1

    result = fibonacci(n - 1) + fibonacci(n - 2)
    cache[n] = result
    return result

print(fibonacci(50))        # 12586269025 — instant
print(f"Calls: {call_count}")  # Calls: 99

call_count = 0
print(fibonacci(100))       # 354224848179261915075 — still instant
print(f"Calls: {call_count}")  # Calls: 99 (51 to 100, rest from cache)
```

Each value is computed **once**. Every subsequent call returns the cached result immediately.

### Using `@lru_cache` (Python's Built-in)

```python
from functools import lru_cache

@lru_cache
def fibonacci(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(100))   # 354224848179261915075 — instant
```

`@lru_cache` does the same thing as our manual dictionary — but Python handles it for you. We haven't covered decorators yet — for now, use this as a recipe. The `@` syntax will be explained in a later part.

### The Difference

```
Without caching: fibonacci(30) → 2,692,537 calls
With caching:    fibonacci(30) → 59 calls
With caching:    fibonacci(50) → 99 calls
With caching:    fibonacci(100) → 199 calls
```

| n | Without caching | With caching | How much faster |
|---|----------------|--------------|-----------------|
| 10 | 177 calls | 19 calls | 9x |
| 30 | 2,692,537 calls | 59 calls | 45,636x |
| 50 | 40+ billion calls | 99 calls | 400,000,000x+ |
| 100 | longer than your lifetime | 199 calls | ♾️ |


From millions of calls to 31. One dictionary. That's the power of "don't compute what you already know."

---

## Practical Examples — Recursion on Real Data

### Flatten a Nested List

In Part 26, we used `nested_sum` to add up numbers in a nested list. Here's a related problem — **flatten** the list into a single level:

```python
def flatten(nested):
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

data = [1, [2, 3], [4, [5, 6]], 7]
print(flatten(data))   # [1, 2, 3, 4, 5, 6, 7]
```

### Count All Keys in a Nested Dictionary

APIs often return deeply nested JSON. How many total keys are there?

```python
def count_keys(d):
    count = 0
    for key, value in d.items():
        count += 1
        if isinstance(value, dict):
            count += count_keys(value)
    return count

config = {
    "database": {
        "host": "localhost",
        "port": 5432,
        "credentials": {
            "user": "admin",
            "password": "secret"
        }
    },
    "debug": True
}

print(count_keys(config))   # 7
```

Both examples follow the same pattern from Part 26: if the item is nested, recurse; otherwise, handle it directly.

---

## Practice Assignment

1. Implement Fibonacci in three ways:
  - `fib_recursive(n)` — naive recursion
  - `fib_iterative(n)` — loop-based
  - `fib_cached(n)` — recursion with `@lru_cache`
2. For each version, count how many function calls are made for `n=30`
3. Print the results:

```
Naive recursive:  fib(30) = 832040, calls = 2692537
Iterative:        fib(30) = 832040, iterations = 29
Cached recursive: fib(30) = 832040, calls = 31
```

1. Bonus: try `fib_cached(100)` — instant. Now imagine `fib_recursive(100)` — it would take longer than your lifetime.

Save as `src/fibonacci_compare.py`.

---

> **Next:** Part 28 — Lambda + Functional Helpers. Anonymous functions, map, filter, reduce — and when comprehensions are the better choice.

