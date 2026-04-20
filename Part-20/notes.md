# Part 20 — Sets

## Connecting to Parts 17, 18, and 19

You already know **lists** (Parts 17-18) and **tuples** (Part 19). All three are collections, but they answer **different questions**.


|                              | **List**                  | **Tuple**                               | **Set**                              |
| ---------------------------- | ------------------------- | --------------------------------------- | ------------------------------------ |
| **Main question it answers** | What is at position `i`?  | What is at position `i` in a fixed row? | Does this value already exist?       |
| **Order / index**            | Yes (`[0]`, slicing)      | Yes                                     | **No** - no indexing                 |
| **Duplicates**               | Allowed                   | Allowed                                 | **Not stored** - only unique members |
| **Mutability**               | Mutable                   | Immutable                               | Mutable                              |
| **Best mental model**        | Working sequence / basket | Locked row / fixed record               | Membership container                 |


### One-line mental model

- **List** = store by **position**
- **Tuple** = store by **position**, but **locked**
- **Set** = store by **membership**

A set is **not** "a list without duplicates."
A set is a **different kind of container** made for a different job.

### Practical contrast

- Use a **list** when order matters, duplicates matter, or you want indexing.
- Use a **tuple** when the row should stay fixed.
- Use a **set** when your main question is:
  - "Have I seen this already?"
  - "Give me only unique values"
  - "What is common between these two groups?"

That is why converting a list to a set is common:

```python
user_ids = [101, 102, 103, 101, 104, 102]
unique_ids = set(user_ids)
print(unique_ids)   # {101, 102, 103, 104}
```

---

## What Is a Set?

A set is an **unordered** collection of **unique values**.

*(Technically, only **hashable** values can be stored — we explain what "hashable" means in the "How Set Works Internally" section below.)*

```python
skills = {"Python", "SQL", "Docker"}
```

### Three core properties


| Property      | Meaning                                         |
| ------------- | ----------------------------------------------- |
| **Unordered** | No position contract, so no indexing or slicing |
| **Unique**    | Equal values collapse into one member           |
| **Mutable**   | You can add and remove members                  |


### Important clarification

**Unordered does not mean random.**
It means Python does **not promise a usable position** like `0`, `1`, `2`.

That is why this has no meaning:

```python
skills[0]   # TypeError
```

### Better beginner sentence

A set is a **membership container**, not a **numbered sequence**.

---

## Why Does Set Exist?

A set exists because sometimes we do **not** care about order.
We care about two different questions:

1. **Is this value already present?**
2. **Can I keep only unique values?**

A list can answer those questions too, but it answers them by **scanning one by one**.
A set answers them using **hashing**, which is much faster on average for lookup.

### Core motivation

```python
# Conceptually:
# List membership:  item in big_list   →  scans one by one (slow for large data)
# Set membership:   item in big_set    →  hash-jump to the right area (fast on average)
```

So the real story is:

- **List** = position + scan
- **Set** = hash + jump

This is your first strong bridge to **DSA thinking**.

---

## Creating Sets

```python
# Curly braces with members
colors = {"red", "green", "blue"}

# Duplicate removal happens automatically
numbers = {1, 2, 2, 3, 3, 3}
print(numbers)   # {1, 2, 3}

# From a list
names = ["Asha", "Ravi", "Asha", "Priya", "Ravi"]
unique_names = set(names)
print(unique_names)

# From a string
letters = set("banana")
print(letters)   # {'b', 'a', 'n'} in some order
```

### Empty set trap

```python
wrong = {}
print(type(wrong))   # <class 'dict'>

correct = set()
print(type(correct))   # <class 'set'>
```

`{}` creates an empty **dictionary**, not a set.
Always use `set()` for an empty set.

---

## No Indexing, No Slicing

Because a set has **no position contract**, indexing is not supported.

```python
colors = {"red", "green", "blue"}
print(colors[0])
# TypeError: 'set' object is not subscriptable
```

### Why?

With a list, `colors[0]` means:

- go to slot 0
- return the reference stored there

With a set, there is no user-facing slot 0.
The internal placement is based on **hash math**, not user-visible position.

### Decision rule

- Need `x[0]`, slicing, or stable order? Use **list** or **tuple**.
- Need uniqueness or fast membership? Use **set**.

