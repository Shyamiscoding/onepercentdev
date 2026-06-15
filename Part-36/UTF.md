# UTF — Why We Need It (Bits, Bytes, and the Boundary Problem)

Flow: **bit → byte → Unicode (you know this) → the problem → meet UTF → examples.**

---

## 1. Bit and Byte — the absolute basics

| Term | What it is | Example |
|------|-----------|---------|
| **Bit** | one switch: `0` (off) or `1` (on) | `1` |
| **Byte** | a group of **8 bits** | `01000001` |

A single bit has **2** options (0 or 1). Every extra bit **doubles** the options:

| Bits | Total values | |
|------|--------------|---|
| 1 bit | 2 | |
| 2 bits | 4 | |
| 3 bits | 8 | |
| 7 bits | 128 | ← old ASCII (values 0–127) |
| **8 bits = 1 byte** | **256** | ← values 0–255 |

---

## 2. How a byte becomes a number (place values)

Each position in a byte has a **place value** (a power of 2). Add the ones switched **ON**:

```
place value:  128   64   32   16    8    4    2    1
the byte 'A':   0    1    0    0     0    0    0    1

ON values:           64                          + 1   =  65
```

So the byte `01000001` = **65**, and **65 = 'A'**.

```python
>>> ord('A')        # the number for 'A'
65
>>> bin(ord('A'))   # that number in binary
'0b1000001'
```

---

## 3. Recall — what Unicode gave us (you already know this)

In the **1990s**, the world agreed on **Unicode**: one giant catalog that gives **every character a unique number** (called a *code point*).

| Character | Unicode number |
|-----------|----------------|
| `A` | 65 |
| `ಕ` | 3221 |
| `😀` | 128512 |

> **Unicode only gives the NUMBER.** It does **not** say how to store that number as bytes on the disk. That part is still missing.

---

## 4. The problem — a number in binary is not enough

We have the number. And we already have binary. So why not just write the Unicode number in binary and save it?

Let's try to store the word `"Aಕ"`:

| Character | Number | Binary |
|-----------|--------|--------|
| `A` | 65 | `1000001` (7 bits) |
| `ಕ` | 3221 | `110010010101` (12 bits) |

Glue them together as raw binary:

```
1000001110010010101...
```

Now the reader is stuck:

> **"Where does the first character END and the next one BEGIN?"**
> Is the first character 7 bits? 8 bits? 12 bits? Raw binary gives the **number**, but **not the boundaries.** Unreadable.

**Same problem in real life:** write amounts with no spaces — `5`, `100`, `7` → `51007`.
Is that `5 / 100 / 7`? Or `51 / 00 / 7`? You can't tell. You need a **system**.

---

## 5. Meet UTF — the missing system

**UTF = Unicode Transformation Format.**

It is the **set of rules that turns a Unicode number into actual bytes** — and, crucially, it adds **boundary markers** so any program can read the bytes back **one character at a time.**

> **Unicode** gives the *number*. **UTF** turns that number into *bytes you can read back correctly.*

There are a few versions of UTF. They are just **different rules** for doing this:

| Encoding | Idea | `A` | `ಕ` | Trade-off |
|----------|------|-----|-----|-----------|
| **UTF-32** | every character is **exactly 4 bytes** (fixed length) | 4 bytes | 4 bytes | simple, but wastes space |
| **UTF-8** | **variable** length, and it **marks where each character ends** | 1 byte | 3 bytes | small + smart ✅ (the world standard) |

---

## 6. Example — the letter ಕ

`ಕ` = Unicode `3221` → UTF-8 stores it in **3 bytes**: `e0 b2 95`

UTF-8 keeps these **3 bytes together as one character** — it knows the character runs "from this byte to this byte," so the reader groups them and rebuilds `ಕ` correctly. (`A`, being English, needs just **1 byte**.)

```python
>>> 'A'.encode('utf-8')        # English  -> 1 byte
b'A'
>>> 'ಕ'.encode('utf-8')        # Kannada  -> 3 bytes
b'\xe0\xb2\x95'
```

**Wait — what is `e0 b2 95`? Is that a number?**

Yes! Each one is just **one byte**, written in a short style called **hex** (a quick way to write a byte using 2 characters). Each byte is a normal number from 0 to 255:

| Byte (hex) | Same byte as a number |
|------------|-----------------------|
| `e0` | 224 |
| `b2` | 178 |
| `95` | 149 |

So `e0 b2 95` just means the **three bytes 224, 178, 149**. (In Python, the `\x` in `b'\xe0\xb2\x95'` simply means "this is a hex byte.")

> **Don't confuse the two numbers:**
> - **`3221`** = ಕ's **number** in the Unicode catalog (its "name").
> - **`e0 b2 95`** = the actual **bytes UTF-8 saves to the file** (224, 178, 149).
>
> They are *not* the same number written differently — UTF-8 **builds** the bytes `e0 b2 95` *from* the number `3221`.

---

## 7. The one-line summary

> **Bit** = one 0/1 switch. **Byte** = 8 bits.
> **Unicode** gives each character a **number**. Raw **binary** can write that number — but in a stream it **can't show where one character ends and the next begins.**
> **UTF (Unicode Transformation Format)** adds those **boundary rules** so any program can read the bytes back, character by character — and **UTF-8** does it while keeping English at just **1 byte**.

```
character 'ಕ'
   → Unicode number:  3221        (the catalog gives the number)
   → UTF-8 rules:      3 bytes + length markers
   → bytes on disk:    e0 b2 95    (now the boundaries are clear)
```
