# Part 36 — File Handling Part 1 (Reading and Writing)

In Parts 33–35, you learned to handle errors. Your programs can now survive when things go wrong. But there is still one big problem — **your programs forget everything when they stop**.

Every variable, list, and dictionary you have made so far lives in RAM. The moment your program closes, all of it is gone.

Files solve this. Write data to a file, and it stays on disk. Read it back later, and your program continues where it left off.

This is how every real app works:

- **Notes apps** save your notes to a file
- **Config files** (`.env`, `config.json`) hold settings on disk
- **AI agent memory** (`AGENTS.md`, `CLAUDE.md`) is a text file the agent reads each session
- **Log files** record what the server did at 3 AM
- **AI datasets, prompts, model weights** — all sit in files

By the end of this part, you will know the one Python function that powers every one of these: `open()`.

> **The 1% Edge:** Most tutorials teach `open()` like it is old news. You will learn it as the door to the AI era — because in 2026, files are still the foundation of every AI tool you use.

### The Big Idea — Files Are an Interface, Not Just Data

Every file you will ever touch follows the same pattern:

```
Layer 1: Bytes on disk           ← the OS gives you this
Layer 2: open() reads/writes     ← what you learn today
Layer 3: Encoding (UTF-8)        ← turns bytes into text
Layer 4: Format parser           ← json, csv, pypdf, openpyxl, PIL (Parts 38–39)
Layer 5: Your application logic  ← every app you build
```

A PDF is not magic. It is `open()` in binary mode + a PDF parser. Excel is `open()` + `openpyxl`. JSON is `open()` + `json.load()`. **Every format is just `open()` + a parser.**

> **Remember these three lines for the whole file handling arc:**
>
> 1. **Files give your programs memory.**
> 2. **Every file = `open()` + a parser.**
> 3. **This is the same function that powers every AI agent in 2026.**

---

## The Story — From Your Code to the Hard Disk

Before we write a single `open()`, let us understand the *why*. This is the story that connects everything you have learned so far to this moment. Follow it step by step.

### Step 1 — Watch Your Data Disappear (REPL Demo)

We will use one simple example through this whole part — a **to-do list**. Everyone understands a to-do list, and by the end of this part you will save a real one to a file (that is your practice assignment).

Remember the REPL from Part 5 — the interactive shell where you type Python and it answers back. Let us open it and build a small to-do list.

```python
>>> tasks = ["Learn file handling", "Build a notes app"]
>>> tasks.append("Practice Python daily")
>>> print(tasks)
['Learn file handling', 'Build a notes app', 'Practice Python daily']
```

Looks good. Now **close the REPL** (type `exit()`), then **open it again** and try to print your tasks:

```python
>>> print(tasks)
NameError: name 'tasks' is not defined
```

Gone. Completely gone. Your whole to-do list vanished.

And here is the important part — this is **not just a REPL thing**. Even when you run a proper `.py` file, the moment the program finishes, every variable inside it disappears. RAM is **temporary memory**. When the program ends, RAM is wiped clean.

```python
# todo.py
tasks = ["Learn file handling", "Build a notes app"]
print(tasks)    # works while running
# program ends here → tasks is gone forever
```

Run it again tomorrow, and the program remembers nothing. Your to-do list starts empty every single time. Useless for a real app.

### Step 2 — The Real Question

If computers forget everything when the program ends, then:

- How does your **bank** remember your balance?
- How does **WhatsApp** remember your chats?
- How does **ChatGPT** remember your conversation?

They all need to save data **permanently** — somewhere that survives after the program closes. The most basic way to do that is to write it to a **file** on your disk (SSD or hard disk).

### Step 3 — But the Computer Does Not Understand Text

So we want to save our to-do list permanently — write the task `"Learn file handling"` onto the SSD so it is still there tomorrow. But here is the next problem. Your computer does **not** understand English. It does not understand Kannada, images, or video.

The hardware understands only ONE thing:

```
0  and  1
```

A single `0` or `1` is called a **bit**. We group **8 bits together** and call it one **byte**.

Everything on the disk — your text, your photos, your Python code, a CSV file — is all just **bytes**. Just 0s and 1s.

### Step 4 — So How Does a Letter Become Bytes? (Callback to Part 9)

Our task starts with the letter `L` ("Learn file handling"). So how does a letter like `L` — or `A`, or any character — become 0s and 1s?

Remember in Part 9 we learned that the letter `'A'` is actually the number `65`, and `65` in binary is `1000001`?

```python
>>> ord('A')        # the number for 'A'
65
>>> bin(ord('A'))   # that number in binary (0s and 1s)
'0b1000001'
```

**Quick binary recall (from Part 9):**

```
1 bit = one switch:   0 = OFF      1 = ON

A byte = 8 bits. Each position has a "place value" (powers of 2):

   place value:  128   64   32   16    8    4    2    1
   the byte 'A':   0    1    0    0     0    0    0    1
                        └──────────────────────────┘
   turn ON the place values where the bit is 1:
        64 + 1  =  65        and        65 = 'A'   ✓

Each extra bit DOUBLES how many values you can make:

   1 bit  -> 2           5 bits -> 32
   2 bits -> 4           6 bits -> 64
   3 bits -> 8           7 bits -> 128   <- ASCII   (values 0–127)
   4 bits -> 16          8 bits -> 256   <- one byte (values 0–255)
```

