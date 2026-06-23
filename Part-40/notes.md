# Part 40 — Debugging

You can now handle exceptions (Parts 33–35), read and write files (Parts 36–38.1), and open Markdown, PDF, Excel, and images (Part 39). As code grows, so do bugs — and before you can *fix* an error, you have to *find* it. That is debugging: tracking down exactly where and why things break.

> **The one idea of this part:** debugging is not guessing, it is a **repeatable method** — and you have three tools to run it: `print()`, `breakpoint()`, and the VS Code debugger.

---

## The Debugging Mindset (the loop)

The best debuggers are not the fastest coders — they are the calmest thinkers. They run the same loop every time instead of randomly changing code:

1. **Reproduce** — make the bug happen on demand. A bug you can't trigger, you can't fix.
2. **Read** — read the error message and traceback *first*. It usually tells you what, where, and why.
3. **Locate** — narrow down to the exact line (prints / breakpoints / binary search).
4. **Hypothesize** — "I think `total` is a string, not a number." A guess you can test.
5. **Change ONE thing** — test the hypothesis. If you change three things and it works, you don't know which fix was real.
6. **Verify** — confirm it's fixed, then re-check the edge cases (empty input, missing file).

Slow is smooth, smooth is fast. Skipping step 2 is the #1 beginner mistake.

---

## Step 1 — Read the Traceback (bottom-up)

When Python errors, it prints a **traceback** — the chain of calls that led to the crash. Read it **from the bottom up**:

```
Traceback (most recent call last):
  File "main.py", line 15, in <module>
    report = generate_report(data)
  File "reports.py", line 22, in generate_report
    summary = calculate_summary(records)
  File "utils.py", line 8, in calculate_summary
    avg = total / count
ZeroDivisionError: division by zero
```

- **Last line** = the error type + message → *what* broke: `ZeroDivisionError: division by zero`
- **Line above it** = the exact line that failed → *where*: `utils.py` line 8
- **Lines higher up** = *who called whom* → the path in: `main.py` → `reports.py` → `utils.py`

The bottom is where it broke; everything above is how you got there.

### Common Errors — Know Them on Sight


| Error                                                    | Typical cause                            |
| -------------------------------------------------------- | ---------------------------------------- |
| `NameError: name 'x' is not defined`                     | typo, or variable used before assignment |
| `TypeError: unsupported operand type(s)`                 | mixing types (e.g. `str + int`)          |
| `IndexError: list index out of range`                    | index that doesn't exist                 |
| `KeyError: 'name'`                                       | dictionary key that doesn't exist        |
| `AttributeError: 'str' object has no attribute 'append'` | method doesn't exist on that type        |
| `ValueError: invalid literal for int()`                  | converting bad data, e.g. `int("abc")`   |
| `FileNotFoundError`                                      | wrong path or file doesn't exist         |


---

## Step 2 — Pick Your Tool


| Tool             | Best for                                         | Cost                           |
| ---------------- | ------------------------------------------------ | ------------------------------ |
| `print()`        | quick "what is this value?" checks               | fast, but you must clean it up |
| `breakpoint()`   | pause and poke around live, no setup             | terminal-based                 |
| VS Code debugger | complex bugs, step through, watch many variables | a few clicks, most powerful    |


### print() — fast and everywhere

Print the value *right before* the line that fails, and at each step of a transformation:

```python
def process_scores(scores):
    print(f"input: {scores}")              # what came in?
    filtered = [s for s in scores if s > 50]
    print(f"after filter: {filtered}")     # what survived?
    return sum(filtered) / len(filtered)   # crashes here? filtered is empty
```

Rule of thumb: print *function inputs*, *loop values*, and *the values going into the line that crashes*. (Part 41 replaces this with proper `logging`.)

### breakpoint() — the built-in debugger

`breakpoint()` (Python 3.7+) **pauses** your program and drops you into an interactive prompt where you can type variable names and expressions to inspect the live state:

```python
def calculate(a, b):
    result = a + b
    breakpoint()      # execution pauses here
    return result * 2
```

Key commands at the prompt:


| Command      | Does                      |
| ------------ | ------------------------- |
| `<variable>` | print its current value   |
| `n`          | next line (step over)     |
| `s`          | step into a function call |
| `c`          | continue running          |
| `q`          | quit                      |


### VS Code Debugger — the visual tool

For anything non-trivial, this beats print debugging: no print statements to add or delete, and you see *every* variable at once.

- **Set a breakpoint:** click the left margin next to a line number → a red dot appears.
- **Start:** press `F5` → choose "Python File". Execution pauses at the red dot.


| Control   | Key         | What it does                           |
| --------- | ----------- | -------------------------------------- |
| Continue  | `F5`        | run to the next breakpoint             |
| Step Over | `F10`       | run the current line, go to the next   |
| Step Into | `F11`       | go *inside* the function on this line  |
| Step Out  | `Shift+F11` | finish this function, return to caller |
| Stop      | `Shift+F5`  | end debugging                          |


**Step Over vs Step Into:** on `result = process_data(input)`, *Step Over* runs the whole function and shows you the result; *Step Into* jumps inside it. Step over when you trust the function; step into when you suspect the bug is inside it.

Three panels do the work for you:

- **Variables** — every local/global value, updating as you step.
- **Watch** — pin specific expressions to track them.
- **Call Stack** — the live call chain (like a traceback you can click through to see each function's variables).

---

## Strategies to Localize a Bug

- **Binary search:** in a long function, check the value at the *middle*. Correct there? Bug is in the second half. Wrong? First half. Repeat — each check halves the search.
- **Rubber duck:** explain the code line by line out loud. You'll often hear yourself say "wait, that's wrong" before you finish.

---

## Worked Example

```python
def calculate_average(scores):
    total = 0
    for score in scores:
        total += scores        # bug: adding the whole list, not the element
    return total / len(scores)

calculate_average([80, 90, 85])   # TypeError: unsupported operand type(s)
```

The traceback says `TypeError` on `total += scores`. Add one print to confirm the hypothesis ("`score` is fine, but I'm adding `scores`"):

```python
for score in scores:
    print(f"score={score}, total={total}")   # total never grows like a number → spot the typo
    total += score                            # fix: score, not scores
```

One print, one hypothesis, one fix — the loop in action.

---

## Practice Assignment

Debug this script — it has 4 intentional bugs (two visible, two that only appear at runtime):

```python
def load_scores(filename):
    scores = []
    with open(filename, "r") as file:
        for line in file:
            scores.append(line)          # Bug 1: not stripped / not int → sum() fails
    return scores

def calculate_stats(scores):
    average = sum(scores) / len(scores)  # Bug 2: ZeroDivisionError if empty
    return {"average": average, "highest": max(scores), "count": len(scores)}

def print_report(stats):
    print(f"Count: {stats['count']}")
    print(f"Average: {stats['averge']}")  # Bug 3: typo in key name

scores = load_scores("scores.txt")        # Bug 4: FileNotFoundError if missing
print_report(calculate_stats(scores))
```

1. Create `scores.txt` with one number per line.
2. Run it, read each traceback bottom-up, and locate the bug.
3. Use `print()` or the VS Code debugger to confirm before fixing.
4. Fix each bug and test edge cases: missing file, empty file.

Save the fixed version as `src/debug_exercise.py`.

---

## Where This Applies in Real Work

- **Production tracebacks:** server errors are logged as tracebacks — reading them fast is the first step to a fix.
- **Data pipelines:** stepping through a transformation in the debugger shows exactly where data gets corrupted.
- **Recursion:** the Call Stack panel makes recursion depth and per-level state visible.

---

