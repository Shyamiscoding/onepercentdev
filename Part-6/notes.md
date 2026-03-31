# Part 6 — How Python Actually Runs Your Code

## Why You Need to Know This

Let me be honest with you.

Most Python developers have no idea what happens when they run their code. They type `python main.py`, something happens in the background, output appears — and they move on. They treat Python like a black box.

And that works — until it doesn't.

When your application crashes in production at 2 AM, AI tools like ChatGPT will give you generic suggestions. But if **you** understand how Python actually executes code — how it reads, parses, compiles, manages memory — you can look at the traceback and pinpoint the problem in minutes. You are not guessing. You know exactly where to look.

Here is the real difference in the AI era: AI can write code. AI can explain syntax. But AI cannot understand **your system**. It does not know how your code flows through the interpreter, how your objects sit in memory, why a specific function call failed. That understanding is yours — and it is the one thing that makes you irreplaceable.

When you understand Python's internals, you do not just use AI — you **guide** AI. You ask precise questions. You evaluate its suggestions with real knowledge. You become the developer who controls AI, not the one who depends on it blindly.

This is rare knowledge. Most developers never learn this. And that is exactly why it is valuable.

---

## The Question Most Developers Cannot Answer

When you type:

```bash
python main.py
```

What actually happens?

Most developers — even those with years of experience — say "Python runs the code." But that answer tells you nothing.

Python parses the text into an internal structure called an **Abstract Syntax Tree (AST)** — a structured representation of your code that Python can understand and work with. You never see this step. It happens automatically.Understanding what happens between pressing Enter and seeing output is what separates surface-level knowledge from real understanding.

---

## The Execution Pipeline

When you run a Python file, these steps happen in order:

```
┌─────────────────┐     ┌───────────────────┐     ┌──────────────────┐
│  Source Code     │────▶│  Lexing           │────▶│  Parsing         │
│  (.py file)      │     │  (Tokenization)   │     │  (AST)           │
└─────────────────┘     └───────────────────┘     └──────────────────┘
                                                           │
                        ┌───────────────────┐              │
                        │  Output           │              ▼
                        │  (Result)         │     ┌──────────────────┐
                        └───────────────────┘     │  Compilation     │
                                 ▲                │  (Bytecode)      │
                                 │                └──────────────────┘
                        ┌───────────────────┐              │
                        │  Python Virtual   │              │
                        │  Machine (PVM)    │◀─────────────┘
                        └───────────────────┘
```

### Step 1 — Python Reads Your Source Code

Python opens the `.py` file and reads the text you wrote. At this point, it is just text — characters in a file.

### Step 2 — Lexing (Tokenization)

Before Python can understand your code, it first breaks the raw text into small meaningful pieces called **tokens**. This step is called **lexing** (or tokenization).

When Python reads `x = 10`, it sees it as one long string of characters: `x`, ` `, `=`, ` `, `1`, `0`. Lexing splits it into individual tokens:

```
x    →  NAME (variable name)
=    →  OP (operator)
10   →  NUMBER (integer)
```

Each token is the smallest meaningful unit — a name, a symbol, a number. Think of it like breaking a sentence into individual words before you can understand the grammar.

You can see tokenization yourself using Python's built-in `tokenize` module:

```python
import tokenize
import io
tokens = tokenize.generate_tokens(io.StringIO("x = 10").readline)
for tok in tokens:
    print(tok)
```

You will see tokens for `x` (NAME), `=` (OP), `10` (NUMBER), and special tokens for newline and end-of-file.

### Step 3 — Parsing

Once Python has the tokens, it structures them into an **Abstract Syntax Tree (AST)** — a tree that represents the meaning of your code. Lexing gave Python the individual words. Parsing figures out the grammar — how those words relate to each other.

For `x = 10`, parsing understands: "this is an assignment, the left side is a variable name called x, the right side is the number 10."

Think of it like reading English. The sentence "Put the book on the table" — first you identify each word (lexing), then you understand the grammar: verb (put), object (book), location (table). Only then can you act. Python works the same way.

This step is also where **syntax errors** are caught. If you write `x = = 10`, Python catches it here — the structure does not make sense. It never reaches bytecode or execution.

The CPython parser — the actual code that does this parsing — is written in C:

