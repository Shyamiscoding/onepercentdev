"""
Part 36 - File Handling Part 1 (Reading and Writing) - runnable demos.

USAGE
-----
Run a single section by its number:
    python3 example.py 1         # section 1  - open()
    python3 example.py 25        # section 25 - the "why is my file empty?" bug

Run a few in sequence:
    python3 example.py 1 2 3

List every section with its title:
    python3 example.py list

NO ARGS = show the list. File demos create real files on disk, so this
script never auto-runs everything at once. You open ONE section at a time,
exactly the way you teach it.

WHERE DO THE FILES GO?
----------------------
Every demo uses a plain file name like "example.txt". When you pass only a
file name (no folder), Python creates/reads it in the CURRENT FOLDER - the
one you are in when you run this script. So if you run this from the Part-36
folder, files like example.txt and output.txt appear right next to this
script. Open them and see what each demo wrote.
"""

import os
import sys


# A real image that ships next to this script. The binary demos (8 and 11)
# read and copy it so you can actually open the picture in your viewer.
SAMPLE_IMAGE = "p-36.jpg"


def section(title):
    width = 64
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width)
    print()


def need_sample_image():
    """Return the sample image name, or None with a friendly note if missing."""
    if os.path.exists(SAMPLE_IMAGE):
        return SAMPLE_IMAGE
    print(f"(this demo needs a real image named {SAMPLE_IMAGE!r} in this folder)")
    return None


# ============================================================
#                  SECTION A - THE BASICS
# ============================================================


def demo_01_open_basic():
    """1. open() - the door to every file in Python   (notes A.1)"""
    section("1. open(filename, mode)")

    # Step 1: create a file we can read back.
    # "example.txt" has no folder in front of it, so Python creates it in
    # the CURRENT folder (where you ran this script).
    # with open("example.txt", "w", encoding="utf-8") as f:
    #     f.write("Hello from Part 36!\n")

    # Step 2: open() returns a file object. Mode "r" means read.
    # WITHOUT `with`, you must call .close() yourself. This is the old style -
    # we show it once so you understand what `with` does for you in section 3.
    file = open("example.txt", "r", encoding="utf-8")
    content = file.read()
    print(content)
    file.close()

    with open("example.txt", "r", encoding="utf-8") as file:
        content = file.read()
        print(content)

    # print("--> open() takes (filename, mode). The old style needs close().")


def demo_02_modes():
    """2. The four basic modes - r / w / a / x   (notes A.2)"""
    section("2. Modes: r, w, a, x")

    # "w" creates the file, or CLEARS it if it already exists.
    # with open("example.txt", "w", encoding="utf-8") as f:
    #     f.write("first write (w created/cleared the file)\n")
    # with open("example.txt", "r", encoding="utf-8") as f:
    #     print(f.read())

    # # "a" appends - the pointer starts at the end, old content stays.
    # with open("example.txt", "a", encoding="utf-8") as f:
    #     f.write("second write (a added to the end)\n")
    # with open("example.txt", "r", encoding="utf-8") as f:
    #     print(f.read())

    # # "x" exclusively creates a new file, and ERRORS if it already exists.
    # if os.path.exists("brand_new.txt"):
    #     os.remove("brand_new.txt")        # delete so the demo can re-run cleanly
    # with open("brand_new.txt", "x", encoding="utf-8") as f:
    #     f.write("x mode = exclusive create\n")
    # with open("brand_new.txt", "r", encoding="utf-8") as f:
    #     print(f.read())

    # # "r" requires the file to exist. A missing file raises FileNotFoundError.
    try:
        open("does_not_exist.txt", "r", encoding="utf-8")
    except FileNotFoundError as e:
        print(f"r mode on a missing file -> {type(e).__name__}: {e}")


