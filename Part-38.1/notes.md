# Part 38.1 — JSON, JSONL, and CSV (Structured Data on Disk)

Part 38 = read/write files safely. Part 38.1 = the three **structured** formats that carry almost all real data.

> **Map of this part:**
>
>
> | Format    | Use it for                                   | Parser                |
> | --------- | -------------------------------------------- | --------------------- |
> | **JSON**  | APIs, config, web data                       | `json`                |
> | **JSONL** | AI datasets, agent logs, anything that grows | `json` (one per line) |
> | **CSV**   | spreadsheets, analytics, Excel exports       | `csv`                 |
>

> You met `json.dumps()` / `json.loads()` (strings) in Part 22. Here: reading, writing, and **updating** the actual **files**, using the safe-write skills from Parts 36 & 38.

> **1% edge:** most tutorials skip JSONL. In 2026 it is *the* AI format — fine-tuning, agent traces, Hugging Face datasets. After this, you speak all three.

---

## SECTION A — JSON

**Map:**


| Need                       | Tool                            |
| -------------------------- | ------------------------------- |
| String ↔ dict              | `json.loads()` / `json.dumps()` |
| File ↔ dict                | `json.load()` / `json.dump()`   |
| Update a file              | load → change → save (atomic)   |
| Non-JSON types (datetime…) | `default=` callback             |


### A.1 Read and Write

```python
import json

data = {"name": "Shyam", "skills": ["Python", "FastAPI"], "active": True}

# WRITE dict -> file
with open("user.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# READ file -> dict
with open("user.json", "r", encoding="utf-8") as f:
    user = json.load(f)

print(user["name"])     # Shyam
```

- `indent=2` → human-readable
- `ensure_ascii=False` → keep Kannada / Hindi / emoji as-is (not `\uXXXX`)

See the difference (ties back to Part 36 — `ಕ` is one code point, 3 UTF-8 bytes):

```python
>>> import json
>>> json.dumps({"city": "ಬೆಂಗಳೂರು"})                       # default: escaped, unreadable
'{"city": "\\u0cac\\u0cc6\\u0c82\\u0c97\\u0cb3\\u0cc2\\u0cb0\\u0cc1"}'
>>> json.dumps({"city": "ಬೆಂಗಳೂರು"}, ensure_ascii=False)   # actual characters
'{"city": "ಬೆಂಗಳೂರು"}'
```

Both read back to the same string — `ensure_ascii` only changes how it *looks* on disk, not the data.

### A.2 The Four Functions


| Function          | Direction     | Use                 |
| ----------------- | ------------- | ------------------- |
| `json.loads(s)`   | string → dict | parse a JSON string |
| `json.dumps(d)`   | dict → string | dict to JSON string |
| `json.load(f)`    | file → dict   | read a JSON file    |
| `json.dump(d, f)` | dict → file   | write a JSON file   |


The **s** versions = **s**trings. The non-s versions = **f**iles.

### A.3 JSON as a Tiny Database (Load → Change → Save)

```python
import json, os
from pathlib import Path

DB = Path("contacts.json")

def load():
    return json.loads(DB.read_text(encoding="utf-8")) if DB.exists() else {}

def save(data):
    tmp = DB.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
    os.replace(tmp, DB)              # atomic swap (Part 38)

contacts = load()
contacts["Alice"] = "9876543210"     # change in Python
save(contacts)
```

Load the whole structure, change it in Python, save it back. Never edit a JSON file line by line. Add `flush()` + `fsync()` before `os.replace()` for critical data (Part 38).

### A.4 Non-JSON Types — `default=`

JSON only knows str, number, list, dict, `true/false/null`. Other types need a converter:

```python
import json
from datetime import datetime
from decimal import Decimal

def encoder(obj):
    if isinstance(obj, datetime): return obj.isoformat()
    if isinstance(obj, Decimal):  return str(obj)
    raise TypeError(f"Cannot serialize {type(obj)}")

json.dumps({"created": datetime.now(), "price": Decimal("99.50")}, default=encoder)
```

Fixes the classic `TypeError: Object of type datetime is not JSON serializable`.

### A.5 More (When Needed)

- **Validate untrusted JSON** before using it: `jsonschema` (check the shape) or `pydantic` (class-based, used by FastAPI).
- **Huge JSON that won't fit in RAM:** stream with `ijson` instead of `json.load()`.

---

## SECTION B — JSONL (The AI-Era Format)

One complete JSON object **per line** — no outer `[ ]`, no commas between records, so each line is independent.

```
{"role": "user", "content": "Hi"}
{"role": "assistant", "content": "Hello!"}
```

**Why it beats a JSON array for growing data:**


| Need            | JSON array             | JSONL                         |
| --------------- | ---------------------- | ----------------------------- |
| Add a record    | rewrite whole file     | append one line               |
| Read 10 GB      | loads all into RAM     | stream line by line           |
| Crash mid-write | whole file may corrupt | only the last line is partial |


### B.1 Write (Append) and Read (Stream)

```python
import json

# WRITE — append one object per line
with open("chat.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps({"role": "user", "content": "Hi"}, ensure_ascii=False) + "\n")

# READ — stream line by line (memory stays flat at any size)
with open("chat.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            record = json.loads(line)
            print(record["role"], record["content"])
```

Always end each line with `\n`.

### B.2 Update a Record

- **Append a correction** (event-log style): old line stays, new line supersedes — cheapest, most common.
- **Stream-rewrite** (when you must change history): read all → change → temp → atomic replace.

