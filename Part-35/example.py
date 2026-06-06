"""
Part 35 — Exceptions Hands-On (runnable demos).

USAGE
-----
Run a single section by its number or letter:
    python3 example.py 4         # only #4 TypeError
    python3 example.py 12        # only #12 FileNotFoundError
    python3 example.py A         # Custom Exceptions demo

List every section with its title:
    python3 example.py list

NOTE on "run all": this file is designed for one-section-at-a-time
teaching. Most BROKEN blocks are ACTIVE (uncommented) by default, so
running `python3 example.py` end-to-end will stop at the first
uncaught exception. That is intentional.

INSIDE EACH SECTION
-------------------
Every demo function contains TWO blocks:

    --- BROKEN (active)        : runs as-is. The error appears live.
    --- FIX    (commented out) : the working version. Uncomment after
                                 you have explained the error to fix it.

TEACHING FLOW (per section)
---------------------------
  1. python3 example.py 4
        -> students see the actual TypeError traceback.
  2. Explain what TypeError means and why it happened.
  3. Open example.py, scroll to demo_04_type_error:
        a. comment out the BROKEN block (or leave it, your choice)
        b. uncomment the FIX block.
  4. python3 example.py 4
        -> students see the FIX print correctly. "Now it works."
  5. python3 example.py 5
        -> next section.

Two sections are special and have BROKEN kept commented:
    #1 SyntaxError, #2 IndentationError
        -> parse-time errors stop the whole file from loading.
        -> copy the BROKEN lines into a fresh file (e.g. bug.py) and
           run that file to demo the error live.
    #26 MemoryError
        -> would actually exhaust your RAM and freeze the machine.
        -> commented with a warning. Treat it as read-only.
"""

import sys


def section(title):
    width = 60
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width)
    print()


# ============================================================
#                 GROUP 1 — EVERYDAY ERRORS
# ============================================================


def demo_01_syntax_error():
    """1. SyntaxError — Python cannot even read your code"""
    section("1. SyntaxError")

    # SPECIAL: SyntaxError happens at parse time. If you uncomment the
    # block below, the WHOLE FILE will fail to load (you would not even
    # reach this print). To demo it live, copy these two lines into a
    # fresh file `bug.py` and run `python3 bug.py`:
    #
    # --- BROKEN (copy to bug.py, do not uncomment here) ---
    x=50
    if x == 5:
        print("hello")

    # --- FIX (active by default, since this is a copy-out demo) ---
    # x = 5
    # if x == 5:
    #     print("hello  (SyntaxError fixed: == not =)")


def demo_02_indentation_error():
    """2. IndentationError — wrong spaces or tabs"""
    section("2. IndentationError")

    # SPECIAL: parse-time error, same caveat as #1. Copy the BROKEN
    # block to bug.py to demo it live.
    #
    # --- BROKEN (copy to bug.py, do not uncomment here) ---
    def greet_bad():
        print("hello")
    greet_bad()

    # --- FIX (active by default) ---
    # def greet():
    #     print("hello  (IndentationError fixed: 4-space indent)")

    # greet()


def demo_03_name_error():
    """3. NameError — variable was never defined"""
    section("3. NameError")

    # --- BROKEN (active) ---
    print("hello")

    # --- FIX (uncomment after explaining) ---
    # print("hello  (NameError fixed: typo 'prnit' -> 'print')")


def demo_04_type_error():
    """4. TypeError — wrong type for the operation"""
    section("4. TypeError")

    # --- BROKEN (active) ---
    # age = "25"
    # next_year = age + 1
    # print(next_year)

    # --- FIX (uncomment after explaining) ---
    age = int("25")
    next_year = age + 1
    print(f"next_year = {next_year}  (TypeError fixed: int('25') + 1)")


def demo_05_value_error():
    """5. ValueError — right type, wrong value"""
    section("5. ValueError")

    # --- BROKEN (active) ---
    # number = int("hello")
    # print(number)

    # --- FIX (uncomment after explaining) ---
    raw = "hello"
    try:
        number = int(raw)
        print(f"number = {number}")
    except ValueError:
        print(f"'{raw}' is not a number  (ValueError handled with try/except)")
        
        
def demo_06_key_error():
    """6. KeyError — dictionary key does not exist"""
    section("6. KeyError")

    user = {"name": "Alice", "age": 30}

    # --- BROKEN (active) ---
    # print(user["name"])

    # --- FIX (uncomment after explaining) ---
    email = user.get("email", "USER@GMAIL.COM")
    print(f"email = {email}  (KeyError fixed: use dict.get with default)")