def demo_03_with_statement():
    """3. Always use `with` - it auto-closes the file   (notes A.3)"""
    section("3. with open(...) as f:")

    # with open("example.txt", "w", encoding="utf-8") as f:
    #     f.write("auto-closed when the block ends\n")

    # We keep a reference to the file object just to PROVE it is closed
    # once the `with` block ends. You would not normally do this.
    # saved_ref = None
    # with open("example.txt", "r", encoding="utf-8") as f:
    #     print(f.read())
    #     saved_ref = f
    # print(f"is the file closed after the block? {saved_ref.closed}")

    # # The key benefit: even if the block CRASHES, the file still closes.
    try:
        with open("hello.txt", "r", encoding="utf-8") as f:
            print("inside the with-block, about to crash...")
            raise RuntimeError("simulated crash")
    except RuntimeError:
        print(f"crash happened, but file still closed? {f.closed}")


def demo_04_reading_methods():
    """4. Four ways to read a file   (notes A.4)"""
    section("4. read / readline / readlines / for-line")

    with open("multiline.txt", "w", encoding="utf-8") as f:
        f.write("Line 1\nLine 2\nLine 3\n")

    # 1) .read() - the WHOLE file as one string.
    with open("multiline.txt", "r", encoding="utf-8") as f:
        print(f"read():\n{f.read()!r}\n")

    # 2) .readline() - ONE line at a time. Keeps the trailing \n.
    with open("multiline.txt", "r", encoding="utf-8") as f:
        print(f"readline() #1: {f.readline()!r}")
        print(f"readline() #2: {f.readline()!r}")

    # 3) .readlines() - ALL lines as a list of strings.
    with open("multiline.txt", "r", encoding="utf-8") as f:
        print(f"\nreadlines(): {f.readlines()}")

    # 4) for line in file - STREAMS line by line. The only safe way for
    #    a 10 GB log file, because it never loads the whole thing into RAM.
    print("\nfor line in file:")
    with open("multiline.txt", "r", encoding="utf-8") as f:
        for line in f:
            print(f"  {line.strip()!r}")   # .strip() drops the trailing \n


def demo_05_writing():
    """5. Writing - write() and writelines()   (notes A.5)"""
    section("5. write() / writelines()")

    # write() takes ONE string. You add the \n yourself.
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write("Hello, World!\n")
        f.write("This is line 2.\n")
    with open("output.txt", "r", encoding="utf-8") as f:
        print(f.read())

    # writelines() takes a LIST of strings - but does NOT add \n for you.
    lines = ["alpha\n", "beta\n", "gamma\n"]
    with open("output1.txt", "w", encoding="utf-8") as f:
        f.writelines(lines)
    with open("output1.txt", "r", encoding="utf-8") as f:
        print(f.read())


def demo_06_appending():
    """6. Append vs overwrite - the most common file bug   (notes A.6)"""
    section("6. `a` (append) vs `w` (overwrite)")

    # Start fresh with one line.
    with open("log.txt", "w", encoding="utf-8") as f:
        f.write("original line\n")

    # APPEND adds to the end - the original line is preserved.
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write("appended line\n")
    print("after append:")
    with open("log.txt", "r", encoding="utf-8") as f:
        print(f.read())

    # OVERWRITE wipes everything that was there before.
    with open("log.txt", "w", encoding="utf-8") as f:
        f.write("only this remains\n")
    print("after overwrite:")
    with open("log.txt", "r", encoding="utf-8") as f:
        print(f.read())

    print("--> use `w` when you meant `a`, and your old data is GONE forever.")


# ============================================================
#           SECTION B - TEXT MODE vs BINARY MODE
# ============================================================


