# Part 5 — Your First Python Code

## The Python Interactive Shell (REPL)

Open your terminal and type:

```bash
python
```

(On Mac/Linux, use `python3`)

You will see:

```
>>>
```

This is the **REPL** — Read, Evaluate, Print, Loop.

- **Read** — Python reads what you type
- **Evaluate** — Python executes it
- **Print** — Python shows the result
- **Loop** — Python waits for the next input

The REPL is useful for quick experiments and testing small pieces of code. It is not meant for building applications.

Try this:

```python
>>> 2 + 3
5
>>> "hello"
'hello'
```

To exit the REPL:

```python
>>> exit()
```

---

## print() — Sending Output to the Screen

`print()` is the most basic way to send data from your program to the screen.

```python
print("Hello, World")
```

Output:

```
Hello, World
```

You can print numbers, text, or results of calculations:

```python
print(10)
print(2 + 3)
print("Python is powerful")
```

### Printing Multiple Values

```python
print("Score:", 95)
```

Output:

```
Score: 95
```

Python automatically adds a space between values when you separate them with commas.

### Why print() Matters Beyond Tutorials

`print()` is the simplest debugging tool. In real projects, when something behaves unexpectedly, developers add `print()` statements to check what values variables hold at different points.

Before learning advanced debugging tools, `print()` is your first line of investigation.

---

## input() — Receiving Data from the User

`input()` pauses the program and waits for the user to type something.

```python
name = input("Enter your name: ")
print("Hello,", name)
```

When this runs:

```
Enter your name: Shyam
Hello, Shyam
```

The text inside `input()` is called a **prompt** — it tells the user what to type.

### Important: input() Always Returns a String

Everything that comes from `input()` is a **string** (text), even if the user types a number.

```python
age = input("Enter your age: ")
print(type(age))
```

Output:

```
<class 'str'>
```

Even if you type `25`, Python treats it as the text `"25"`, not the number `25`.

### Converting Input to a Number

To work with numbers from input, convert using `int()` or `float()`:

```python
age = int(input("Enter your age: "))
print(type(age))
```

Output:

```
<class 'int'>
```

Now `age` is an actual number and you can do math with it.

---

## Your First Interactive Program

### Program 1 — Greeting

```python
name = input("What is your name? ")
print("Welcome to OnePercentDev,", name)
```

### Program 2 — Simple Calculator

```python
a = int(input("Enter first number: "))
b = int(input("Enter second number: "))

print("Sum:", a + b)
print("Difference:", a - b)
print("Product:", a * b)
```

This program takes two numbers, performs basic math, and shows the results.

---

## f-strings — Clean Output Formatting

Python provides a clean way to embed values inside strings using **f-strings** (formatted string literals).

```python
name = "Shyam"
age = 28
print(f"My name is {name} and I am {age} years old")
```

Output:

```
My name is Shyam and I am 28 years old
```

The `f` before the quotes tells Python to look for `{}` placeholders and replace them with actual values.

f-strings are the modern, preferred way to format output in Python. You will use them constantly.

---

## The Fundamental Program Model

Every program — from a simple calculator to a complex AI system — follows the same core model:

```
Input → Process → Output
```


| Step    | What Happens                         | Example             |
| ------- | ------------------------------------ | ------------------- |
| Input   | Data comes in                        | User types a number |
| Process | Program does something with the data | Calculate the sum   |
| Output  | Result goes out                      | Print the answer    |


This model applies everywhere:

- A web API receives a request (input), processes it, and returns a response (output)
- An AI model receives text (input), processes it through the model, and generates a response (output)
- A data pipeline reads raw data (input), cleans and transforms it (process), and stores the result (output)

Every system you will ever build follows this pattern. Understanding it now creates a mental framework for everything ahead.

---

## REPL vs Script File

There are two ways to run Python code:

### REPL (Interactive Shell)

- Type `python` in terminal
- Execute code line by line
- Results appear immediately
- Good for quick experiments and testing

### Script File (.py)

- Write code in a file (e.g., `main.py`)
- Run with `python main.py`
- Executes the entire file top to bottom
- Used for real programs and projects

**When to use which:**


| Use Case                      | REPL or Script? |
| ----------------------------- | --------------- |
| Testing a quick calculation   | REPL            |
| Checking how a function works | REPL            |
| Building an actual program    | Script          |
| Working on a project          | Script          |
| Saving your work              | Script          |


In professional work, scripts are the standard. The REPL is a tool for exploration.

---

## Comments

Comments are lines that Python ignores. They are notes for humans reading the code.

```python
# This calculates the user's age
birth_year = int(input("Enter your birth year: "))
current_year = 2026
age = current_year - birth_year
print(f"You are {age} years old")
```

The `#` symbol marks a comment. Everything after `#` on that line is ignored by Python.

Use comments to explain **why** something is done, not **what** is done. The code itself should show what is happening. Comments should explain the reasoning behind decisions.

---

## Where This Applies in Real Work

- `print()` — used daily for quick debugging in development. When a variable has an unexpected value, `print()` is the fastest way to check.
- `input()` — the concept of receiving external data applies to APIs (receiving HTTP requests), reading files, and accepting command-line arguments.
- f-strings — used everywhere: log messages, API responses, error messages, database queries, email templates.
- Input → Process → Output — this is the architecture of every backend service, every data pipeline, and every AI system.

---

## Practice Assignment

Build a program in a file called `about_me.py` that:

1. Asks for the user's name
2. Asks for their birth year
3. Calculates their age (use 2026 as the current year)
4. Prints a formatted message using an f-string:

```
Hello [name], you are [age] years old. Welcome to your 1% developer journey!
```

Save it in your `src/` folder and run it with `python src/about_me.py`.

---

> **Next:** Part 6 — How Python actually runs your code. What happens between typing `python main.py` and seeing the output. 