def demo_07_index_error():
    """7. IndexError — list position does not exist"""
    section("7. IndexError")

    numbers = [10, 20, 30]

    # --- BROKEN (active) ---
    # print(numbers[5])

    # --- FIX (uncomment after explaining) ---
    if len(numbers) > 2:
        print(numbers[2])
    else:
        print(f"only {len(numbers)} items  (IndexError prevented: length-check)")


def demo_08_attribute_error():
    """8. AttributeError — object has no such method or attribute"""
    section("8. AttributeError")

    name = "alice"

    # --- BROKEN (active) ---
    name.append(" smith")

    # --- FIX (uncomment after explaining) ---
    # full_name = name + " smith"
    # print(f"full_name = {full_name!r}  (AttributeError fixed: + instead of .append)")


def demo_09_zero_division_error():
    """9. ZeroDivisionError — divided by zero"""
    section("9. ZeroDivisionError")

    total = 100
    people = 0

    # --- BROKEN (active) ---
    # average = total / people
    # print(average)

    # --- FIX (uncomment after explaining) ---
    average = total / people if people else 0
    print(f"average = {average}  (ZeroDivisionError prevented: guard people==0)")


def demo_10_module_not_found_error():
    """10. ModuleNotFoundError — package is not installed"""
    section("10. ModuleNotFoundError")

    # --- BROKEN (active) ---
    # import definitely_fake_pkg  # noqa: F401

    # --- FIX (uncomment after explaining) ---
    try:
        import definitely_fake_pkg  # noqa: F401
    except ModuleNotFoundError as e:
        print(f"missing package: {e}  (ModuleNotFoundError handled)")


def demo_11_import_error():
    """11. ImportError — package is there, but the name inside is wrong"""
    section("11. ImportError")

    # --- BROKEN (active) ---
    # from math import xyz  # noqa: F401

    # --- FIX (uncomment after explaining) ---
    from math import sqrt
    print(f"sqrt(16) = {sqrt(16)}  (ImportError fixed: use a real name)")


# ============================================================
#             GROUP 2 — FILE & NETWORK ERRORS
# ============================================================


def demo_12_file_not_found_error():
    """12. FileNotFoundError — the file is not there"""
    section("12. FileNotFoundError")

    # --- BROKEN (active) ---
    with open("definitely_missing_file.txt") as f:
        print(f.read())

    # --- FIX (uncomment after explaining) ---
    try:
        with open("definitely_missing_file.txt") as f:
            config = f.read()
    except FileNotFoundError:
        config = "default"
        print(f"file missing, using {config!r}  (FileNotFoundError handled)")


def demo_13_permission_error():
    """13. PermissionError — file exists but the OS says no"""
    section("13. PermissionError")

    # --- BROKEN (active) ---
    # NOTE: writing /etc/passwd is denied by macOS/Linux SIP — it is
    # safe to run; the OS rejects it with PermissionError.
    # with open("/etc/passwd", "w") as f:
    #     f.write("nope")

    # --- FIX (uncomment after explaining) ---
    try:
        with open("/etc/passwd", "w") as f:
            f.write("nope")
    except PermissionError as e:
        print(f"refused: {e}  (PermissionError handled: pick a writable folder)")


def demo_14_os_error():
    """14. OSError — the generic OS error (parent of file errors)"""
    section("14. OSError")

    import os

    # --- BROKEN (active): bad file descriptor -> plain OSError ---
    # os.fdopen(99999, "r")

    # --- FIX (uncomment after explaining) ---
    # try:
    #     os.fdopen(99999, "r")
    # except OSError as e:
    #     print(f"bad fd: {e}  (OSError handled)")


    fd = os.open("hello.txt", os.O_RDONLY)
    print("OS gave me fd =", fd)
    f = os.fdopen(fd, "r")
    print(f.read())
    f.close()

def demo_15_connection_error():
    """15. ConnectionError — the network failed"""
    section("15. ConnectionError")

    import urllib.request

    # --- BROKEN (active) ---
    # urllib.request.urlopen(
    #     "http://this-domain-does-not-exist-12345.com", timeout=2
    # )

    # --- FIX (uncomment after explaining) ---
    import urllib.error
    try:
        urllib.request.urlopen(
            "http://this-domain-does-not-exist-12345.com", timeout=2
        )
    except (urllib.error.URLError, ConnectionError, OSError) as e:
        print(f"network problem: {e}  (ConnectionError handled)")