```python
import json, os
from pathlib import Path

LOG, TMP = Path("records.jsonl"), Path("records.jsonl.tmp")

with open(LOG, encoding="utf-8") as src, open(TMP, "w", encoding="utf-8") as dst:
    for line in src:
        rec = json.loads(line)
        if rec.get("id") == "user-42":
            rec["status"] = "active"
        dst.write(json.dumps(rec) + "\n")
os.replace(TMP, LOG)                 # same atomic pattern as Part 38
```

### B.3 Compressed `.jsonl.gz`

```python
import gzip, json

with gzip.open("dataset.jsonl.gz", "rt", encoding="utf-8") as f:   # "rt" = text mode
    for line in f:
        record = json.loads(line)
```

Hugging Face datasets often ship like this — smaller on disk, same streaming.

### B.4 Where JSONL Is Used (2026)

OpenAI fine-tuning · Anthropic batch API · Hugging Face datasets · agent / LangSmith traces · Cursor & Claude Code chat history · structured app event logs.

> Go into AI in 2026 and you write JSONL every day.

---

## SECTION C — CSV

```
name,age,score
Alice,20,85
Bob,21,92
```

Rows separated by newlines, values by commas, first row = header. **Every value reads as a string** — convert numbers yourself.

**Map:**


| Need                | Tool                         |
| ------------------- | ---------------------------- |
| Read by column name | `csv.DictReader` (preferred) |
| Read as plain lists | `csv.reader`                 |
| Write from dicts    | `csv.DictWriter`             |
| Unknown delimiter   | `csv.Sniffer`                |


### C.1 Read — DictReader

```python
import csv

with open("students.csv", encoding="utf-8", newline="") as f:
    for row in csv.DictReader(f):          # header row becomes dict keys
        print(row["name"], row["score"])   # Alice 85   (strings!)
```

### C.2 Write — DictWriter

```python
import csv

rows = [{"name": "Alice", "age": 20}, {"name": "Bob", "age": 21}]

with open("out.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["name", "age"])
    w.writeheader()
    w.writerows(rows)
```

Always pass `newline=""` when writing CSV (prevents blank lines on Windows).

### C.3 Update a Row (Read → Modify → Write → Atomic)

```python
import csv, os
from pathlib import Path

CSV, TMP = Path("students.csv"), Path("students.csv.tmp")

with open(CSV, encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    fields = reader.fieldnames
    rows = list(reader)

for row in rows:
    if row["name"] == "Bob":
        row["score"] = "95"

with open(TMP, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)
os.replace(TMP, CSV)
```

### C.4 Gotchas

- **Delimiter isn't always a comma:** `csv.reader(f, delimiter=";")` (European Excel) or `"\t"` (tab). Auto-detect with `csv.Sniffer().sniff(sample)`.
- **Commas/quotes inside values:** the `csv` module handles `"Alice, Bob"` correctly — never split on commas yourself.
- **Excel BOM:** Excel CSVs start with a hidden marker → open with `encoding="utf-8-sig"`.
- **Missing fields:** `row.get("score", "0")` for a default.

---

## SECTION D — Convert CSV ↔ JSON

```python
import csv, json
from pathlib import Path

# CSV -> JSON
rows = list(csv.DictReader(open("students.csv", encoding="utf-8", newline="")))
for r in rows:
    r["age"] = int(r["age"])           # CSV values are strings — convert
Path("students.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
```

```python
import csv, json
from pathlib import Path

# JSON -> CSV
rows = json.loads(Path("students.json").read_text(encoding="utf-8"))
with open("students.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)
```

---

## SECTION E — Storage Decision Matrix

Files are the **starting point**, not always the end point. Pick by need:


| Your need                           | Best choice                    | Why                                      |
| ----------------------------------- | ------------------------------ | ---------------------------------------- |
| Notes, config, agent memory         | Text / JSON / Markdown file    | simple, Git-friendly, human-editable     |
| Structured data, one user, < 100 MB | JSON file or **SQLite**        | SQLite = one file with real SQL          |
| Tabular analytics, big data         | **CSV** now, **Parquet** later | Parquet is 5–10× smaller                 |
| Multi-user web app                  | **PostgreSQL / MySQL**         | concurrent writes, transactions, indexes |
| Files shared across servers         | **S3 / cloud storage**         | URL-addressable, no disk limit           |
| Fast key lookups, sessions          | **Redis**                      | in-memory speed                          |
| Append-only events, AI logs         | **JSONL** file                 | stream-friendly, crash-survivable        |


**Ask:** How much data? How many writers at once? Need fast search? Must it survive on another machine? → the more "yes" to scale, the sooner you move off plain files.

---

## Practice Assignment

Create `students.csv`:

```
name,age,score,grade
Alice,20,85,B
Bob,21,92,A
Charlie,19,45,F
Diana,22,78,C
Eve,20,95,A
Frank,21,62,D
```

1. Read it with `csv.DictReader`, converting `age` and `score` to `int`
2. Filter students with `score > 70`
3. Write the filtered list to `passing_students.json` (pretty-printed)
4. Write each filtered record as one line in `passing_students.jsonl`
5. Write a summary to `report.txt`:

```
Student Report
==============
Total students: 6
Passing (score > 70): 4
Average score: 76.17
Highest: Eve (95)
Lowest: Charlie (45)
```

Save as `src/data_converter.py`.

---