def demo_07_text_vs_binary():
    """7. Two kinds of files - text (str) and binary (bytes)   (notes B.1)"""
    section("7. text mode (str) vs binary mode (bytes)")

    # with open("note.txt", "w", encoding="utf-8") as f:
    #     f.write("Hello, world!")

    # # Text mode -> Python gives you a str.
    # with open("note.txt", "r", encoding="utf-8") as f:
    #     data = f.read()
    # print(f"text mode   : type={type(data).__name__}, value={data!r}")

    # Binary mode ('rb') -> same file, but you get raw bytes.
    with open("note.txt", "rb") as f:
        raw = f.read()
    print(f"binary mode : type={type(raw).__name__}, value={raw!r}")
    print(raw)
    print(list(raw))

def demo_08_read_text_vs_bytes():
    """8. Reading the same data as str vs bytes   (notes B.2)"""
    section("8. reading bytes vs text")

    image = need_sample_image()      # a real .jpg sitting next to this script
    if image is None:
        return

    # Reading as bytes is the CORRECT way for an image. The first bytes
    # b'\xff\xd8\xff' are the JPEG signature - that is how a viewer knows
    # this file is a JPEG.
    # with open(image, "rb") as f:
    #     raw = f.read()
    # print(f"reading {image} as bytes:")
    # print(f"  first 4 bytes: {raw[:4]!r}   (\\xff\\xd8\\xff = JPEG signature)")
    # print(f"  length       : {len(raw):,} bytes")

    # Reading the same image AS TEXT crashes - the bytes are not valid UTF-8.
    try:
        with open(image, "r", encoding="utf-8") as f:
            f.read()
    except UnicodeDecodeError as e:
        print(f"reading the image as text -> {type(e).__name__}: {e}")


def demo_09_when_binary():
    """9. When you need binary mode (informational)   (notes B.3)"""
    section("9. when to reach for `rb` / `wb`")

    for line in [
        "Use binary mode for:",
        "  - Images:   .jpg .png .webp   (every multimodal AI app)",
        "  - PDFs:     .pdf              (binary even though they hold text)",
        "  - Archives: .zip .gz .tar",
        "  - AI model files: .pt .safetensors .bin",
        "  - Audio / video files",
        "  - Whatever you get from requests.get(url).content",
        "",
        "Rule of thumb:",
        "  human reads it      -> text mode + encoding='utf-8'",
        "  image/pdf/zip/model -> binary mode + bytes",
    ]:
        print(line)


def demo_10_encode_decode():
    """10. Converting between str and bytes   (notes B.4)"""
    section("10. .encode() and .decode()")

    text = "Hello, \u0c95\u0ca8\u0ccd\u0ca8\u0ca1"   # "Hello, " + Kannada

    # str -> bytes with .encode(encoding)
    raw = text.encode("utf-8")
    print(f"text          : {text!r}")
    print(f"text.encode() : {raw!r}  ({len(raw)} bytes)")

    # bytes -> str with .decode(encoding)
    back = raw.decode("utf-8")
    print(f"raw.decode()  : {back!r}")
    print(f"round trip equal? {text == back}")


def demo_11_copy_binary():
    """11. Copying a binary file - the upload/download pattern   (notes B.5)"""
    section("11. copy a binary file (rb -> wb)")

    image = need_sample_image()      # a real .jpg sitting next to this script
    if image is None:
        return
    copy = "p-36_copy.jpg"

    # Read all the bytes from the source, write them straight to the copy.
    # This same shape is how you save an upload or a downloaded image.
    with open(image, "rb") as src, open(copy, "wb") as dst:
        dst.write(src.read())

    with open(image, "rb") as src, open(copy, "rb") as dst:
        identical = src.read() == dst.read()
    print(f"copied {os.path.getsize(image):,} bytes: {image} -> {copy}")
    print(f"bytes identical? {identical}")
    print(f"--> open {image} and {copy} in your viewer:")
    print("    two identical pictures, copied using only read() and write().")


# ============================================================
#        SECTION C - ENCODING (UTF-8 IS THE RIGHT CHOICE)
# ============================================================