def demo_16_timeout_error():
    """16. TimeoutError — operation took too long"""
    section("16. TimeoutError")

    import socket

    # --- BROKEN (active) ---
    # socket.create_connection(("example.com", 80), timeout=0.001)

    # --- FIX (uncomment after explaining) ---
    try:
        socket.create_connection(("example.com", 80), timeout=0.001)
    except (TimeoutError, OSError) as e:
        print(f"too slow: {e}  (TimeoutError handled: try a longer timeout)")


# ============================================================
#          GROUP 3 — PROGRAM BEHAVIOR ERRORS
# ============================================================


def demo_17_keyboard_interrupt():
    """17. KeyboardInterrupt — user pressed Ctrl+C"""
    section("17. KeyboardInterrupt")
    print("(this section will run forever — press Ctrl+C to stop it)")

    import time

    # --- BROKEN (active): infinite loop. Press Ctrl+C in the terminal. ---
    # while True:
    #     print("working...")
    #     time.sleep(1)

    # --- FIX (uncomment after explaining; comment the loop above) ---
    try:
        while True:
            print("working...")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nstopped by user, saving and exiting  (KeyboardInterrupt handled)")


def demo_18_recursion_error():
    """18. RecursionError — function called itself too many times"""
    section("18. RecursionError")

    # --- BROKEN (active) ---
    # def runaway(n):
    #     return runaway(n + 1)

    # runaway(0)

    # --- FIX (uncomment after explaining) ---
    def countdown(n):
        if n <= 0:
            return "done"
        return countdown(n - 1)
    print(f"countdown(5) = {countdown(5)}  (RecursionError prevented: base case)")


def demo_19_unbound_local_error():
    """19. UnboundLocalError — used a local variable before assigning"""
    section("19. UnboundLocalError")

    # --- BROKEN (active) ---
    
    def add_one_bad():
        count = 0
        count = count + 1
        return count

    print(add_one_bad())

    # --- FIX (uncomment after explaining) ---
    # def add_one(count):
    #     count = count + 1
    #     return count
    # print(f"add_one(0) = {add_one(0)}  (UnboundLocalError fixed: pass argument)")


def demo_20_stop_iteration():
    """20. StopIteration — iterator has no more values"""
    section("20. StopIteration")

    # --- BROKEN (active) ---
    # it = iter([1, 2])
    # next(it)
    # next(it)

    # --- FIX (uncomment after explaining) ---
    it = iter([1, 2])
    while True:
        try:
            print(f"  next -> {next(it)}")
        except StopIteration:
            print("done  (StopIteration handled, or just use a for loop)")
            break


def demo_21_runtime_error():
    """21. RuntimeError — generic runtime problem"""
    section("21. RuntimeError")

    # --- BROKEN (active) ---
    # d = {"a": 1, "b": 2}
    # for key in d:
    #     del d[key]

    # --- FIX (uncomment after explaining) ---
    d = {"a": 1, "b": 2}
    for key in list(d):
        del d[key]
    print(f"d = {d}  (RuntimeError prevented: iterate list(d))")


def demo_22_assertion_error():
    """22. AssertionError — your sanity check failed"""
    section("22. AssertionError")

    # --- BROKEN (active) ---
    # def withdraw_bad(balance, amount):
    #     assert amount > 0, "amount must be positive 111"
    #     return balance - amount

    # withdraw_bad(100, -50)

    # --- FIX (uncomment after explaining) ---
    def withdraw(balance, amount):
        if amount <= 0:
            raise ValueError(f"amount must be positive, got {amount}")
        return balance - amount
    
    
    try:
        withdraw(100, -50)
    except ValueError as e:
        print(f"refused: {e}  (AssertionError replaced with proper raise)")


# ============================================================
#       GROUP 4 — LESS COMMON (recognize, rarely catch)
# ============================================================


def demo_23_system_exit():
    """23. SystemExit — sys.exit() was called"""
    section("23. SystemExit")
    print("(this section will exit the script with code 1)")

    # --- BROKEN (active): the script will exit here ---
    # sys.exit("usage: python script.py <name>")

    # --- FIX (uncomment after explaining) ---
    try:
        sys.exit("simulated exit")
    except SystemExit as e:
        print(f"sys.exit raised: {e}  (SystemExit normally exits the program)")


def demo_24_overflow_error():
    """24. OverflowError — number too big for the type (floats)"""
    section("24. OverflowError")

    import math

    # --- BROKEN (active) ---
    # print(math.exp(1000))

    # --- FIX (uncomment after explaining) ---
    try:
        math.exp(1000)
    except OverflowError as e:
        print(f"too big: {e}  (OverflowError handled: use log space)")


