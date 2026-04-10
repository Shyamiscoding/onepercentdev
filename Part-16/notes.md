# Part 16 — For Loops

## Connecting to Part 15

In Part 15 you learned **while** loops — the general engine of repetition — along with `break`, `continue`, and **while-else**. You also saw why **definite** iteration (a known sequence or a fixed count) is exactly where Python’s **for** loop shines: same control-flow ideas, less boilerplate, and no manual counter to forget.

This part builds on that: `for`, `range()`, iterating over strings, **for-else** (the companion to while-else), and nested loops — the patterns you will use in almost every script from here on.

---

## Why this is not “just a for loop”

Most real programs spend most of their time **doing the same kind of thing many times**: scan a string, walk rows in a table, try candidates in a search, train for another epoch, poll until a service answers. That shape is **iteration**. Conditionals decide *what* to do in each step; loops decide *how long* the story continues.

If iteration is fuzzy, **algorithms stay fuzzy** — searching, sorting, two-pointer tricks, prefix sums, and dynamic programming all sit on top of clean loop invariants. Interview screens (FizzBuzz is only the front door), coding challenges, and production codebases all assume you can read and write loops without guessing.

**Machine learning and “AI systems”** are not magic spaghetti: at the engineering level they are still **massive repetition** — another pass over the dataset, another batch, another step in a pipeline — glued together with the same control flow you are learning here. The math is extra; the **loop** is the skeleton.

So this part is a **load-bearing wall**, not decoration. Get loops solid before you chase frameworks or claim to “write algorithms.”

---

## Power and expressiveness: what each loop can do

*This block is **theory** — which kind of loop is strictly more general, and why both exist. Right after it comes a short **history** section; then **Side by side** shows the **same Python program** written with `while` and with `for` — that is **syntax**, not philosophy.*

Part 15 already gave you the deep truth from **Böhm and Jacopini (1966)**: any program can be built from **sequence**, **selection** (`if`), and **iteration** in the **`while` shape**. In that sense, **`while` is the general machine**.

**What follows in practice:**

| Idea | Reality |
|------|--------|
| **Everything you write with `for`**, you *could* rewrite with `while` | Use an index (`i = 0` … `while i < n` … `i += 1`) or, equivalently, walk an iterator by hand. More typing, easier to get wrong — same idea. |
| **Not everything you write with `while` is a natural `for`** | Sentinel input (`until "quit"`), waiting on external state, **irregular updates** (not “next index”), compound conditions — these are **`while` territory**. |

So: **`for` is not “more powerful.”** It is **narrower and safer** for the case **“visit each item in a known sequence or count with `range`.”** **`while` stays strictly broader.** That is why we teach **`while` first** in this series: you see **initialization, condition, update** (or open-ended conditions) in the open. **`for` is the convenience layer** — the automatic transmission — once the pattern is familiar. Part 15’s **manual vs automatic** analogy is exactly this.

---

## Why `for` exists — convenience, theory, and a bit of history

**Theory (structured programming):** Once people proved that **`while`-style iteration** is enough to express **any** computable control flow, language designers still added **`for`**-style loops for one reason: **humans** kept writing the same **counter and “next element”** boilerplate and **getting it wrong** (off-by-one, forgotten increment, infinite loops). **`for`** captures a **documented pattern**: *iterate this sequence*. Fewer moving parts, clearer intent.

**History (short and honest):** Counted loops are **old** — **FORTRAN** had **`DO`** loops in the 1950s for scientific code. So “which came first in computing history?” is **not** a simple “`while` then `for`” story. What *is* simple is your **learning order**: we put **`while` first** so you **feel the engine**. **Python’s `for`** is not C’s `for (i=0; i<n; i++)`; it is **foreach-over-iterable** — walk anything that yields items (`range`, strings, and soon **lists** in Part 17). That design comes from Python’s roots (ideas from **ABC** and emphasis on **readability**).

**Languages without Python’s `while`?** Essentially none for general-purpose work. **`while` stays the fallback for “I cannot name a finite sequence up front.”**

**`do … while` (other languages):** Python has **no** separate syntax. The idiom is **`while True:`** + **`break`** when the exit condition is met (body runs at least once).

---

## Side by side: the same count with `while` and `for`

