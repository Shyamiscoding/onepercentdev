# Part 50 — Iterators and Generators

In **Part 23** you saw **generator expressions** — `(x for x in ...)` — and using them with `sum()` without building a list. This part explains **why that works**: the **iterator protocol**, `next()` / `StopIteration`, and `yield` in functions, and when to choose lazy generators vs lists.

---

## What Happens Inside a for Loop

Every `for` loop you have written since Part 16 uses the **iterator protocol** behind the scenes:

```python
for item in [1, 2, 3]:
    print(item)
```

What Python actually does:

```python
# Step 1: Get an iterator from the list
iterator = iter([1, 2, 3])

# Step 2: Call next() repeatedly
print(next(iterator))   # 1
print(next(iterator))   # 2
print(next(iterator))   # 3
print(next(iterator))   # StopIteration exception — loop ends
```

Every `for` loop calls `iter()` to get an iterator, then calls `next()` until `StopIteration` is raised.

---



## Iterables vs Iterators

Get these two words straight first — they are the heart of this whole part.

- An **iterable** is anything you *can* loop over. It has `__iter__`. Think of a **book** — it can be read.
- An **iterator** is the thing that *tracks your position* and hands you the next value. It has **both** `__iter__` and `__next__`. Think of a **bookmark** — it remembers where you are and knows what comes next.

```python
my_list = [1, 2, 3]        # Iterable — has __iter__, does NOT have __next__
iterator = iter(my_list)   # Iterator — has BOTH __iter__ and __next__
```