# Defined once so the demos below stay readable.
KANNADA = "\u0c95\u0ca8\u0ccd\u0ca8\u0ca1"        # the word "Kannada" in Kannada
HINDI = "\u0939\u093f\u0902\u0926\u0940"          # "Hindi" in Devanagari
CHINESE = "\u4e2d\u6587"                          # "Chinese"
GRIN = "\U0001f600"                               # grinning face emoji


def demo_12_encoding():
    """12. What is encoding? UTF-8 is the answer.   (notes C.1)"""
    section("12. encoding='utf-8'")

    # encoding='utf-8' is how Python turns the characters below into the exact
    # bytes on disk - and back again on read. It handles every language + emoji.
    with open("hello_world.txt", "w", encoding="utf-8") as f:
        f.write(f"English, {KANNADA}, {HINDI}, {CHINESE}, {GRIN}\n")

    with open("hello_world.txt", "r", encoding="utf-8") as f:
        print(f.read())

    print("encoding='utf-8' = the bridge between bytes on disk and characters.")


def demo_13_history():
    """13. A 60-second history of encodings (informational)   (notes C.2)"""
    section("13. short history of encodings")

    for line in [
        "1963  ASCII   - 128 chars, English only. No Kannada/Hindi/emoji.",
        "80s   cp1252, ISO-8859-1, Shift-JIS, GB2312 - one per region.",
        "      Files broke the moment they crossed a border.",
        "1993  UTF-8   - one encoding for every language + emoji (1-4 bytes/char).",
        "2026  UTF-8 has WON: >98% of the web, every API, every AI model.",
    ]:
        print(line)


def demo_14_without_utf8():
    """14. What goes wrong without encoding='utf-8'   (notes C.3)"""
    section("14. why you must pass encoding='utf-8'")

    # macOS/Linux usually default to utf-8 (safe). Windows often defaults to
    # cp1252, which CANNOT store non-Latin text. We show the default, then
    # force the cp1252 failure that a Windows user would hit silently.
    import locale
    print(f"this machine's default encoding: "
          f"{locale.getpreferredencoding()!r}")

    try:
        KANNADA.encode("cp1252")     # what Windows would try without encoding=
    except UnicodeEncodeError as e:
        print(f"\nencoding Kannada as cp1252 -> {type(e).__name__}:")
        print(f"  {e}")

    raw = KANNADA.encode("utf-8")
    print(f"\nencoding Kannada as utf-8  -> {raw!r}")
    print("--> pass encoding='utf-8' and it works on every OS.")


def demo_15_errors_option():
    """15. The errors= option - strict / replace / ignore   (notes C.4)"""
    section("15. errors='strict' / 'replace' / 'ignore'")

    # A file containing bytes that are NOT valid UTF-8.
    with open("bad_bytes.bin", "wb") as f:
        f.write(b"\xff\xfe\xfd hello world")

    # 1) strict (the default) - crash loudly on bad bytes. Safest.
    try:
        with open("bad_bytes.bin", "r", encoding="utf-8") as f:
            f.read()
    except UnicodeDecodeError as e:
        print(f"errors='strict'  -> {type(e).__name__}: {e}")

    # 2) replace - swap each bad byte with the replacement marker.
    with open("bad_bytes.bin", "r", encoding="utf-8", errors="replace") as f:
        print(f"errors='replace' -> {f.read()!r}")

    # 3) ignore - silently drop bad bytes (you lose data - use with care).
    with open("bad_bytes.bin", "r", encoding="utf-8", errors="ignore") as f:
        print(f"errors='ignore'  -> {f.read()!r}")


