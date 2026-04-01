# Part 6.1 — Memory: Stack and Heap

## Connecting to Part 6

In Part 6, we followed `x = 10` through the entire execution pipeline:

```
Source Code → Tokens → AST → Bytecode → PVM executes
```

We saw the bytecode:

```
LOAD_SMALL_INT   10
STORE_NAME       0 (x)
```

We said the PVM reads these instructions and executes them. The PVM picks up `LOAD_SMALL_INT 10` — it loads the value 10. Then `STORE_NAME x` — it stores it with the name x.

But — **stores it WHERE?** Where in your computer is the value `10` sitting right now? Where is the name `x` sitting? Are they in the same place? Are they in different places?

Is the data on your **hard disk**? Is it in the **CPU**? Is it somewhere else entirely?

---

## Where Does Data Live When a Program Runs?

Not on the hard disk. The hard disk is for permanent storage — files, photos, videos. When a program is **running** — actively doing work — it does not operate from the hard disk. That would be too slow.

Not in the CPU. The CPU is the processor — it executes instructions, but it does not store your program's data long-term.

The data lives in **RAM** — your computer's working memory.

Think of it like this:

- **Hard disk** = bookshelf. Stores everything permanently. Large but slow.
- **RAM** = your desk. Where the active work happens. Smaller but fast.
- **CPU** = your brain. Processes things, but does not store them.

When you want to read a book, you take it off the shelf (hard disk) and place it on your desk (RAM). Now it is right in front of you — fast and accessible. When you are done, you put it back on the shelf.

---

## When Does This Happen?

**Not when you save the file.** When you save `example.py`, it is just a text file sitting on your hard disk. Nothing is running. No memory is used. It is like writing a recipe on paper — the recipe exists, but nobody is cooking.

**It happens when you run the program.** The moment you type `python3 main.py` and press Enter — that is when the OS loads the Python interpreter into RAM and gives it memory to work with.

```
Save file           → nothing happens in memory (just text on disk)
Run python3 main.py → OS loads program into RAM, execution begins
```

---

## Programs Use RAM — All of Them

Right now, your computer is running many programs — VS Code, Chrome, Spotify, maybe a terminal. **Every single one of them is sitting in RAM.**

Even if Chrome is open with a blank tab and you are doing nothing — Chrome is occupying RAM. It is a book placed on your desk. Even if you are not reading it, it is taking up desk space.

That is why your computer slows down when you open too many programs. Your desk (RAM) is full. There is no space left.

Your operating system gives each program its own portion of RAM. When you run `python3 main.py`, your Python program gets its own portion too — just like Chrome or VS Code. It is no different.

---

## What Is RAM Really?

So we know data lives in RAM. But here is the next question — **how is RAM organized?**

When you buy a 8GB or 16GB or 32GB RAM stick, every byte of it is identical. There is no "stack section" or "heap section" built into the hardware. RAM is just a flat block of memory — billions of storage slots, one after another. No labels. No divisions. All identical.

So if RAM is just a flat, blank block — **how does your program organize it?** How does it know where to put the name `x` and where to put the value `10`?

**Stack and heap are not hardware divisions. They are created by software.**

Think of it like buying a blank notebook (RAM) and deciding "pages 1–50 are for quick notes, pages 51–200 are for detailed work." The notebook itself does not know the difference — you decided how to use it. RAM is that notebook. Stack and heap are the sections.

---

## Who Creates the Stack and Heap?

| Who | What They Do |
|-----|-------------|
| **OS** | Sets up the **stack** automatically when the program starts |
| **OS** | Gives memory when the program requests it (this becomes the **heap**) |
| **CPython** | Requests memory from OS when it needs to create data |
| **CPython** | Manages that memory internally — decides where to put data, tracks what is in use, runs garbage collection |

The OS is like the **building owner**. When a company (your Python program) moves in, the building owner gives them a small fixed reception area (stack) automatically. When the company needs workspace, they ask the building owner for rooms. The building owner provides them. But how the company arranges desks and chairs inside — that is the company's business.

```
Hardware:    RAM = flat block of bytes (no division)
                      ↓
OS:          Gives stack automatically + gives heap memory on request
                      ↓
Program:     Each program gets: Stack (small, fixed) + Heap (large, flexible)
                      ↓
Python:      CPython uses C's stack/heap, then manages its own data on the heap
```

---

## The IT Company Analogy

To understand stack and heap, think of an IT company building:

```
IT Company Building = Your program's portion of RAM

  ┌─────────────────────────────────────────────────┐
  │                                                 │
  │   OFFICE FLOORS (Heap)                          │
  │   ┌──────────────────────────────────────────┐  │
  │   │  Large, flexible workspace               │  │
  │   │  Employees sit wherever there is space    │  │
  │   │  Actual work happens here                 │  │
  │   │  New employees join, some leave           │  │
  │   │  Cleanup crew removes empty desks         │  │
  │   └──────────────────────────────────────────┘  │
  │                                                 │
  │   RECEPTION DESK (Stack)                        │
  │   ┌──────────────────────────────────────────┐  │
  │   │  Small, organized, fast                  │  │
  │   │  Tracks names and locations              │  │
  │   │  Register: "x → 4th floor, Desk 12"     │  │
  │   │  Does not do any work — just tracking    │  │
  │   └──────────────────────────────────────────┘  │
  │                                                 │
  │   HR PERSON (PVM)                               │
  │   ┌──────────────────────────────────────────┐  │
  │   │  Reads the task list (bytecode)          │  │
  │   │  Escorts employees to desks (heap)       │  │
  │   │  Registers names at reception (stack)    │  │
  │   │  The only active person doing the work   │  │
  │   └──────────────────────────────────────────┘  │
  │                                                 │
  └─────────────────────────────────────────────────┘
```

This analogy maps throughout the rest of this part.

---

## Stack

The stack is the **reception desk** of your program — small, fast, and organized.

It tracks:

- Which function is currently running
- The order of function calls
- The **names** you create — like `x`, `y`, `total`

The reception desk does not do any actual work. It does not build software. It does not store data. It just **tracks** — who came in, what their name is, and where they are sitting.

The stack is usually **1–8 MB** in size. It does not grow dynamically. It is fixed — because it is just a tracking register, not a workspace.

---

## Heap

The heap is the **office workspace** — large, flexible, and where all actual data lives.

It stores:

- All the actual values your program creates — numbers, text, everything
- Any data your program produces during execution

When your program creates data, it goes into the heap wherever there is space — like a new employee being assigned a desk on one of the office floors. A cleanup crew (**garbage collector**) comes periodically to remove desks that nobody is using anymore.

The heap can grow as needed — it is only limited by your total RAM.

---

## Stack vs Heap — Same RAM, Different Purpose

|                    | Stack                            | Heap                          |
| ------------------ | -------------------------------- | ----------------------------- |
| Same physical RAM? | Yes                              | Yes                           |
| Size               | Small, fixed (1–8 MB)            | Large, grows as needed        |
| Speed              | Very fast (organized)            | Slower (flexible)             |
| Managed by         | OS sets it up automatically      | Program requests memory from OS |
| What goes here     | Names, function call tracking    | Actual values and data        |
| Analogy            | Reception desk                   | Office workspace              |

---

## What Happens When You Write `x = 10`

Two things happen, **in a specific order**. The order matters.

### Step 1 — The value is created in the heap FIRST

The PVM (the HR person) reads the bytecode instruction `LOAD_SMALL_INT 10`. It creates the value `10` in the **heap** — wherever there is space. Now the value exists and has an address (a desk number).

The PVM holds that address temporarily — like writing it on a sticky note.

### Step 2 — The name is registered on the stack SECOND

The PVM reads the next instruction `STORE_NAME x`. It goes to the **stack**, creates the name `x`, and attaches the address (the sticky note) to it. Now `x` on the stack has an arrow pointing to where `10` lives in the heap.

```
   STACK (reception desk)       HEAP (office workspace)
  ┌──────────────────┐        ┌──────────────────────┐
  │  x  ─────────────────────▶│  the value: 10       │
  └──────────────────┘        └──────────────────────┘
  (the name)                  (the actual data)
  registered SECOND           created FIRST
```

### Why This Order?

Can the receptionist register a name and point to a desk **before** someone is sitting at that desk? No. The value must exist first so that the name has somewhere to point.

The bytecode proves this order:

```
LOAD_SMALL_INT  10      ← Step 1: create the value (heap)
STORE_NAME      0 (x)   ← Step 2: register the name (stack)
```

### The PVM Is the Middleman

The value `10` does not go anywhere by itself. The name `x` does not appear on its own. The **PVM does all the work** — it is the only active entity:

```
Bytecode (task list)              PVM (the HR person)
┌─────────────────────┐
│ 1. LOAD_SMALL_INT 10│  ───▶   PVM creates value 10 in heap,
│                     │          gets the address, holds it
│                     │
│ 2. STORE_NAME x     │  ───▶   PVM goes to stack, registers
│                     │          name "x", attaches the address
└─────────────────────┘
```

The bytecode is just a task list — passive, written on paper. The PVM is the person who reads that task list and does the actual work in memory.

### Plain Language → Formal Terms

The **value** sitting in the heap — Python calls it an **object**. Every piece of data Python creates is an object. What exactly an object is, what properties it has — we will go deep in Part 7.

The **name** `x` on the stack — most people call it a "variable." But it does not work like a box holding a value. It holds an **arrow** pointing to a value. We will break the "variable is a box" myth completely in Part 7.

For now: **names on the stack, values in the heap, arrows connecting them.**

---

## What Happens When You Run `python3 main.py`

```
You type: python3 main.py  →  Press Enter
                                    │
                        OS loads CPython into RAM
                        OS gives it a stack (automatic, fixed)
                                    │
                        CPython reads main.py from disk
                        CPython tokenizes → parses → compiles to bytecode
                                    │
                        PVM starts executing bytecode
                                    │
                        Hits "x = 10"
                        PVM creates value 10 in heap (requests memory from OS)
                        PVM registers name "x" on stack, pointing to 10
                                    │
                        Program finishes
                        All memory freed back to OS
```

---

## What Happens When the Program Ends?

When your program finishes execution, **everything is destroyed**. The OS takes back all the memory — both stack and heap. Every name, every value, every arrow — gone.

It is like the IT company closing for the day — reception clears the register, employees leave, desks are emptied. The next morning (next program run), everything starts fresh. Nothing carries over.

```
Run 1:  python3 main.py  →  x = 10 created  →  program ends  →  ALL memory freed
Run 2:  python3 main.py  →  starts fresh, x does not exist, nothing from Run 1 remains
```

This is why if you run a program, set `x = 10`, and then run it again — `x` does not have the value `10` from last time. The entire memory was freed between runs.

---

## Step-by-Step: How Memory Changes

### Step 1: `x = 10`

```python
x = 10
print(f"x = {x}")
print(f"id(x) = {id(x)}")
```

Output:

```
x = 10
id(x) = 4392513792
```

One name on the stack, one value in the heap, one arrow. The `id()` is the desk number — where the value 10 is sitting in the heap.

```
  STACK                     HEAP
 ┌──────┐                ┌────────────┐
 │  x  ────────────────▶ │  value: 10 │  (desk 4392513792)
 └──────┘                └────────────┘
```

---

### Step 2: `y = x`

```python
y = x
print(f"x = {x}")
print(f"y = {y}")
print(f"id(x) = {id(x)}")
print(f"id(y) = {id(y)}")
print(f"Same id? {id(x) == id(y)}")
```

Output:

```
x = 10
y = 10
id(x) = 4392513792
id(y) = 4392513792
Same id? True
```

`y` points to the **same value** — no new value is created. Two names, one value. Same desk number proves it.

```
  STACK                     HEAP
 ┌──────┐                ┌────────────┐
 │  x  ────────────────▶ │  value: 10 │  (desk 4392513792)
 │  y  ────────────────▶ │            │
 └──────┘                └────────────┘
 Two names                Same desk
```

---

### Step 3: `x = 20`

```python
x = 20
print(f"x = {x}")
print(f"y = {y}")
print(f"id(x) = {id(x)}")
print(f"id(y) = {id(y)}")
print(f"Same id? {id(x) == id(y)}")
```

Output:

```
x = 20
y = 10
id(x) = 4392514112
id(y) = 4392513792
Same id? False
```

A **new** value `20` is created in the heap at a new desk. `x` is repointed to the new value. `y` is untouched — still points to the original `10` at the original desk.

```
  STACK                     HEAP
 ┌──────┐                ┌────────────┐
 │  x  ────────────────▶ │  value: 20 │  (desk 4392514112) ← new
 │      │                └────────────┘
 │  y  ──────────┐       ┌────────────┐
 └──────┘        └──────▶│  value: 10 │  (desk 4392513792) ← unchanged
                         └────────────┘
```

Reassignment does not change the old value. It creates a new value and moves the arrow. The old value stays untouched.

---

## What `id()` Returns

`id()` returns the **memory address** — the location of the value in the heap. Think of it as the **desk number** in the office.