def demo_25_unicode_decode_error():
    """25. UnicodeDecodeError — bytes do not match the declared encoding"""
    section("25. UnicodeDecodeError")

    import os

    # Setup: create a tiny binary file with bytes that are NOT valid UTF-8.
    # In real life you hit this when a file was saved in a different
    # encoding (e.g. Windows-1252) but you opened it as UTF-8.
    demo_file = "_part35_encoding_demo.bin"
    with open(demo_file, "wb") as f:
        f.write(b"\xff\xfe\xfd hello")

    try:
        # --- BROKEN (active) ---
        # We tell Python "this file is UTF-8" via encoding="utf-8",
        # but the first three bytes (0xff 0xfe 0xfd) are illegal in UTF-8.
        # Python refuses to decode them and raises UnicodeDecodeError.
        # with open(demo_file, encoding="utf-8") as f:
        #     print(f.read())

        # --- FIX (uncomment after explaining; comment the BROKEN block above) ---
        # errors="replace" tells Python: "do not crash on bad bytes —
        # swap each unreadable byte with the replacement character �".
        # Use this when you must read a file of unknown/legacy encoding
        # and you would rather see partial text than a crash.
        #
        with open(demo_file, encoding="utf-8", errors="replace") as f:
            text = f.read()
        print(f"read with errors='replace': {text!r}  (UnicodeDecodeError handled)")
    finally:
        if os.path.exists(demo_file):
            os.remove(demo_file)


def demo_26_memory_error():
    """26. MemoryError — out of RAM"""
    section("26. MemoryError")

    # SPECIAL: do NOT uncomment the BROKEN block — it can freeze your
    # machine for real. Treat it as read-only. The FIX below shows the
    # production-grade pattern (process data in chunks).
    #
    # --- BROKEN (read-only; freezes your machine if uncommented) ---
    # big = [0] * (10 ** 12)
    # print(len(big))

    # --- FIX (active by default) ---
    def chunked(seq, size):
        for i in range(0, len(seq), size):
            yield seq[i : i + size]

    total = sum(sum(chunk) for chunk in chunked(list(range(1000)), 100))
    print(f"chunked sum = {total}  (MemoryError prevented: process in chunks)")


def demo_27_not_implemented_error():
    """27. NotImplementedError — placeholder, not yet written"""
    section("27. NotImplementedError")

    class PaymentGateway:
        def charge(self, amount):
            raise NotImplementedError("Subclasses must implement charge()")

    # --- BROKEN (active) ---
    PaymentGateway().charge(100)

    # --- FIX (uncomment after explaining) ---
    # class StripeGateway(PaymentGateway):
    #     def charge(self, amount):
    #         return f"charged ${amount} via Stripe"
    # print(f"{StripeGateway().charge(100)}  (NotImplementedError fixed: subclass it)")


# ============================================================
#       PATTERN DEMOS — same as in notes.md
# ============================================================
# These are NOT broken-vs-fix demos. They show end-to-end patterns.


def demo_A_custom_exceptions():
    """A. Custom Exceptions — Bank Account"""
    section("A. Custom Exceptions — Bank Account")

    class InsufficientFundsError(Exception):
        pass

    class NegativeAmountError(Exception):
        pass

    class Account:
        def __init__(self, owner, balance=0):
            self.owner = owner
            self.balance = balance

        def withdraw(self, amount):
            if amount <= 0:
                raise NegativeAmountError(f"amount must be positive, got {amount}")
            if amount > self.balance:
                raise InsufficientFundsError(
                    f"{self.owner} tried to withdraw {amount} but balance is {self.balance}"
                )
            self.balance -= amount
            return self.balance

    account = Account("Alice", balance=100)
    for attempt in [50, -10, 200, 25]:
        try:
            new_balance = account.withdraw(attempt)
            print(f"OK -- withdrew {attempt}, balance now {new_balance}")
        except NegativeAmountError as e:
            print(f"bad amount: {e}")
        except InsufficientFundsError as e:
            print(f"refused: {e}")


def demo_B_try_except_else_finally():
    """B. try / except / else / finally"""
    section("B. try / except / else / finally")

    def divide(a, b):
        try:
            result = a / b
        except ZeroDivisionError:
            print("  cannot divide by zero")
            return None
        else:
            print("  division succeeded")
            return result
        finally:
            print("  done with divide()")

    print(f"divide(10, 2) = {divide(10, 2)}")
    print("---")
    print(f"divide(10, 0) = {divide(10, 0)}")


