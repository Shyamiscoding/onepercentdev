# Part 10 — Strings

## Connecting to Part 9

In Part 9, we mapped every data type Python offers and went deep into numbers — how integers are stored as binary in the heap, why floats cannot represent `0.1` exactly, and how the `type()` of an object tells Python how to interpret the 0s and 1s in memory.

The next type on our roadmap is `str`. In the Part 9 overview table, you saw that strings are **immutable** — just like integers. That means every time you "change" a string, Python creates a new object in the heap and repoints the variable. Keep that in mind as we go through this part.

---

## Why Strings Matter

Strings are not a beginner topic that you learn and forget.

In the real world:

- AI models process text — prompts, responses, embeddings
- APIs send and receive data as JSON strings
- Databases store and return text fields
- Log files are strings
- User input is always a string

Mastering strings means mastering the most common data type in software development.

---

## Creating Strings

Python supports multiple ways to create strings:

```python
# Single quotes
name = 'OnePercentDev'

# Double quotes
greeting = "Hello, World"

# Triple quotes (multiline strings)
message = """This is a
multiline string.
It preserves line breaks."""

print(message)
```

Output:

```
This is a
multiline string.
It preserves line breaks.
```

Single and double quotes behave identically. Use whichever is convenient. Triple quotes are used for multiline text and documentation strings (docstrings).

---

## Strings Are Immutable

This is one of the most important concepts in Python.

Once a string is created, it **cannot be changed in place**.

```python
name = "Python"
name[0] = "J"  # TypeError: 'str' object does not support item assignment
```

This error confirms immutability — you cannot modify individual characters of a string.

If you need a different string, Python creates a **new** one:

```python
name = "Python"
new_name = "J" + name[1:]
print(new_name)  # Jython
```

The original `"Python"` string remains unchanged in memory. `new_name` points to a completely new string object.

---

## Indexing

Every character in a string has a position, called an **index**. Indexing starts at 0.

```python
text = "Python"

print(text[0])    # P
print(text[1])    # y
print(text[5])    # n
```

### Negative Indexing

Negative indices count from the end:

```python
print(text[-1])   # n (last character)
print(text[-2])   # o (second from last)
print(text[-6])   # P (same as text[0])
```

### Index Out of Range

```python
print(text[10])   # IndexError: string index out of range
```

Accessing an index that does not exist causes an error. Always be aware of string length.

---

## Slicing

Slicing extracts a portion of a string. The syntax is:

```
string[start : end : step]
```

- `start` — where to begin (inclusive)
- `end` — where to stop (exclusive)
- `step` — how many positions to skip

```python
text = "Python"

print(text[0:3])    # Pyt (characters at index 0, 1, 2)
print(text[2:5])    # tho
print(text[:3])     # Pyt (start defaults to 0)
print(text[3:])     # hon (end defaults to last)
print(text[:])      # Python (full copy)
```

### Step

```python
print(text[::2])    # Pto (every second character)
print(text[1::2])   # yhn (every second character, starting from index 1)
```

### Reversing a String

```python
print(text[::-1])   # nohtyP
```

A step of `-1` reverses the string. This is a common Python idiom.

### Slicing Creates a New Object

Because strings are immutable, every slice creates a new string:

```python
original = "Python"
sliced = original[0:3]

print(id(original) == id(sliced))  # False — different objects
```

---

## len() — String Length

```python
text = "Python"
print(len(text))    # 6

empty = ""
print(len(empty))   # 0
```

`len()` returns the number of characters in a string. It works on many other types too — you will see it again with lists and other collections.

---

## Escape Characters

Some characters have special meaning when preceded by a backslash `\`:


| Escape | What It Does                             | Example Output  |
| ------ | ---------------------------------------- | --------------- |
| `\n`   | New line                                 | Line 1 ↵ Line 2 |
| `\t`   | Tab                                      | Word1 Word2     |
| `\\`   | Literal backslash                        | `C:\Users`      |
| `\'`   | Single quote inside single-quoted string | `It's`          |
| `\"`   | Double quote inside double-quoted string | `He said "hi"`  |


```python
print("Line 1\nLine 2")
print("Name:\tOnePercentDev")
print("Path: C:\\Users\\onepercentdev")
```

### Raw Strings

If you need to ignore escape characters (common with file paths), use a raw string:

```python
print(r"C:\Users\new_folder")  # Prints literally, \n is NOT a newline
```

---

## f-strings — Deeper Look

We introduced f-strings briefly in Part 5. Here is a deeper look.

### Expressions Inside f-strings

You can put any valid Python expression inside `{}`:

```python
a = asdas
b = 3
print(f"{a} divided by {b} is {a / b}")
# 10 divided by 3 is 3.3333333333333335
```

### Formatting Numbers

Control decimal places:

```python
price = 49.99
tax = price * 0.18
total = price + tax

print(f"Price: {price:.2f}")
print(f"Tax: {tax:.2f}")
print(f"Total: {total:.2f}")
```

Output:

```
Price: 49.99
Tax: 9.00
Total: 58.99
```

The `:.2f` format specifier means "display as a float with 2 decimal places."

### Padding and Alignment

```python
name = "OnePercentDev"
score = 95

print(f"{'Name':<15}: {name:>15}")
print(f"{'Score':<15}: {score:>15}")
print(f"{'Status':<15}: {'Active':>15}")
```

Output:

```
Name           :  OnePercentDev
Score          :              95
Status         :          Active
```

f-string formatting is used in log messages, reports, and CLI output in real applications.

### The Older Way — .format()

Before Python 3.6, f-strings did not exist. The standard way to insert values into strings was `.format()`:

```python
name = "Dev"
age = 25

print("Hello, {}. You are {} years old.".format(name, age))
print("Hello, {0}. You are {1} years old.".format(name, age))
print("Hello, {name}. You are {age} years old.".format(name=name, age=age))
```

All three produce the same output: `Hello, Dev. You are 25 years old.`

f-strings are preferred for all new code — they are shorter and more readable. But you will see `.format()` in older codebases, documentation, and Stack Overflow answers. Recognize it when you encounter it.

---

## String Concatenation

Strings can be joined with `+`:

```python
first = "OnePer"
last = "centDev"
full = first + last
print(full)  # OnePercentDev
```

### Mixing Strings and Numbers — The TypeError Trap

You cannot concatenate a string and a number directly:

```python
age = 25
print("Age: " + age)   # TypeError: can only concatenate str (not "int") to str
```

Convert the number to a string first with `str()`:

```python
print("Age: " + str(25))   # Age: 25
```

In Part 9, we learned `int()` and `float()` convert strings to numbers. `str()` does the reverse — it converts any value to its string representation.

The better approach is to use f-strings, which handle the conversion automatically:

```python
print(f"Age: {age}")   # Age: 25  — no str() needed
```

### Why + Concatenation in Loops Is Bad

```python
result = ""
for i in range(1000):
    result = result + str(i)  # Creates a new string every iteration
```

Because strings are immutable, each `+` creates a new string object. In a loop with many iterations, this is slow and wastes memory.

The efficient alternative is `join()` — covered below.

---

## String Repetition with `*`

You can repeat a string by multiplying it with an integer:

```python
print("ha" * 3)       # hahaha
print("-" * 40)        # ----------------------------------------
print("AB" * 5)        # ABABABABAB
```

This is useful for creating visual separators, padding, and simple text patterns. The number must be an `int` — multiplying a string by a float raises a `TypeError`.

```python
print("=" * 50)   # A common pattern for section dividers in terminal output
```

---

## String Methods

String methods are built-in functions that perform operations on strings. Every method returns a **new** string — the original is never modified.

```python
name = "  OnePercentDev  "
cleaned = name.strip()

print(name)     # "  OnePercentDev  " (unchanged)
print(cleaned)  # "OnePercentDev"     (new string)
```

---

## Case Conversion Methods

```python
text = "python for 1% developers"

print(text.upper())       # PYTHON FOR 1% DEVELOPERS
print(text.lower())       # python for 1% developers
print(text.title())       # Python For 1% Developers
print(text.capitalize())  # Python for 1% developers
```


| Method          | What It Does                          |
| --------------- | ------------------------------------- |
| `.upper()`      | All characters to uppercase           |
| `.lower()`      | All characters to lowercase           |
| `.title()`      | First letter of each word capitalized |
| `.capitalize()` | Only the first character capitalized  |


### Real-World Use

When comparing user input, always normalize the case first:

```python
user_input = input("Enter yes or no: ")

if user_input.lower() == "yes":
    print("Confirmed")
```

Without `.lower()`, inputs like "YES", "Yes", "yEs" would all fail the comparison.

---

## Whitespace Methods

```python
text = "   Hello World   "

print(text.strip())    # "Hello World"  (removes from both sides)
print(text.lstrip())   # "Hello World   " (removes from left only)
print(text.rstrip())   # "   Hello World" (removes from right only)
```

### Why Stripping Matters

User input almost always has accidental spaces. Form fields, API data, file content — whitespace is everywhere.

```python
username = input("Enter username: ")  # User types "  onepercentdev  "
username = username.strip()           # Now it's "onepercentdev"
```

Without stripping, `"  onepercentdev  "` and `"onepercentdev"` would be treated as different usernames. This causes login failures, duplicate records, and data inconsistencies.

---

## Searching and Replacing

### .find()

Returns the index of the first occurrence. Returns `-1` if not found.

```python
text = "Python is powerful"

print(text.find("is"))       # 7
print(text.find("java"))     # -1 (not found)
```

### .count()

Counts how many times a substring appears:

```python
text = "banana"
print(text.count("a"))    # 3
print(text.count("na"))   # 2
```

### .replace()

Replaces all occurrences of a substring:

```python
text = "I love Java"
print(text.replace("Java", "Python"))  # I love Python
```

`.replace()` returns a new string. The original is unchanged.

### Real-World Example: Cleaning Data

```python
raw_data = "  User:  OnePercentDev  "
cleaned = raw_data.strip().replace("  ", " ")
print(cleaned)  # "User: OnePercentDev"
```

You can chain methods because each one returns a new string.

---

## Checking Content

These methods return `True` or `False`:

```python
print("12345".isdigit())     # True
print("hello".isalpha())     # True
print("hello123".isalnum())  # True
print("HELLO".isupper())     # True
print("hello".islower())     # True
print("  ".isspace())        # True
```

### Real-World Use: Input Validation

```python
age_input = input("Enter your age: ")

if age_input.isdigit():
    age = int(age_input)
    print(f"Your age is {age}")
else:
    print("Invalid input. Please enter a number.")
```

Before converting user input with `int()`, check with `.isdigit()` to avoid crashes. This is defensive programming — a professional habit.

---

## Prefix and Suffix Checks

```python
filename = "report_2026.pdf"

print(filename.startswith("report"))   # True
print(filename.endswith(".pdf"))       # True
print(filename.endswith(".csv"))       # False
```

### Real-World Use

```python
url = "https://api.example.com/data"

if url.startswith("https://"):
    print("Secure connection")

file = "data.json"
if file.endswith(".json"):
    print("JSON file detected")
```

Checking file extensions, URL protocols, and data prefixes is a common operation in backend development and data pipelines.

---

## split() and join()

### .split() — Breaking a String into Parts

`.split()` breaks a string at each space (or a specified separator) and returns a collection called a **list**. Lists are covered in depth in a later part — for now, observe how split works:

```python
sentence = "Python is the language of AI"
words = sentence.split()
print(words)   # ['Python', 'is', 'the', 'language', 'of', 'AI']
print(len(words))  # 6
```

Split with a custom separator:

```python
data = "OnePercentDev,Python,Bangalore,Developer"
parts = data.split(",")
print(parts)   # ['OnePercentDev', 'Python', 'Bangalore', 'Developer']
```

CSV (Comma-Separated Values) files are processed exactly like this — splitting each line by commas.

### .join() — Combining Parts Back into a String

`.join()` is the reverse of `.split()`. It takes a collection of strings and joins them with a separator:

```python
words = ["Python", "is", "powerful"]
sentence = " ".join(words)
print(sentence)   # "Python is powerful"
```

```python
parts = ["2026", "03", "19"]
date = "-".join(parts)
print(date)   # "2026-03-19"
```

### Why join() Is Better Than + in Loops

`+` concatenation in loops is inefficient because it creates a new string every iteration. `join()` is the professional solution:

```python
numbers = []
for i in range(5):
    numbers.append(str(i))
result = ", ".join(numbers)
print(result)  # "0, 1, 2, 3, 4"
```

`.join()` is always preferred over repeated `+` concatenation.

---

## Method Chaining