```python
x = 10
print(id(x))   # 4345618128 — this is the desk number where 10 is sitting
```

When two names show the same `id()`, they are pointing to the **same desk** — the same value in the heap. When the IDs are different, they are pointing to **different desks** — different values.

---

## Garbage Collection

When a value in the heap has **no names pointing to it**, it becomes an orphan — sitting in memory, taking up space, but nobody can access it.

```python
x = 10    # x points to 10
x = 20    # x now points to 20 — nobody points to 10 anymore
```

```
  STACK                     HEAP
 ┌──────┐                ┌────────────┐
 │  x  ────────────────▶ │  value: 20 │
 └──────┘                └────────────┘
                          ┌────────────┐
               nobody ──▶ │  value: 10 │  ← orphan, no arrows pointing here
                          └────────────┘
```

The **garbage collector** periodically checks the heap: "Does anyone still point to this value? No? Then I will free up that space." The orphaned value is cleaned up. The memory becomes available again.

In our IT company analogy — it is the cleanup crew walking through the office floors, finding empty desks that no one is assigned to, and clearing them out.

---

## Stack Overflow — The Name You Already Know

You have probably heard of a website called **Stack Overflow**. That name comes from a real programming error.

The stack is small — 1 to 8 MB, fixed. It does not grow. When there are too many function calls piling onto the stack — one calling another calling another, endlessly — the stack runs out of space. That is a **stack overflow**. The stack literally overflows.

In Python, you will see this as a `RecursionError: maximum recursion depth exceeded`. We will see exactly how this happens when we learn functions and recursion. But now you know where the name comes from.

---

## Tracebacks and the Call Stack

When an application crashes, you see a **traceback** — a list of function calls that led to the error.

```
Traceback (most recent call last):
  File "main.py", line 5, in <module>
    result = calculate(data)
  File "utils.py", line 12, in calculate
    return value / count
ZeroDivisionError: division by zero
```

This traceback is showing you the **call stack** — the stack we just discussed. It tells you:

- Which file the error occurred in
- Which line
- Which function
- What the error was

It is like the reception desk at our IT company. If there is a problem, reception can tell you exactly who entered, in what order, and where each person went. The traceback is the stack's record of what happened.

Developers who understand the call stack read tracebacks and find bugs in minutes. Developers who do not understand it stare at error messages and feel lost.

---

## Where This Applies in Real Work

- **Debugging production errors** — understanding the call stack and traceback saves hours of investigation
- **Performance optimization** — knowing that Python creates data on the heap explains why memory usage grows with large datasets, and why you need tools like generators for memory-efficient processing
- **Memory efficiency** — understanding stack vs heap explains why local variables are fast and why global state should be minimized
- **DSA foundation** — every data structure is about how data is organized in the heap. Every recursive function call adds to the stack. Stack overflow is literally the stack running out of space. If you understand stack and heap, DSA stops being abstract.

---

## Stack and Heap Are Universal

Stack and heap are **not** Python concepts. They are **computer science** concepts that have existed since the 1950s–60s.

| Language   | Execution Engine | Stack and Heap? |
|------------|-----------------|-----------------|
| Python     | PVM             | Yes — same model |
| Java       | JVM             | Yes — same model |
| C#         | CLR             | Yes — same model |
| JavaScript | V8 / SpiderMonkey | Yes — same model |
| C / C++    | No VM — compiles to machine code | Yes — **still the same model** |
| Rust       | No VM — compiles to machine code | Yes — **still the same model** |

Every program that runs on a computer with RAM and an OS uses a stack and a heap. The specific implementations differ, but the core concept is identical.

What you learned here is not just how Python works. It is how **programs** work. This knowledge transfers to every language you will ever use.

---

## Practice Assignment

1. Open the Python REPL and run:

```python
x = 10
print(id(x))

y = x
print(id(y))
```

2. Both IDs are the same — `x` and `y` are two names on the stack, both pointing to the same value `10` in the heap. Same desk number.

3. Now try:

```python
x = 20
print(id(x))
print(id(y))
```

4. The IDs are now different — `x` was repointed to a new value `20` in the heap, but `y` still points to the original `10`. This proves that reassignment creates a new value, it does not change the old one.

5. Draw the stack and heap diagrams for each step on paper. Verify your diagrams match the `id()` output.

---

> **Next:** Part 7 — Variables, Names, and Objects. The "variable is a box" myth is wrong, and understanding the truth prevents the most common Python bugs.
