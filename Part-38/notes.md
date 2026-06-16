# Part 38 — File Handling Part 2 (Production Level)

Part 37.1 = `open()` one file. Part 37.2 = working with **many files**, in the **right place**, **safely** — the way production code does.

> **Map of this whole part:**
>
>
> | Problem                          | Tool                      | Section |
> | -------------------------------- | ------------------------- | ------- |
> | Where do my files even go?       | `pathlib`                 | A       |
> | Find / loop over many files      | `glob`, `rglob`           | B       |
> | A crash corrupts my file         | atomic write + `tempfile` | C       |
> | Copy, move, zip, in-memory files | `shutil`, `io`, `gzip`    | D       |
> | User input touches my files      | security rules            | E       |
>

> Carry-over from Part 36: **files give your programs memory; every file = `open()` + a parser.**

---

## SECTION A — Paths (pathlib)

**Problem:** `open("notes.txt", "w")` creates the file — but **where?** In the folder the program was *launched from* (the "current directory"), not where your `.py` file lives. Launch it from a different folder and the file lands somewhere else. You lose control of where your data sits.

**Fix:** a **path** names the exact location. `pathlib` is the modern tool to build, inspect, and use paths.

**Map:**


| Need            | Tool                                         |
| --------------- | -------------------------------------------- |
| Build a path    | `Path("data") / "2026" / "report.txt"`       |
| Special folders | `Path.cwd()`, `Path.home()`                  |
| Path info       | `.name` `.stem` `.suffix` `.parent` `.parts` |
| Does it exist?  | `.exists()` `.is_file()` `.is_dir()`         |
| Make a folder   | `.mkdir(parents=True, exist_ok=True)`        |
| Read / write    | `.read_text()` `.write_text()`               |


### A.1 Relative vs Absolute

```python
from pathlib import Path

Path("data/notes.txt")                # relative — under the current directory
Path("/Users/shyam/data/notes.txt")   # absolute — this exact spot, always

print(Path.cwd())     # where the program is running from
print(Path.home())    # your home folder
```

### A.2 Build and Inspect a Path

```python
p = Path("data") / "reports" / "summary_2026.csv"

print(p)           # data/reports/summary_2026.csv
print(p.name)      # summary_2026.csv
print(p.stem)      # summary_2026
print(p.suffix)    # .csv
print(p.parent)    # data/reports
```

### A.3 Exists, Make Folder, Read, Write

```python
p = Path("data/message.txt")

p.parent.mkdir(parents=True, exist_ok=True)   # create "data/" if missing
p.write_text("Hello\n", encoding="utf-8")     # write (opens + closes for you)

if p.exists():
    print(p.read_text(encoding="utf-8"))      # Hello
```

- `parents=True` → also create missing parent folders
- `exist_ok=True` → don't crash if the folder already exists
- For append / more control, paths work with `open()`: `with open(p, "a", encoding="utf-8") as f:`

> `/` joins parts and works on Windows, Mac, and Linux. The old way (`os.path.join`, string `+`) still works but is clunkier and error-prone.

---

## SECTION B — Finding Many Files (glob)

**Problem:** real work is "do X to *every* `.txt` in this folder" — not one file at a time.

**Map:**


| Need                          | Tool                |
| ----------------------------- | ------------------- |
| Everything in a folder        | `dir.iterdir()`     |
| Match a pattern (this folder) | `dir.glob("*.txt")` |
| Match in sub-folders too      | `dir.rglob("*.py")` |
| Huge file, low memory         | `for line in file`  |


### B.1 The Core Pattern — Find + Loop

```python
from pathlib import Path

data = Path("data")
total = 0
for f in data.glob("*.txt"):
    words = len(f.read_text(encoding="utf-8").split())
    total += words
    print(f.name, words)        # notes.txt 120

print("Total:", total)
```

This — **find files with `.glob()`, process each in a loop** — is the foundation of every data pipeline.

### B.2 Search Sub-Folders Too