*You already saw **why** `while` is the broader tool and **why** `for` is the convenience layer. Here is one concrete job — print `0` through `4` — in both forms.*

In Part 15, we learned while loops — they repeat as long as a condition is `True`. You manage the counter, the condition, and the update manually.

For loops are different. They iterate over a sequence automatically. No manual counter. No risk of forgetting the update.

### `for` loop syntax — three ideas (parallel to Part 15’s `while`)

Part 15 split **`while`** into **initialization → condition → update** — all written **by you**. Python’s **`for`** follows one template:

```text
for <variable> in <iterable>:
    <body>
```

| Piece | What it does |
|-------|----------------|
| **`for`** | Starts the loop. |
| **`<variable>`** | A name that receives **one value per iteration** (often `i`, `ch`, `item`). |
| **`in <iterable>`** | The **source** you walk: something that yields values one at a time (`range(5)`, a string, later a list). When there are no more values, the loop ends — **no** separate condition or `+=` line at your keyboard. |
| **`<body>`** | The indented block — runs **once per value**. |

Annotated example (same job as Part 15’s `count` loop):

```python
# 1. Iterable — defines what to walk (here: 0, 1, 2, 3, 4)
# 2. Loop variable — i is set to each value in turn
# 3. Body — runs once per value
for i in range(5):
    print(i)
```

**Where did the `while` three parts go?** They are **not missing** — they are **inside the iterable**. `range(5)` knows where to start, when to stop, and how to step; the `for` statement asks it for the **next** value each round. You only name the variable and write the body.

**Tiny trace (compare to Part 15’s execution trace):**

```
Round 1: i = 0, body runs, print(0)
Round 2: i = 1, body runs, print(1)
…
Round 5: i = 4, body runs, print(4)
range(5) has no more values → loop ends
```

```python
# While loop — manual control (you write all three parts)
i = 0
while i < 5:
    print(i)
    i += 1

# For loop — same effect (iterable carries the walking logic)
for i in range(5):
    print(i)
```

Both produce the same output. The for loop is shorter, safer, and more Pythonic.

**Rule:** If you know how many times to iterate or have a sequence to iterate over, use a for loop. Use while loops for indefinite iteration (when you do not know in advance when to stop).

### Classroom contrast — `quit` and why it is not a `for` job

**Indefinite input until the user types `quit`** — the same pattern as Part 15 (sentinel + `break`):

```python
while True:
    line = input("Type something (or 'quit' to exit): ")
    if line == "quit":
        break
    print(f"You typed: {line}")
```

**Students sometimes ask:** “`break` works in a `for` loop too — so what is the difference?”

The difference is **not** `break`. **`break` exits the nearest loop in both `while` and `for`.** The difference is the **problem shape**: here there is **no sequence to walk** before the program runs — no `range`, no string of future inputs, no list. The stopping rule is **“keep asking until `quit`.”** That is **`while` territory** because you are describing **repetition until a condition**, not **for each item in X**.

**Could you force a `for` anyway?** Yes, as a **hack** — for example an **infinite iterator** so the `for` never runs out of items, and you still `break` on `quit`:

```python
# Jugaad — mimics "infinite" for; NOT recommended, not idiomatic
for _ in iter(int, 1):
    line = input("Type something (or 'quit' to exit): ")
    if line == "quit":
        break
    print(f"You typed: {line}")
```

`iter(int, 1)` keeps calling `int()` with argument `1` forever (always `1`), so the `for` never finishes on its own. It works, but it is **`while True` in disguise** — harder to read and pointless. **Prefer `while True` + `break` for this pattern.**

**Same fixed count — both are valid; `for` is shorter:**

```python
for i in range(5):
    print(i)
```

```python
i = 0
while i < 5:
    print(i)
    i += 1
```

---

## range() — Generating Number Sequences

`range()` generates a sequence of numbers. It does not create them all at once — it produces them one at a time, which is memory efficient.

### range(stop)

Generates numbers from 0 up to (but not including) `stop`:

```python
for i in range(5):
    print(i)
```

Output:

```
0
1
2
3
4
```

Note: `range(5)` generates 5 numbers (0, 1, 2, 3, 4). The stop value is **exclusive**.