---

## Adding and Removing Members

### `.add(x)` - add one member

```python
skills = {"Python", "SQL"}
skills.add("Docker")
print(skills)
```

If the member already exists, nothing breaks and nothing new is added:

```python
skills.add("Python")
print(skills)   # still same set
```

### `.remove(x)` - strict remove

```python
skills = {"Python", "SQL", "Docker"}
skills.remove("SQL")
print(skills)

skills.remove("Java")
# KeyError
```

### `.discard(x)` - safe remove

```python
skills = {"Python", "Docker"}
skills.discard("Java")   # no error
print(skills)
```

### `.pop()` - removes an arbitrary member

```python
skills = {"Python", "SQL", "Docker"}
removed = skills.pop()
print(removed)
print(skills)
```

Do **not** explain `.pop()` like list pop-from-end.
For a set, `.pop()` removes an **arbitrary** member.

### `.clear()` - remove everything

```python
skills = {"Python", "SQL"}
skills.clear()
print(skills)   # set()
```

---

## Set Operations

This is where sets become visually powerful and mathematically clean.

```python
frontend = {"HTML", "CSS", "JavaScript", "React"}
backend = {"Python", "JavaScript", "SQL", "Docker"}
```

### Union `|` - all unique members from both

```python
all_skills = frontend | backend
print(all_skills)

all_skills = frontend.union(backend)
```

### Intersection `&` - common members

```python
common = frontend & backend
print(common)   # {'JavaScript'}

common = frontend.intersection(backend)
```

### Difference `-` - first set minus second

```python
only_frontend = frontend - backend
print(only_frontend)

only_backend = backend - frontend
print(only_backend)
```

### Symmetric difference `^` - in either, but not both

```python
exclusive = frontend ^ backend
print(exclusive)
```

### Visual summary

```text
frontend:  {HTML, CSS, JavaScript, React}
backend:   {Python, JavaScript, SQL, Docker}

Union (|):          everything unique from both
Intersection (&):   only shared members
Difference (-):     direction matters
Symmetric (^):      everything except the shared part
```

### Heap / identity reminder

These operations usually build a **new set object**.
So this is a good place to connect with `id()`:

```python
a = {1, 2, 3}
b = {3, 4, 5}
c = a | b

print(id(a))
print(id(c))   # different id - new object
```

That matches earlier parts:

- mutation = same object changes
- expression creating a new result = new object

---

## Fast Membership Testing

The real superpower of a set is fast average-case membership testing.

```python
big_list = list(range(1_000_000))
big_set = set(range(1_000_000))

print(999_999 in big_list)
print(999_999 in big_set)
```

Both return `True`, but they work very differently.

### List membership

For a list, Python checks one member after another:

- compare with slot 0
- compare with slot 1
- compare with slot 2
- continue until found or end

That is a **scan**.
Average idea: **O(n)**.

### Set membership

For a set, Python:

1. computes a **hash** of the value
2. uses hash math to jump near the correct slot area
3. confirms with equality if needed

Average idea: **O(1)**.

### One-line memory aid

**Hash narrows the search; equality confirms the match.**

---

## How Set Works Internally — Why `in` Is Fast

This is the crux section. Remember **Part 6** — your Python code becomes bytecode, and the PVM executes it in **C**. The hash table inside a set is part of that C layer. That is where the speed comes from.

---

### 1) Hashable vs unhashable

A set can only store **hashable** objects.

### Usually hashable

- `None`
- `bool`
- `int`
- `float`
- `complex`
- `str`
- `bytes`
- `range`
- `tuple` - only if all items inside are hashable
- `frozenset` - only if all items inside are hashable

### Not hashable

- `list`
- `dict`
- `set`
- `bytearray`

### Practical rule

Mutable built-in containers are not hashable.
Most immutable built-ins are hashable.

### Live proof

```python
print(hash(42))
print(hash("hi"))
print(hash((1, 2)))

print(hash([]))
# TypeError: unhashable type: 'list'
```

That is exactly why this fails:

```python
bad = {[1, 2]}
# TypeError: unhashable type: 'list'
```

And this works:

```python
good = {(1, 2)}
print(good)
```

### Important precision

Do not teach this as only:
"immutable = hashable"

The real rule is:

