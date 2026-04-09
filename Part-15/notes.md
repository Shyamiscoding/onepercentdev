# Part 15 — While Loops

## Connecting to Part 14

In Parts 11–14, your programs learned to compare values, evaluate truthiness, and make decisions with `if` / `elif` / `else`. Your programs can now **think**. But they still run once and stop. A program that checks one condition and exits is not very useful in the real world.

What is missing is **repetition** — the ability to do something over and over until a goal is met. That idea sounds simple. It is not. Before programming languages had a clean way to express repetition, it was the single biggest source of bugs and unreadable code in the industry. The solution — the `while` loop — did not just appear out of nowhere. It was fought for. It replaced something ugly. And a mathematical theorem proved it was the **only** loop construct you would ever truly need.

This part teaches the while loop. But before the syntax, you need to understand the problem it solved and why it is the foundation every other loop is built on.

---

## Before Loops — The GOTO Era

In the 1940s and 1950s, programs were sequential — instruction 1, instruction 2, instruction 3, done. If you needed to repeat something, you used **GOTO**: an instruction that told the computer to jump back to an earlier line and continue from there.

Here is what repeating a task looked like:

```
1. SET count TO 0
2. PRINT count
3. ADD 1 TO count
4. IF count < 5 GOTO 2
5. PRINT "Done"
```

Line 4 says: *"If count is still less than 5, jump back to line 2."* The program loops by jumping backwards. It works. But now imagine a real program with hundreds of these jumps — GOTO line 47, GOTO line 12, GOTO line 83. The flow of the program becomes a tangled mess of arrows jumping in every direction. Developers called this **spaghetti code** — because tracing the execution path looked like a plate of tangled spaghetti.

Now look at the same logic with a while loop:

```python
count = 0
while count < 5:
    print(count)
    count += 1
print("Done")
```

No line numbers. No jumps. The structure itself tells you what repeats, when it stops, and what comes after. You can read it top to bottom and understand it immediately.

