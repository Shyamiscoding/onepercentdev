# Part 24 — Functions Part 1 (Foundation)

## Connecting to Parts 17–23

You now have the complete data toolkit: **lists** and **tuples** (Parts 17–19), **sets** (Part 20), **dictionaries** (Parts 21–22), and **comprehensions** to build any of them in a single line (Part 23). You can store data, look it up instantly, count things, group things, and ship data as JSON.

But look at every program you have written so far — it runs **top to bottom**, one long script. The DMart catalog? One script. The contact book? One script. Everything lives in one continuous flow. That works for 30-line exercises. It does not work for a 5,000-line backend or a team of five developers working on the same codebase.

This part introduces the tool that fixes that: **functions**. Functions let you take any piece of logic, give it a name, and reuse it from anywhere. Every method you have already called — `.append()`, `.get()`, `.items()`, `len()`, `print()` — is a function someone wrote and named so you could use it without knowing how it works inside. Now you learn to write your own.

---

## Two Ways to Organize Code

You now know data types, loops, and conditionals — the raw building blocks. But as programs grow bigger, you need a way to **organize** your code. Let us see the problem first.

### Without Functions — The Problem

Imagine you are building a simple banking app. Three customers deposit money:

```python
# Customer 1
balance1 = 1000
balance1 = balance1 + 500
print(f"Shyam: {balance1}")    # Shyam: 1500

# Customer 2
balance2 = 2000
balance2 = balance2 + 300
print(f"Priya: {balance2}")    # Priya: 2300

# Customer 3
balance3 = 500
balance3 = balance3 + 1000
print(f"Ravi: {balance3}")     # Ravi: 1500
```

Three customers, and you have already copy-pasted the same deposit logic three times. Now imagine 1,000 customers. Or imagine the bank adds a rule — every deposit above 10,000 needs a tax deduction. You would have to find and fix every single copy. This does not scale.

### With Functions — Procedural Programming

Now wrap that logic in a function. Write once, call anywhere:

```python
def deposit(balance, amount):
    return balance + amount

balance1 = deposit(1000, 500)
balance2 = deposit(2000, 300)
balance3 = deposit(500, 1000)

print(f"Shyam: {balance1}")   # Shyam: 1500
print(f"Priya: {balance2}")   # Priya: 2300
print(f"Ravi: {balance3}")    # Ravi: 1500
```