- stable hash value during lifetime
- consistent equality behavior

For now, the practical shortcut covers 99% of cases: **if it is a mutable built-in container (`list`, `dict`, `set`), it is not hashable. If it is immutable (`int`, `str`, `tuple`, `frozenset`), it usually is.**

---

### 2) `hash(x)` vs `id(x)`

Students must not confuse these two.


| Function  | Meaning                                        |
| --------- | ---------------------------------------------- |
| `id(x)`   | identity of the object                         |
| `hash(x)` | fingerprint integer used for hash-based lookup |


```python
x = "python"
print(id(x))
print(hash(x))
```

These numbers are different because they do different jobs.

### Mental model

- `id(x)` = who this object is
- `hash(x)` = where to start looking in a hash-based container

### Important note

For strings and bytes, hash values can differ across process runs because Python enables hash randomization by default.
Inside one run they stay consistent, but across runs they may change.

---

### 3) `in` on list vs `in` on set

#### List

```python
target in my_list
```

Conceptually:

- compare with first element
- compare with second
- compare with third
- keep scanning

This is why large lists become slower for repeated membership checks.

#### Set

```python
target in my_set
```

Conceptually:

- compute `hash(target)`
- use hash math to locate the right slot neighborhood
- compare for confirmation

This is why membership is fast on average.

### Strong teaching sentence

A list finds by **walking**.
A set finds by **jumping**.

---

### 4) What the hidden hash table looks like

Inside the set object, CPython maintains an internal **table of slots**.

Important: this is **not** a normal Python list that you can access.
It is a lower-level implementation detail hidden inside the set object.

### Conceptual picture

```text
name on stack/frame  --->  set object in heap
                              |
                              |-- hidden table of slots
                              |-- each occupied slot stores:
                                  - cached hash code
                                  - reference to member object
```

### Very important note

You, as a Python programmer, do **not** control these internal slot numbers.
They are for the runtime, not for user-facing indexing.

That is why:

- set has no `s[0]`
- iteration order is not a contract
- membership is fast

---

### 5) How placement happens conceptually

When a member is inserted:

1. Python computes `hash(member)`
2. It uses that hash to choose a slot region
3. If that slot is free, store it there
4. If there is a collision, probe nearby slots

You do **not** need to reimplement this in this part.
Students only need the idea:

**hash -> slot selection -> possible probe -> equality confirmation**

---

### 6) Collision, briefly

A collision means two different members want the same slot area.

Python handles this internally.
It does **not** give up, and it does **not** scan the whole structure like a list.
It follows a probe sequence to check nearby slots.

### What to say, and what not to say

Say:

- collisions are normal
- Python handles them internally
- average lookup stays fast

Do not go deep into:

- separate chaining vs open addressing theory
- full probe formulas
- reimplementing hash tables

That belongs in a separate DSA episode.

---

### 7) Resizing and spare room

A hash table cannot stay packed tight forever.
It needs empty space to stay fast.

So conceptually:

- some slots stay empty
- when the table becomes too full, Python resizes it
- members are redistributed into the larger table

### Demo idea

Use `sys.getsizeof()` just as evidence that the set grows in jumps:

```python
import sys

s = set()
for i in range(20):
    s.add(i)
    print(i, sys.getsizeof(s))
```

### Important wording

`sys.getsizeof()` shows the size of the set object itself, not the full recursive size of every object it references.

### CPython detail

CPython starts with a small internal table (commonly **8 slots**) and grows as needed. The exact starting size and growth strategy are **implementation details** — the CPython team keeps them internal so they can optimize performance freely between Python versions without breaking anyone's code.

---

### 8) `hash` is not password hashing

This is a one-sentence cleanup point.

The word **hash** is used in two very different worlds:

- **set/dict hashing** -> fast placement and lookup inside a data structure
- **password hashing** -> security (`hashlib`, bcrypt, SHA, etc.)

Same English word, different purpose.

---

### 9) DSA bridge

This is the moment to make students feel powerful.

### One-liner

**DSA asks two questions:**

1. How do I store?
2. How do I find?

### In this series so far

- **List** stores by position and finds by scanning
- **Tuple** stores by position, but locked
- **Set** stores by hashing and finds by jumping

That means students have already started learning DSA thinking.

---

## Proving Mutability with `id()`