In **1968**, the Dutch computer scientist **Edsger Dijkstra** published a letter that changed programming forever: **["Go To Statement Considered Harmful"](https://dl.acm.org/doi/10.1145/362929.362947)**. It is one of the most famous publications in the history of computer science. Dijkstra argued that GOTO should be eliminated from programming languages entirely. It made programs impossible to reason about, impossible to prove correct, and impossible to maintain.

His proposal: replace all GOTOs with just three structured constructs:

1. **Sequence** — execute statements in order (you have been doing this since Part 1)
2. **Selection** — `if-else` (Parts 13–14)
3. **Iteration** — `while` loop (this part)

That is it. No GOTO. No jumps. Three constructs, and you can write any program. This movement became known as **structured programming**, and it is the reason every modern language — Python, Java, JavaScript, C, Rust — gives you `if` and `while` as core building blocks instead of GOTO.

The while loop is not just "a way to repeat things." It is the construct that **replaced chaos with structure**. It exists because the alternative was unreadable, unmaintainable spaghetti.

---

## The Böhm-Jacopini Theorem — Why While is THE Loop

Dijkstra argued that three constructs were enough. But was he right? Could you actually replace **every possible program** with just sequence, selection, and while — and never lose any capability?

Two years before Dijkstra's letter, in **1966**, two Italian mathematicians — **Corrado Böhm** and **Giuseppe Jacopini** — proved it mathematically. Their theorem states:

> **Any computable function can be expressed using only three control structures: sequence, selection (if-else), and iteration (while).**

Read that again. It says **any**. Not "most programs." Not "simple programs." Any computation that a computer can perform — from printing "Hello World" to training a neural network — can be written using only these three structures.

What this means for you:

- **While is not "a type of loop."** It is THE loop. The minimum viable iteration construct. Everything else — `for`, `do-while`, `foreach` — is a convenience layer built on top of it.
- **Every for loop can be rewritten as a while loop.** Not every while loop can be rewritten as a for loop. While is strictly more expressive.
- **Python could have shipped with only `while`** and you could still write every program. The `for` loop exists because one specific while pattern is so common that it earned a shortcut (you will see this in Part 16).

Here is a way to feel this: your CPU — the physical chip running your code right now — is itself a while loop. The processor executes a cycle called **fetch-decode-execute**: fetch the next instruction from memory, decode what it means, execute it, repeat. This cycle runs from the moment you turn on your computer until you shut it down. It is a while loop at the hardware level. The most fundamental operation a computer performs is iteration — and `while` is its direct expression in code.

---

## Why While Before For

If `for` is safer and shorter, why are we learning `while` first? Why not start with the easier tool?

Because **while exposes the machinery that for hides**.

A while loop forces you to write all three parts explicitly:

```python
i = 0              # 1. Initialization — you set the starting state
while i < 5:       # 2. Condition — you decide when to stop
    print(i)
    i += 1         # 3. Update — you move toward the exit
```

A for loop hides all three:

```python
for i in range(5):  # init, condition, and update — all hidden inside range()
    print(i)
```

The for loop is cleaner. But if you learn it first, you never confront the questions that matter: *Where does `i` start? What makes the loop stop? What changes each iteration?* You use `range(5)` like a magic spell without understanding the engine underneath.

Learning while first is like learning to drive a manual car before an automatic. It is harder. You will stall. You will grind the gears. But when you switch to automatic later, you **understand what the car is doing for you** — and when the automatic fails (and it will), you know how to take manual control.

The `for` loop exists because one specific while pattern — *initialize a counter, check the counter, increment the counter* — is so overwhelmingly common that Python gives it a dedicated, safer syntax. You will learn that in Part 16. But first, you need to understand the pattern it is automating. Otherwise, you are memorizing syntax without understanding computation.

---

## The Trade-Off — Manual Control is the Feature

The biggest complaint about while loops is that you have to manage everything yourself. Forget the update? Infinite loop. Wrong condition? Off-by-one error. Wrong initialization? Incorrect results.

This is real. The manual control IS the cost. But that cost is also why while loops can do things for loops **cannot**.

**What only while can do naturally:**

```python
# 1. Indefinite iteration — you don't know when to stop
while user_input != "quit":
    user_input = input("Command: ")

# 2. Complex, multi-variable conditions
while fuel > 0 and altitude > 0 and not landed:
    adjust_thrust()

# 3. Non-linear state updates — not just +1
while n != 1:          # Collatz — the update is wildly unpredictable
    if n % 2 == 0:
        n = n // 2
    else:
        n = 3 * n + 1

# 4. External conditions — waiting for something outside your program
while not server_response:
    server_response = check_server()
    time.sleep(1)
```

None of these fit the for loop pattern of "iterate over a known sequence." You do not know how many times the user will type before quitting. You do not know how the Collatz sequence will unfold. You do not know when the server will respond. The number of iterations is **determined at runtime by conditions you cannot predict in advance**.

**What for does better:**

```python
# Iterate exactly 10 times
for i in range(10):
    print(i)

# Process each character in a string
for char in "Python":
    print(char)

# Process each item in a collection
for item in shopping_list:
    process(item)
```

These are **definite iteration** — you know the sequence in advance. For loops are shorter, safer, and impossible to accidentally make infinite. When the iteration is definite, for is the right tool.

| | **while** | **for** |
|---|---|---|
| Iteration type | Indefinite — you do not know when to stop | Definite — you know the sequence in advance |
| Control | Manual — you manage init, condition, update | Automatic — the sequence handles it |
| Risk | Infinite loops if you forget the update | Cannot accidentally loop forever |
| Power | Can express ANY iteration | Only iterates over known sequences |
| Best for | User input, polling, retry, unknown stopping points | Collections, ranges, strings, files |

The relationship is clear: **while is the engine, for is cruise control**. Cruise control is great on a highway — smooth, effortless, safe. But you cannot use cruise control in a parking lot, in traffic, or on a winding mountain road. Those require manual control. While gives you that.

You need to understand the engine before cruise control makes sense. That is why we start here.

---

## While Loop Structure

A while loop has three essential parts:

```python
# 1. Initialization
count = 0

# 2. Condition
while count < 5:
    print(count)
    # 3. Update
    count += 1
```

Output:

```
0
1
2
3
4
```

### The Three Parts

| Part | Purpose | What Happens If Missing |
|------|---------|----------------------|
| Initialization | Set the starting state | Variable is undefined — error |
| Condition | Decide when to stop | Loop never starts or never stops |
| Update | Change state each iteration | Loop runs forever (infinite loop) |

### Execution Trace

Understanding how each iteration works is critical:

```
Iteration 1: count = 0, condition 0 < 5 → True, prints 0, count becomes 1
Iteration 2: count = 1, condition 1 < 5 → True, prints 1, count becomes 2
Iteration 3: count = 2, condition 2 < 5 → True, prints 2, count becomes 3
Iteration 4: count = 3, condition 3 < 5 → True, prints 3, count becomes 4
Iteration 5: count = 4, condition 4 < 5 → True, prints 4, count becomes 5
Check:       count = 5, condition 5 < 5 → False, loop ends
```

Tracing through iterations manually is the best way to understand loops and catch bugs.

---

## Infinite Loops

If the condition never becomes `False`, the loop runs forever:

```python
# WARNING: This runs forever
while True:
    print("Running...")
```

To stop an infinite loop manually, press `Ctrl + C` in the terminal.

### When Infinite Loops Are Intentional

Not all infinite loops are bugs. Some are designed to run until explicitly stopped:

```python
while True:
    command = input("Enter command (quit to exit): ").strip().lower()
    if command == "quit":
        print("Goodbye!")
        break
    print(f"You entered: {command}")
```

This is the **sentinel loop pattern** — the loop runs indefinitely until a specific condition triggers an exit.

### When Infinite Loops Are Bugs

```python
# Bug: forgot to update i
i = 0
while i < 5:
    print(i)
    # Missing: i += 1
    # This prints 0 forever
```

Forgetting the update step is the most common loop bug.

---

## break — Exit the Loop Early

`break` immediately exits the loop, regardless of the condition:

```python
count = 0
while count < 100:
    if count == 5:
        print("Reached 5, stopping early")
        break
    print(count)
    count += 1
```

Output:

```
0
1
2
3
4
Reached 5, stopping early
```

The loop was set to run 100 times, but `break` stopped it at 5.

---

## continue — Skip the Current Iteration

`continue` skips the rest of the current iteration and jumps back to the condition check:

```python
count = 0
while count < 10:
    count += 1
    if count % 2 == 0:
        continue
    print(count)
```

Output:

```
1
3
5
7
9
```

Even numbers are skipped because `continue` jumps back to the top of the loop before `print()` executes.

---

## Sentinel Loop Pattern (Real-World Pattern)

This is how interactive programs, CLI tools, and servers work:

```python
while True:
    user_input = input("Enter a number (or 'done' to finish): ").strip()
    
    if user_input.lower() == "done":
        break
    
    if not user_input.isdigit():
        print("Please enter a valid number.")
        continue
    
    number = int(user_input)
    print(f"You entered: {number}")

print("Program finished.")
```

This pattern:

1. Runs indefinitely (`while True`)
2. Takes input each iteration
3. Validates the input (`continue` if invalid)
4. Processes valid input
5. Exits on a specific command (`break`)

This is exactly how a web server works — it listens for requests in an infinite loop, processes each one, and only stops when explicitly shut down.

---

## Accumulator Pattern

A common pattern where you build up a result over multiple iterations:

```python
total = 0
count = 0

while True:
    value = input("Enter a number (or 'done'): ").strip()
    if value.lower() == "done":
        break
    if not value.isdigit():
        print("Invalid number, skipping.")
        continue
    
    total += int(value)
    count += 1

if count > 0:
    print(f"Sum: {total}")
    print(f"Count: {count}")
    print(f"Average: {total / count:.2f}")
else:
    print("No numbers entered.")
```

The accumulator (`total`) and counter (`count`) are updated each iteration to compute a final result.

---

## while-else

Python has a unique feature: you can attach an `else` block to a while loop. The `else` runs only if the loop completes normally (without `break`):

```python
target = 7
guess = 0

while guess < 5:
    attempt = int(input("Guess a number: "))
    guess += 1
    if attempt == target:
        print("Correct!")
        break
else:
    print("Out of attempts. The number was 7.")
```

If the user guesses correctly, `break` executes and `else` is skipped. If all 5 attempts are used without a correct guess, the `else` block runs.

---

## Thinking in Loops — From Problem to Solution

Knowing the syntax of `while` is easy. The hard part is looking at a problem and figuring out **how to turn it into a loop**. This is the skill that separates someone who memorized syntax from someone who can actually solve problems.

### Step 1: Recognize the Loop

Before writing any code, ask yourself: **"Is there repetition?"**

Not every problem needs a loop. But when you see phrases like these — in a problem description, in your head, or in real-world requirements — you need a while loop:

- "Keep doing X **until** Y happens"
- "Repeat **as long as** the condition holds"
- "Try **again** if it fails"
- "Process items **one by one** until there are none left"
- "Wait **until** the result is ready"

The word "until" almost always means a while loop. "For each item" usually means a for loop (Part 16). Learn to listen for these words.

### Step 2: Ask Four Questions

Once you know you need a loop, answer these before writing a single line of code:

| Question | What It Determines |
|----------|-------------------|
| 1. Where do I start? | **Initialization** — what variables exist before the loop begins? |
| 2. When do I stop? | **Condition** — what must become `False` to end the loop? |
| 3. What happens each time? | **Body** — what work does each iteration do? |
| 4. What changes each time? | **Update** — what moves me closer to the exit condition? |

If you cannot answer question 4, you will write an infinite loop. If you cannot answer question 2, you do not understand the problem yet.

### Step 3: What Goes Inside vs Outside?

This is where beginners get confused. Here is the rule:

**Outside the loop (before it):** Variables that need to **persist across all iterations** — counters, accumulators, flags, the initial state.

**Inside the loop:** Work that happens **each iteration** — reading input, processing data, checking conditions, updating state.

**After the loop:** Code that uses the **final result** — printing the answer, returning the value, making a decision based on what the loop computed.

```python
# OUTSIDE: These persist across iterations
total = 0        # accumulator — builds up over time
count = 0        # counter — tracks how many iterations

while True:
    # INSIDE: This happens each time
    value = input("Enter number (or 'done'): ")
    if value == "done":
        break
    total += int(value)
    count += 1

# AFTER: Use the final result
print(f"Average: {total / count}")
```

A common mistake is putting initialization **inside** the loop — then it resets every iteration and your accumulator never accumulates.

### Step 4: Solve One Iteration First

Do not try to write the whole loop at once. First, write the code for **a single pass** — as if the loop only runs once. Then wrap it.

**Problem:** "Check if a number is prime."

First, think about what you need to do once: check if a specific divisor divides the number.

```python
# One iteration: check one divisor
if number % divisor == 0:
    print("Not prime")
```

Now ask: what needs to repeat? You need to check **many divisors** — from 2 up to the square root of the number. Wrap it:

```python
number = int(input("Enter a number: "))
divisor = 2
is_prime = True

while divisor * divisor <= number:
    if number % divisor == 0:
        is_prime = False
        break
    divisor += 1

if number > 1 and is_prime:
    print(f"{number} is prime")
else:
    print(f"{number} is not prime")
```

Notice how the four questions are answered:
1. **Start:** `divisor = 2`, `is_prime = True`
2. **Stop:** when `divisor * divisor > number` (we have checked enough)
3. **Each time:** check if `divisor` divides `number`
4. **Changes:** `divisor += 1`

### Step 5: Trace Before You Run

Before hitting run, trace through the first few iterations **by hand**. This is the single most important debugging skill for loops.

Let us trace the prime checker with `number = 15`:

```
divisor = 2: 2 * 2 = 4 ≤ 15 → True. 15 % 2 = 1 ≠ 0. divisor becomes 3.
divisor = 3: 3 * 3 = 9 ≤ 15 → True. 15 % 3 = 0 == 0. Not prime! break.
```

Now with `number = 7`:

```
divisor = 2: 2 * 2 = 4 ≤ 7 → True. 7 % 2 = 1 ≠ 0. divisor becomes 3.
divisor = 3: 3 * 3 = 9 ≤ 7 → False. Loop ends. is_prime is still True.
```

Three iterations on paper saved you from bugs that might take 30 minutes of staring at a screen. **Tracing is not optional.** Professional developers do it. It is the fastest way to understand and debug any loop.

### Full Walkthrough: Password Lockout System

Let us apply all five steps to a real problem.

**Problem:** "Write a program that asks for a password. If the user gets it wrong, let them try again. But after 3 failed attempts, lock them out."

**Step 1 — Recognize the loop:** "Try again" = repetition. "After 3 attempts" = a stopping condition. This is a while loop.

**Step 2 — Four questions:**
1. Where do I start? `attempts = 0`, `max_attempts = 3`, `password = "secret123"`
2. When do I stop? When they get it right OR when they run out of attempts.
3. What happens each time? Ask for input, check it.
4. What changes? `attempts` increases by 1.

**Step 3 — Inside vs outside:**
- Outside: `attempts`, `max_attempts`, `password` (persist across iterations)
- Inside: `user_input` (fresh each iteration), the check, the attempt counter update
- After: print whether they got in or got locked out

**Step 4 — One iteration first:**

```python
user_input = input("Enter password: ")
if user_input == password:
    print("Access granted!")
```

**Step 5 — Wrap it and trace:**

```python
password = "secret123"
max_attempts = 3
attempts = 0

while attempts < max_attempts:
    user_input = input("Enter password: ")
    attempts += 1
    
    if user_input == password:
        print("Access granted!")
        break
    
    remaining = max_attempts - attempts
    if remaining > 0:
        print(f"Wrong password. {remaining} attempts remaining.")
else:
    print("Account locked. Too many failed attempts.")
```

Trace with wrong, wrong, correct:

```
attempts = 0: 0 < 3 → True. Input: "abc". attempts = 1. Wrong. 2 remaining.
attempts = 1: 1 < 3 → True. Input: "xyz". attempts = 2. Wrong. 1 remaining.
attempts = 2: 2 < 3 → True. Input: "secret123". attempts = 3. Correct! break.
else block skipped (break was hit).
```

Trace with wrong, wrong, wrong:

```
attempts = 0: 0 < 3 → True. Input: "abc". attempts = 1. Wrong. 2 remaining.
attempts = 1: 1 < 3 → True. Input: "xyz". attempts = 2. Wrong. 1 remaining.
attempts = 2: 2 < 3 → True. Input: "123". attempts = 3. Wrong. 0 remaining.
attempts = 3: 3 < 3 → False. Loop ends normally. else block runs: "Account locked."
```

This walkthrough used every pattern from this part — the three-part structure, `break`, `continue` (we did not need it here — knowing when **not** to use a tool matters too), `while-else`, the accumulator (counting attempts), and the sentinel concept (password is the sentinel). More importantly, it showed the **thinking process** — how to go from a problem statement to working code, step by step.

---

## The Collatz Conjecture — When a Simple Loop Becomes an Unsolved Mystery

You have now written while loops that clearly terminate (the condition eventually becomes `False`) and loops that clearly run forever (`while True` with no `break`). But what about a loop where **nobody knows** if it always terminates?

### The Rules

Pick any positive integer. If it is even, divide it by 2. If it is odd, multiply by 3 and add 1. Repeat. The conjecture says: **no matter what number you start with, you will always eventually reach 1.**

```python
n = int(input("Enter a positive integer: "))
steps = 0

while n != 1:
    if n % 2 == 0:
        n = n // 2
    else:
        n = 3 * n + 1
    steps += 1
    print(n, end=" → ")

print(f"\nReached 1 in {steps} steps")
```

Try it with 7:

```
22 → 11 → 34 → 17 → 52 → 26 → 13 → 40 → 20 → 10 → 5 → 16 → 8 → 4 → 2 → 1 →
Reached 1 in 16 steps
```

### Why This Matters

This is not a toy problem. It is one of the most famous **unsolved problems in mathematics**, studied since 1937. The legendary mathematician Paul Erdős said about it: *"Mathematics is not yet ready for such problems."*

Here is what we know:
- Every number up to approximately **2.95 × 10²⁰** (295 quintillion) has been tested by computers. They all reach 1.
- No one has found a counterexample.
- **No one has proven it always works.**

Think about that. The code is 6 lines. A child could follow the rules. Yet the greatest mathematicians alive cannot prove the loop always reaches 1. In fact, Alan Turing proved in 1936 that there is **no general method** to determine whether any given loop will halt or run forever — a result called the Halting Problem. The Collatz Conjecture is that idea made real: a simple while loop, and we genuinely do not know if it halts for every possible input.

### What This Teaches You About Loops

1. **Simple code can have complex behavior.** The Collatz sequence for 27 takes 111 steps and reaches a peak of 9,232 before eventually falling to 1. A loop's behavior is not always obvious from its code.
2. **Testing is not proof.** 295 quintillion successful tests, and we still cannot say "always." This is why understanding your loop's logic matters more than just running it a few times.
3. **While loops model open-ended processes.** This is fundamentally a while loop problem — you do not know in advance how many steps it takes. A for loop cannot express this naturally.

---

## Retry with Backoff — A Pattern Used Everywhere

When your code talks to external systems (APIs, databases, networks), things fail. The professional pattern is not to give up on the first failure — it is to **retry with increasing delays**:

```python
import time

max_retries = 5
attempt = 0
wait_time = 1

while attempt < max_retries:
    attempt += 1
    print(f"Attempt {attempt}...")
    
    success = attempt == 4  # Simulating: fails 3 times, succeeds on 4th
    
    if success:
        print("Success!")
        break
    
    if attempt < max_retries:
        print(f"Failed. Retrying in {wait_time} seconds...")
        time.sleep(wait_time)
        wait_time *= 2  # Double the wait each time: 1s, 2s, 4s, 8s...
else:
    print("All retries exhausted. Giving up.")
```

Output:

```
Attempt 1...
Failed. Retrying in 1 seconds...
Attempt 2...
Failed. Retrying in 2 seconds...
Attempt 3...
Failed. Retrying in 4 seconds...
Attempt 4...
Success!
```

This is called **exponential backoff**. The wait time doubles each time: 1 second, 2 seconds, 4 seconds, 8 seconds. This is not a textbook exercise — it is used in production at every major tech company. AWS, Google Cloud, and Stripe all recommend this pattern in their API documentation. When thousands of clients hit a server simultaneously and all fail, exponential backoff prevents them from all retrying at the same time and crashing the server again.

Notice this example also uses `while-else` — the `else` block runs only when all retries are exhausted without success (no `break`). This is one of the best real-world uses of Python's `while-else`.

---

## Debugging Loops

When a loop does not behave as expected:

1. **Print the state** at the start of each iteration:

```python
i = 0
while i < 5:
    print(f"DEBUG: i = {i}")   # Temporary debug line
    # ... rest of loop
    i += 1
```

2. **Ask three questions:**
   - Is the initialization correct?
   - Is the condition ever becoming `False`?
   - Is the update changing the right variable?

3. **Check for off-by-one errors:** Does the loop run one too many or one too few times?

```python
# Runs 5 times: 0, 1, 2, 3, 4
i = 0
while i < 5:
    i += 1

# Runs 5 times: 1, 2, 3, 4, 5
i = 1
while i <= 5:
    i += 1
```

---

## Where This Applies in Real Work

- **Retry mechanisms:** API calls that fail are retried with exponential backoff — the exact pattern you learned above. Every cloud SDK (AWS, GCP, Azure) implements this.
- **Server event loops:** Web servers (Django, FastAPI, Flask) run in an infinite loop listening for HTTP requests. Each request is processed in one iteration.
- **User input handling:** CLI tools and interactive programs use sentinel loops to accept commands until the user quits.
- **Data processing:** Reading data line by line from a file or stream until there is no more data.
- **Polling:** Checking the status of a task repeatedly until it is complete (deployment status, CI/CD pipeline progress, long-running job completion).
- **Game loops:** Every video game has a while loop at its core — read input, update state, render frame, repeat. This "game loop" runs 30–60 times per second.
- **Authentication and security:** Login systems with attempt limits, CAPTCHA retry flows, and session timeouts — all while loops with counters.

---

## Practice Assignments

### Assignment 1: Number Guessing Game

Build a number guessing game:

1. Set a secret number (hardcode it, e.g., `secret = 42`)
2. Ask the user to guess the number
3. If the guess is too high, print "Too high!"
4. If the guess is too low, print "Too low!"
5. If correct, print "Correct!" and the number of attempts
6. If the user types "quit", exit the game
7. Validate that the input is a number before comparing

Example session:

```
Guess the number: 50
Too high!
Guess the number: 30
Too low!
Guess the number: 42
Correct! You got it in 3 attempts.
```

### Assignment 2: Collatz Explorer

Build a Collatz sequence explorer:

1. Ask the user for a positive integer
2. Print the full Collatz sequence until it reaches 1
3. Print the total number of steps and the highest number the sequence reached
4. After finishing, ask if the user wants to try another number (use a sentinel loop)
5. Validate the input — reject non-integers, zero, and negative numbers

Example session:

```
Enter a positive integer (or 'quit'): 27
27 → 82 → 41 → 124 → 62 → 31 → ... → 4 → 2 → 1
Steps: 111
Peak value: 9232

Enter a positive integer (or 'quit'): quit
Goodbye!
```

This assignment combines: while loops, the accumulator pattern, sentinel loop pattern, input validation, and conditionals.

### Assignment 3: Simple Calculator with Retry

Build a calculator that:

1. Runs in a loop — keeps accepting calculations until the user types "quit"
2. Accepts input in the format: `number operator number` (e.g., `10 + 5`)
3. Supports `+`, `-`, `*`, `/`
4. Handles division by zero gracefully
5. If the input format is invalid, print an error and let the user try again (do not crash)

This assignment uses: sentinel loop, `break`, `continue`, input validation, and conditionals from Parts 13–14.

Save all as separate files in `src/`.

---

> **Next:** Part 16 — For Loops. A cleaner, safer way to iterate. For loops are the foundation of data processing and the most commonly used loop in Python.
