# Part 31 — Virtual Environments and Modern Dependency Management

In Part 30, you installed `requests` and `openai` using `pip install`, and everything worked perfectly. But we left you with a cliffhanger — `pip` installs packages globally, and if two projects need different versions of the same library, they will collide and crash.

That is where virtual environments come in. And once you understand them, we will go one step further — because even the classic approach has a hidden flaw that the industry has since fixed with modern tools.

---

## The Problem — Why Isolation Matters

Imagine you have two projects:

- **Project A (Your AI Chatbot)** needs `openai==0.28.0`
- **Project B (A newer AI App)** needs `openai==1.14.0`

If you install packages globally (directly into your system Python), both projects share the same installation. You install 1.14.0 for Project B, and Project A breaks completely because the OpenAI library completely changed how its code works between those versions.

This is not a hypothetical problem. It happens constantly in teams and deployments.

The solution: **virtual environments** — isolated Python installations, one per project.

---

## What Is a Virtual Environment?

A virtual environment is a self-contained directory that has:

- Its own Python interpreter (a copy or symlink of the system one)
- Its own `pip`
- Its own `site-packages` (where installed packages live)

Packages installed in one virtual environment do not affect any other environment or the system Python. Under the hood, activating a virtual environment changes `sys.path` (which you saw in Part 29) so Python looks for packages inside the `venv/` folder first instead of the system-wide location.

```
project_a/
├── venv/          ← Project A's packages live here
├── main.py
└── requirements.txt

project_b/
├── venv/          ← Project B's packages live here (completely separate)
├── main.py
└── requirements.txt
```