```python
skills = {"Python", "SQL"}
print(id(skills))

skills.add("Docker")
print(id(skills))   # same id
```

The object identity stays the same.
That means the same set object was changed in place.

### Contrast with operation creating a new set

```python
a = {1, 2}
b = {2, 3}
c = a | b

print(id(a))
print(id(c))   # different id
```

So:

- `.add()`, `.remove()`, `.discard()`, `.clear()`, `.update()` = mutate same set
- `a | b`, `a & b`, `a - b`, `a ^ b` = build new set objects

---

## Set vs List vs Tuple - Decision Rule


| Need                         | Best choice  | Why                    |
| ---------------------------- | ------------ | ---------------------- |
| Order matters                | List / Tuple | position is meaningful |
| Need indexing                | List / Tuple | set has no indexing    |
| Need duplicates              | List / Tuple | set removes duplicates |
| Need fixed row               | Tuple        | immutable sequence     |
| Need uniqueness              | Set          | duplicates collapse    |
| Need fast average membership | Set          | hash-based lookup      |


### The simplest decision rule

- Need **position**? Use **list** or **tuple**.
- Need **existence / uniqueness**? Use **set**.

### Strong contrast line

A list answers: "What is at index `i`?"
A set answers: "Does `x` exist?"

---

## Set Methods Reference

### Core mutation methods


| Method        | Meaning                                    |
| ------------- | ------------------------------------------ |
| `.add(x)`     | Add one member                             |
| `.remove(x)`  | Remove member, raise `KeyError` if missing |
| `.discard(x)` | Remove member, no error if missing         |
| `.pop()`      | Remove and return an arbitrary member      |
| `.clear()`    | Remove all members                         |
| `.copy()`     | Shallow copy                               |


### Operations that return a new set


| Method / operator                     | Meaning                 |
| ------------------------------------- | ----------------------- |
| `.union(other)` or `                  | `                       |
| `.intersection(other)` or `&`         | Common members          |
| `.difference(other)` or `-`           | In first, not in second |
| `.symmetric_difference(other)` or `^` | In either, but not both |


### In-place update methods


| Method                                | Meaning                       |
| ------------------------------------- | ----------------------------- |
| `.update(other)`                      | In-place union                |
| `.intersection_update(other)`         | Keep only common members      |
| `.difference_update(other)`           | Remove members found in other |
| `.symmetric_difference_update(other)` | Keep non-common members       |


### Relationship checks


| Method               | Meaning                           |
| -------------------- | --------------------------------- |
| `.issubset(other)`   | Is every member in `other`?       |
| `.issuperset(other)` | Does this contain all of `other`? |
| `.isdisjoint(other)` | Do they share nothing?            |


---

## `frozenset` - Immutable Set

```python
permissions = frozenset({"read", "write"})
print(permissions)

permissions.add("delete")
# AttributeError
```

### Mental model

- `tuple` is to `list`
- `frozenset` is to `set`

### Why does `frozenset` exist?

Because sometimes you want set behavior, but the container itself must be immutable.

### Real use cases

- use as a **dictionary key**
- store a set-like object **inside another set**
- represent a fixed group of permissions / tags / options

### Example

```python
role_permissions = {
    frozenset({"read", "write"}): "editor",
    frozenset({"read"}): "viewer"
}
```

---

## Hash-Table Family: `dict`, `set`, `frozenset`

This is your bridge to Part 21.

### Same family

- **set** = members only
- **frozenset** = immutable members only
- **dict** = key -> value pairs

### Different family

- **list** = ordered dynamic array of references
- **tuple** = ordered fixed sequence of references

### Strong family sentence

`dict` and `set` are hash-table siblings.
`list` is a different family.

This prepares students for the next part naturally.

---

## When NOT to Use a Set

Do **not** use a set when:

- order matters
- duplicates matter
- you need indexing or slicing
- your values are unhashable
- you want stable user-facing position

### Bad example

```python
bad = {[1, 2], [3, 4]}
# TypeError: unhashable type: 'list'
```

### Good replacement

```python
good = {(1, 2), (3, 4)}
print(good)
```

### Another common mistake

If your app needs to keep insertion sequence for display,
do **not** use a set as the main display container.
Use a list or another structure for presentation.

---

