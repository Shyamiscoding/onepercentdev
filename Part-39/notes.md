# Part 39 — Files in the AI Era (One Mental Model for Every File)

Parts 36–38.1 taught `open()`, safe writes, and the structured formats (JSON, JSONL, CSV). This part is **not** a tour of ten libraries. It gives you **one reflex** so you never fear a file format again:

> **When I face any file, I ask two things: do I need a parser, and which one do I install?**

Get this reflex and you can open *anything* in 2026 — Markdown agent memory, `.env` secrets, PDF, Excel, an image for GPT-4o — including formats nobody has invented yet.

---

## The Mental Model — `open()` + maybe a parser

Every file comes off the disk as raw **bytes**. Two translation layers turn those bytes into something you can use:

```
file on disk  →  open()  →  text  →  parser  →  Python object
                   ↑                    ↑
              encoding (UTF-8)     library (json, pypdf, Pillow…)
              bytes → characters   text/bytes → dict, image, table
```

- `**open()**` is always the door. With an **encoding** (UTF-8) it turns bytes into **text**. — *Part 36.*
- A **parser** is a library that turns that text/bytes into a **richer object** (a dict, an image, a table).

The key insight:


| File                                          | Need a parser? | Why                                                            |
| --------------------------------------------- | -------------- | -------------------------------------------------------------- |
| Plain text (`.txt`, `.md`)                    | **No**         | text is already a usable Python `str` — you stop at `open()`   |
| Anything structured (`.json`, `.pdf`, image…) | **Yes**        | you want more than a string, so a parser interprets the format |


So `open()` is the common skill. The parser is the only thing that changes — and **someone already wrote it** so you just call 3 functions.

---

## The Hero Table — Which File Needs Which Parser

This one table is the whole part. Memorize the *reflex*, not the rows:


| File / format          | Need a parser?                                | Library              | Built-in or `pip`? | You get back (Python object)     |
| ---------------------- | --------------------------------------------- | -------------------- | ------------------ | -------------------------------- |
| `.txt` plain text      | **No** — `open()` + encoding                  | —                    | built-in           | `str` (text)                     |
| `.md` Markdown         | **No** (plain text; parser only for metadata) | `python-frontmatter` | pip (optional)     | `str` (text)                     |
| `.json`                | Yes                                           | `json`               | built-in           | `dict` / `list`                  |
| `.csv`                 | Yes                                           | `csv`                | built-in           | list of rows / dicts             |
| `.toml`                | Yes (read)                                    | `tomllib`            | built-in (3.11+)   | `dict`                           |
| `.yaml`                | Yes                                           | `pyyaml`             | pip                | `dict`                           |
| `.env`                 | Yes                                           | `python-dotenv`      | pip                | env vars → `str` via `os.getenv` |
| `.pdf`                 | Yes                                           | `pypdf`              | pip                | page objects → text              |
| `.xlsx` Excel          | Yes                                           | `openpyxl`           | pip                | workbook → sheets → cells        |
| `.jpg` / `.png` images | Yes                                           | `Pillow`             | pip                | `Image` object                   |
| `.db` SQLite           | Yes                                           | `sqlite3`            | built-in           | query result rows                |


Reading the table is the skill: *"Markdown? just open it. YAML? `pip install pyyaml`. PDF? `pip install pypdf`."* You already proved this with `json` and `csv` in Part 38.1 — now you see the pattern is the same for **every** format.

---

## Four Quick Proofs (install the lib, call 3 functions)

These are not tutorials — they show the reflex in action for the four files an AI engineer touches most.

### 1. Markdown — NO parser (this is AI agent memory)

```python
from pathlib import Path

MEMORY = Path("agent_memory.md")

with open(MEMORY, "a", encoding="utf-8") as f:   # just open + encoding — no parser
    f.write("- User prefers Kannada explanations\n")

print(MEMORY.read_text(encoding="utf-8"))
```

That is the core of every AI agent's memory — Cursor (`AGENTS.md`), Claude Code (`CLAUDE.md`) all read a Markdown file each turn. Plain text, no parser needed.

### 2. `.env` — parser `python-dotenv` (your API keys)

```python
# pip install python-dotenv
from dotenv import load_dotenv
import os

load_dotenv()                       # the parser reads .env into the environment
api_key = os.getenv("OPENAI_API_KEY")
```

```
# .env  ← NEVER commit. Add it to .gitignore.
OPENAI_API_KEY=sk-proj-...
```

> **Real story:** GitHub scans public repos for key patterns. Push a `.env` by accident and a bot can drain $200–$2000 of credits in 30 minutes. `.gitignore` it *before* your first commit.

### 3. PDF — parser `pypdf` (the start of every "chat with your PDF")

```python
# pip install pypdf
from pypdf import PdfReader

reader = PdfReader("contract.pdf")                       # parser understands PDF
text = "\n".join(p.extract_text() or "" for p in reader.pages)
# now feed `text` to an LLM → summary, Q&A, RAG
```

> PDF text is messy (tables, columns). For heavy work use `pymupdf`; for scanned PDFs (images) you need OCR (`pytesseract`).

### 4. Image — parser `Pillow` + `base64` (multimodal AI)

```python
# pip install pillow
from PIL import Image
import base64, io

img = Image.open("invoice.jpg")     # Pillow parses the image bytes
img.thumbnail((1024, 1024))         # shrink → lower API cost

buf = io.BytesIO()                  # in-memory file (Part 38)
img.save(buf, format="JPEG")
encoded = base64.b64encode(buf.getvalue()).decode("ascii")
# send `encoded` to a multimodal LLM (GPT-4o, Claude, Gemini)
```

This is exactly how receipt scanners and "explain this chart" tools send an image to a model.

> **YAML / TOML / Excel / SQLite** follow the *same* reflex — find the row in the table, install the library, call its read/write functions. No new skill, just a different parser.

---

## Three Gotchas Worth Remembering


| Gotcha                                    | Fix                                                      |
| ----------------------------------------- | -------------------------------------------------------- |
| `.env` pushed to GitHub                   | revoke the key, rotate it, add `.env` to `.gitignore`    |
| `yaml.load()` on an untrusted file        | always use `yaml.safe_load()` (the unsafe one runs code) |
| Excel shows `=SUM(...)` instead of values | `load_workbook(..., data_only=True)`                     |


---

## Practice — Mini AI Memory CLI

Build the persistent layer of an AI agent (the LLM comes in Part 70). Create `src/memory_cli.py`:

1. `**remember(fact)`** — append `- fact` to `memory.md` (no parser — plain text)
2. `**recall()**` — read and print `memory.md`
3. `**export_jsonl(path)**` — write each fact as one JSONL line (parser: `json`)
4. `**load_secrets()**` — read `.env`, confirm `OPENAI_API_KEY` is set without printing it (parser: `python-dotenv`)

You'll touch a no-parser file (Markdown), a built-in parser (`json`), and a pip parser (`dotenv`) — the whole mental model in one exercise.

---