```python
for py in Path("my_project").rglob("*.py"):    # this folder AND every sub-folder
    print(py)
```

### B.3 Big Files — Stream Line by Line

`.read()` loads the whole file into memory; a 10 GB log crashes. Loop instead — memory stays low at any size:

```python
errors = 0
with open("server.log", "r", encoding="utf-8") as f:
    for line in f:
        if "ERROR" in line:
            errors += 1
print(errors)
```

---

## SECTION C — Safe Writing (Atomic Write)

**Problem:** writing straight to the real file is dangerous.

```python
with open("important.json", "w", encoding="utf-8") as f:
    f.write(big_string)    # crash / power cut here = half-written file, original gone
```

**Fix — atomic write:** write to a *temp* file, then **rename** it over the real one. A rename is all-or-nothing — you always end up with either the old file or the complete new file, never a half-file.

**Map:**


| Step             | Code                       |
| ---------------- | -------------------------- |
| 1. write to temp | `open(tmp, "w")`           |
| 2. force to disk | `f.flush()` + `os.fsync()` |
| 3. atomic swap   | `os.replace(tmp, path)`    |


### C.1 The Pattern

```python
import os
from pathlib import Path

def atomic_write_text(path, content, encoding="utf-8"):
    path = Path(path)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding=encoding) as f:
        f.write(content)
        f.flush()                 # Python buffer -> OS
        os.fsync(f.fileno())      # OS buffer -> physical disk
    os.replace(tmp, path)         # atomic rename
```

```python
atomic_write_text("config.json", '{"theme": "dark"}')
```

> This is how SQLite survives a power cut and Git never half-corrupts a commit. Use it for important user data.

### C.2 Scratch Space — tempfile

Need a throwaway file or folder? Don't hand-name `"temp.txt"`; use `tempfile` (unique name, OS temp location):

```python
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as d:          # whole folder, auto-deleted
    (Path(d) / "out.csv").write_text("a,b\n1,2\n")
    # ...use it...
# folder and contents gone here
```

> **Gotcha:** `os.replace()` is atomic only when temp and target are on the **same disk/partition**. Keep the temp file in the **same folder** as the target (`tempfile.mkstemp(dir=path.parent)`).

---

## SECTION D — Everyday Power Tools

**Map:**


| Need                                | Tool                        |
| ----------------------------------- | --------------------------- |
| Copy / move / delete / zip          | `shutil`                    |
| A "file" in memory (no disk)        | `io.StringIO`, `io.BytesIO` |
| Read/write `.gz`, `.zip` directly   | `gzip`, `zipfile`           |
| Find-and-replace in place           | `fileinput`                 |
| Huge file in chunks / random access | `f.read(size)`, `mmap`      |


### D.1 shutil — Terminal File Ops in Python

```python
import shutil

shutil.copy2("a.txt", "b.txt")        # copy (keep timestamps)
shutil.move("old.txt", "new.txt")     # move / rename
shutil.copytree("v1", "v2")           # copy a whole folder
shutil.make_archive("backup", "zip", "project_dir")   # -> backup.zip
shutil.rmtree("old_folder")           # delete folder + contents (PERMANENT — no recycle bin)
```

### D.2 In-Memory Files — StringIO / BytesIO

A file-like object that lives in memory, never touches disk (e.g. build a CSV to send over an API):

```python
import io, csv

buf = io.StringIO()
csv.writer(buf).writerows([["name", "age"], ["Alice", 30]])
print(buf.getvalue())     # name,age\r\nAlice,30\r\n
```

Use `io.BytesIO()` for binary (e.g. an image to send over HTTP).

### D.3 Compressed Files — Read Without Extracting

```python
import gzip
with gzip.open("server.log.gz", "rt", encoding="utf-8") as f:   # "rt" = text mode
    for line in f:
        ...
```

```python
from zipfile import ZipFile
with ZipFile("archive.zip") as z:
    print(z.namelist())                    # files inside
    data = z.read("data.csv").decode("utf-8")   # read one, no extract
```

### D.4 More Tools (When Needed)