## Time Complexity (Mental Model Level)


| Operation     | Set                                   | Why                          |
| ------------- | ------------------------------------- | ---------------------------- |
| `x in s`      | O(1) average                          | hash-based lookup            |
| `s.add(x)`    | O(1) average                          | place by hash                |
| `s.remove(x)` | O(1) average                          | find by hash                 |
| `len(s)`      | O(1)                                  | tracked internally           |
| `s1           | s2`                                   | O(len(s1) + len(s2))         |
| `s1 & s2`     | O(min(len(s1), len(s2))) average idea | compare against smaller side |


### Important teaching precision

Say **average-case O(1)**, not absolute magical O(1).
Collisions exist, but Python's implementation is designed so average membership stays fast.

---

## Where Sets Are Actually Used — Real Applications

This section answers the question students always ask: **"Where do we use sets in real work?"**

### 1) Backend — Deduplicating API input

APIs receive data from users, forms, mobile apps. Duplicate entries are common. Before inserting into a database, backends routinely deduplicate.

```python
submitted_emails = [
    "ravi@gmail.com", "asha@outlook.com", "ravi@gmail.com",
    "dev@yahoo.com", "asha@outlook.com"
]
unique_emails = set(submitted_emails)
print(f"Received {len(submitted_emails)}, unique: {len(unique_emails)}")
```

This pattern is used in **Django**, **FastAPI**, **Flask** backends every day — whenever form data, webhook payloads, or batch uploads arrive with potential repeats.

### 2) Backend — Idempotent event processing (webhooks, queues)

Payment gateways like Razorpay or Stripe can send the same webhook event multiple times. Backends track processed event IDs in a set (or Redis set) to avoid double-processing.

```python
processed_events = set()

incoming_events = ["evt_1001", "evt_1002", "evt_1001", "evt_1003", "evt_1002"]

for event_id in incoming_events:
    if event_id in processed_events:
        print(f"Skipping duplicate: {event_id}")
        continue
    processed_events.add(event_id)
    print(f"Processing: {event_id}")
```

In production, the `processed_events` set may live in **Redis** (which has a native `SET` data type) rather than Python memory, but the **concept** is identical.

### 3) Backend — Permission and role checks

Web applications check user permissions before allowing actions. A set of permissions makes `in` checks instant.

```python
user_permissions = {"read", "write", "deploy"}

if "deploy" in user_permissions:
    print("Deploy access granted")
else:
    print("Access denied")
```

Frameworks like **Django** (`user.has_perm`) and **FastAPI** (dependency-injected auth) use this pattern internally — checking membership in a collection of granted permissions.

### 4) Backend — Finding common or exclusive users across groups

Product teams ask: "Which users are in both the free tier **and** the waitlist?" or "Which premium users have **not** completed onboarding?"

```python
free_users = {"Asha", "Ravi", "Nisha", "Dev", "Meera"}
waitlist = {"Dev", "Nisha", "Kiran", "Priya"}

in_both = free_users & waitlist
print(f"In both groups: {in_both}")

only_free = free_users - waitlist
print(f"Free but not on waitlist: {only_free}")
```

This is **intersection** and **difference** — the same math from the set operations section, applied to real user segmentation.

### 5) Web crawlers and AI agents — Visited URL tracking

A web crawler or an AI research agent must not revisit the same URL forever. A set of visited URLs prevents infinite loops.

```python
visited_urls = set()

urls_to_crawl = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page1",
    "https://example.com/page3",
]

for url in urls_to_crawl:
    if url in visited_urls:
        print(f"Already visited: {url}")
        continue
    visited_urls.add(url)
    print(f"Crawling: {url}")
```

This is the **same "seen before?" pattern** as webhook dedup — applied to crawlers, scrapers, and **AI agent loops** that explore links or tool calls.

### 6) AI / RAG — Deduplicating retrieved documents

In Retrieval-Augmented Generation (RAG), multiple search queries can return overlapping document chunks. Before stuffing context into the LLM prompt, you deduplicate by document ID.

```python
query_1_results = {"doc_101", "doc_205", "doc_312"}
query_2_results = {"doc_205", "doc_312", "doc_489"}

unique_docs = query_1_results | query_2_results
print(f"Total unique documents for context: {len(unique_docs)}")
```