> **Book vs Bookmark**
>
> - **Iterable = the book** → has `__iter__` only → reusable (every loop gets a fresh bookmark).
> - **Iterator = the bookmark** → has `__iter__` **and** `__next__` → tracks position, and is one-shot (once it ends, it's done).
> - `iter(...)` turns an iterable into an iterator; `next(...)` advances an iterator.

Lists, tuples, strings, dicts, sets, and files are all **iterables** — not iterators. Calling `iter()` on them hands you a separate iterator.

**Every iterator is also an iterable, but not every iterable is an iterator.** The book is not the bookmark — but a bookmark can point to itself (that is exactly what custom iterators and generators do).

---



## The Iterator Protocol

The "protocol" is just the **rule** Python uses to decide what is an iterable and what is an iterator — two dunder methods (from Part 49):


| Method       | Belongs to | Purpose                                                     |
| ------------ | ---------- | ----------------------------------------------------------- |
| `__iter__()` | Iterable   | Returns an iterator                                         |
| `__next__()` | Iterator   | Returns the next value, or raises `StopIteration` when done |


**How to tell which is which:**

- Has only `__iter__` → **iterable** (like a list).
- Has both `__iter__` **and** `__next__` → **iterator** (like a bookmark, or a generator).

And this is the exact flow every `for` loop follows behind the scenes:

```
for x in thing:
    1. iter(thing)      ->  thing.__iter__()      (get the iterator = bookmark)
    2. next(iterator)   ->  iterator.__next__()   (get next value)  --> repeat step 2
    3. StopIteration    ->  iterator says "done"  (loop stops)
```

---



## Building a Custom Iterator

Now that you know the rule, you can build your own object that plugs into the *same* `for` loop — just implement both methods:

```python
class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value
```

```python
for num in Countdown(5):
    print(num)
```

Output:

```
5
4
3
2
1
```

The `for` loop calls `__iter__()` to get the iterator, then `__next__()` for each value. When `StopIteration` is raised, the loop ends. Notice `Countdown` returns `self` from `__iter__` — it *is* its own bookmark, which is why it's one-shot.

### Manual Iteration

You can drive it by hand — this is literally what the `for` loop does for you:

```python
countdown = Countdown(3)
it = iter(countdown)

print(next(it))   # 3
print(next(it))   # 2
print(next(it))   # 1
print(next(it))   # StopIteration
```

---



## Generator Functions — Iterators Made Simple

Writing iterator classes is verbose. Generator functions create iterators with much less code:

```python
def countdown(start):
    current = start
    while current > 0:
        yield current
        current -= 1
```

```python
for num in countdown(5):
    print(num)
# 5, 4, 3, 2, 1
```



### How yield Works

`yield` pauses the function and returns a value. The next time `next()` is called, execution resumes from where it paused:

```python
def simple_generator():
    print("Before first yield")
    yield 1
    print("Before second yield")
    yield 2
    print("Before third yield")
    yield 3
    print("After last yield")
```

```python
gen = simple_generator()

print(next(gen))   # Prints "Before first yield", returns 1
print(next(gen))   # Prints "Before second yield", returns 2
print(next(gen))   # Prints "Before third yield", returns 3
# next(gen)        # Prints "After last yield", raises StopIteration
```

The function's state — local variables, position — is preserved between calls. This is fundamentally different from regular functions, which start fresh every time.

### Generators Are Iterators

A generator function returns a generator object, which is an iterator:

```python
gen = countdown(3)
print(type(gen))        # <class 'generator'>
print(next(gen))        # 3
print(next(gen))        # 2
```

No need to write `__iter__` or `__next__`. The `yield` keyword handles everything.

---



## Generator Expressions

Just like list comprehensions, but lazy:

```python
# List comprehension — creates all values immediately
squares_list = [x ** 2 for x in range(1000000)]

# Generator expression — creates values on demand
squares_gen = (x ** 2 for x in range(1000000))
```

```python
import sys

print(sys.getsizeof(squares_list))   # ~8 MB
print(sys.getsizeof(squares_gen))    # ~200 bytes
```

The list stores one million integers in memory. The generator stores only the formula — it computes each value when asked.

```python
# Use like any iterator
for square in squares_gen:
    if square > 100:
        print(square)
        break          # 121 — and we never computed the remaining 999,989 values
```



### Generator Function vs Generator Expression

Both create the **same thing** — a generator object (a lazy iterator). They are only two different ways to write it:


| Aspect           | Generator Function                       | Generator Expression          |
| ---------------- | ---------------------------------------- | ----------------------------- |
| How you write it | `def` with `yield`                       | `(expr for item in iterable)` |
| Size             | Multiple lines                           | One line                      |
| Best for         | Complex logic (branches, multiple steps) | Simple one-line transforms    |
| Returns          | A generator object                       | A generator object            |
| `type()`         | `<class 'generator'>`                    | `<class 'generator'>`         |
| One-shot?        | Yes                                      | Yes                           |


```python
# Generator function
def squares():
    for x in range(5):
        yield x ** 2

# Generator expression — same result, one line
squares = (x ** 2 for x in range(5))
```

**The** `( )` **is not a tuple.** There is no tuple comprehension in Python — the bracket decides what you build:

```python
[x for x in range(5)]    # list comprehension    -> list
{x for x in range(5)}    # set comprehension     -> set
(x for x in range(5))    # generator expression  -> generator (NOT a tuple)
```

```python
print(type([x for x in range(5)]))   # <class 'list'>
print(type((x for x in range(5))))   # <class 'generator'>
```



### When to Use Generator Expressions


| Use List Comprehension               | Use Generator Expression          |
| ------------------------------------ | --------------------------------- |
| You need random access (`result[5]`) | You iterate through once          |
| You need `len()`                     | You only need one value at a time |
| The data fits in memory              | The data might be huge            |
| You reuse the data multiple times    | Single pass processing            |


---



## Memory Efficiency — Why Generators Matter



### Reading a Large File

```python
# Bad — loads entire file into memory
def read_all_lines(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.readlines()   # All lines in memory

# Good — yields one line at a time
def read_lines(filename):
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            yield line.strip()
```

For a 10GB log file, `readlines()` crashes. The generator version processes the file with constant memory, no matter the file size.

---



## Generator Pipelines

Connect generators like a **conveyor belt in a factory**. Each stage does one small job on a value and passes it along to the next stage:

```python
def read_numbers():
    for n in [1, 2, 3, 4, 5, 6]:
        yield n

def keep_even(numbers):
    for n in numbers:
        if n % 2 == 0:
            yield n

def double(numbers):
    for n in numbers:
        yield n * 2

pipeline = double(keep_even(read_numbers()))
print(list(pipeline))   # [4, 8, 12]
```

Read it inside-out: `read_numbers()` produces `1..6`, `keep_even` lets only `2, 4, 6` pass, and `double` turns them into `4, 8, 12`.

The key idea: values are **pulled one at a time** through the belt. `double` asks `keep_even` for a value, which asks `read_numbers` — so no stage ever builds a full list in between. This is exactly how real data pipelines (log lines, CSV rows, records) are processed.

---



## Infinite Generators

Generators can produce values forever:

```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b
```

The generator never runs out. You take as many values as you need:

```python
gen = fibonacci()
for _ in range(10):
    print(next(gen))   # 0, 1, 1, 2, 3, 5, 8, 13, 21, 34
```

---



## Real-World Example — Simulating AI Streaming

When you use ChatGPT, the response appears word by word. That is a generator pattern — each token is yielded as it is produced:

```python
import time

def stream_response(text):
    for word in text.split():
        time.sleep(0.3)
        yield word

for word in stream_response("Generators process data one piece at a time"):
    print(word, end=" ", flush=True)
```

The generator does not have the full sentence ready. It produces each word on the fly and sends it immediately.

Without generators, the user stares at a blank screen for 5 seconds until everything is ready. Generators let the consumer start working **immediately** instead of waiting for everything to finish. This is the core idea behind streaming.

---



## Where This Applies in Real Work

- **File iteration:** When you write `for line in file`, you are using the iterator protocol. Files are iterators that yield one line at a time.
- **AI token streaming:** When ChatGPT streams its response word by word, that is an iterator yielding tokens as they are generated — exactly the `stream_response` pattern above.
- **ML data loading:** PyTorch's `DataLoader` uses iterators to feed batches of training data to the model, one batch at a time.
- **ETL pipelines:** Extract-Transform-Load pipelines chain generators: read from source, transform, write to destination — all streaming.

---



## Practice Assignment

1. Create `fibonacci()`, `even_only(iterable)`, and `square(iterable)` generators
2. Chain them: `square(even_only(fibonacci()))` — get the first 10 squared-even Fibonacci numbers
3. Create `read_csv_rows(filename)` that yields each row as a dictionary
4. Compare memory: list of 1M squares vs generator of 1M squares using `sys.getsizeof()`

Save as `src/generators.py`.

---