def demo_16_utf8_sig():
    """16. The Excel trap - utf-8-sig strips the hidden BOM   (notes C.5)"""
    section("16. utf-8-sig for CSVs exported from Excel")

    # Excel prepends a 3-byte BOM (\xef\xbb\xbf) to its CSV files.
    with open("from_excel.csv", "wb") as f:
        f.write(b"\xef\xbb\xbf" + "name,score\nAlice,95\n".encode("utf-8"))

    # Plain utf-8 leaves a stray \ufeff glued to your first column header.
    with open("from_excel.csv", "r", encoding="utf-8") as f:
        print(f"utf-8     -> header={f.readline()!r}  (BOM sneaks in!)")

    # utf-8-sig recognizes and removes the BOM for you.
    with open("from_excel.csv", "r", encoding="utf-8-sig") as f:
        print(f"utf-8-sig -> header={f.readline()!r}  (clean)")


def demo_17_code_points():
    """17. Bytes vs code points vs grapheme clusters   (notes C.6)"""
    section("17. len() counts code points, NOT what humans see")

    samples = [
        "A",                      # 'A'    -> 1 code point,  1 byte   (plain English)
        KANNADA[0],               # 'ಕ'    -> 1 code point,  3 bytes  (1 letter, 3 bytes!)
        "caf\u00e9",              # 'café' -> 4 code points, 5 bytes  (é is ONE piece)
        "cafe\u0301",             # 'café' -> 5 code points, 6 bytes  (é is e + ´, SAME look!)
        "\U0001f926\U0001f3fd\u200d\u2642\ufe0f",   # '🤦🏽‍♂️' -> 5 code points, 17 bytes (looks like 1!)
    ]
    for s in samples:
        print(f"  {s!r:>24}  code_points={len(s):>2}  bytes={len(s.encode('utf-8')):>2}")

    # Expected output (what the loop above prints):
    #                        'A'  code_points= 1  bytes= 1
    #                        'ಕ'  code_points= 1  bytes= 3
    #                     'café'  code_points= 4  bytes= 5
    #                     'café'  code_points= 5  bytes= 6      <-- looks same as above, len differs!
    #               '🤦🏽\u200d♂️'  code_points= 5  bytes=17     <-- humans see 1 emoji, Python sees 5

    print("\nlen() is right for memory limits - NOT for 'how many letters "
          "did the user type'.")


def demo_18_mojibake():
    """18. Mojibake - garbled text from the wrong decoding   (notes C.7)"""
    section("18. mojibake = bytes decoded with the WRONG encoding")

    original = KANNADA
    raw = original.encode("utf-8")           # the correct bytes
    print(f"correct bytes      : {raw!r}")

    # WRONG: decode UTF-8 bytes as latin-1 -> nonsense.
    garbled = raw.decode("latin-1")
    print(f"decoded as latin-1 : {garbled!r}   <-- mojibake")

    # RIGHT: decode with the SAME encoding used to encode.
    fixed = raw.decode("utf-8")
    print(f"decoded as utf-8   : {fixed!r}   <-- fixed")

    # Expected output:
    #   correct bytes      : b'\xe0\xb2\x95\xe0\xb2\xa8\xe0\xb3\x8d\xe0\xb2\xa8\xe0\xb2\xa1'
    #   decoded as latin-1 : 'à²\x95à²¨à³\x8dà²¨à²¡'   <-- mojibake (wrong encoding = garbage)
    #   decoded as utf-8   : 'ಕನ್ನಡ'   <-- fixed (same encoding back = original text)


def demo_19_normalization():
    """19. Unicode normalization - same look, different bytes   (notes C.8)"""
    section("19. unicodedata.normalize('NFC', ...)")

    import unicodedata

    a = "caf\u00e9"          # e-acute as ONE code point  (U+00E9)
    b = "cafe\u0301"         # e + combining acute          (U+0065 U+0301)
    print(f"a = {a!r}  (len={len(a)})")
    print(f"b = {b!r}  (len={len(b)})")
    print(f"a == b ?  {a == b}    <-- they LOOK identical but differ in bytes")

    a_nfc = unicodedata.normalize("NFC", a)
    b_nfc = unicodedata.normalize("NFC", b)
    print(f"after NFC normalize: a == b ?  {a_nfc == b_nfc}")
    print("Normalize before: comparing input, deduping, hashing, indexing.")

    # Expected output:
    #   a = 'café'  (len=4)                <-- é stored as 1 piece
    #   b = 'café'  (len=5)                <-- é stored as 2 pieces (e + ´), SAME look
    #   a == b ?  False                    <-- identical on screen, NOT equal to Python!
    #   after NFC normalize: a == b ?  True   <-- normalizing makes them match