> **Don't confuse `venv` with `pyenv`.** They sound similar but solve different problems:
>
> - `**venv`** (what we're learning here) → manages **packages** for one project. Built into Python.
> - `**pyenv`** → manages **Python versions** on your machine (e.g., switching between 3.10, 3.11, 3.12). A separate tool you install — see [pyenv (Mac/Linux)](https://github.com/pyenv/pyenv) or [pyenv-win (Windows)](https://github.com/pyenv-win/pyenv-win).
>
> Both can be used together, but they are unrelated tools. `uv` (covered later in this part) can actually do `pyenv`'s job too with `uv python install 3.12`.

---

## Creating a Virtual Environment

### Step 1 — Create

```bash
python -m venv venv
```

This creates a `venv/` directory inside your project folder. The second `venv` is the folder name — it is a convention, not a requirement.

### Step 2 — Activate

**Mac / Linux:**

```bash
source venv/bin/activate
```

**Windows (Command Prompt):**

```bash
venv\Scripts\activate
```

**Windows (PowerShell):**

```bash
venv\Scripts\Activate.ps1
```

After activation, your terminal prompt changes to show the environment name:

```bash
(venv) $ python --version
Python 3.12.0
```

### Step 3 — Verify

```bash
which python        # Mac/Linux
where python         # Windows
```

The output should point to the `venv/` directory, not the system Python.

---

## Installing Packages with pip

With the virtual environment activated:

```bash
pip install requests
```

This installs `requests` only inside this virtual environment.

```bash
pip list
```

Shows all installed packages in the current environment.

```bash
pip show requests
```

Shows details about a specific package — version, location, dependencies.

---

## requirements.txt — Pinning Dependencies

In Part 29's project structure, you saw `requirements.txt` listed alongside `main.py`, `models/`, and `utils/`. That file is not decoration — it is the contract that defines exactly which packages your project needs.

### Freezing Current Packages

```bash
pip freeze > requirements.txt
```

This creates a file listing every installed package with its exact version:

```
certifi==2024.2.2
charset-normalizer==3.3.2
idna==3.7
requests==2.31.0
urllib3==2.2.1
```

### Why Version Pinning Matters

Without pinning:

```
requests
```

This installs the latest version, whatever it is today. Six months from now, the latest version might have breaking changes.

With pinning:

```
requests==2.31.0
```

This installs exactly version 2.31.0. Every developer, every server, every deployment gets the same version.

### Installing from requirements.txt

When another developer clones your project:

**Mac / Linux:**

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Every package is installed at the exact pinned version. The project works identically everywhere.

---

## Deactivating and Cleanup

```bash
deactivate
```

Your terminal returns to the system Python. The virtual environment still exists in the `venv/` folder — it is just not active.

### .gitignore — Never Commit the venv Folder

The `venv/` directory contains hundreds of files (Python interpreter, installed packages). It should never be committed to Git.

Add this to your `.gitignore`:

```
venv/
__pycache__/
*.pyc
```

Other developers recreate the virtual environment from `requirements.txt`. They do not need your `venv/` folder — they create their own.

---

## The Complete Classic Workflow

Starting a new project:

**Mac / Linux:**

```bash
mkdir my_project
cd my_project
python -m venv venv
source venv/bin/activate
pip install requests
pip freeze > requirements.txt
git init
echo "venv/" >> .gitignore
echo "__pycache__/" >> .gitignore
```

**Windows:**

```bash
mkdir my_project
cd my_project
python -m venv venv
venv\Scripts\activate
pip install requests
pip freeze > requirements.txt
git init
echo venv/ >> .gitignore
echo __pycache__/ >> .gitignore
```

Cloning an existing project:

**Mac / Linux:**

```bash
git clone <repo-url>
cd my_project
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows:**

```bash
git clone <repo-url>
cd my_project
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

This is the foundation. Millions of projects use this workflow, and every Python developer must know it.

---

## The Hidden Crack in requirements.txt

You did everything right. You created a virtual environment, pinned `requests==2.31.0` in `requirements.txt`, committed the file, and sent the repo to a friend.

Your friend clones the project, creates a venv, runs `pip install -r requirements.txt`. Everything installs. They run `python main.py`.

It crashes.

How? You pinned the version. You used a virtual environment. What went wrong?

Look at your `requirements.txt` again. You wrote `requests==2.31.0`. But `requests` secretly relies on 4 other libraries under the hood — `urllib3`, `certifi`, `charset-normalizer`, `idna`. These are called **transitive dependencies**.

If you used `pip freeze`, those sub-dependencies were pinned too. But what if you had only written `requests==2.31.0` manually? Your friend would get the *latest* `urllib3` — possibly a version with a bug that breaks `requests`.

Even `pip freeze` has problems — it dumps a flat list of every package with no distinction between what *you* asked for and what got pulled in automatically. Six months later, you look at 47 lines in `requirements.txt` and have no idea which ones are yours and which are transitive noise.

The infamous **"Works on My Machine"** problem strikes again, despite doing everything "right." The classic tools work, but they are fragile. The industry needed something stronger.

---

## The Modern Solution: pyproject.toml and Lockfiles

### pyproject.toml — The Modern Configuration File

For almost 15 years, Python projects were configured using executable Python scripts called `setup.py`. This was slow and caused security vulnerabilities.

In 2016, the Python community introduced a new standard through **[PEP 518](https://peps.python.org/pep-0518/)**: `pyproject.toml` (TOML stands for "Tom's Obvious, Minimal Language"). Later, **[PEP 621](https://peps.python.org/pep-0621/)** (2020) standardized the `[project]` table inside it — which is what modern tools like `uv` use.

> **What is a PEP?** PEP stands for **Python Enhancement Proposal** — the official document format for proposing changes to Python. Every major Python standard, including `pyproject.toml`, was introduced through a PEP. Browse them all at [https://peps.python.org](https://peps.python.org). Famous ones you may have heard of: [PEP 8](https://peps.python.org/pep-0008/) (style guide) and [PEP 20](https://peps.python.org/pep-0020/) (Zen of Python).

Instead of a script, `pyproject.toml` is a **static text file**. Think of it as the passport and instruction manual for your project.

It acts as a single source of truth for:

1. **Metadata:** What is this project called? Who wrote it?
2. **Dependencies:** What does this project need to run?
3. **Tool Settings:** How should code formatters or linters behave?

### Lockfiles — The Missing Piece

A lockfile records the exact version of every dependency AND every transitive dependency at the moment you installed them. When someone else runs the install command, the tool reads the lockfile and reproduces the exact same environment — byte for byte.

This is what `requirements.txt` tried to do but could not guarantee. Lockfiles solve it completely.

---

## The Modern Ecosystem (Concept Overview)

To use `pyproject.toml` and lockfiles, the industry built two powerful tools. Before we install anything, let's first understand what these tools do and why they exist. We will install them in the hands-on section below.

### Poetry (The Current Industry Standard)

Website: [https://python-poetry.org](https://python-poetry.org)

Poetry was built to do everything automatically. Instead of running `python -m venv` and `pip install` and `pip freeze` manually, Poetry handles it all in one tool.

Once Poetry is installed, here is what a typical command looks like:

```bash
poetry add requests
```

This single command does three things:

1. Automatically creates and manages a virtual environment for you.
2. Updates `pyproject.toml` to list `requests`.
3. Generates a file called `poetry.lock`.

**The Lockfile:** `poetry.lock` pins down the exact version of `requests` AND the exact versions of all its transitive dependencies. It guarantees that if a million people download your project, every single one gets the exact same installation.

*(Don't run this yet — we will install Poetry first in the hands-on section.)*

### uv (The Blazing-Fast Future)

Website: [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)

Python tooling was historically written in Python, which made it slow.

Recently, engineers at a company called [Astral](https://astral.sh) rewrote these tools in a blazing-fast language called **Rust**. They created `uv`.

`uv` does everything `pip`, `venv`, `pipx`, `pyenv`, and Poetry do — all in one tool. And it is **10-100x faster** than those individual tools. This is why `uv` is rapidly becoming the new standard.

Once `uv` is installed, here is what its commands look like:

```bash
uv init        # creates a pyproject.toml file
uv add requests # creates a virtual environment, installs requests, generates uv.lock
```

*(Again — concept only. We will install `uv` in the hands-on section.)*

### Other Tools to Know By Name

- **conda / Anaconda:** Common in Data Science and Machine Learning for handling complex C/C++ math libraries.
- **pipx:** Used for installing global command-line tools safely without breaking your system Python. Docs: [https://pipx.pypa.io](https://pipx.pypa.io).
- **pyenv:** Manages multiple **Python versions** on the same machine (e.g., switching between Python 3.10 and 3.12). It does **not** manage packages — that is still `venv`'s job. Mac/Linux: [pyenv](https://github.com/pyenv/pyenv). Windows: [pyenv-win](https://github.com/pyenv-win/pyenv-win). Note: `uv` can also do this with `uv python install 3.12`, so if you're using uv, you may not need pyenv at all.

---

## Hands-On: Two Projects, Two Tools

We have created two copies of the same project from Part 30 — same code, different tooling. You will set up each one, run it, and then delete the environment. Nothing touches your system.

### Project Structure (same for both)

```
poetry_project/ (or uv_project/)
├── main.py
├── chat.py
├── my_module.py
├── my_package/
│   ├── __init__.py
│   └── text_utils.py
├── pyproject.toml          ← replaces requirements.txt
├── .env
└── .gitignore
```

The only difference is `pyproject.toml` — Poetry uses `[tool.poetry]`, uv uses `[project]`.

---

### Project 1: Poetry

> Official docs: [https://python-poetry.org/docs/](https://python-poetry.org/docs/)

We will follow this order:

1. Check that Python is installed (prerequisite).
2. Install Poetry itself (pick one of three methods below).
3. Verify Poetry works.
4. Use Poetry to set up and run the project.

---

#### Step 1 — Prerequisite: Make sure Python works

Before installing Poetry, confirm that Python is available on your system. Open your terminal and run:

```bash
python --version
```

You should see a version number (3.10 or higher). If `python` doesn't work, try `python3` (Mac/Linux) or `py` (Windows). If none of them work, go back to Part 4 and install Python first.

---

#### Step 2 — Install Poetry (one-time setup)

There are **three official ways** to install Poetry. Pick **one** based on your situation. All three are documented at [https://python-poetry.org/docs/#installation](https://python-poetry.org/docs/#installation).


| Method                                | Best For                           | Extra Tools Needed            |
| ------------------------------------- | ---------------------------------- | ----------------------------- |
| **Way 1 — Official installer script** | Beginners, simplest setup          | None (just Python)            |
| **Way 2 — pipx**                      | Professional setups, easy upgrades | `pipx` (and Scoop on Windows) |
| **Way 3 — Manual via pip**            | Advanced users, full control       | None                          |


For this course, **Way 1 is recommended** because it has no extra prerequisites and is the easiest to follow. The other two are documented so you know your options.

##### Way 1 — Official Installer Script (recommended for this course)

This is the simplest method — it only requires Python, creates an isolated environment for Poetry automatically, and needs no additional tools.

**Mac / Linux:**

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

**Windows (PowerShell):**

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

If `py` is not recognized (e.g., you installed Python from the Microsoft Store), use `python` instead of `py`.

After the installer finishes, it will print a message telling you where Poetry was installed (e.g., `%APPDATA%\Python\Scripts` on Windows, `~/.local/bin` on Mac/Linux). **Close and reopen your terminal** so the PATH update takes effect.

##### Way 2 — Using pipx (preferred for professional/long-term use)

`pipx` is a tool that installs Python command-line apps in their own isolated environments. The [official Poetry docs](https://python-poetry.org/docs/#installing-with-pipx) list this as their primary recommended method because upgrades are simple: `pipx upgrade poetry`.

The catch: you need to install `pipx` first. The [official pipx docs](https://pipx.pypa.io/stable/how-to/install-pipx/) recommend a different tool per OS:

**Mac:**

```bash
brew install pipx
pipx ensurepath
pipx install poetry
```

**Windows:** First install [Scoop](https://scoop.sh/) (a Windows package manager), then:

```powershell
scoop install pipx
pipx ensurepath
pipx install poetry
```

**Linux (Ubuntu 23.04+):**

```bash
sudo apt install pipx
pipx ensurepath
pipx install poetry
```

After `pipx ensurepath`, close and reopen your terminal.

##### Way 3 — Manual via pip (advanced, Unix only)

For full control, you can install Poetry into its own virtual environment manually. This is documented at [Poetry docs → Manually](https://python-poetry.org/docs/#installing-manually). Not recommended for beginners.

```bash
python3 -m venv $HOME/.poetry-venv
$HOME/.poetry-venv/bin/pip install -U pip setuptools
$HOME/.poetry-venv/bin/pip install poetry
```

Then add `$HOME/.poetry-venv/bin/poetry` to your PATH.

---

#### Step 3 — Verify Poetry is installed

Whichever method you chose, open a fresh terminal and run:

```bash
poetry --version
```

You should see something like `Poetry (version 2.x.x)`.

If you get "command not found" or "'poetry' is not recognized":

1. Make sure you **closed and reopened** your terminal after installation.
2. If it still doesn't work, the installer's directory is not in your PATH:
  - **Windows:** Manually add `%APPDATA%\Python\Scripts` to your system PATH (System Settings → Environment Variables → Edit PATH → Add the folder).
  - **Mac/Linux:** Add `export PATH="$HOME/.local/bin:$PATH"` to your `~/.bashrc` or `~/.zshrc` file, then run `source ~/.bashrc` or `source ~/.zshrc`.

---

#### Step 4 — Set up the project

Now that Poetry is installed and verified, navigate into the project folder and let Poetry handle the rest:

```bash
cd poetry_project
poetry install
```

That one command reads `pyproject.toml`, creates an isolated virtual environment, installs all three libraries (`requests`, `openai`, `python-dotenv`), and generates `poetry.lock` — the lockfile that pins every single dependency.

---

#### Step 5 — Run the project

```bash
poetry run python main.py
```

`poetry run` ensures Python uses the isolated environment, not your system Python.

---

#### Step 6 — Clean up (delete the environment)

```bash
poetry env remove --all
```

The virtual environment is gone. Your system Python is untouched. The code and `pyproject.toml` remain — anyone can recreate the environment by running `poetry install` again.

---

### Project 2: uv

> Official docs: [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)

We will follow the same order as before:

1. Check prerequisites.
2. Install `uv` itself (pick one of the methods below).
3. Verify `uv` works.
4. Use `uv` to set up and run the project.

---

#### Step 1 — Prerequisite check

Unlike Poetry, `uv` does **not** require Python or pip to be installed first. The installer downloads a standalone binary written in Rust. You only need a terminal.

---

#### Step 2 — Install uv (one-time setup)

The [official uv docs](https://docs.astral.sh/uv/getting-started/installation/) list several ways to install. Pick **one** based on your situation.


| Method                           | Best For                              | Extra Tools Needed                     |
| -------------------------------- | ------------------------------------- | -------------------------------------- |
| **Way 1 — Standalone installer** | Beginners, all platforms              | None                                   |
| **Way 2 — WinGet**               | Windows users with WinGet             | None (WinGet ships with Windows 10/11) |
| **Way 3 — Homebrew**             | Mac users with Homebrew               | `brew`                                 |
| **Way 4 — pip / pipx**           | Users who already have Python tooling | `pip` or `pipx`                        |


For this course, **Way 1 is recommended** on Mac/Linux and **Way 2 (WinGet) is recommended** on Windows because both require zero prerequisites.

##### Way 1 — Standalone Installer (recommended for Mac/Linux)

**Mac / Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

After it finishes, **close and reopen your terminal** so the PATH update takes effect.

##### Way 2 — WinGet (recommended for Windows)

Windows 10 (recent updates) and Windows 11 come with [WinGet](https://learn.microsoft.com/en-us/windows/package-manager/winget/) built in. This is the simplest option for Windows users:

```powershell
winget install --id=astral-sh.uv -e
```

##### Way 3 — Homebrew (Mac)

If you already use [Homebrew](https://brew.sh/):

```bash
brew install uv
```

##### Way 4 — pip or pipx

If you already have Python and want to install `uv` like any other Python package:

```bash
pipx install uv     # recommended (isolated)
# or
pip install uv      # quick but installs into your active environment
```

---

#### Step 3 — Verify uv is installed

Whichever method you chose, open a fresh terminal and run:

```bash
uv --version
```

You should see a version number. If you get "command not found" or "'uv' is not recognized":

1. Make sure you **closed and reopened** your terminal after installation.
2. If it still doesn't work, the PATH was not updated. On Windows, manually add `%USERPROFILE%\.local\bin` to your system PATH (System Settings → Environment Variables → Edit PATH → Add the folder).
3. On Mac/Linux, check if `~/.local/bin` is in your PATH by running `echo $PATH`. If it's missing, add `export PATH="$HOME/.local/bin:$PATH"` to your `~/.bashrc` or `~/.zshrc` file.

---

#### Step 4 — Set up the project

Now that `uv` is installed and verified, navigate into the project folder:

```bash
cd uv_project
uv sync
```

That one command reads `pyproject.toml`, creates a `.venv/` folder, installs everything, and generates `uv.lock`. It does the same thing Poetry does — but noticeably faster.

---

#### Step 5 — Run the project

```bash
uv run python main.py
```

---

#### Step 6 — Clean up (delete the environment)

```bash
rm -rf .venv          # Mac/Linux
rmdir /s /q .venv     # Windows
```

Gone. Your system is clean. Run `uv sync` again anytime to recreate it.

---

## Poetry vs uv — Side by Side


| Action             | Poetry                      | uv                                                         |
| ------------------ | --------------------------- | ---------------------------------------------------------- |
| Prerequisites      | Python 3.10+                | None (standalone binary)                                   |
| Install the tool   | Official installer script   | `curl ... | sh` (Mac/Linux) or PowerShell/WinGet (Windows) |
| Set up project     | `poetry install`            | `uv sync`                                                  |
| Add a library      | `poetry add requests`       | `uv add requests`                                          |
| Run a script       | `poetry run python main.py` | `uv run python main.py`                                    |
| Lockfile           | `poetry.lock`               | `uv.lock`                                                  |
| Delete environment | `poetry env remove --all`   | `rm -rf .venv`                                             |
| Speed              | Good                        | 10-100x faster                                             |


Both tools solve the same problem: isolated, reproducible environments with locked dependencies. Poetry is the established standard. uv is the fast newcomer rapidly gaining adoption.

---

## Quick Reference: requirements.txt vs pyproject.toml vs Poetry vs uv

*Why these tools exist and what each one replaces — keep this section bookmarked.*

### Feature Comparison


| Feature                          | `requirements.txt`                     | `pyproject.toml`                       | Poetry                    | uv                               |
| -------------------------------- | -------------------------------------- | -------------------------------------- | ------------------------- | -------------------------------- |
| List dependencies                | Yes                                    | Yes                                    | Yes                       | Yes                              |
| Pin exact versions               | Manual (`pip freeze`)                  | Manual                                 | Automatic (`poetry.lock`) | Automatic (`uv.lock`)            |
| Create virtual environment       | No (need `venv` separately)            | No (need `venv` separately)            | Yes (built-in)            | Yes (built-in)                   |
| Lock file (reproducible builds)  | No                                     | No                                     | Yes (`poetry.lock`)       | Yes (`uv.lock`)                  |
| Dependency conflict detection    | No                                     | No                                     | Yes                       | Yes                              |
| Project metadata (name, version) | No                                     | Yes                                    | Yes                       | Yes (uses `pyproject.toml`)      |
| Speed                            | Slow                                   | Slow                                   | Moderate                  | Extremely fast (written in Rust) |
| Install Python itself            | No                                     | No                                     | No                        | Yes (`uv python install 3.14`)   |
| Run scripts without install      | No                                     | No                                     | No                        | Yes (`uv run script.py`)         |
| Install CLI tools globally       | `pip install pytest` (pollutes system) | `pip install pytest` (pollutes system) | Not supported             | Yes (`uv tool install pytest`)   |


---

### Command Comparison — pip vs Poetry vs uv

*The same task, three different ways to do it.*


| Task                             | pip / manual                         | Poetry                          | uv                                              |
| -------------------------------- | ------------------------------------ | ------------------------------- | ----------------------------------------------- |
| Start a new project              | (no command — create files manually) | `poetry init`                   | `uv init`                                       |
| Create virtual env               | `python3 -m venv venv`               | `poetry install` (auto)         | `uv sync` (auto)                                |
| Activate virtual env             | `source venv/bin/activate`           | `poetry shell`                  | `uv run` (no activation needed)                 |
| Add a package                    | `pip install requests` + edit file   | `poetry add requests`           | `uv add requests`                               |
| Add a dev-only package           | `pip install pytest` + edit file     | `poetry add pytest --group dev` | `uv add pytest --dev`                           |
| Remove a package                 | `pip uninstall` + edit file          | `poetry remove requests`        | `uv remove requests`                            |
| Install all dependencies         | `pip install -r requirements.txt`    | `poetry install`                | `uv sync`                                       |
| Update all packages              | `pip install --upgrade` (each one)   | `poetry update`                 | `uv lock --upgrade && uv sync`                  |
| Update one package               | `pip install --upgrade requests`     | `poetry update requests`        | `uv lock --upgrade-package requests && uv sync` |
| Show installed packages          | `pip list`                           | `poetry show`                   | `uv pip list`                                   |
| Run a script                     | `python main.py`                     | `poetry run python main.py`     | `uv run main.py`                                |
| Run with a specific Python       | `python3.14 main.py`                 | `poetry env use 3.14`           | `uv run --python 3.14 main.py`                  |
| Install Python itself            | (download from python.org)           | Not supported                   | `uv python install 3.14`                        |
| Generate lock file               | `pip freeze > requirements.txt`      | `poetry lock`                   | `uv lock`                                       |
| Install CLI tools (pytest, ruff) | `pip install pytest` (global)        | Not supported                   | `uv tool install pytest`                        |
| Run CLI tool without installing  | Not possible                         | Not possible                    | `uvx pytest`                                    |
| Check env info                   | (manual)                             | `poetry env info`               | `uv python list`                                |


---

### Steps to Set Up a Project

*Watch how the number of manual steps shrinks with each modern tool.*

#### With `requirements.txt` — 5 manual steps


| Step                            | Command                           |
| ------------------------------- | --------------------------------- |
| 1. Create virtual env           | `python3 -m venv venv`            |
| 2. Activate it                  | `source venv/bin/activate`        |
| 3. Install packages one by one  | `pip install requests openai`     |
| 4. Freeze versions to file      | `pip freeze > requirements.txt`   |
| 5. Share with team / re-install | `pip install -r requirements.txt` |


#### With `pyproject.toml` + pip — 4 manual steps


| Step                                               | Command                    |
| -------------------------------------------------- | -------------------------- |
| 1. Create virtual env                              | `python3 -m venv venv`     |
| 2. Activate it                                     | `source venv/bin/activate` |
| 3. Manually write dependencies in `pyproject.toml` | (edit file by hand)        |
| 4. Install                                         | `pip install .`            |


#### With Poetry — 2 steps


| Step                  | Command                                    |
| --------------------- | ------------------------------------------ |
| 1. Add packages       | `poetry add requests openai python-dotenv` |
| 2. Install everything | `poetry install`                           |


#### With uv — 2 steps (fastest)


| Step                         | Command                                           |
| ---------------------------- | ------------------------------------------------- |
| 1. Initialize + add packages | `uv init && uv add requests openai python-dotenv` |
| 2. Install everything        | `uv sync`                                         |


---

### What Poetry and uv Replace

*Each row shows a manual step that modern tools automate.*


| Manual step you used to do       | Poetry does it for you                  | uv does it for you               |
| -------------------------------- | --------------------------------------- | -------------------------------- |
| `python3 -m venv venv`           | `poetry install` (auto-creates `.venv`) | `uv sync` (auto-creates `.venv`) |
| `source venv/bin/activate`       | `poetry run` / `poetry shell`           | `uv run` (no activation needed)  |
| `pip install requests`           | `poetry add requests`                   | `uv add requests`                |
| `pip freeze > requirements.txt`  | `poetry.lock` (auto-generated)          | `uv.lock` (auto-generated)       |
| Manually edit `requirements.txt` | `poetry add` / `poetry remove`          | `uv add` / `uv remove`           |
| Hope versions don't conflict     | Resolves conflicts automatically        | Resolves conflicts automatically |
| Install Python from website      | Not supported                           | `uv python install 3.14`         |


---

### Poetry vs uv — When to Use Which?


|                | Poetry                            | uv                          |
| -------------- | --------------------------------- | --------------------------- |
| Written in     | Python                            | Rust                        |
| Speed          | Moderate                          | 10–100x faster              |
| Maturity       | Stable, widely adopted since 2018 | Newer (2024), growing fast  |
| Install Python | No                                | Yes                         |
| Config file    | `pyproject.toml`                  | `pyproject.toml`            |
| Lock file      | `poetry.lock`                     | `uv.lock`                   |
| Best for       | Teams already using Poetry        | New projects, speed matters |


---

### One-line summary

> `**requirements.txt*`* = a shopping list you write by hand.
> `**pyproject.toml**` = a smarter list with project info.
> **Poetry** = a manager that writes the list, shops, and organizes everything for you.
> **uv** = the same manager but on a sports car — does everything Poetry does, but 10–100x faster, and can even install Python for you.

---

## Summary

1. `**venv` & `requirements.txt`**: The classic foundation. You must know this — millions of projects still use it.
2. **The flaw**: `requirements.txt` cannot reliably lock transitive dependencies. The industry needed something stronger.
3. `**pyproject.toml`**: The modern configuration file that replaces `requirements.txt` + `setup.py`.
4. **Poetry**: The current industry standard. One command to install, lock, and run.
5. **uv**: The blazing-fast future. Same workflow, written in Rust.

The journey in this episode: **problem** (version conflicts) → **classic solution** (venv + requirements.txt) → **hidden flaw** (transitive dependencies) → **modern solution** (pyproject.toml + lockfiles with Poetry or uv). Each step fixed what the previous step left broken.

---