Without dedup, the same paragraph would appear twice in the prompt — wasting tokens and confusing the model.

### 7) NLP / Data Science — Unique vocabulary extraction

Building a vocabulary from text is a classic NLP preprocessing step. Sets handle uniqueness naturally.

```python
text = "python is great and python is simple"
words = text.split()
vocabulary = set(words)
print(f"Total words: {len(words)}, Unique words: {len(vocabulary)}")
print(vocabulary)
```

Libraries like **NLTK**, **spaCy**, and **scikit-learn**'s `CountVectorizer` use similar ideas internally — a set (or set-like structure) of unique tokens.

### 8) Namma Metro / transit — Unique stations visited

```python
tap_log = ["Majestic", "Indiranagar", "Majestic", "MG Road", "Indiranagar"]
unique_stations = set(tap_log)
print(f"Tapped {len(tap_log)} times, visited {len(unique_stations)} unique stations")
```

Any system that logs repeated events (metro taps, toll booths, bus stops) and needs **distinct counts** uses this pattern.

### 9) Government / enterprise — Application deduplication

A government office or bank receives applications — the same person may apply multiple times.

```python
applications = [
    "XXXX-1234", "XXXX-5678", "XXXX-1234",
    "XXXX-9012", "XXXX-5678", "XXXX-3456"
]
unique_applicants = set(applications)
print(f"Total applications: {len(applications)}")
print(f"Unique applicants: {len(unique_applicants)}")
```

### 10) DMart-style — Distinct products scanned

Your shopping basket is still a **list** because order and history of actions may matter. But if the store manager asks: "How many **distinct** products touched the scanner today?" — that becomes a **set** question.

```python
scans = ["rice_5kg", "dal_1kg", "rice_5kg", "oil_1l", "rice_5kg"]
distinct = set(scans)
print(f"{len(scans)} scans, {len(distinct)} distinct SKUs")
```

### 11) Graph search / pathfinding — Visited nodes

In algorithms (BFS, DFS) and AI agent planners, a `visited` set prevents revisiting the same node.

```python
visited = set()
```

Whenever your code needs to track **"already visited / already processed / already seen"**, that is a strong set signal. This applies to:

- graph traversal (BFS/DFS)
- game state exploration
- AI agent action loops

---

## Story Version of the Mental Model

Use this internally while teaching.

### List story

A list is like a row of numbered desks in a classroom.
You can say:

- give me desk 0
- give me desk 1
- give me desk 2

Position is the meaning.

### Set story

A set is like the **security register at a tech park gate** (Manyata, EcoWorld, Electronic City — any tech park your audience knows).

The security guard does not care what order people arrived. The guard only checks:

- "Is this badge ID already in the system?"
- "Has this visitor already entered today?"
- "Which visitors are common across both entry gates?"

You do **not** ask: "Give me the person at position 2."
You ask: "Is this person **in** the register?"

That is why set is not about position.
It is about **fast yes/no membership logic**.

---

## Practice Assignment

You have enrollment data for two classes:

```python
class_a = ["Asha", "Ravi", "Priya", "Dev", "Meera", "Ravi"]
class_b = ["Ravi", "Dev", "Kiran", "Nisha", "Asha", "Kiran"]
```

### Tasks

1. Convert both lists to sets
2. Find students in **both** classes
3. Find students in **only Class A**
4. Find students in **only Class B**
5. Find **all unique students**
6. Find students in **exactly one** class
7. Print each result with a label

### Expected idea

```text
Both classes: {'Asha', 'Ravi', 'Dev'}
Only Class A: {'Priya', 'Meera'}
Only Class B: {'Kiran', 'Nisha'}
All students: {'Asha', 'Ravi', 'Priya', 'Dev', 'Meera', 'Kiran', 'Nisha'}
Exactly one class: {'Priya', 'Meera', 'Kiran', 'Nisha'}
```

Printed order may differ because sets do not guarantee element position.

Save as `src/student_sets.py`.

---

## Closing Bridge to Part 21

Today you saw a container that answers:

**Does this member exist?**

Next, we move to a container that answers:

**If this key exists, what value belongs to it?**

That next container is the **dictionary**.

### Strong bridge line

- **set** = membership only
- **dict** = key -> value mapping

Both belong to the same hash-table family.

---

