# Part 32 — Publishing Your Own Package (To PyPI)

Since Part 30, you have been using `my_package/` with `clean_text`, `count_words`, and `reverse_words`. You built it, imported it, set up virtual environments for it, and managed it with Poetry and uv.

But right now, only you can use it. What if your friend in another country wants to use your text utilities? They can't — your code lives on your laptop.

In this part, you take that same code, package it properly, and **upload it to the internet**. By the end, anyone in the world will be able to run `pip install` and use your functions.

---

## 1. The Official Python Package Index (PyPI)

When you type `pip install requests`, where does the code come from? It comes from **PyPI** — the official database of third-party Python packages.


| Site                   | URL                                            | Purpose                                                                                 |
| ---------------------- | ---------------------------------------------- | --------------------------------------------------------------------------------------- |
| **PyPI** (Real)        | [https://pypi.org](https://pypi.org)           | The production database. Real packages that anyone can `pip install` normally.          |
| **TestPyPI** (Sandbox) | [https://test.pypi.org](https://test.pypi.org) | Official sandbox for practice. Works exactly like the real one, but meant for learning. |


Because this is practice, we will use **TestPyPI**. It works identically to the real PyPI, but it won't clutter the main database. Even on the test server, anyone in the world can still install your package.

### Step 1: Create Accounts

1. **TestPyPI (required now):** Go to [https://test.pypi.org/account/register/](https://test.pypi.org/account/register/) and create a free account
2. **PyPI (optional, for later):** When you're ready to publish for real, create an account at [https://pypi.org/account/register/](https://pypi.org/account/register/)

---

## 2. The Project — Same Code, New Structure

We have already created the publishable project inside `publish_project/`. It uses the same `text_utils` functions you have been working with — but restructured into the `src/` layout that PyPI expects.

Here is the old structure from Part 30 and the new publishable structure — same code, different wrapping:

**Old (Part 30) — local project:**

```
example_project/
├── main.py
├── chat.py
├── my_module.py
├── my_package/
│   ├── __init__.py
│   └── text_utils.py
├── requirements.txt
├── .env
└── .gitignore
```

**New (Part 32) — publishable to PyPI:**

```
publish_project/
├── src/
│   └── onepercentutils/         ← The package users will import
│       ├── __init__.py          ← Exposes your functions
│       └── text_utils.py        ← Your actual code (same as Part 30!)
├── pyproject.toml               ← Tells PyPI about your package
├── README.md                    ← The front page of your package on PyPI
└── .gitignore
```

**What changed and why:**

- `my_package/` → `src/onepercentutils/` — the package folder moved inside a `src/` wrapper, and got a globally-unique name. This is the layout PyPI expects.
- `main.py`, `chat.py`, `my_module.py` are gone — those were *consumers* of your code. A publishable package only ships the library itself, not the scripts that use it.
- `requirements.txt` → `pyproject.toml` — instead of just listing dependencies, `pyproject.toml` describes the whole package (name, version, author, dependencies) so PyPI knows what it is.
- `README.md` is new — this becomes the front page of your package on PyPI.

### The Code (already in the project)

`**src/onepercentutils/text_utils.py`** — the same functions you wrote:

```python
def clean_text(text):
    """Removes extra spaces and makes everything lowercase."""
    return text.strip().lower()

def count_words(text):
    """Returns the number of words in a string."""
    return len(text.split())

def reverse_words(text):
    """Reverses the order of words. 'hello world' → 'world hello'"""
    return " ".join(text.split()[::-1])

def format_currency(amount):
    """Format a number as Indian Rupee currency."""
    return f"₹{amount:,.2f}"
```

`**src/onepercentutils/__init__.py**` — exposes everything:

```python
from .text_utils import clean_text, count_words, reverse_words, format_currency
```

### Why the `src/` folder?

Without `src/`, Python might accidentally import your local package instead of the installed one during testing. The `src/` layout forces Python to only use the properly installed version. This is the modern standard for publishable packages.

---

## 3. The Configuration (`pyproject.toml`)

In Part 31, you learned that `pyproject.toml` is the master instruction manual. Here it tells PyPI what your package is called, who wrote it, and what version it is:

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "onepercentutils-yourname"
version = "0.0.1"
authors = [
  { name = "Your Name", email = "your.email@example.com" },
]
description = "Text utility functions from the OnePercent Python series"
readme = "README.md"
requires-python = ">=3.10"
```

**Important:** The `name` field must be **unique across all of PyPI**. Replace `yourname` with your actual name or add numbers (e.g., `onepercentutils-shyam-42`). The folder is called `onepercentutils` (that's what users `import`), but the pip install name must be globally unique.

---

## 4. Building the Package (Creating the Wheel)

Now we convert your code into compressed files that PyPI can distribute.

Open your terminal inside `publish_project/`:

```bash
cd publish_project
pip install build
python -m build
```

Python creates a `dist/` folder with two files:

- `onepercentutils_yourname-0.0.1.tar.gz` (the raw source code)
- `onepercentutils_yourname-0.0.1-py3-none-any.whl` (the compiled "Wheel")

These are the exact files that get downloaded when someone types `pip install`.

---

## 5. Uploading to TestPyPI (Deployment)

To upload safely, we use **Twine**:

```bash
pip install twine
python -m twine upload --repository testpypi dist/*
```

**Authentication:**

- Go to your TestPyPI account and generate an API Token: [https://test.pypi.org/manage/account/#api-tokens](https://test.pypi.org/manage/account/#api-tokens)
- Set the scope to "Entire account" (since this is your first upload)
- When Twine asks for username, type exactly: `__token__`
- When it asks for password, paste your API token (it starts with `pypi-` and will be invisible as you type)

Once successful, Twine gives you a live URL to your package's page on TestPyPI! You can view it at:
`https://test.pypi.org/project/onepercentutils-yourname/`

---

## 6. Proving It Works (The Grand Finale)

Your package is now live on the internet. Let's prove it by installing it like a user in another country would.

1. Create a completely new folder somewhere else on your computer
2. Create and activate a fresh virtual environment (like you learned in Part 31)
3. Install your package from TestPyPI:

```bash
pip install --index-url https://test.pypi.org/simple/ onepercentutils-yourname
```

**Two important things about this command:**

- **The name** (`onepercentutils-yourname`) must match the `name` field you set in `pyproject.toml` exactly. That is the global identity of your package on PyPI.
- **The `--index-url` flag is required here** because TestPyPI is a separate database from the real PyPI. By default, `pip install` only searches `pypi.org` — so without this flag, pip would look in the wrong place and fail with `No matching distribution found`. When you publish to the real PyPI later, you simply drop the flag and run `pip install onepercentutils-yourname`.

1. Open Python and use it:

```python
from onepercentutils import clean_text, count_words, reverse_words, format_currency

print(clean_text("  Hello World  "))       # hello world
print(count_words("Python is amazing"))     # 3
print(reverse_words("hello world"))         # world hello
print(format_currency(150000))              # ₹150,000.00
```

### From Consumer to Creator

These are the same functions you wrote in Part 30 inside `my_package/text_utils.py`. Back then, only your `main.py` could use them. Now anyone in the world can `pip install` them.

You didn't just write a script — you authored, packaged, and distributed an open-source library to the global Python ecosystem.

*(When you're ready to publish for real: create an account at [https://pypi.org/account/register/](https://pypi.org/account/register/), generate a token at [https://pypi.org/manage/account/#api-tokens](https://pypi.org/manage/account/#api-tokens), and run the same upload command without the `--repository testpypi` flag.)*

---

> **Next:** Part 33 — Exceptions Part 1. Your package is live and strangers will use it in ways you never tested. Time to learn how to handle the inevitable — errors, bad input, and broken connections — without crashing.



