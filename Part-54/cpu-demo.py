"""Part 54 Lab 0 — See concurrency & the GIL with your own eyes.

The whole point of this script is to make the GIL, threads, and processes
VISIBLE in Activity Monitor (Mac) or Task Manager (Windows). You'll watch
Python's own CPU usage prove the theory in real time.

USAGE
-----
  python cpu-demo.py            # show machine info + how to use
  python cpu-demo.py 1          # one thread    → ~1 core busy   (the mystery)
  python cpu-demo.py 2          # max threads   → STILL ~1 core  (GIL is real!)
  python cpu-demo.py 3          # max processes → ALL cores busy (parallelism)

Override the count (defaults to your total logical cores):
  python cpu-demo.py 2 100      # try 100 threads (still ~1 core!)
  python cpu-demo.py 3 4        # try only 4 processes on a 14-core box

Press Ctrl+C to stop any demo.
"""

from __future__ import annotations

import multiprocessing
import os
import platform
import subprocess
import sys
import threading


# ═══════════════════════════════════════════════════════════════════════════
# Machine detection — so students see THEIR chip, THEIR cores, THEIR math
# ═══════════════════════════════════════════════════════════════════════════

def core_count() -> int:
    """Number of logical CPUs (physical cores × hardware-threads-per-core)."""
    return os.cpu_count() or 4


def chip_name() -> str:
    """Best-effort friendly chip name."""
    system = platform.system()
    if system == "Darwin":
        try:
            out = subprocess.check_output(
                ["sysctl", "-n", "machdep.cpu.brand_string"], text=True
            ).strip()
            if out:
                return out
        except Exception:
            pass
    return platform.processor() or platform.machine() or "Unknown chip"


def print_banner(cores: int) -> None:
    """One-glance diagnostic — what students should see on their machine."""
    per_core = 100 / cores
    print("━" * 64)
    print(f" Chip                 : {chip_name()}")
    print(f" OS                   : {platform.system()} {platform.release()}")
    print(f" Python               : {platform.python_version()}")
    print(f" Logical CPU cores    : {cores}")
    print("─" * 64)
    print(" How to read Activity Monitor / Task Manager:")
    print(f"   Method 1 (per-process, can go above 100%):")
    print(f"     • 1 core busy   = 100%   of that process")
    print(f"     • All cores busy = {cores * 100}%  of that process")
    print(f"   Method 2 (system-wide total, always max 100%):")
    print(f"     • 1 core busy   ≈ {per_core:5.1f}%  of total system CPU")
    print(f"     • All cores busy ≈ 100.0%  of total system CPU")
    print("━" * 64)


# ═══════════════════════════════════════════════════════════════════════════
# The workload — a pure Python CPU-bound infinite loop
# ═══════════════════════════════════════════════════════════════════════════

def burn_cpu() -> None:
    """Never returns. Pure Python bytecode — always needs the GIL to run."""
    x = 0
    while True:
        x = (x + 1) % 1_000_000


# ═══════════════════════════════════════════════════════════════════════════
# Demo 1 — ONE thread   (the mystery: 1 core busy, the rest idle)
# ═══════════════════════════════════════════════════════════════════════════

def demo_one_thread(_n: int) -> None:
    cores = core_count()
    print("DEMO 1 — ONE thread burning CPU\n")
    print("Watch Activity Monitor / Task Manager:")
    print(f"  • The `python` process shows ~100% CPU (that's 100% of 1 core)")
    print(f"  • Total system CPU rises by only ~{100 / cores:.1f}%")
    print(f"  • {cores - 1} of your {cores} cores stay idle")
    print("  • You paid for all cores. Python is only using one.")
    print("\n>>> THIS IS THE MYSTERY. Part 54 sets out to solve it. <<<\n")
    print("Press Ctrl+C to stop.\n")
    burn_cpu()