Because every string method returns a new string, you can chain them:

```python
raw = "   Hello, WORLD!   "
clean = raw.strip().lower().replace("!", "")
print(clean)   # "hello, world"
```

Each method operates on the result of the previous one. This is a common and clean pattern in Python.

---

## Unicode Awareness

Python strings support Unicode — they can hold characters from any language:

```python
greeting = "ನಮಸ್ಕಾರ"  # Kannada
print(greeting)
print(len(greeting))
```

Python handles multi-language text natively. This is important for applications that serve users in different languages.

---

## Complete String Methods Reference

Here is every string method covered in this part, in one place. Every method returns a **new** value — the original string is never modified.


| Method                | What It Does                                                        | Returns |
| --------------------- | ------------------------------------------------------------------- | ------- |
| `.upper()`            | All characters to uppercase                                         | `str`   |
| `.lower()`            | All characters to lowercase                                         | `str`   |
| `.title()`            | First letter of each word capitalized                               | `str`   |
| `.capitalize()`       | Only the first character capitalized                                | `str`   |
| `.strip()`            | Removes whitespace from both sides                                  | `str`   |
| `.lstrip()`           | Removes whitespace from left side                                   | `str`   |
| `.rstrip()`           | Removes whitespace from right side                                  | `str`   |
| `.split(sep)`         | Splits string into a list by separator (default: whitespace)        | `list`  |
| `sep.join(list)`      | Joins list items into a string with separator                       | `str`   |
| `.replace(old, new)`  | Replaces all occurrences of `old` with `new`                        | `str`   |
| `.find(sub)`          | Returns index of first occurrence, or `-1` if not found             | `int`   |
| `.index(sub)`         | Returns index of first occurrence, raises `ValueError` if not found | `int`   |
| `.startswith(prefix)` | Checks if string starts with prefix                                 | `bool`  |
| `.endswith(suffix)`   | Checks if string ends with suffix                                   | `bool`  |
| `.count(sub)`         | Counts non-overlapping occurrences of substring                     | `int`   |
| `.isdigit()`          | `True` if all characters are digits                                 | `bool`  |
| `.isalpha()`          | `True` if all characters are letters                                | `bool`  |
| `.isalnum()`          | `True` if all characters are letters or digits                      | `bool`  |
| `.isupper()`          | `True` if all cased characters are uppercase                        | `bool`  |
| `.islower()`          | `True` if all cased characters are lowercase                        | `bool`  |
| `.zfill(width)`       | Pads with zeros on the left to fill `width`                         | `str`   |
| `.center(width)`      | Centers string within `width`, padding with spaces                  | `str`   |
| `.ljust(width)`       | Left-justifies string within `width`                                | `str`   |
| `.rjust(width)`       | Right-justifies string within `width`                               | `str`   |


---

## Where This Applies in Real Work

- **API development:** JSON data is text. Parsing, slicing, and formatting strings is a daily task.
- **AI prompt engineering:** Building prompts for language models involves combining strings, inserting variables with f-strings, and careful formatting.
- **Data cleaning:** Input data often has extra spaces, wrong casing, or invalid characters. `.strip()`, `.lower()`, `.replace()` are the first step in any data pipeline.
- **Log analysis:** Extracting information from log lines uses `.find()`, `.startswith()`, slicing, and `.split()`.
- **Input validation:** `.isdigit()`, `.isalpha()`, `.startswith()`, `.endswith()` are used in every form validation system.
- **File paths:** Handling file paths requires understanding escape characters and raw strings.

---

## Practice Assignment

### Assignment 1

1. Create a variable `brand = "OnePercentDev"`
2. Print the first character and the last character
3. Print the brand name reversed
4. Print the total number of characters
5. Print the first 3 characters and the last 3 characters separately
6. Print the brand name with every other character: `OePretDv`

### Assignment 2

1. Ask the user to enter a sentence
2. Strip any extra whitespace
3. Convert it to lowercase
4. Count how many words are in the sentence (using `.split()` and `len()`)
5. Ask the user for a word to replace and its replacement
6. Perform the replacement and print the final cleaned sentence

Save as `src/string_practice.py`.

---

> **Next:** Part 11 — Operators, Truthiness, and Conditionals. Comparison operators, logical operators, truthy/falsy values, and decision-making with if/elif/else.