In Python 3, `range()` returns a **`range` object**, not a list. Values are produced **lazily** (one at a time), which keeps memory use small even for large spans. If you need a real list — for example to print or inspect every value while debugging — use `list(range(5))` → `[0, 1, 2, 3, 4]`.

**Empty range:** If `start >= stop` with a positive step, there are no numbers to yield — the loop body runs **zero** times:

```python
for i in range(3, 3):
    print(i)   # never runs
```

### range(start, stop)

Start from a specific number:

```python
for i in range(2, 7):
    print(i)
```

Output:

```
2
3
4
5
6
```

### range(start, stop, step)

Control the increment between numbers:

```python
# Count by 2
for i in range(0, 10, 2):
    print(i)
```

Output:

```
0
2
4
6
8
```

### Counting Backwards

Use a negative step:

```python
for i in range(5, 0, -1):
    print(i)
```

Output:

```
5
4
3
2
1
```

### Off-by-One Awareness

The most common for loop mistake is forgetting that `range()` is exclusive on the upper end:

```python
# Prints 1 to 9, NOT 1 to 10
for i in range(1, 10):
    print(i)

# To print 1 to 10:
for i in range(1, 11):
    print(i)
```

---

## Iterating Over Strings

Strings are **iterable** — you can loop through them character by character:

```python
for char in "Python":
    print(char)
```

Output:

```
P
y
t
h
o
n
```

### The Word "Iterable"

An **iterable** is anything you can loop over. So far, you know two iterables:

- `range()` — generates numbers
- `str` — strings (each character is one iteration)

Later, you will learn about lists, tuples, dictionaries, and files — all iterables. The for loop works the same way with all of them.

### When you need the index and the character

If you only care about each character, `for char in text` is enough. When you also need the **position** (index), loop over valid indices and use string indexing from Part 10:

```python
text = "Python"
for i in range(len(text)):
    print(i, text[i])
```

Indices are **0-based**, same as `text[0]`, `text[1]`, …

This pattern is correct and appears often in exercises. In **Part 18** you will learn **`enumerate()`**, which pairs each index with its value in a more idiomatic way — for now, `range(len(text))` plus `text[i]` is enough.

---

## Practical Example: Counting Characters

```python
text = input("Enter a sentence: ")

vowel_count = 0
consonant_count = 0

for char in text.lower():
    if char in "aeiou":
        vowel_count += 1
    elif char.isalpha():
        consonant_count += 1

print(f"Vowels: {vowel_count}")
print(f"Consonants: {consonant_count}")
```

This combines:

- For loop (iterate over string)
- `in` operator (check membership in `"aeiou"`)
- `.lower()` (normalize case)
- `.isalpha()` (skip spaces and punctuation)
- Accumulator pattern (counting)

---

## break and continue in For Loops

`break` and `continue` work the same way as in while loops.

### break — Exit Early

```python
for i in range(10):
    if i == 5:
        print("Found 5, stopping")
        break
    print(i)
```

Output:

```
0
1
2
3
4
Found 5, stopping
```

### continue — Skip Current Iteration

```python
for i in range(10):
    if i % 3 == 0:
        continue
    print(i)
```

Output:

```
1
2
4
5
7
8
```

Multiples of 3 (0, 3, 6, 9) are skipped.

---

## for-else

This mirrors **while-else** from Part 15: the `else` runs only when the loop finishes **without** `break`. The same mental model applies — only the loop type changes.

The `else` block on a for loop runs only if the loop completes **without** hitting a `break`:

```python
target = "x"
text = "Python"

for char in text:
    if char == target:
        print(f"Found '{target}'!")
        break
else:
    print(f"'{target}' not found in '{text}'")
```

Output:

```
'x' not found in 'Python'
```

If `target = "t"`, the `break` would execute and `else` would be skipped.

This pattern is useful for search operations — "did I find what I was looking for?"

---

## Nested For Loops

You can place a for loop inside another for loop:

```python
for i in range(1, 4):
    for j in range(1, 4):
        print(f"{i} x {j} = {i * j}")
    print("---")
```

Output:

```
1 x 1 = 1
1 x 2 = 2
1 x 3 = 3
---
2 x 1 = 2
2 x 2 = 4
2 x 3 = 6
---
3 x 1 = 3
3 x 2 = 6
3 x 3 = 9
---
```