# ═══════════════════════════════════════════════════════════════════════════
# Demo 2 — Many threads  (still ~1 core — the GIL is real!)
# ═══════════════════════════════════════════════════════════════════════════

def demo_many_threads(n: int) -> None:
    print(f"DEMO 2 — {n} threads burning CPU\n")
    print("Watch Activity Monitor / Task Manager:")
    print(f"  • The `python` process spawns {n} REAL OS threads")
    print(f"  • Look at the Threads column — you'll see {n} (plus a few more)")
    print(f"  • But CPU usage is STILL only ~100% (1 core's worth)!")
    print(f"  • The GIL forces all {n} threads to take turns running Python")
    print(f"  • Only ONE thread executes Python bytecode at any instant")
    print("\n>>> THIS PROVES THE GIL. Threads don't parallelise Python CPU work. <<<\n")
    print("Press Ctrl+C to stop.\n")
    threads = [threading.Thread(target=burn_cpu, daemon=True) for _ in range(n)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


# ═══════════════════════════════════════════════════════════════════════════
# Demo 3 — Many processes  (all cores light up — true parallelism)
# ═══════════════════════════════════════════════════════════════════════════

def _process_worker() -> None:
    burn_cpu()


def demo_many_processes(n: int) -> None:
    cores = core_count()
    print(f"DEMO 3 — {n} processes burning CPU\n")
    print("Watch Activity Monitor / Task Manager:")
    print(f"  • You'll see {n} SEPARATE `python` processes appear")
    print(f"  • Each has its own interpreter, its own memory, its OWN GIL")
    print(f"  • Total system CPU climbs toward 100%")
    print(f"  • Every one of your {cores} cores lights up")
    print("  • Your laptop's fans will probably start spinning")
    print("\n>>> THIS IS TRUE PARALLELISM. Multiprocessing bypasses the GIL. <<<\n")
    print("Press Ctrl+C to stop.\n")
    procs = [multiprocessing.Process(target=_process_worker) for _ in range(n)]
    for p in procs:
        p.start()
    for p in procs:
        p.join()


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

DEMOS = {
    "1": ("ONE thread (the mystery)", demo_one_thread),
    "2": ("MAX threads (GIL bottleneck)", demo_many_threads),
    "3": ("MAX processes (true parallelism)", demo_many_processes),
}


def usage(cores: int) -> None:
    print()
    print("Part 54 Lab 0 — CPU Demo")
    print()
    print_banner(cores)
    print()
    print("Open Activity Monitor (Mac) or Task Manager (Windows), find the")
    print("`python` process, then run ONE demo at a time and watch the graphs:\n")
    print(f"  python cpu-demo.py 1        # 1 thread            → ~1 core busy")
    print(f"  python cpu-demo.py 2        # {cores} threads (GIL)      → STILL ~1 core busy")
    print(f"  python cpu-demo.py 3        # {cores} processes         → ALL {cores} cores busy")
    print()
    print("Optional — override the auto-count with your own number:")
    print(f"  python cpu-demo.py 2 100    # try 100 threads (still ~1 core!)")
    print(f"  python cpu-demo.py 3 4      # try only 4 processes")
    print()
    print("Companion visualiser: Part-54/concurrency-visual-guide.html")
    print()


def main() -> None:
    default_n = core_count()

    if len(sys.argv) < 2 or sys.argv[1] not in DEMOS:
        usage(default_n)
        sys.exit(0)

    n = default_n
    if len(sys.argv) >= 3:
        try:
            n = max(1, int(sys.argv[2]))
        except ValueError:
            print(f"Invalid count '{sys.argv[2]}', using default {default_n}.\n")

    _, fn = DEMOS[sys.argv[1]]
    print()
    print_banner(default_n)
    print()

    try:
        fn(n)
    except KeyboardInterrupt:
        print("\n\nStopped. Now open concurrency-visual-guide.html to understand "
              "what you just saw.\n")


if __name__ == "__main__":
    main()