def demo_C_exception_chaining():
    """C. Exception Chaining (raise ... from e)"""
    section("C. Exception Chaining (raise ... from e)")

    class ConfigError(Exception):
        pass

    def load_timeout(config):
        try:
            return int(config["timeout"])
        except KeyError as e:
            raise ConfigError("config is missing the 'timeout' key") from e
        except ValueError as e:
            raise ConfigError(
                f"timeout must be a number, got {config['timeout']!r}"
            ) from e

    try:
        load_timeout({"retries": 3})
    except ConfigError as e:
        print(f"high-level: {e}")
        print(f"caused by:  {type(e.__cause__).__name__}: {e.__cause__}")


def demo_D_reraise():
    """D. Re-raise after logging"""
    section("D. Re-raise After Logging")

    def process(data):
        try:
            return int(data)
        except ValueError:
            print(f"  [log] bad data seen: {data!r}")
            raise

    try:
        process("not a number")
    except ValueError as e:
        print(f"top-level caught: {e}")


def demo_E_retry():
    """E. Retry with exponential backoff"""
    section("E. Retry with Exponential Backoff")

    import random
    import time

    class TemporaryError(Exception):
        pass

    def flaky_operation():
        if random.random() < 0.7:
            raise TemporaryError("network glitch")
        return "got the data"

    def with_retry(func, max_retries=4, delay=0.2):
        for attempt in range(1, max_retries + 1):
            try:
                print(f"  attempt {attempt}...")
                return func()
            except TemporaryError as e:
                if attempt == max_retries:
                    print("  out of retries, giving up")
                    raise
                print(f"    failed ({e}), retrying in {delay:.2f}s")
                time.sleep(delay)
                delay *= 2

    try:
        print(f"result: {with_retry(flaky_operation)}")
    except TemporaryError as e:
        print(f"final failure: {e}")


def demo_F_fallback():
    """F. Fallback / graceful degradation"""
    section("F. Fallback / Graceful Degradation")

    def fetch_user_name(user_id):
        raise ConnectionError("API down")

    def display_name(user_id):
        try:
            return fetch_user_name(user_id)
        except ConnectionError:
            return f"User #{user_id}"

    print(f"display_name(42) = {display_name(42)!r}  (graceful fallback)")


# ============================================================
#                     CLI DISPATCHER
# ============================================================


DEMOS = {
    "1":  demo_01_syntax_error,
    "2":  demo_02_indentation_error,
    "3":  demo_03_name_error,
    "4":  demo_04_type_error,
    "5":  demo_05_value_error,
    "6":  demo_06_key_error,
    "7":  demo_07_index_error,
    "8":  demo_08_attribute_error,
    "9":  demo_09_zero_division_error,
    "10": demo_10_module_not_found_error,
    "11": demo_11_import_error,
    "12": demo_12_file_not_found_error,
    "13": demo_13_permission_error,
    "14": demo_14_os_error,
    "15": demo_15_connection_error,
    "16": demo_16_timeout_error,
    "17": demo_17_keyboard_interrupt,
    "18": demo_18_recursion_error,
    "19": demo_19_unbound_local_error,
    "20": demo_20_stop_iteration,
    "21": demo_21_runtime_error,
    "22": demo_22_assertion_error,
    "23": demo_23_system_exit,
    "24": demo_24_overflow_error,
    "25": demo_25_unicode_decode_error,
    "26": demo_26_memory_error,
    "27": demo_27_not_implemented_error,
    "A":  demo_A_custom_exceptions,
    "B":  demo_B_try_except_else_finally,
    "C":  demo_C_exception_chaining,
    "D":  demo_D_reraise,
    "E":  demo_E_retry,
    "F":  demo_F_fallback,
}


def print_list():
    print("Available sections:\n")
    for key, fn in DEMOS.items():
        print(f"  {key:>3}  {fn.__doc__ or fn.__name__}")
    print(
        "\nRun a single section:    python3 example.py 4"
        "\nRun a few in sequence:   python3 example.py 12 13 14"
        "\n                         python3 example.py A B"
        "\n\nNote: most BROKEN blocks are active by default. Running"
        "\n`python3 example.py` end-to-end stops at the first error."
    )


def main(argv):
    args = argv[1:]

    if not args:
        for fn in DEMOS.values():
            fn()
            print()
        print("\nAll demos complete.")
        return

    if args[0].lower() in ("list", "--list", "-l", "help", "--help", "-h"):
        print_list()
        return

    for arg in args:
        key = arg.upper() if arg.isalpha() else arg
        fn = DEMOS.get(key)
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