Same result, but the deposit logic lives in **one place**. If the bank adds a tax rule, you fix it once inside `deposit()`. Need 1,000 customers? Just call `deposit()` 1,000 times. Write once, use everywhere — this is the **DRY principle** (Don't Repeat Yourself). This approach is called **Procedural Programming** — you write functions, pass data in, get results out.

### A Glimpse of OOP

Python gives you a second approach — **Object-Oriented Programming (OOP)**. Instead of passing data to separate functions, you bundle data and behavior together into an object:

```python
class BankAccount:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

acc = BankAccount("Shyam", 1000)
acc.deposit(500)
print(f"{acc.name}: {acc.balance}")   # Shyam: 1500
```

Here `acc` is not just a number — it is an object that **knows** its own name and balance, and **knows how** to deposit money. You say `acc.deposit(500)` instead of `deposit(balance, 500)`. The data carries its own function with it.

```
Without functions:  copy-paste logic everywhere       → breaks at scale
Procedural:         deposit(balance, 500)             → reusable, data goes TO the function
OOP:                acc.deposit(500)                  → data carries the function WITH it
```

Same problem, three levels of organization. Neither procedural nor OOP is "better" — most real Python projects use both. We will explore OOP in depth in Parts 43–44 — for now, this glimpse is enough.

### Why Procedural First

We start with the procedural branch — functions. The reason is simple: **OOP is built on functions.** Every method inside a class is a function. If you do not understand functions deeply, OOP will never make sense.

Here is the path ahead:

1. **Procedural branch** — Functions, recursion, lambda, functional programming
2. **Project skills** — Modules, error handling, file I/O, debugging, logging
3. **OOP branch** — Classes, encapsulation, inheritance, polymorphism, dunder methods

Functions first, then we build real project skills with them, then we enter OOP with a solid foundation.

---

## Defining a Function

```python
def function_name(parameter1, parameter2):
    # function body
    return result
```

- `def` — keyword that starts a function definition
- `function_name` — follows the same naming rules as variables (lowercase, underscores)
- `parameters` — inputs the function accepts (inside parentheses)
- `return` — sends a value back to the caller

### A Complete Example

```python
def calculate_area(length, width):
    area = length * width
    return area

room = calculate_area(5, 4)
print(f"Room area: {room}")   # Room area: 20
```

---

## Parameters vs Arguments

These terms are often confused:

```python
def greet(name):       # 'name' is a PARAMETER (defined)
    return f"Hello, {name}!"

greet("Alice")         # "Alice" is an ARGUMENT (passed)
```


| Term      | Where                      | What              |
| --------- | -------------------------- | ----------------- |
| Parameter | In the function definition | The variable name |
| Argument  | In the function call       | The actual value  |


---

## Return Values

### Returning a Value

```python
def square(n):
    return n ** 2

result = square(5)
print(result)   # 25
```

`return` does two things:

1. Sends a value back to the caller
2. Immediately exits the function

```python
def check_age(age):
    if age >= 18:
        return "Adult"
    return "Minor"

print(check_age(20))   # Adult
print(check_age(15))   # Minor
```

The second `return` only runs if the first one did not.

### Functions Without return

If a function has no `return` statement, it returns `None` by default:

```python
def say_hello(name):
    print(f"Hello, {name}!")

result = say_hello("Bob")
print(result)   # None
```

### Returning Multiple Values

Functions can return multiple values using a tuple (callback to Part 19):

```python
def min_max(numbers):
    return min(numbers), max(numbers)

lowest, highest = min_max([4, 1, 7, 2, 9])
print(f"Min: {lowest}, Max: {highest}")   # Min: 1, Max: 9
```

Python packs the values into a tuple, and you unpack them on the other side.

---

## Calling Functions

A function does nothing until it is called:

```python
def greet(name):
    return f"Hello, {name}!"

# Function is defined but not called yet

message = greet("Shyam")   # NOW it runs
print(message)
```

You can call a function as many times as you need:

```python
print(greet("Alice"))
print(greet("Bob"))
print(greet("Charlie"))
```

### Using Return Values in Expressions

```python
def double(n):
    return n * 2

total = double(5) + double(3)
print(total)   # 16
```

Return values can be used anywhere a value is expected — in expressions, as arguments to other functions, in conditions.

---

## Docstrings

A docstring is a string that documents what a function does. It is placed immediately after the `def` line:

```python
def calculate_bmi(weight_kg, height_m):
    """Calculate Body Mass Index from weight and height.

    Parameters:
        weight_kg: Weight in kilograms
        height_m: Height in meters

    Returns:
        BMI as a float
    """
    return weight_kg / (height_m ** 2)
```

### Why Docstrings Matter

```python
help(calculate_bmi)
```

This prints the docstring. When your codebase has hundreds of functions, docstrings are how developers (including your future self) understand what each function does without reading the implementation.

### Docstring Rules

- Use triple quotes `"""`
- First line: brief description of what the function does
- Optional: parameters, return value, examples
- Keep it concise but useful

---

## Scope — Where Variables Live

Variables created inside a function are **local** — they exist only inside that function:

```python
def calculate():
    x = 10
    return x

calculate()
print(x)   # NameError: name 'x' is not defined
```

Variables created outside all functions are **global** — they are accessible everywhere:

```python
app_name = "Calculator"

def show_title():
    print(app_name)   # Can READ global variables

show_title()   # Calculator
```

### The LEGB Rule

When Python encounters a variable name, it searches in this order:

1. **L**ocal — inside the current function
2. **E**nclosing — inside any outer function (for nested functions)
3. **G**lobal — at the module level
4. **B**uilt-in — Python's built-in names (`print`, `len`, `range`, etc.)

```python
x = "global"

def outer():
    x = "enclosing"

    def inner():
        x = "local"
        print(x)   # local

    inner()

outer()
```

Python finds `x` at the Local level first and stops searching.

### The global Keyword

You can modify a global variable inside a function using `global`:

```python
counter = 0

def increment():
    global counter
    counter += 1

increment()
increment()
print(counter)   # 2
```

**Important:** If the global variable is a **mutable object** (list, dict, set), you can modify its **contents** without `global` — because you are not reassigning the variable, just changing what is inside it:

```python
items = [1, 2, 3]

def add_item():
    items.append(4)     # modifying contents — no reassignment, no 'global' needed

add_item()
print(items)   # [1, 2, 3, 4]
```

But if you try to **reassign** the variable itself, you need `global`:

```python
items = [1, 2, 3]

def reset_items():
    items = []          # this creates a NEW local variable, global 'items' is untouched

reset_items()
print(items)   # [1, 2, 3] — unchanged

def really_reset_items():
    global items
    items = []          # now it reassigns the global variable

really_reset_items()
print(items)   # [] — changed
```

The rule: **reading or mutating contents = no `global` needed. Reassigning the variable itself = `global` required.**

**Avoid global state in production code.** Global state makes programs hard to debug and test. Functions should receive data through parameters and return results — not reach out and modify external variables.

---

## Functions as First-Class Objects

In Python, functions are objects. You can store them in variables, put them in lists, and pass them around:

```python
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

operation = add
print(operation(5, 3))   # 8

operation = subtract
print(operation(5, 3))   # 2
```

```python
operations = [add, subtract]

for op in operations:
    print(op(10, 4))
# 14
# 6
```

This is a preview — we will use this concept more in later parts (lambda, decorators, callbacks).

---

## Where This Applies in Real Work

- **Backend endpoints:** In Django or FastAPI, every API endpoint is a function that receives a request and returns a response. The function signature defines what data the endpoint accepts.
- **Data pipelines:** Each step in a pipeline — load data, clean data, transform data, save data — is a function. This makes each step testable and reusable independently.
- **AI model inference:** Calling a model for predictions is a function call: `predictions = model.predict(input_data)`. The function abstracts away the complexity of the model internals.
- **Utility libraries:** Every `import` you use provides functions — `math.sqrt()`, `json.dumps()`, `os.path.join()`. Your own code should be organized the same way.
- **Testing:** Automated tests call your functions with known inputs and verify the outputs. Functions without global state are easy to test. Functions with global state are a nightmare.

---

## Practice Assignment

Build a function-based calculator:

1. Create four functions: `add(a, b)`, `subtract(a, b)`, `multiply(a, b)`, `divide(a, b)`
2. `divide` should handle division by zero — return a message instead of crashing
3. Add docstrings to all four functions
4. Use a `while True` loop with a menu:

```
Calculator
1. Add
2. Subtract
3. Multiply
4. Divide
5. Quit
```

1. Ask for two numbers, call the appropriate function, print the result
2. Loop until the user chooses Quit

Example session:

```
Calculator
1. Add
2. Subtract
3. Multiply
4. Divide
5. Quit

Choice: 1
First number: 10
Second number: 5
Result: 15.0

Choice: 4
First number: 10
Second number: 0
Cannot divide by zero

Choice: 5
Goodbye!
```

Save as `src/calculator.py`.

---

> **Next:** Part 25 — Functions Part 2. Default parameters, the mutable default argument trap, *args, **kwargs, and how professional Python frameworks use them.