- `fileinput.input(path, inplace=True, backup=".bak")` — find-and-replace a text file in place
- `while chunk := f.read(1024*1024):` — read a huge binary file 1 MB at a time
- `mmap` — map a huge file into memory for random access (large logs, model weights)

---

## SECTION E — File Security

**Rule:** the moment a path or filename comes from a user or the internet, it is a security boundary.

**Map:**


| Risk                                | Defense                                          |
| ----------------------------------- | ------------------------------------------------ |
| Path traversal (`../../etc/passwd`) | `.resolve()` + check it stays inside a safe root |
| Bad filename (`/`, `\`, `CON`)      | strip to safe characters                         |
| `eval` / `pickle` on untrusted file | never do it                                      |
| Giant upload fills memory           | check size first                                 |
| Two processes write at once         | file lock                                        |


### E.1 Path Traversal — The Classic Attack

A user sends `filename = "../../etc/passwd"` → reads the server's password file. Fix: resolve the final path and confirm it's still inside the safe folder.

```python
from pathlib import Path

SAFE_ROOT = Path("user_files").resolve()

def safe_open(filename):
    target = (SAFE_ROOT / filename).resolve()       # cleans up ".." and symlinks
    if SAFE_ROOT != target and SAFE_ROOT not in target.parents:
        raise PermissionError("path escapes safe folder")
    return target.read_bytes()
```

### E.2 Clean a Filename

```python
import re
from pathlib import Path

def safe_filename(name):
    name = Path(name).name                          # drop any folder part
    return re.sub(r"[^A-Za-z0-9._-]", "_", name) or "untitled"
```

### E.3 Quick Rules

- Never `eval()` / `exec()` file contents, and never `pickle.load()` an untrusted file — both can run arbitrary code.
- Check file size before reading into memory.
- Two processes writing one file → use a lock (see E.4).

### E.4 File Locking — Two Processes, One File

**Problem:** if two processes append at the same instant, their lines interleave and corrupt each other (`"Hello"` + `"World"` → `"HeWolrllod"`). A lock forces "one at a time" — the second writer waits its turn.

**Unix / macOS — `fcntl` (built-in):**

```python
import fcntl

with open("shared.log", "a", encoding="utf-8") as f:
    fcntl.flock(f.fileno(), fcntl.LOCK_EX)    # exclusive lock (others wait)
    f.write("Safe line\n")
    fcntl.flock(f.fileno(), fcntl.LOCK_UN)    # release
```

**Cross-platform (works on Windows too) — `portalocker`** (`pip install portalocker`):

```python
import portalocker

with open("shared.log", "a", encoding="utf-8") as f:
    portalocker.lock(f, portalocker.LOCK_EX)
    f.write("Safe line\n")
    portalocker.unlock(f)
```

- `LOCK_EX` = exclusive (one writer); `LOCK_SH` = shared (many readers, no writer)
- **When you need it:** multiple workers appending to one log, cron jobs updating the same JSON config, any shared file on a server.

> Real apps log with the `**logging`** module (levels, rotation, timestamps), not `open("app.log", "a")`. Full coverage in Part 41.

---

## Practice Assignment

Build a small file analysis tool:

1. `analyze_directory(dir_path)`:
  - Turn the string into a `Path`; raise `FileNotFoundError` if it doesn't exist
  - Find all `.txt` files with `.glob()`
  - For each: count lines, count words, size (`.stat().st_size`)
  - Return a list of dicts
2. `save_report_safely(results, output_path)`:
  - Write the report using the **atomic write** pattern (Section C)
3. `print_report(results)`:
  - Print a clean table + totals

Example output:

```
File Analysis Report
====================
notes.txt      — 15 lines, 120 words, 845 bytes
readme.txt     —  8 lines,  65 words, 412 bytes
todo.txt       — 22 lines, 180 words, 1,234 bytes
--------------------
Total: 3 files, 45 lines, 365 words, 2,491 bytes
```

Save as `src/file_analyzer.py`.

---