The outer loop runs 3 times. For each outer iteration, the inner loop runs 3 times. Total: 9 iterations.

### Performance Awareness

Nested loops multiply the number of iterations:

| Outer Loop | Inner Loop | Total Iterations |
|-----------|-----------|-----------------|
| 10 | 10 | 100 |
| 100 | 100 | 10,000 |
| 1,000 | 1,000 | 1,000,000 |

With large data, nested loops can become very slow. Understanding this relationship between loop depth and performance is important for writing efficient code.

---

## Combining range() with Conditionals

Powerful patterns emerge when you combine for loops with conditions:

### Find All Even Numbers

```python
for i in range(1, 21):
    if i % 2 == 0:
        print(i)
```

### Sum of Numbers

```python
total = 0
for i in range(1, 101):
    total += i
print(f"Sum of 1 to 100: {total}")  # 5050
```

### FizzBuzz (Classic Interview Problem)

```python
for i in range(1, 16):
    if i % 3 == 0 and i % 5 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)
```

FizzBuzz is one of the most common programming interview questions. It tests your understanding of loops, conditionals, and the modulus operator — all things you already know.

---

## Where This Applies in Real Work

- **Data processing:** Iterating through records, rows, or entries is the core of every data pipeline. For loops process each item in sequence.
- **Text analysis:** Iterating through characters (as we did with the vowel counter) is the basis of text parsing, tokenization, and NLP preprocessing.
- **Batch operations:** Processing items in batches (e.g., send emails to 1000 users, process 500 records) uses for loops with range.
- **Report generation:** Generating reports by iterating through data and accumulating results.
- **Testing:** Running test cases in a loop, checking multiple inputs against expected outputs.
- **API pagination:** Fetching data page by page from an API uses a loop with a counter or condition.

---

## Interviews and common sharp edges

These show up constantly in screening problems and in code review:

- **`range` stops before the end** — the classic off-by-one bug; say aloud “stop is exclusive.”
- **Nested loops multiply cost** — two nested loops over \(n\) items is **on the order of \(n^2\)** steps; know why the table in this part matters.
- **`break` vs `return`:** In a **plain script** (not inside `def`), you **cannot** use **`return`** to exit a loop — use **`break`**. **`return`** ends a **function** (Part 24). Mixing these up is a frequent beginner mistake.
- **Prefer the right loop:** definite walk → **`for`**; open-ended or condition-driven → **`while`** (see **Power and expressiveness** near the start of this part).

---

## Practice Assignment

### Assignment 1 — Multiplication Table

Write a program that:

1. Asks the user for a number
2. Prints the multiplication table for that number (1 to 10)

Example for input `7`:

```
7 x 1 = 7
7 x 2 = 14
7 x 3 = 21
...
7 x 10 = 70
```

### Assignment 2 — Vowel Counter

Write a program that:

1. Asks the user for a string
2. Counts and prints the number of vowels (a, e, i, o, u)
3. Counts and prints the number of consonants
4. Prints each vowel found and its position

For positions, use **`range(len(text))` with `text[i]`** (see above), or track a running index. Decide whether you display positions as **0-based** (like Python indices) or **1-based** (like “first character is position 1”) and stay consistent. Part 18 will introduce **`enumerate()`** for this kind of task.

Example:

```
Enter text: Python
Vowels: 1 (o at position 5)
Consonants: 5
```

### Assignment 3 — Star Pattern

Write a program that asks the user for a number `n` and prints a triangle pattern. Hint: `"*" * i` creates a string of `i` asterisks.

```
*
**
***
****
*****
```

### Assignment 4 — FizzBuzz

Write the FizzBuzz program for numbers 1 to 50. This is the most classic interview question — practice it until you can write it from memory.

Save all as separate files in `src/`.

---

## Further reading

- Python Tutorial — [for statements](https://docs.python.org/3/tutorial/controlflow.html#for-statements) and [`range()`](https://docs.python.org/3/library/stdtypes.html#range) (official docs).

---

> **Next:** Part 17 — Lists. The most important data structure in Python. Lists are mutable, ordered collections that power data processing, API responses, database results, and virtually every real-world application.