def demo_20_python_default():
    """20. Python is moving to UTF-8 by default (informational)   (notes C.9)"""
    section("20. PEP 597 and PEP 686")

    for line in [
        "PEP 597 - turn on EncodingWarning TODAY to catch code that forgot",
        "          encoding=. Run with `-X warn_default_encoding`, or set",
        "          PYTHONWARNDEFAULTENCODING=1 in your environment.",
        "",
        "PEP 686 - Python 3.15 makes UTF-8 mode the default on all platforms.",
        "",
        "Until then: ALWAYS pass encoding='utf-8' yourself. No exceptions.",
        "If you truly want the OS locale (rare): encoding='locale'.",
    ]:
        print(line)


# ============================================================
#         SECTION D - THE FILE POINTER (tell / seek)
# ============================================================


def demo_21_pointer_intro():
    """21. What is the file pointer? (informational)   (notes D.1)"""
    section("21. the file pointer (the cursor inside the file)")

    for line in [
        "Every open file tracks a POSITION: where the next read/write happens.",
        "Each read or write moves that position forward.",
        "",
        "  tell() -> 'where am I?'   (bytes from the start)",
        "  seek() -> 'jump to here'",
        "",
        "Understanding this saves you from the #1 confusing file bug:",
        "  'I wrote to the file, but reading it shows nothing!'  (see section 25)",
    ]:
        print(line)


def demo_22_tell():
    """22. tell() - the current position, in bytes from the start   (notes D.2)"""
    section("22. tell()")

    with open("greeting.txt", "w", encoding="utf-8") as f:
        print(f"at the start    : tell() = {f.tell()}")
        f.write("Hello")
        print(f"after 'Hello'   : tell() = {f.tell()}")
        f.write(", world!")
        print(f"after the rest  : tell() = {f.tell()}")


def demo_23_seek():
    """23. seek(offset, whence) - jump around inside the file   (notes D.3)"""
    section("23. seek()")

    with open("greeting.txt", "w", encoding="utf-8") as f:
        f.write("Hello, world!")

    with open("greeting.txt", "r", encoding="utf-8") as f:
        f.seek(0)                # whence=0 (default): from the START
        print(f"seek(0),  read(5) -> {f.read(5)!r}")

        f.seek(7)                # jump straight to byte 7
        print(f"seek(7),  read()  -> {f.read()!r}")

        f.seek(0, 2)             # whence=2: measure from the END
        print(f"seek(0, 2), tell() = {f.tell()}  (= size of the file)")


def demo_24_plus_modes():
    """24. The + modes - read AND write one file (r+/w+/a+)   (notes D.4)"""
    section("24. r+ / w+ / a+  (read and write together)")

    # Start with a file that already has content (so r+ has something to read).
    with open("plus_demo.txt", "w", encoding="utf-8") as f:
        f.write("line one\n")

    # r+ : the file must EXIST. Read it, then writing continues from the pointer.
    with open("plus_demo.txt", "r+", encoding="utf-8") as f:
        old = f.read()                       # this moves the pointer to the END
        f.write("line two (added by r+)\n")
        print(f"r+ read first  -> {old!r}")
    with open("plus_demo.txt", "r", encoding="utf-8") as f:
        print(f"file after r+  -> {f.read()!r}\n")

    # w+ : creates/WIPES the file, opens for read+write. Pointer at the start.
    with open("plus_demo.txt", "w+", encoding="utf-8") as f:
        f.write("fresh content")
        f.seek(0)                            # rewind to read what we just wrote
        print(f"w+ wiped+wrote -> {f.read()!r}")

    # a+ : creates if missing, NEVER wipes. Pointer starts at the END.
    with open("plus_demo.txt", "a+", encoding="utf-8") as f:
        f.write(" + appended")
        f.seek(0)                            # a+ starts at the end, so rewind to read all
        print(f"a+ appended    -> {f.read()!r}")