[https://github.com/python/cpython/blob/main/Parser/parser.c](https://github.com/python/cpython/blob/main/Parser/parser.c)

### Seeing the AST with the ast Module

Python has a built-in `ast` module that lets you see this parsed structure yourself.

Open the REPL and try:

```python
import ast
tree = ast.parse("x = 10")
print(ast.dump(tree, indent=2))
```

Output:

```
Module(
  body=[
    Assign(
      targets=[
        Name(id='x', ctx=Store())],
      value=Constant(value=10))],
  type_ignores=[])
```

Look at what Python understood from your simple line `x = 10`:

- The whole thing is an `Assign` statement
- The target is a `Name` with id `'x'` — that is your variable name
- The value is a `Constant` with value `10` — that is the number you assigned
- `ctx=Store()` means Python knows it needs to **store** a value into this name

Your one line `x = 10` became a structured tree. This tree is what gets compiled into bytecode in the next step.

You do not need to memorize AST structures. The point is simple — Python does not run your text directly. It first understands the structure of what you wrote, then compiles that structure into bytecode.

### Step 4 — Compilation to Bytecode

Python compiles the parsed structure into **bytecode**.

Bytecode is:

- A lower-level representation of your code
- Not machine code (not 0s and 1s)
- Not human readable
- An intermediate instruction set that the Python engine can execute

This compilation happens automatically. You do not run a separate compile step.

### Why Bytecode? Why Not Compile Directly to Machine Code?

If Python compiled directly to machine code — like C does — your compiled program would only work on one specific type of processor. Code compiled for an Intel CPU would not run on an Apple Silicon chip. Code compiled for Windows would not work on Linux. You would need to compile separately for every platform.

Bytecode solves this. Bytecode is **platform-independent** — it is the same no matter what computer you are on. The same `.pyc` file works on Mac, Windows, and Linux. What changes is the Python Virtual Machine (PVM) on each system — the PVM is built specifically for that platform and knows how to execute the bytecode on that hardware.

This is the tradeoff Python makes: bytecode is slower than machine code (because the PVM still has to translate it at runtime), but you get **portability**. You write your code once, and it runs everywhere Python is installed. That is why you can write a script on your Mac and send it to someone on Windows, and it just works.

You may notice `__pycache__/` folders appearing in your project. Those contain `.pyc` files — cached bytecode. Python saves these so it does not have to recompile unchanged files every time.

### Step 5 — Python Virtual Machine (PVM) Executes Bytecode

The **Python Virtual Machine** reads the bytecode instructions one by one and executes them.

### What Is the PVM Really?

The name "Virtual Machine" sounds like something big — like VirtualBox or VMware, a whole computer running inside another computer. But the PVM is nothing like that.

The PVM is simply a **loop inside the CPython program**. When you installed Python, you got a C program (the interpreter). Inside that C program, there is a loop that does this:

1. Pick up the next bytecode instruction
2. Figure out what it means
3. Do the operation
4. Move to the next instruction
5. Repeat until done

That loop **is** the PVM. It is not a separate application. It is not a separate environment. It does not create a "space" or a "container." It is just a piece of C code running inside the Python interpreter.

It is called a "virtual machine" because it behaves like a computer — but in software. A real machine (your CPU) reads machine code instructions and executes them. The PVM reads bytecode instructions and executes them. It does the same job as a CPU, but it is implemented in software instead of hardware. That is why it is **virtual**.

The PVM also:

- Manages memory
- Handles function calls
- Tracks execution order

The actual PVM loop lives in this file in CPython's source code:

[https://github.com/python/cpython/blob/main/Python/ceval.c](https://github.com/python/cpython/blob/main/Python/ceval.c)

### Step 6 — Output

The result of execution is sent to the screen (or wherever the program directs it).

---

## Why Python Is Called "Interpreted"

### First — What Does "Interpreted" Mean?

In a **compiled** language like C, you write code, then run a separate compiler program that translates your entire code into machine code (binary). That compiled file is saved on disk. Then you run that compiled file, and the CPU executes it directly. The compiler is done before your program starts. The compiler and the execution are two completely separate steps.

In an **interpreted** language, there is no separate compilation step. Another program — the **interpreter** — reads your code and executes it. The interpreter is always present during execution. You never get a standalone compiled file. You always need the interpreter to run your code.

That is why when you run Python, you always type `python main.py` — you are telling the Python interpreter to read and execute your file. Without the interpreter, your `.py` file is just text. It cannot run on its own.

### Why Python Is Called Interpreted — But It Is Not the Full Picture

Python is called interpreted because from the developer's perspective, that is what it looks like. You type `python main.py` and it runs. No separate compile step. No compiled file you run later. It feels interpreted.

But now you know the truth — Python **does** compile. It compiles to bytecode. Then the PVM interprets that bytecode. So Python is actually a hybrid — it compiles first, then interprets. The compilation just happens silently and automatically, so you never see it.


| Language | What Happens                             | Who Runs the Code          |
| -------- | ---------------------------------------- | -------------------------- |
| C        | Compiles to machine code (separate step) | CPU runs it directly       |
| Java     | Compiles to bytecode (separate step)     | JVM interprets/executes it |
| Python   | Compiles to bytecode (automatic, hidden) | PVM interprets/executes it |


Python's process is actually closer to Java's than to C's. Both compile to bytecode and run on a virtual machine. The difference is that Java makes you compile explicitly (`javac`), while Python does it silently behind the scenes.

So the next time someone says "Python is interpreted" — they are not wrong, but they are only seeing the surface. The full picture is: **Python compiles to bytecode, then the PVM interprets that bytecode.**

---

## Seeing Bytecode with the dis Module

Python has a built-in module called `dis` (disassemble) that lets you see the bytecode instructions.

Open the REPL and try:

```python
import dis
dis.dis("x = 10")
```

Output (will look similar to):

```
  0           0 RESUME                   0

  1           2 LOAD_CONST               0 (10)
              4 STORE_NAME               0 (x)
              6 RETURN_CONST             1 (None)
```

What this shows:

- `LOAD_CONST 0 (10)` — load the constant value 10
- `STORE_NAME 0 (x)` — store it with the name x

The same `x = 10` you wrote became multiple bytecode instructions. This is what the PVM actually executes — step by step.

You do not need to memorize bytecode instructions. The point is to understand that Python translates your readable code into lower-level instructions before executing them.

---

## The Complete Picture

When you run `python main.py`:

1. The operating system loads the Python interpreter (CPython) into RAM
2. CPython reads your `.py` file from disk
3. It breaks the source code into tokens (lexing)
4. It structures the tokens into an Abstract Syntax Tree (parsing)
5. It compiles the AST into bytecode
6. The Python Virtual Machine executes the bytecode
7. Output is sent to the screen

All of this happens in milliseconds for simple programs.

---

## Where This Applies in Real Work

- **Performance optimization** — knowing that Python compiles to bytecode (not machine code) explains why CPU-heavy loops are slower than in C, and why you use optimized libraries (NumPy, written in C) for heavy computation
- **`__pycache__` management** — understanding bytecode caching explains why stale `.pyc` files sometimes cause confusing behavior, and why you add `__pycache__/` to `.gitignore`
- **Deployment** — when deploying to servers, understanding the interpreter, bytecode, and environment setup prevents mysterious failures

---

## Practice Assignment

Follow `x = 10` through every stage of the pipeline yourself:

1. Open the Python REPL

2. See the **tokens** (lexing step):

```python
import tokenize, io
tokens = tokenize.generate_tokens(io.StringIO("x = 10").readline)
for tok in tokens:
    print(tok)
```

3. See the **AST** (parsing step):

```python
import ast
print(ast.dump(ast.parse("x = 10"), indent=2))
```

4. See the **bytecode** (compilation step):

```python
import dis
dis.dis("x = 10")
```

5. Compare all three — tokens show the **individual pieces**, the AST shows the **structure** Python understood, the bytecode shows the **instructions** it generated from that structure. Same line of code, three different representations.

You do not need to memorize any of this. The goal is to see with your own eyes that `x = 10` goes through multiple transformations before Python actually stores the value. That awareness puts you ahead of most developers.

---

> **Next:** Part 6.1 — Memory: Stack and Heap. When your Python program runs, where does the data actually live? Understanding stack and heap is the key to understanding how variables, objects, and memory work in Python.