But here is the question almost nobody asks: **who decided that `'A'` should be `65` and not `99`?**

That rulebook — the one that maps every character to a number, and then to bytes — is called **encoding**. The story of encoding has three stages:

1. **ASCII (1960s) — the first rulebook.** This is where `'A' = 65` comes from. ASCII had only 128 characters — English letters, digits, and punctuation. That is all. No Kannada, no Hindi, no emoji.
2. **Regional rulebooks — the chaos.** Because ASCII could not handle other languages, every region invented its own rulebook. They clashed. A file written in one country turned into garbage when opened in another.
3. **UTF-8 (1990s) — the one rulebook for the whole world.** UTF-8 can handle every language on Earth — English, Kannada, Hindi, Chinese — and even emoji. It kept ASCII's numbers (`'A'` is still `65`) but extended them to cover everything.

In 2026, **UTF-8 has won** — more than 98% of the internet uses it. So whenever we open a text file, we tell Python to use this rulebook: `encoding="utf-8"`. (Full history with examples in Section C.)

> **📖 See the rulebook yourself (show this to prove it):**
>
> - **The simplest proof — Python itself:** `ord('A')` returns `65`. No website needed.
> - **'A' on the official-style lookup:** [compart.com/en/unicode/U+0041](https://www.compart.com/en/unicode/U+0041) — shows the code point `U+0041` and the exact UTF-8 bytes (`0x41`). The decimal `65` appears in the **HTML Entity** row as `A` (an HTML `&#nnn;` entity uses the decimal code point; `0x41` hex = `65` decimal).
> - **A friendly ASCII table with a clear Decimal column:** [ascii-code.com](https://www.ascii-code.com/) — find the row `Dec = 65` and you will see `A`.
> - **The official Unicode chart** (the actual rulebook): [Unicode "Basic Latin" code chart (PDF)](https://www.unicode.org/charts/PDF/U0000.pdf) — the same grid that started as ASCII; `A` sits at position `41` (hex) = `65` (decimal). Full index: [unicode.org/charts](https://www.unicode.org/charts/).
> - **The Kannada rulebook:** Kannada is *not* in ASCII — it has its own chart. Official: [Unicode "Kannada" code chart (PDF)](https://www.unicode.org/charts/PDF/U0C80.pdf) (block `U+0C80`–`U+0CFF`) · browse it on [compart.com (Kannada block)](https://www.compart.com/en/unicode/block/U+0C80) · the letter ಕ = [U+0C95](https://www.compart.com/en/unicode/U+0C95).

**The "1 byte vs 3 bytes" moment — show this live:** `A` kept ASCII's old number, so UTF-8 stores it in **1 byte**. Kannada came later, so it needs **3 bytes**. That is exactly why UTF-8 uses "1 to 4 bytes per character":

```python
>>> ord('A'), ord('ಕ')          # the numbers (code points)
(65, 3221)
>>> 'A'.encode('utf-8')          # English -> 1 byte
b'A'
>>> 'ಕ'.encode('utf-8')          # Kannada -> 3 bytes
b'\xe0\xb2\x95'
>>> len('A'.encode('utf-8')), len('ಕ'.encode('utf-8'))
(1, 3)
```

### Step 5 — Other Files Have Their Own Rulebooks

UTF-8 is only for **text** (`.txt`, `.csv`, `.json`, `.py`, `.md` — all text).

But an image? A PDF? Those are not text. They have their OWN rulebooks:

- A `.jpg` follows the **JPEG** rules
- A `.pdf` follows the **PDF** rules
- An `.mp3` follows the **MP3** rules

We call this the **file format** — the rules for what the bytes mean. (We work with these formats in Parts 38–39.)

### Step 6 — Where Do the Bytes Physically Go?

Now I have turned my text into bytes. I want to save them on the SSD. But the SSD has millions of empty spaces — **who decides where my bytes go, and how to find them again later?**

That job belongs to the **file system** — `NTFS` on Windows, `ext4` on Linux, `APFS` on Mac. Think of it as the city planning for your disk: it decides which house (your bytes) goes on which street (folder), and keeps the address so it can find it later.

### Step 7 — The Door: open()

So now look at the whole world that lives *under* a file:

```
Your Python program
        │
     ╔══╧══╗
     ║ open() ║   ← THE DOOR. The only way in.
     ╚══╤══╝
        │
   Encoding (UTF-8)        → turns characters into bytes
        ↓
   File format (.txt .jpg .pdf)  → rules for what the bytes mean
        ↓
   File system (NTFS, ext4, APFS) → decides where bytes go on disk
        ↓
   SSD / Hard Disk         → stores the raw 0s and 1s
```

Here is the final question: how does **your program** reach into all of that?

You will not talk to the SSD directly. You will not talk to the file system yourself. Python gives you **one doorway** — one built-in function — that handles all of it for you. It is called `**open()`**.

`open()` is the first command you learn that connects your code directly to the hardware — to permanent storage. You tell it *which file* and *what you want to do* (read it, write it, add to it), and it handles everything underneath.

**That is why file handling matters. `open()` is the door. Let us open it.**

---

## What You Will Learn (5 Small Sections)

This part is split into 5 small sections so you can follow it one at a time:

- **Section A — The Basics** → `open()`, modes, `with`, read, write, append
- **Section B — Text Mode vs Binary Mode** → `str` and `bytes`, when to use each
- **Section C — Encoding (UTF-8)** → why Kannada, Hindi, and emoji need it, plus which format uses which encoding and library
- **Section D — The File Pointer** → `tell()` and `seek()`
- **Section E — Real-World Patterns** → exception handling, common bugs, where this is used

Then a practice assignment.

---

## SECTION A — The Basics

### A.1 Opening a File with open()

```python
file = open("example.txt", "r")
content = file.read()
print(content)
file.close()
```

`open()` takes two main arguments — the **file name** and the **mode** (how you want to use the file). 📖 Reference: [open() — Python docs](https://docs.python.org/3/library/functions.html#open).

### A.2 The Four Basic Modes


| Mode  | Purpose    | Behavior                                    |
| ----- | ---------- | ------------------------------------------- |
| `"r"` | Read       | File must exist. Error if missing.          |
| `"w"` | Write      | Creates file. **Overwrites** if it exists.  |
| `"a"` | Append     | Creates file. Adds to the end if it exists. |
| `"x"` | Create new | Creates file. Error if it already exists.   |


### A.3 The with Statement — Always Use This

```python
with open("example.txt", "r") as file:
    content = file.read()
    print(content)
```

`with` automatically closes the file when the block ends — even if an error happens.

Without `with`, you must remember to call `file.close()` yourself. If an error happens before `close()`, the file stays open. Too many open files and the OS will stop your program from opening more.

```python
# Bad — file stays open if an error happens
file = open("data.txt", "r")
content = file.read()   # if this crashes, file.close() never runs
file.close()

# Good — file always closes
with open("data.txt", "r") as file:
    content = file.read()   # even if this crashes, the file closes
```

**Rule: always use `with` when working with files.** 📖 More on the `with` statement and context managers: [Python docs — the with statement](https://docs.python.org/3/reference/compound_stmts.html#the-with-statement).

### A.4 Reading Files — Four Ways

`**.read()` — get the whole file as one string**

```python
with open("example.txt", "r") as file:
    content = file.read()
    print(content)
```

`**.readline()` — read one line at a time**

```python
with open("example.txt", "r") as file:
    first_line = file.readline()
    second_line = file.readline()
```

The newline character `\n` is included at the end of each line.

`**.readlines()` — get all lines as a list**

```python
with open("example.txt", "r") as file:
    lines = file.readlines()
    print(lines)   # ['Line 1\n', 'Line 2\n', 'Line 3\n']
```

**Looping line by line (best for big files)**

```python
with open("example.txt", "r") as file:
    for line in file:
        print(line.strip())
```

This reads one line at a time without loading the whole file into memory. For a 10 GB log file, this is the only safe way.

### A.5 Writing Files

```python
with open("output.txt", "w") as file:
    file.write("Hello, World!\n")
    file.write("This is line 2.\n")
```

`"w"` mode creates the file if it does not exist. If the file already exists, **it erases the old content first**.

You can also write a list of strings with `.writelines()`:

```python
lines = ["Line 1\n", "Line 2\n", "Line 3\n"]

with open("output.txt", "w") as file:
    file.writelines(lines)
```

> `.writelines()` does NOT add newlines for you — include `\n` yourself.

### A.6 Appending to Files

```python
with open("log.txt", "a") as file:
    file.write("New entry added.\n")
```

`"a"` adds content to the end of the file without erasing what is already there. If the file does not exist, it creates one.

**Watch out — `"w"` vs `"a"` is one of the most common bugs:**

```python
# This ERASES the file and starts fresh
with open("data.txt", "w") as file:
    file.write("Only this remains.\n")

# This ADDS to the end of the file
with open("data.txt", "a") as file:
    file.write("This is added at the bottom.\n")
```

If you overwrite when you meant to append, your old data is gone forever.

---

## SECTION B — Text Mode vs Binary Mode

### B.1 Two Kinds of Files

So far, every file we opened was a **text file** — readable in any editor. Python reads them as `str` (regular Python strings).

But not every file is text. Images, PDFs, ZIP files, music, AI model weights — these are **binary files**. They store raw bytes, not characters. To work with them, you add `b` to the mode:


| Mode   | Meaning       | What You Get    |
| ------ | ------------- | --------------- |
| `"r"`  | Read text     | `str`           |
| `"w"`  | Write text    | accepts `str`   |
| `"rb"` | Read binary   | `bytes`         |
| `"wb"` | Write binary  | accepts `bytes` |
| `"ab"` | Append binary | accepts `bytes` |


### B.2 Reading Text vs Reading Bytes

```python
with open("notes.txt", "r", encoding="utf-8") as f:
    content = f.read()
print(type(content))    # <class 'str'>
print(content)          # Hello, world!

with open("photo.jpg", "rb") as f:
    raw = f.read()
print(type(raw))        # <class 'bytes'>
print(raw[:10])         # b'\xff\xd8\xff\xe0\x00\x10JFIF'
```

The first call gives you a string. The second gives you raw bytes — exactly what is on disk.

### B.3 When You Need Binary Mode

- **Images** (`.jpg`, `.png`, `.webp`) — every multimodal AI app reads images as bytes
- **PDFs** (`.pdf`) — PDF files are binary even though they contain text
- **ZIP, GZIP, TAR** — compressed files
- **AI model files** (`.pt`, `.safetensors`, `.bin`)
- **Audio, video** files
- Whatever you get from `requests.get(...).content`

### B.4 Converting Between str and bytes

`str` and `bytes` are different types, but you can switch between them when the data is actually text:

```python
text = "Hello, ಕನ್ನಡ"

raw = text.encode("utf-8")           # str  -> bytes
print(raw)                           # b'Hello, \xe0\xb2\x95\xe0\xb2\xa8...'

back = raw.decode("utf-8")           # bytes -> str
print(back)                          # Hello, ಕನ್ನಡ
```

> **Simple rule:** if a human reads it, use text mode with `encoding="utf-8"`. If it is an image, PDF, ZIP, or model file, use binary mode (`"rb"` / `"wb"`) and work with `bytes`.

### B.5 Copying a Binary File

```python
with open("photo.jpg", "rb") as src:
    with open("photo_copy.jpg", "wb") as dst:
        dst.write(src.read())
```

You will use this same pattern when saving file uploads, downloading images for AI models, or saving images that an LLM generated.

---

## SECTION C — Encoding (UTF-8 is the Right Choice)

### C.1 What Is Encoding?

When Python opens a file in text mode, it has to decide how to turn bytes on disk into the letters you see on screen. That decision is called the **encoding**. 📖 Deep dive: [Python Unicode HOWTO](https://docs.python.org/3/howto/unicode.html) · [list of standard encodings](https://docs.python.org/3/library/codecs.html#standard-encodings).

```python
with open("data.txt", "r", encoding="utf-8") as file:
    content = file.read()

with open("data.txt", "w", encoding="utf-8") as file:
    file.write("ಕನ್ನಡ text\n")
```

### C.2 Short History (1 Minute)

- **ASCII (1963)** — only 128 characters. English letters, digits, punctuation. No Kannada, no Hindi, no emoji.
- **cp1252, ISO-8859-1, Shift-JIS, GB2312** — every region made its own encoding. Files broke when sent between countries.
- **UTF-8 (1993)** — one encoding that handles every language and every emoji. Uses 1 to 4 bytes per letter.

In 2026, **UTF-8 has won.** More than 98% of the web uses UTF-8. Every modern API, database, and AI model expects UTF-8. 📖 Worth a read: [The Absolute Minimum Every Developer Must Know About Unicode](https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/) · [unicode.org — what is Unicode?](https://home.unicode.org/basic-info/faq/) · [UTF-8 spec (RFC 3629)](https://datatracker.ietf.org/doc/html/rfc3629).

### C.3 What Goes Wrong Without It

Without `encoding="utf-8"`, Python uses your system default — which is:

- **Linux / macOS:** usually UTF-8 (safe)
- **Windows:** often `cp1252` — which **cannot store** Kannada, Hindi, Tamil, Chinese, Japanese, or emoji

A file written on Windows without `encoding="utf-8"` will fail when read on another system.

```python
# On a Windows machine without encoding specified:
with open("greeting.txt", "w") as f:
    f.write("ಕನ್ನಡ")    # UnicodeEncodeError: 'charmap' codec can't encode characters
```

```python
# The fix — works on every OS:
with open("greeting.txt", "w", encoding="utf-8") as f:
    f.write("ಕನ್ನಡ")
```

### C.4 The `errors=` Option

Sometimes you read a file from an unknown source and it has bad bytes. You have three options:

```python
# 1. Default — crash on bad bytes (safest)
open("data.txt", "r", encoding="utf-8", errors="strict")

# 2. Replace bad bytes with � markers
open("data.txt", "r", encoding="utf-8", errors="replace")

# 3. Silently skip bad bytes
open("data.txt", "r", encoding="utf-8", errors="ignore")
```

Use `"replace"` for log files where you would rather see *something* than crash. Use `"strict"` (the default) everywhere else. 📖 All handlers: [codecs — error handlers](https://docs.python.org/3/library/codecs.html#error-handlers).

### C.5 The Excel Trap — utf-8-sig

Microsoft Excel saves CSV files with a hidden 3-byte marker at the start (called the **BOM** — [byte order mark](https://en.wikipedia.org/wiki/Byte_order_mark)). Reading such a file with plain UTF-8 leaves a strange `\ufeff` character in your first column.

```python
# CSV exported from Excel — use utf-8-sig to remove the hidden marker
with open("from_excel.csv", "r", encoding="utf-8-sig") as f:
    content = f.read()
```

> **Two simple rules:**
>
> - Always pass `encoding="utf-8"` when opening text files
> - Use `encoding="utf-8-sig"` for CSVs from Excel

### C.6 Characters vs Code Points vs Bytes vs Graphemes

This is where many developers get confused — even after they learn UTF-8.

- **Bytes** — what is actually on disk (0–255 values)
- **Code points** — Unicode numbers for each symbol (U+0041 = "A", U+0C95 = "ಕ"). Look up any character — number, UTF-8 bytes, and name — at [compart.com/en/unicode](https://www.compart.com/en/unicode/) or the official [Unicode code charts](https://www.unicode.org/charts/)
- **Characters (`str`)** — what Python stores in memory (a sequence of code points)
- **Grapheme clusters** — what a human sees as one "letter" (may be multiple code points)

```python
text = "🤦🏽‍♂️"
print(len(text))           # 5  (five code points, not one emoji)
print(len(text.encode("utf-8")))   # 17 bytes on disk
```

When you build a chat app, a search feature, or a character counter — `len()` counts code points, not what the user sees on screen. For user-facing length limits, you may need a library like [grapheme](https://pypi.org/project/grapheme/) (`pip install grapheme`) later. For now, just know the difference exists. 📖 More: [Unicode HOWTO — the string type](https://docs.python.org/3/howto/unicode.html#the-string-type).

### C.7 Mojibake — When Text Looks Like Garbage

**Mojibake** means "garbled text." It happens when bytes are decoded with the **wrong encoding**.

```python
original = "ಕನ್ನಡ"
raw = original.encode("utf-8")        # correct bytes

# Wrong — decode UTF-8 bytes as Latin-1:
garbled = raw.decode("latin-1")
print(garbled)   # looks like nonsense: à²¨à³à²¡

# Fix — decode with the same encoding used to encode:
fixed = raw.decode("utf-8")
print(fixed)     # ಕನ್ನಡ
```

You will see mojibake when:

- A file was saved on Windows with `cp1252` and opened as UTF-8
- An API sends bytes but you call `.text` with the wrong encoding
- Someone double-encodes text (encode then encode again)

**Rule:** always know which encoding was used to create the bytes. When in doubt, try UTF-8 first.

### C.8 Unicode Normalization — When "Same" Text Is Not Equal

The same visual text can be stored two different ways in Unicode:

```python
import unicodedata

a = "café"    # é as one character (U+00E9)
b = "café"    # e + combining accent (U+0065 + U+0301)

print(a == b)              # False — different bytes!

# Fix — normalize before comparing:
print(unicodedata.normalize("NFC", a) == unicodedata.normalize("NFC", b))   # True
```

**When to normalize:**

- Before comparing user input (search, dedup, login names)
- Before saving to a database
- Before hashing or indexing text

**Use `"NFC"`** for storage and display. That is what macOS and the web use by default. 📖 Reference: [unicodedata.normalize()](https://docs.python.org/3/library/unicodedata.html#unicodedata.normalize) · [Unicode normalization forms (UAX #15)](https://unicode.org/reports/tr15/).

### C.9 Python Is Moving to UTF-8 by Default (PEP 597 and PEP 686)

Python is slowly making UTF-8 the default everywhere:

- **[PEP 597](https://peps.python.org/pep-0597/)** — you can turn on `EncodingWarning` today to find code that forgets `encoding=`. Run with `-X warn_default_encoding` or set `PYTHONWARNDEFAULTENCODING=1`.
- **[PEP 686](https://peps.python.org/pep-0686/)** — Python 3.15 will make UTF-8 mode the default on all platforms.

If you **do** want the OS locale encoding (rare), be explicit:

```python
with open("legacy.txt", "r", encoding="locale") as f:
    content = f.read()
```

For everything else in 2026: `**encoding="utf-8"**`. No exceptions in your code.

### C.10 One Byte, Many Meanings (Text vs Image vs CSV)

A common confusion: "is the binary *different* for an image?" No. **Turning 8 bits into a number is always the same math** — the place values never change:

```
bits:         0   1   0   0   0   0   0   1
place value: 128  64  32  16   8   4   2   1
            = 64 + 1 = 65        ← every file does this identical step
```

A byte is **always** a number from 0 to 255. What changes is the **rulebook** (the file format) that decides what that number *means*:


| The byte `01000001` = `65` read as… | Means                                                |
| ----------------------------------- | ---------------------------------------------------- |
| **UTF-8 / text**                    | the letter `'A'`                                     |
| **a grayscale image**               | a pixel's brightness — `65` out of `255` → dark gray |
| **raw audio**                       | how far the speaker moves at this instant            |


Same 0s and 1s on disk. Same number. **The format decides the meaning.** Prove it in one line:

```python
b = 0b01000001        # one byte of 0s and 1s
print(b)              # 65    -> the number is always the same
print(chr(b))         # 'A'   -> the TEXT rulebook says 65 = letter A
# the IMAGE rulebook would say: 65 = a dark-gray pixel (0=black, 255=white)
```

**Images don't change the math — they group the bytes differently.** Text reads *one byte = one character*. A raw image reads bytes in *groups of 3 = one pixel* (Red, Green, Blue), after a small header that says "I'm an image, 2 wide, 2 tall":

```
2x2 image:           bytes on disk (each 0-255):
┌─────┬─────┐        FF 00 00 | 00 FF 00 | 00 00 FF | FF FF FF
│ red │green│        └pixel 1┘  └pixel 2┘  └pixel 3┘  └pixel 4┘
├─────┼─────┤         red        green      blue       white
│blue │white│
└─────┴─────┘
```

That is why opening an image with `encoding="utf-8"` crashes with `UnicodeDecodeError` (see B.2): you are handing pixel bytes to the *text* rulebook, and they are not valid letters.

**CSV is the opposite surprise — it is still plain UTF-8 text.** Every byte is a normal letter. The CSV parser just gives a *structural* job to two characters:

```
name,age         comma   (byte 44)  ->  "next column"
Alice,30         newline (byte 10)  ->  "next row"
Bob,25
```

The parser turns that flat text into a table:

```python
[["name", "age"], ["Alice", "30"], ["Bob", "25"]]
```

> **The one-line mental model:** **bits → number** is universal math; **number → meaning** is the format's rulebook. Text speaks UTF-8, images group bytes into pixels, CSV is text + comma/newline rules. Use the wrong rulebook and you get garbage.

### C.11 Which Format Uses Which Encoding (and Which Library Opens It)

Every file falls into one of **two buckets**. This is the single most useful thing to remember from this whole part:

> **Text files** → read with a **character encoding** (UTF-8). Open with `encoding="utf-8"`.
> **Binary files** → **no** character encoding; the format has its own spec. Open with `rb` / `wb`.
>
> Quick test: if Notepad shows readable words, it is **text → UTF-8**. If it shows garbage, it is **binary → `rb`**.

**Bucket 1 — TEXT formats (these use UTF-8):**

Every text file goes through **two layers**, and a parser is only the *second* one:

```
raw bytes
   |   Layer 1: DECODE with UTF-8   <- ALWAYS happens, built into open(encoding="utf-8")
   v
a plain string (just characters)
   |   Layer 2: PARSE the structure <- ONLY if the format has structure
   v
a Python object (dict / list / table)
```

So **plain text like `.txt` and `.log` needs no parser** — the string you get back is the final answer. Only *structured* text (`.csv`, `.json`, `.yaml`…) needs a Layer-2 parser:


| Format              | Daily use                                | Needs a parser?                   | Library (the parser)                                                                                                                                   | Built-in or pip?       |
| ------------------- | ---------------------------------------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------- |
| `.txt`              | notes, logs, scratch data                | No — just a string                | *(just `open`)*                                                                                                                                        | built-in               |
| `.log`              | server logs                              | No — read line by line            | *(just `open`)*                                                                                                                                        | built-in               |
| `.md`               | READMEs, docs, AI agent memory           | No to read (Yes to render)        | *(text)* / [markdown](https://pypi.org/project/Markdown/)                                                                                              | pip *(only to render)* |
| `.py .js .css .sql` | source code                              | Not by you — the interpreter does | *(text editor)*                                                                                                                                        | built-in               |
| `.csv`              | spreadsheets, data exports               | Yes                               | [csv](https://docs.python.org/3/library/csv.html)                                                                                                      | built-in               |
| `.json`             | REST API requests/responses, config      | Yes                               | [json](https://docs.python.org/3/library/json.html)                                                                                                    | built-in               |
| `.jsonl`            | AI datasets, agent logs, fine-tuning     | Yes (one per line)                | [json](https://docs.python.org/3/library/json.html)                                                                                                    | built-in               |
| `.yaml`             | Docker, Kubernetes, CI/CD config         | Yes                               | [pyyaml](https://pyyaml.org/wiki/PyYAMLDocumentation)                                                                                                  | pip                    |
| `.toml`             | Python project config (`pyproject.toml`) | Yes                               | [tomllib](https://docs.python.org/3/library/tomllib.html) (read)                                                                                       | built-in (3.11+)       |
| `.xml` / `.html`    | web pages, old APIs, configs             | Yes                               | [ElementTree](https://docs.python.org/3/library/xml.etree.elementtree.html) / [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) | built-in / pip         |
| `.env`              | secrets, API keys                        | Yes                               | [python-dotenv](https://pypi.org/project/python-dotenv/)                                                                                               | pip                    |


**Bucket 2 — BINARY formats (NO UTF-8 — own spec, open with `rb`/`wb`):**


| Format                  | What the bytes really are           | Library                                                                                                                                                                     | Built-in or pip? |
| ----------------------- | ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- |
| `.jpg .png .webp .gif`  | pixels (RGB) + compression          | [Pillow](https://pillow.readthedocs.io/) (`from PIL import Image`)                                                                                                          | pip              |
| `.pdf`                  | text + layout in a binary container | [pypdf](https://pypdf.readthedocs.io/)                                                                                                                                      | pip              |
| `.xlsx`                 | a ZIP of XML files!                 | [openpyxl](https://openpyxl.readthedocs.io/)                                                                                                                                | pip              |
| `.docx`                 | a ZIP of XML files!                 | [python-docx](https://python-docx.readthedocs.io/) (`import docx`)                                                                                                          | pip              |
| `.zip` / `.gz` / `.tar` | compressed bytes                    | [zipfile](https://docs.python.org/3/library/zipfile.html) / [gzip](https://docs.python.org/3/library/gzip.html) / [tarfile](https://docs.python.org/3/library/tarfile.html) | built-in         |
| `.sqlite` / `.db`       | a whole database in one file        | [sqlite3](https://docs.python.org/3/library/sqlite3.html)                                                                                                                   | built-in         |
| `.parquet`              | columnar data (big analytics)       | [pyarrow](https://arrow.apache.org/docs/python/) / [pandas](https://pandas.pydata.org/docs/)                                                                                | pip              |
| `.pt` / `.safetensors`  | AI model weights (numbers)          | [torch](https://pytorch.org/docs/stable/index.html) / [safetensors](https://huggingface.co/docs/safetensors/)                                                               | pip              |


**Library vs parser vs serializer** — say it precisely and you sound senior:

```
LIBRARY / MODULE   <- the toolbox you import (json, csv, PIL, openpyxl)
   |-- PARSER      <- reads bytes  ->  Python object   (the "in" direction)
   '-- SERIALIZER  <- Python object ->  bytes          (the "out" direction)
```

**What does "serialize" mean?** A Python object (like a dict) lives in RAM, but a disk only stores flat bytes — you cannot write a living dict straight to a file. **Serialize = flatten the object into text/bytes you can save** (the chair won't fit through the door, so you flat-pack it into a box). **Parse = rebuild the object** from those bytes (reassemble the chair). The verbs say it directly: **dump** = out, **load** = in.

```python
import json
data = {"name": "Alice", "age": 30}   # a Python object in RAM
text = json.dumps(data)               # SERIALIZE -> '{"name": "Alice", "age": 30}'  (flat text, ready to save)
back = json.loads(text)               # PARSE     -> {"name": "Alice", "age": 30}    (a real dict again)
```

So `json`, `csv`, and `openpyxl` are **libraries**. Each gives you a **parser** to read and a **serializer** to write:


| Format  | Read (parser)                  | Write (serializer)             |
| ------- | ------------------------------ | ------------------------------ |
| `.json` | `json.load()` / `json.loads()` | `json.dump()` / `json.dumps()` |
| `.csv`  | `csv.reader()`                 | `csv.writer()`                 |
| `.yaml` | `yaml.safe_load()`             | `yaml.safe_dump()`             |
| `.toml` | `tomllib.load()`               | `tomli_w.dump()`               |
| images  | `Image.open()` (decoder)       | `img.save()` (encoder)         |


The verbs all point at the same two directions: **read** = parse / decode / deserialize / **load**; **write** = serialize / encode / **dump**. (For images/audio/video the right word is **codec** — decode/encode — not "parser", because the job is decompress/compress, not parse text.)

> **Two gotchas engineers love:** (1) `.xlsx` and `.docx` are secretly **ZIP files** full of UTF-8 XML — rename one to `.zip` and unzip it to see. (2) The **pip name often differs from the import name**: `pip install pillow` → `import PIL`; `pip install beautifulsoup4` → `from bs4 import ...`; `pip install python-dotenv` → `from dotenv import ...`.

---

## SECTION D — The File Pointer (tell and seek)

### D.1 What Is the File Pointer?

When you open a file, Python keeps track of **where you currently are** inside the file. This position is called the **file pointer** (or cursor). Every read or write moves it forward.

Understanding the pointer will save you from one of the most confusing file bugs in Python — "I wrote, but reading shows nothing!"

### D.2 tell() — Where Am I?

```python
with open("greeting.txt", "w", encoding="utf-8") as f:
    print(f.tell())          # 0  (start of file)
    f.write("Hello")
    print(f.tell())          # 5  (wrote 5 characters)
    f.write(", world!")
    print(f.tell())          # 13
```

`tell()` gives you the current position, counted in bytes from the start. 📖 Reference: [io — tell() and seek()](https://docs.python.org/3/library/io.html#io.IOBase.seek) (the file methods Python gives every open file).

### D.3 seek() — Jump to a Position

`seek(offset, whence)` moves the pointer. The second argument tells it where to measure from:


| `whence` | Means                     |
| -------- | ------------------------- |
| `0`      | From the start (default)  |
| `1`      | From the current position |
| `2`      | From the end              |


```python
with open("greeting.txt", "r", encoding="utf-8") as f:
    f.seek(0)             # jump to start
    print(f.read(5))      # Hello

    f.seek(7)             # jump to byte 7
    print(f.read())       # world!

    f.seek(0, 2)          # jump to the end
    print(f.tell())       # 13
```

### D.4 The + Modes — Read and Write in One File

The four basic modes from Section A (`r`, `w`, `a`, `x`) do only **one** job each — read OR write. Add a `+` to the mode and the file opens for **both** reading and writing at the same time:


| Mode   | Read? | Write? | File must exist?       | Erases existing content? | Pointer starts at |
| ------ | ----- | ------ | ---------------------- | ------------------------ | ----------------- |
| `"r+"` | yes   | yes    | yes (error if missing) | no                       | start             |
| `"w+"` | yes   | yes    | no (creates it)        | **yes — wipes it**       | start             |
| `"a+"` | yes   | yes    | no (creates it)        | no                       | end               |


These modes only make sense together with `seek()` — because you are jumping back and forth in the same open file. That is exactly why we cover them here, in the file-pointer section.

```python
# r+  : the file must already exist; read it, then update it
with open("notes.txt", "r+", encoding="utf-8") as f:
    old = f.read()           # read everything (pointer moves to the end)
    f.write("\nNew line")    # write continues from where we are (the end)
```

> Quick rule: use `"r+"` to update an existing file, `"w+"` to create-and-rewrite, `"a+"` to add-and-occasionally-read. If you only need one job (just read, or just write), stick with the simple `r`, `w`, or `a`.

### D.5 The Classic "Why Is My File Empty?" Bug

```python
with open("data.txt", "w+", encoding="utf-8") as f:
    f.write("Hello, world!")
    content = f.read()       # returns ""
    print(f"Content: '{content}'")
```

Why is `content` empty? Because `"w+"` opens for read and write, but after `write()`, the pointer is at the **end** of the file. There is nothing left to read.

The fix is to `seek(0)` before reading:

```python
with open("data.txt", "w+", encoding="utf-8") as f:
    f.write("Hello, world!")
    f.seek(0)                # jump back to the start
    content = f.read()
    print(f"Content: '{content}'")    # Hello, world!
```

> For text mode, only use `seek()` with `0` (start) or with values you got back from `tell()`. In binary mode, `seek()` works with exact byte positions.

---

## SECTION E — Real-World Patterns

### E.1 Combining with Exception Handling

What if the file does not exist? Use try/except:

```python
def read_file_safe(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return None

content = read_file_safe("missing.txt")
if content is not None:
    print(content)
```

### E.2 A Complete Read-Write Example

```python
def save_items(filename, items):
    """Save a list of items to a file, one per line."""
    with open(filename, "w", encoding="utf-8") as file:
        for item in items:
            file.write(f"{item}\n")

def load_items(filename):
    """Load items from a file, one per line."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        return []

# Save
tasks = ["Buy milk", "Study Python", "Exercise"]
save_items("tasks.txt", tasks)

# Load
loaded = load_items("tasks.txt")
print(loaded)   # ['Buy milk', 'Study Python', 'Exercise']
```

### E.3 Common Bugs to Avoid

1. **FileNotFoundError** — reading a file that does not exist. Use try/except.
2. **Overwriting when you meant to append** — `"w"` erases everything. Use `"a"` to add.
3. **Forgetting encoding** — leads to crashes on Kannada, Hindi, or emoji.
4. **Not stripping newlines** — `readline()` and `for line in file:` include `\n`. Use `.strip()`.
5. **Reading huge files with .read()** — loads it all into RAM. Loop line by line instead.
6. **Mixing text and binary modes** — `.write("hello")` on a `"wb"` file gives a `TypeError`. Encode first.
7. **Read right after write without `seek(0)`** — pointer is at the end, you get empty string.
8. **Excel BOM in CSV files** — use `encoding="utf-8-sig"` for files saved by Excel.

### E.4 Where This Is Used in Real Work

- **Config files:** Apps read `config.json`, `.env` at startup. All use `open()`.
- **Log files:** Servers write log lines continuously. Engineers read these files to debug.
- **Saving user data:** Simple apps store data in text files. Bigger apps use databases — but every database eventually imports and exports as files.
- **Reports:** Reading documents, writing summaries — all `open()`.
- **Data pipelines:** Raw data arrives as CSV / JSON / text. Processed results go back to files.
- **AI training data:** Every dataset (Hugging Face, Kaggle, OpenAI fine-tuning) is a file.
- **AI agent memory:** Cursor, Claude Code, Continue, Devin — they all keep memory in `.md` files. You will build one in Part 39.
- **Multimodal AI:** Sending an image to GPT-4o means opening it in binary mode and encoding the bytes. You will do this in Part 39.

### E.5 print() Is Also a File Write

Here is a mind-blowing connection: `**print()` writes to a file.**

```python
import sys

with open("output.txt", "w", encoding="utf-8") as f:
    print("Hello", file=f)           # same as f.write("Hello\n")

print("On screen")                   # same as sys.stdout.write("On screen\n")
```

When you type `print("hello")`, Python writes to `sys.stdout` — which is a file object connected to your terminal. Same `open()` primitive. Different destination.

### E.6 When Files Are Enough — and When They Are Not (Teaser)

Files are perfect for notes, configs, and small datasets. But real apps outgrow plain files:


| Need                         | Start with       | Graduate to        |
| ---------------------------- | ---------------- | ------------------ |
| Single-user notes, config    | Text / JSON file | —                  |
| Structured queries, < 100 MB | JSON file        | SQLite (one file!) |
| Multi-user web app           | —                | PostgreSQL / MySQL |
| Sharing across machines      | —                | S3 / cloud storage |
| Fast key lookups             | —                | Redis              |


You will see the full decision guide in Part 38. For now: **files first, databases when you need them.**

---

## Practice Assignment

Build a small notes app:

1. Function `add_note(filename, note)` — append a note with a timestamp.
2. Function `view_notes(filename)` — read and print all notes. Handle missing file.
3. Function `clear_notes(filename)` — empty the file.
4. Function `count_notes(filename)` — return how many notes are in the file.

Wrap them in a menu:

```
Notes App
1. Add note
2. View notes
3. Clear notes
4. Note count
5. Quit
```

For the timestamp:

```python
from datetime import datetime
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
```

Example file content after a few notes:

```
[2026-03-19 14:30:15] Buy groceries
[2026-03-19 14:31:02] Study Part 36
```

Save as `src/notes_app.py`.

---