def demo_25_empty_read_bug():
    """25. The classic 'why is my file empty?' bug   (notes D.5)"""
    section("25. write then read: the pointer is at the END")

    # THE BUG: after write(), the pointer sits at the end. read() finds
    # nothing after it, so you get an empty string.
    with open("rw_demo.txt", "w+", encoding="utf-8") as f:
        f.write("Hello, world!")
        content = f.read()
        print(f"no seek(0): content = {content!r}   <-- empty!")

    # THE FIX: seek(0) rewinds to the start before reading.
    with open("rw_demo.txt", "w+", encoding="utf-8") as f:
        f.write("Hello, world!")
        f.seek(0)
        content = f.read()
        print(f"seek(0)   : content = {content!r}")


# ============================================================
#             SECTION E - REAL-WORLD PATTERNS
# ============================================================


def demo_26_exception_handling():
    """26. Combining `with open` and try/except   (notes E.1)"""
    section("26. handle FileNotFoundError gracefully")

    def read_file_safe(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            print(f"  file not found: {filename}")
            return None

    # A missing file: we get None instead of a crash.
    result = read_file_safe("never_created.txt")
    print(f"result = {result!r}\n")

    # A real file: we get its contents.
    with open("real.txt", "w", encoding="utf-8") as f:
        f.write("I exist.\n")
    result = read_file_safe("real.txt")
    print(f"result = {result!r}")


def demo_27_save_load():
    """27. A complete save / load round-trip   (notes E.2)"""
    section("27. save_items / load_items")

    def save_items(filename, items):
        """Save a list of items, one per line."""
        with open(filename, "w", encoding="utf-8") as f:
            for item in items:
                f.write(f"{item}\n")

    def load_items(filename):
        """Load items back into a list. Missing file -> empty list."""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return [line.strip() for line in f]
        except FileNotFoundError:
            return []

    tasks = ["Buy milk", "Study Python", "Exercise"]
    save_items("tasks.txt", tasks)
    print(f"saved  : {tasks}")
    print(f"loaded : {load_items('tasks.txt')}")


def demo_28_common_bugs():
    """28. The 8 most common file bugs (informational)   (notes E.3)"""
    section("28. bugs to avoid")

    bugs = [
        "FileNotFoundError - reading a missing file. Wrap in try/except.",
        "Overwrite vs append - `w` erases everything; use `a` to add.",
        "Forgot encoding= - crashes on Kannada/Hindi/emoji (esp. Windows).",
        "Forgot .strip() - readline()/for-line keep the trailing \\n.",
        "Reading a huge file with .read() - OOM. Loop line by line instead.",
        "Wrote a str to a 'wb' file - TypeError. .encode('utf-8') first.",
        "Read right after write without seek(0) - you get an empty string.",
        "Excel CSV has a hidden BOM - use encoding='utf-8-sig'.",
    ]
    for i, bug in enumerate(bugs, start=1):
        print(f"  {i}. {bug}")


def demo_29_where_used():
    """29. Where files show up in real work (informational)   (notes E.4)"""
    section("29. every real app uses open()")

    for line in [
        "Config files     : config.json, .env, settings.yaml",
        "Log files        : servers write log lines continuously",
        "User data        : notes apps, todo apps, draft saves",
        "Reports          : read documents in, write summaries out",
        "Data pipelines   : raw CSV/JSON in, processed files out",
        "AI training data : every Hugging Face / Kaggle dataset is files",
        "AI agent memory  : Cursor, Claude Code, Continue - .md files on disk",
        "Multimodal AI    : image to GPT-4o = open('rb') + base64-encode",
    ]:
        print(line)


def demo_30_print_is_file_write():
    """30. print() is just a file write to sys.stdout   (notes E.5)"""
    section("30. print(...) is f.write under the hood")

    # print() can target ANY file object via file=, not only the screen.
    with open("print_to_file.txt", "w", encoding="utf-8") as f:
        print("Hello, file!", file=f)            # same as f.write("Hello, file!\n")
        print("col a", "col b", file=f, sep=" | ")

    # This one goes to sys.stdout - the file object wired to your terminal.
    print("on screen: same primitive, different destination (sys.stdout)")

    print("\ncontents that print() wrote to the file:")
    with open("print_to_file.txt", "r", encoding="utf-8") as f:
        print(f.read())


def demo_31_when_files_enough():
    """31. When files are enough - and when they are not (informational)   (notes E.6)"""
    section("31. files first, databases when you need them")

    rows = [
        ("Need", "Start with", "Graduate to"),
        ("Single-user notes / config", "Text or JSON file", "-"),
        ("Structured queries, < 100 MB", "JSON file", "SQLite (one file!)"),
        ("Multi-user web app", "-", "PostgreSQL / MySQL"),
        ("Sharing across machines", "-", "S3 / cloud storage"),
        ("Fast key lookups", "-", "Redis"),
    ]
    for need, start, grad in rows:
        print(f"  {need:<32} {start:<20} {grad:<22}")


# ============================================================
#                     CLI DISPATCHER
# ============================================================


DEMOS = {
    # Section A - The Basics
    "1": demo_01_open_basic,
    "2": demo_02_modes,
    "3": demo_03_with_statement,
    "4": demo_04_reading_methods,
    "5": demo_05_writing,
    "6": demo_06_appending,
    # Section B - Text vs Binary
    "7": demo_07_text_vs_binary,
    "8": demo_08_read_text_vs_bytes,
    "9": demo_09_when_binary,
    "10": demo_10_encode_decode,
    "11": demo_11_copy_binary,
    # Section C - Encoding
    "12": demo_12_encoding,
    "13": demo_13_history,
    "14": demo_14_without_utf8,
    "15": demo_15_errors_option,
    "16": demo_16_utf8_sig,
    "17": demo_17_code_points,
    "18": demo_18_mojibake,
    "19": demo_19_normalization,
    "20": demo_20_python_default,
    # Section D - The File Pointer
    "21": demo_21_pointer_intro,
    "22": demo_22_tell,
    "23": demo_23_seek,
    "24": demo_24_plus_modes,
    "25": demo_25_empty_read_bug,
    # Section E - Real-World Patterns
    "26": demo_26_exception_handling,
    "27": demo_27_save_load,
    "28": demo_28_common_bugs,
    "29": demo_29_where_used,
    "30": demo_30_print_is_file_write,
    "31": demo_31_when_files_enough,
}


def print_list():
    print("Part 36 - File Handling, one section at a time\n")
    for key, fn in DEMOS.items():
        print(f"  {key:>3}  {fn.__doc__ or fn.__name__}")
    print(
        "\nRun a single section:    python3 example.py 1"
        "\nRun a few in sequence:   python3 example.py 1 2 3"
        "\n\nFiles created by the demos appear in the folder you run this from."
    )


def main(argv):
    args = argv[1:]

    if not args or args[0].lower() in ("list", "--list", "-l", "help", "--help", "-h"):
        print_list()
        return

    for arg in args:
        fn = DEMOS.get(arg)
        if fn is None:
            print(
                f"Unknown section: {arg!r}. "
                f"Run `python3 example.py list` to see all sections."
            )
            sys.exit(2)
        fn()
        print()


if __name__ == "__main__":
    main(sys.argv)
