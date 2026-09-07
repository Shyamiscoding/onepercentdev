# Part 54 — Concurrency (Async, Threads, Processes, and the GIL)

In Part 53, you made your code clear and type-safe. Now we tackle a different kind of slowness — the kind that comes from *waiting* on the network or disk, and the kind that comes from *using only one CPU core* while others sit idle. This one part covers all three concurrency tools: async, threads, and processes.

> **Hands-on lab:** `cpu-demo.py` — see the GIL in Activity Monitor with your own eyes.

---



## How to Use These Notes

**Read order (do it exactly like this, once):**

1. **Run the demo first.** Open a terminal in `Part-54/` and run `python cpu-demo.py 1`. Open Activity Monitor (Mac) / Task Manager (Windows). Look at your CPU cores. Watch just 1 of them max out. **Leave that terminal open** — it plants the question this whole part answers.
2. **Then read from the top** of this file. Every section either sets up that question (why does Python only use 1 core?) or answers it.
3. **Come back to the demo at the end.** Run `python cpu-demo.py 3`. Watch every core light up. You will now be able to explain *exactly* why, in one paragraph.

The `concurrency-visual-guide.html` file has the full diagrams. Use it for the classroom walkthrough; use this file for reading later.

---



## The One-Minute Version (If You Read Nothing Else)

**The problem:** Sequential code either (A) sits idle while waiting on network/disk, or (B) uses one CPU core while the rest do nothing.

**Concurrency** = many tasks *in progress* (structure). **Parallelism** = many tasks running *at the same instant* (execution). Concurrency does **not** require parallelism — async on one thread is concurrent but not parallel.

**Python's three tools:**


| Tool              | Solves                                   | Concurrent? | Parallel on multiple cores?                                   |
| ----------------- | ---------------------------------------- | ----------- | ------------------------------------------------------------- |
| `asyncio`         | IO-bound waiting                         | Yes         | No — one thread, smarter switching                            |
| `threading`       | IO-bound with blocking libs (`requests`) | Yes         | No for pure Python; yes for C extensions that release the GIL |
| `multiprocessing` | CPU-bound compute                        | Yes         | **Yes** — each process has its own GIL                        |


**The one-line summary:** *"*`asyncio` *and* `threading` *help Python deal with many things at once. Only* `multiprocessing` *lets Python actually do many things at once."*

**GIL:** Only one thread runs Python bytecode at a time. Threads help IO, not CPU math. Processes bypass this. Python 3.14 (free-threaded build) makes it optional, but the standard build still has it.

---



# Part I — The Hardware Backstory (Why Concurrency Matters *Now*)



## Concurrency is older than you think — parallelism is what's new

Do not confuse these two. Getting this straight saves a lot of interview grief.

- **Concurrency** (the *idea* of interleaving many tasks) has existed since the 1960s. Multics (1964), OS/360 (1967), Unix (1969) all did preemptive multitasking on a **single CPU**. Dijkstra formalised mutual exclusion in **1965**. Windows NT (1993), Linux (1991), Mac OS X (2001) all ran hundreds of programs concurrently on single-core CPUs. Even on a 2003 laptop with one core, you could run Firefox, WinAmp, MSN Messenger and a background download at the same time — the OS time-sliced them. **Python's** `threading` **module was added by Guido in 1992 — 13 years before consumer multi-core existed.** So no, concurrency was not born in 2005.
- **Parallelism** (many tasks actually running at the *same instant*) is what became mainstream for consumer software in 2005. Before that, threads on one core simply *took turns*. After that, threads on multiple cores could actually run **simultaneously** — and only *then* did concurrent code start to give real CPU speedups.


| Era              | Consumer chip clock   | Cores per chip                                 | What concurrency was used for                                                      |
| ---------------- | --------------------- | ---------------------------------------------- | ---------------------------------------------------------------------------------- |
| 1960s–70s        | kHz → few MHz         | 1                                              | Time-sharing on mainframes (many users, one CPU)                                   |
| 1980s–90s        | MHz → hundreds of MHz | 1                                              | Preemptive multitasking on desktop OSes (many programs on one core, IO overlap)    |
| 1993–2005        | ~200 MHz → ~3.8 GHz   | 1 (Intel HT gave 1 core → 2 threads from 2002) | Same, plus GUIs staying responsive while background work happened                  |
| **2005 → today** | stuck at ~3–5 GHz     | **2 → 4 → 8 → 18+**                            | **Parallel compute in application code — real CPU speedups from using many cores** |




## The 2005 wall — what actually changed

From 1971 (Intel 4004, **740 kHz** clock, ~92,000 instructions/sec) to 2005 (Pentium 4 Prescott, ~3.8 GHz), consumer clock speeds rose ~5,000×. Existing code ran faster every year — programmers got a **free lunch**. In 2005, Intel's Pentium 4 hit **the wall** — physics stopped clock speeds from rising (heat, power, and the speed of light itself). Chipmakers stopped racing on frequency and started adding **cores**.

So what changed for us as Python developers?

- **Before 2005** — threads and async were about *hiding IO latency* (overlap 3 slow API calls so their waits happen at the same time). No CPU speedup was even possible from threads — there was only one core.
- **After 2005** — real CPU speedup is now available from using multiple cores. But **only** if you use `multiprocessing`. Python's `threading` still doesn't give it to you because of the **GIL**. That's exactly why `multiprocessing` was added in Python 2.6 (2008) — to let application code finally benefit from multi-core hardware.

Your laptop today has 10–18 cores. Your Python script uses **one**. Threads take turns because of the GIL. Only processes truly use all your cores. That's the problem this whole part exists to solve.

## The multi-core pivot (2006 onwards)

- 2006 — Intel Core Duo (2 cores in one chip)
- 2007 — Intel Core 2 Quad (4 cores)
- 2017 — AMD Ryzen (8 cores at consumer prices)
- 2020 — Apple M1 (8-core SoC — CPU + GPU + Neural Engine on one die)
- 2024–2026 — 10–32 cores everywhere (Intel Core Ultra, AMD Ryzen 9, Apple M4 / M4 Pro / M4 Max / M3 Ultra, Snapdragon X2 Elite)

Chip design and manufacturing split into two industries:


| Role                                           | Companies (2026)                                 |
| ---------------------------------------------- | ------------------------------------------------ |
| **Designers** (draw the blueprint)             | Apple, AMD, Intel, Qualcomm, NVIDIA              |
| **Foundries** (actually etch the silicon)      | TSMC (Taiwan) ~70% share, Samsung, Intel Foundry |
| **IP licensors** (own the CPU instruction set) | ARM Holdings (UK), Intel (x86), RISC-V (open)    |
| **Toolmakers** (the machines that make chips)  | ASML (Netherlands, sole EUV lithography source)  |




### Practical: this is why the Python installer has multiple options

When you land on [python.org/downloads](https://www.python.org/downloads/), the site asks you to pick a build. That choice IS the ARM vs x86 story from above.


| Your machine                                    | Chip                    | ISA          | What to download                                                                                            |
| ----------------------------------------------- | ----------------------- | ------------ | ----------------------------------------------------------------------------------------------------------- |
| **This MacBook (M4 Pro)** or any Mac since 2020 | Apple M1/M2/M3/M4       | ARM64        | **macOS 64-bit universal2 installer** — one `.pkg`, both arm64 and x86_64 inside, macOS picks automatically |
| Intel Mac (2006–2020)                           | Intel Core i5/i7/i9     | x86-64       | Same universal2 installer works                                                                             |
| Windows Intel/AMD PC                            | Intel Core / AMD Ryzen  | x86-64       | **Windows installer (64-bit)**                                                                              |
| Windows on ARM — Copilot+ PC                    | Snapdragon X / X2 Elite | ARM64        | **Windows installer (ARM64)** — different file from the 64-bit x86 one                                      |
| Legacy 32-bit Windows                           | Old Intel/AMD           | x86 (32-bit) | Windows installer (32-bit) — only for very old machines                                                     |


**Verify what you're actually running:**

```bash
python3 -c "import platform, sys; print('Machine:', platform.machine(), '| Python:', sys.version.split()[0])"
```

On this M4 Pro laptop it prints `Machine: arm64`. On Intel/AMD it prints `x86_64`. On Snapdragon it prints `ARM64`.

**The gotcha:** if you accidentally install the x86_64 Python on an Apple Silicon Mac, it will still run — through **Rosetta 2**, Apple's on-the-fly Intel-to-ARM translator — but ~20–40% slower, and every C extension you `pip install` will be x86 too. Always use the `universal2` installer on Mac and the ARM64 installer on Snapdragon.

**Why the choice exists at all:** a compiled program contains native machine code for one specific instruction set. ARM64 code cannot run directly on x86, and vice versa. Every `.so`/`.pyd` file in your Python install is native — no magic. That is exactly why ARM Holdings collects a royalty every time an ARM binary runs.

## Apple Silicon and the SoC model

An **SoC** (System-on-Chip) puts CPU cores + GPU + Neural Engine + memory controller + I/O all on one silicon die. Apple's M-series is the poster child:

- **P-cores** (Performance) — high-power cores for foreground work.
- **E-cores** (Efficiency) — low-power cores for background tasks.
- **GPU** — parallel math for graphics and ML.
- **Neural Engine (NPU)** — dedicated matrix hardware for on-device AI.
- **Unified memory** — one RAM pool shared by CPU, GPU, and NPU (no PCIe copy).

When you run `python cpu-demo.py 1`, exactly **one P-core** on that giant SoC lights up. The other P-core, all E-cores, the whole GPU, and the whole NPU sit idle. That's the waste this course teaches you to fix.

## The chip in this course — the instructor's actual machine

Every "14 cores / 20 GPU / 48 GB" reference below is the *real* laptop this course is filmed on. Verified from `system_profiler SPHardwareDataType`:

```
Model Name:              MacBook Pro
Model Identifier:        Mac16,7           (16-inch, late 2024)
Chip:                    Apple M4 Pro
Total Number of Cores:   14 (10 Performance and 4 Efficiency)
GPU:                     20-core (Metal 4)
Memory:                  48 GB unified (LPDDR5X, 273 GB/s)
Neural Engine:           16 cores, 38 TOPS
OS:                      macOS 26.6.2
```

Full spec sheet:


| Spec             | This MacBook (M4 Pro, upgraded tier)                  |
| ---------------- | ----------------------------------------------------- |
| Model            | MacBook Pro 16" (Mac16,7)                             |
| CPU cores        | **14 (10 P-cores + 4 E-cores)**                       |
| CPU threads      | 14 (Apple has no Hyper-Threading — 1 thread per core) |
| GPU cores        | **20**                                                |
| Neural Engine    | 16 cores, 38 TOPS                                     |
| P-core max clock | 4.51 GHz                                              |
| E-core max clock | 2.6 GHz                                               |
| Unified memory   | **48 GB** (LPDDR5X)                                   |
| Memory bandwidth | 273 GB/s                                              |
| Transistors      | ~55 billion                                           |
| Die size         | 325 mm²                                               |
| Process          | TSMC N3E (3 nm, 2nd-gen)                              |
| Released         | Oct 30, 2024                                          |


**Where the M4 Pro sits in Apple's lineup** (Oct 2024 → today):

- **M4 (base)** — 10-core CPU (4P+6E), 28B transistors — MacBook Air / base MBP / Mac mini / iMac
- **M4 Pro (this laptop)** — 12 or 14-core CPU, 55B transistors — 14"/16" MacBook Pro, Mac mini
- **M4 Max** — 14 or 16-core CPU, ~76B transistors — top-end MacBook Pro / Mac Studio
- **M3 Ultra** (there is *no* M4 Ultra) — 32-core CPU, 184B transistors — Mac Studio

If your machine is different, the *math* below scales — just substitute your core count wherever "14" appears.

## Under the surface — where the silicon in your M4 Pro actually came from

None of this course requires you to understand chip manufacturing. But if a student asks, here is the honest answer with links to the definitive sources.

### The refinement pipeline — from rock to wafer

The silicon in your MacBook did **not** come from "beach sand" — that's a common oversimplification. It started as a specific rock and went through four industrial stages to reach the purity a chip demands.


| #   | Stage                     | Material                              | Purity                            | How it's done                                                                                                                                                                                         |
| --- | ------------------------- | ------------------------------------- | --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Mining**                | Quartzite rock (80–99% SiO₂)          | ~99%                              | Quarried from specific mines: Spruce Pine (USA), Kyshtym (Russia), Norway, Brazil, China                                                                                                              |
| 2   | **Arc-furnace reduction** | Metallurgical-grade silicon (MGS)     | ~98–99%                           | Quartzite + carbon (coke) heated to 1,800–2,000 °C in an arc furnace: `SiO₂ + 2 C → Si + 2 CO`                                                                                                        |
| 3   | **Siemens process**       | Electronic-grade polysilicon rods     | **99.9999999% (9N–11N)**          | MGS + HCl → trichlorosilane (SiHCl₃) liquid → fractionally distilled → CVD-deposited on hot silicon rods at 1,100 °C for 200–300 hours                                                                |
| 4   | **Czochralski method**    | Monocrystalline silicon ingot (boule) | Same purity, now a single crystal | Polysilicon melted at 1,420 °C in a quartz crucible → seed crystal dipped in → rotated and pulled up at 1–2 cm/hour → 300 mm × 2 m ingot, 200–300 kg, hangs from a "necked" thread just a few mm wide |
| 5   | **Wire sawing + CMP**     | 300 mm silicon wafer, ~0.775 mm thick | Same                              | Ingot sliced by diamond wire saw, polished by Chemical Mechanical Polishing to atomic flatness                                                                                                        |


**Key facts worth memorising:**

- **11 nines** purity = 1 non-silicon atom per 10 billion silicon atoms. Purest material humans have ever produced.
- The Czochralski ingot is **one continuous single crystal** — every silicon atom is in a perfect lattice. Transistors will not work on a defect-filled crystal.
- One 300 mm ingot yields ~1,000 wafers. One wafer yields hundreds of chips. One Apple M4 Pro die is 325 mm² — small enough that ~180 fit on one wafer.



### What a transistor actually is

- A **transistor** is a three-terminal electrical switch (Source, Gate, Drain). Voltage on the Gate opens the channel between Source and Drain → conducts (1). Remove voltage → open circuit (0). Every calculation your Mac does is 55 billion of these switching in sync, up to 4.5 billion times per second on each P-core.
- The specific type is a **MOSFET** (Metal-Oxide-Semiconductor Field-Effect Transistor), invented at Bell Labs in 1959.
- Modern chips like your M4 Pro use a **3D** version called **FinFET** or **GAA (Gate-All-Around)**. The channel is a vertical fin (or nanosheet) surrounded by the gate — flat MOSFETs stopped shrinking at 22 nm around 2011.
- "**Doping**" = shooting phosphorus or boron atoms into precise regions of silicon at controlled depths using an **ion implantation machine**. That's what makes plain silicon behave as an n-type or p-type semiconductor.
- "**Lithography**" = using ultraviolet light through a mask to draw the transistor patterns on the wafer. Modern chips use **EUV lithography** at 13.5 nm wavelength, from ASML machines that cost ~$200M each.
- "**3 nm**" is a *marketing label*, not a physical dimension. Actual features on "3 nm" chips are 20–25 nm; the number refers to a density/performance class.



### Further reading (all links open in the HTML guide too)

**Refinement pipeline:**

- Wikipedia — [Quartzite](https://en.wikipedia.org/wiki/Quartzite), [Metallurgical-grade silicon](https://en.wikipedia.org/wiki/Silicon#Metallurgical_grade), [Siemens process](https://en.wikipedia.org/wiki/Polycrystalline_silicon#Siemens_process), [Czochralski method](https://en.wikipedia.org/wiki/Czochralski_method), [Monocrystalline silicon](https://en.wikipedia.org/wiki/Monocrystalline_silicon), [Silicon wafer](https://en.wikipedia.org/wiki/Wafer_(electronics))
- [Bernreuter Research — Siemens process explained](https://www.bernreuter.com/polysilicon/production-processes/) (industry reference)

**Transistor physics:**

- Wikipedia — [MOSFET](https://en.wikipedia.org/wiki/MOSFET), [Doping (semiconductor)](https://en.wikipedia.org/wiki/Doping_(semiconductor)), [Ion implantation](https://en.wikipedia.org/wiki/Ion_implantation), [Photolithography](https://en.wikipedia.org/wiki/Photolithography), [FinFET](https://en.wikipedia.org/wiki/FinFET), [ASML](https://en.wikipedia.org/wiki/ASML_Holding), [TSMC](https://en.wikipedia.org/wiki/TSMC)

**Videos:**

- [Branch Education — "How are Microchips Made?"](https://www.youtube.com/watch?v=dX9CGRZwD-w) (22-min 3D animation of the full process)
- [Real Engineering — "How are Silicon Wafers Made?"](https://www.youtube.com/watch?v=aWVywhzuHnQ) (15-min visual walkthrough of the refinement)
- [Applied Science — "Homemade transistor in a garage lab"](https://www.youtube.com/watch?v=NGFhc8R_uO4) (32 min — a hobbyist actually builds a working MOSFET)

**Industry:**

- TSMC — [Process node roadmap](https://www.tsmc.com/english/dedicatedFoundry/technology/logic)

---



# Part II — Cores vs Threads (the mental model)

Get this straight before any code. The word "thread" is used in three different layers and mixing them up is the #1 source of confusion.


| Layer                                   | What it is                                                                                         | Example on this course's laptop (14-core Apple M4 Pro)                       |
| --------------------------------------- | -------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| **Physical core**                       | A real block of silicon that executes instructions                                                 | 14 (10 P-cores + 4 E-cores)                                                  |
| **Hardware thread / logical processor** | An execution slot on a core (Intel/AMD Hyper-Threading gives 2 per P-core; Apple gives 1 per core) | 14 (Apple has no HT). A 14-core Intel i9 with HT on P-cores would report 24+ |
| **OS thread**                           | A software execution path scheduled by the OS onto hardware threads                                | Thousands at once (macOS/Windows/Linux time-slice them)                      |
| **Python thread** (`threading.Thread`)  | A real OS thread that runs Python bytecode                                                         | Same as OS thread — but only 1 holds the GIL at a time                       |




## Hyper-Threading / SMT — the "2 workers per chair" trick

Intel calls it **Hyper-Threading (HT)**; AMD calls it **SMT (Simultaneous Multi-Threading)**. Same idea: a single physical core keeps two thread contexts warm and switches between them when one stalls waiting for memory. Result: ~20–30% more throughput per core, not 2×.

- **Intel P-cores** — HT on.
- **Intel E-cores** — HT off.
- **AMD Ryzen** — SMT on all cores.
- **Apple M-series** — no HT/SMT. Every core is 1 hardware thread.

That's why `sysctl -n hw.ncpu` on this 14-core M4 Pro reports `14`, but on a 14-core Intel Core i9 (with HT on P-cores) would report `24` or higher.

## How Python threads map down

```
Python thread (threading.Thread)
    └── OS thread (kernel-scheduled)
            └── Hardware thread (a slot on a physical core)
                    └── Physical core (silicon that executes bytecode)
```

Every Python thread is a *real OS thread* — that's not the problem. The problem is the **GIL** at the top: only one Python thread may execute bytecode at a time, no matter how many cores you have. We get to that in Part VIII.

---



# Part III — Two Kinds of Slow

Before writing concurrent code, diagnose which kind of slow you have. Wrong diagnosis = wrong tool = wasted effort.


| Symptom                              | Kind          | Example                                       | Right tool               |
| ------------------------------------ | ------------- | --------------------------------------------- | ------------------------ |
| One core pinned at 100%, others idle | **CPU-bound** | Number crunching, image resizing, ML training | `multiprocessing`        |
| All cores idle, program still slow   | **IO-bound**  | API calls, DB queries, file reads             | `asyncio` or `threading` |


Rule of thumb: **look at Activity Monitor before you code.** If your `python` process shows ~100% CPU, you're CPU-bound. If it shows ~2% CPU while the program still waits, you're IO-bound.

---



# Part IV — Concurrency vs Parallelism (Rob Pike's Definitions)

Rob Pike (co-creator of Go) gave the definitive talk in 2012 — [Concurrency Is Not Parallelism](https://www.youtube.com/watch?v=oV9rvDllKEg). His one-sentence version:

- **Concurrency** = the *composition* of independently executing tasks. It's how you **structure** a program.
- **Parallelism** = **simultaneous execution** of (possibly related) computations. It's about **doing** things at the same instant.

Pike's gopher analogy: one gopher moving books from one pile to another is *sequential*. Two gophers carrying two books at once is *parallelism*. One gopher who cleverly interleaves loading, walking, and unloading so books flow smoothly is *concurrency* — even alone.

Concurrency **enables** parallelism, but they are not the same. `asyncio` is 100% concurrent, 0% parallel — proof that the two ideas are separate.

Mapping to Python:


| Tool              | Concurrency?                  | Parallelism?                                                   |
| ----------------- | ----------------------------- | -------------------------------------------------------------- |
| `asyncio`         | Yes (one thread, cooperative) | **No**                                                         |
| `threading`       | Yes                           | **No** for pure Python (GIL); yes when C code releases the GIL |
| `multiprocessing` | Yes                           | **Yes** — separate processes, separate GILs                    |




## Preemptive vs Cooperative Multitasking

This is the concept behind *how* the switching between tasks actually happens. It's the difference between `threading` and `asyncio`.


| Style           | Who decides when to switch?                                                              | Used by                                                  |
| --------------- | ---------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| **Preemptive**  | The OS forcibly pauses a thread mid-instruction and hands the core to another thread     | `threading`, `multiprocessing`, every OS-level scheduler |
| **Cooperative** | Tasks *voluntarily* yield control at specific points; nothing else can run until they do | `asyncio` (yields at every `await`)                      |


Consequences:

- **Preemptive** — a thread can be interrupted anywhere, even mid-`counter += 1`. That's why threads need `Lock`s to guard shared data (races are real).
- **Cooperative** — a coroutine only pauses at `await`. Between two `await`s the code is atomic *for other coroutines in the same loop*. Fewer races, but one runaway coroutine that never awaits will freeze the whole event loop.

Restaurant analogy:

- **Synchronous (preemptive style, one waiter)** — one waiter takes an order, stands in the kitchen until food is ready, delivers it, then serves the next table. Everyone else waits.
- **Asynchronous (cooperative)** — the waiter fires off order 1, immediately takes orders 2 and 3, and delivers each plate whenever it's ready. One waiter, many tables. The waiter yields control every time he passes an order to the kitchen — that's the `await`.

---



# Part V — Tool 1: `asyncio`



## The Problem: Waiting

```python
import time
import requests

def fetch_user(user_id: int) -> dict:
    return requests.get(
        f"https://jsonplaceholder.typicode.com/users/{user_id}",
        timeout=10,
    ).json()

start = time.time()
fetch_user(1)
fetch_user(2)
fetch_user(3)
print(f"Total: {time.time() - start:.2f}s")   # ~0.9s — all sequential
```

Three requests, ~0.9s total — but the CPU was idle 99% of that time, waiting on the network. What if you could start all three at once and wait together? That's **async**.

## Coroutines — the unit `asyncio` runs

A **coroutine** is a function that can *pause* mid-execution and hand control back to the event loop, then *resume* later exactly where it left off. It is **not** a thread — it's a plain Python object that lives in one thread. Thousands of coroutines can share one thread.

- `async` and `await` are **language keywords** — `async def` marks a function as a coroutine; `await` is where it can pause.
- `asyncio` is the **standard library** that provides the event loop, primitives (`gather`, `Lock`, `Queue`, `TaskGroup`), and network integration.
- A coroutine is what `async def` *creates*. Calling it doesn't run it — it returns a coroutine object that the event loop must schedule.



## async / await

```python
import asyncio

async def greet(name: str) -> str:
    print(f"Starting {name}")
    await asyncio.sleep(1)     # pauses THIS coroutine, lets others run
    return f"Hello, {name}!"

async def main():
    print(await greet("Alice"))

asyncio.run(main())
```

- `async def` defines a coroutine; `await` pauses it while waiting and lets other coroutines run.
- A coroutine doesn't run by itself — it needs an **event loop**.



## The Event Loop

`asyncio.run(main())` creates the loop, runs `main()`, and closes the loop. One thread, one event loop. The loop rotates between coroutines whenever one hits an `await`. That's **cooperative multitasking** — no OS preemption, no GIL contention between coroutines, no thread overhead.

## asyncio.sleep vs time.sleep

```python
time.sleep(2)          # BLOCKS the whole event loop — nothing else runs
await asyncio.sleep(2) # YIELDS control — other coroutines run meanwhile
```

Using `time.sleep()` (or any blocking call) inside async code defeats the purpose.

## Running Tasks Concurrently — `asyncio.gather`

```python
import asyncio
import time

async def fetch(source: str, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"Data from {source}"

async def main():
    start = time.time()
    results = await asyncio.gather(
        fetch("API-1", 2),
        fetch("API-2", 1),
        fetch("API-3", 1.5),
    )
    print(results, f"{time.time() - start:.2f}s")   # ~2s, not 4.5s

asyncio.run(main())
```

`asyncio.gather()` starts all coroutines at once; the slowest one determines total time. The work didn't get faster — the *waiting* got smarter.

## `asyncio.TaskGroup` — the modern gather (Python 3.11+)

`TaskGroup` is what you should reach for in new code. It gives you **structured concurrency** — if one task fails, the group cleanly cancels the others.

```python
import asyncio

async def fetch(url: str) -> str:
    await asyncio.sleep(0.1)
    return f"body of {url}"

async def main():
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(fetch("https://a.example"))
        t2 = tg.create_task(fetch("https://b.example"))
        t3 = tg.create_task(fetch("https://c.example"))
    print(t1.result(), t2.result(), t3.result())

asyncio.run(main())
```

Prefer `TaskGroup` over `gather` when you want *all-or-nothing* behavior.

## `asyncio.as_completed` — stream results as they arrive

```python
import asyncio

async def fetch(url: str) -> str:
    await asyncio.sleep(0.1)
    return f"body of {url}"

async def main():
    urls = ["https://a.example", "https://b.example", "https://c.example"]
    tasks = [fetch(u) for u in urls]
    for coro in asyncio.as_completed(tasks):
        result = await coro
        print("first back:", result)   # in whatever order they finish

asyncio.run(main())
```

Great when you want to react as soon as *any* result is ready (e.g. return the fastest of several redundant API calls).

## `asyncio.timeout` — Python 3.11+ (the good timeout)

```python
import asyncio

async def slow_operation():
    await asyncio.sleep(10)

async def main():
    try:
        async with asyncio.timeout(5):
            await slow_operation()
    except TimeoutError:
        print("Timed out after 5s")

asyncio.run(main())
```

Older `asyncio.wait_for(coro, timeout=5)` still works, but `asyncio.timeout()` composes better and is preferred for new code.

## `asyncio.Semaphore` — rate limiting

Limit how many things happen concurrently (e.g. don't hammer an API with 1000 requests at once).

```python
import asyncio

sem = asyncio.Semaphore(10)   # at most 10 concurrent

async def fetch(url):
    async with sem:
        await asyncio.sleep(0.1)
        return f"body of {url}"
```



## `asyncio.to_thread` — bridge to blocking libraries

You want to call a blocking library (`requests`, DB drivers, disk IO) inside async code without blocking the event loop. Use `to_thread`:

```python
import asyncio
import requests

def blocking_get(url):
    return requests.get(url, timeout=10).text

async def main():
    text = await asyncio.to_thread(blocking_get, "https://example.com")
    print(text[:100])

asyncio.run(main())
```

Under the hood, `to_thread` runs the function in a `ThreadPoolExecutor` and awaits its result. Uses ~1 real OS thread per call.

## `loop.run_in_executor` — CPU work inside async code

Same idea as `to_thread`, but you supply your own pool — and it can be a `ProcessPoolExecutor` for CPU-bound work:

```python
import asyncio
from concurrent.futures import ProcessPoolExecutor

def heavy_compute(n):
    return sum(i * i for i in range(n))

async def main():
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, heavy_compute, 10_000_000)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```



## Real async HTTP with `httpx`

```python
import asyncio
import httpx

async def fetch_user(client: httpx.AsyncClient, uid: int) -> dict:
    r = await client.get(f"https://jsonplaceholder.typicode.com/users/{uid}")
    return r.json()

async def main():
    async with httpx.AsyncClient(timeout=10) as client:
        users = await asyncio.gather(
            *(fetch_user(client, i) for i in range(1, 6))
        )
    for u in users:
        print(u["name"])

asyncio.run(main())   # pip install httpx
```

`httpx.AsyncClient` is the async version of `requests.Session`; `async with` closes it automatically. All 5 requests run concurrently.

## The big pitfall — blocking the event loop

The event loop runs in **one thread**. Anything that blocks that thread stalls *every* coroutine.

- Never call `time.sleep()`, `requests.get()`, DB queries, or CPU-heavy loops directly in async code.
- Use the async equivalent (`await asyncio.sleep`, `httpx.AsyncClient`, async DB drivers).
- If you must call a blocking library, wrap it in `asyncio.to_thread(...)`.

---



# Part VI — Tool 2: `threading`



## Threads — shared memory, lightweight, blocked by the GIL for Python code

```python
import threading
import time

def download(url: str) -> None:
    time.sleep(1)   # simulate network delay
    print(f"got {url}")

start = time.time()
threads = [
    threading.Thread(target=download, args=(f"url/{i}",))
    for i in range(5)
]
for t in threads: t.start()
for t in threads: t.join()
print(f"Total: {time.time() - start:.2f}s")   # ~1s, not 5s
```

Great for **IO-bound** work with blocking libraries. **No speedup** for pure-Python CPU work (see GIL).

## Race conditions — "the GIL doesn't save you"

Even with the GIL, threads share memory. This code is broken:

```python
import threading

counter = 0

def increment():
    global counter
    for _ in range(1_000_000):
        counter += 1   # NOT atomic — read, add, write

threads = [threading.Thread(target=increment) for _ in range(4)]
for t in threads: t.start()
for t in threads: t.join()
print(counter)   # NOT 4_000_000. Something like 1_842_193.
```

`counter += 1` compiles to 3 bytecodes (`LOAD`, `ADD`, `STORE`) — a thread can be swapped out between them (preemptive multitasking, remember?).

## The fix — `threading.Lock`

```python
import threading

counter = 0
lock = threading.Lock()

def increment():
    global counter
    for _ in range(1_000_000):
        with lock:
            counter += 1

threads = [threading.Thread(target=increment) for _ in range(4)]
for t in threads: t.start()
for t in threads: t.join()
print(counter)   # 4_000_000
```

Now the read-modify-write is atomic. Correct result, ~10× slower.

## Sync primitives you should know


| Primitive      | Use it when                                                   |
| -------------- | ------------------------------------------------------------- |
| `Lock`         | Only one thread in the critical section at a time             |
| `RLock`        | Same thread may `acquire` the lock more than once (reentrant) |
| `Semaphore(n)` | At most N threads inside a section                            |
| `Event`        | One thread signals, others `wait`                             |
| `Condition`    | Wait for a state change (producer/consumer)                   |
| `Barrier(n)`   | N threads must all reach a point before any proceeds          |
| `queue.Queue`  | Thread-safe producer/consumer — often the *simplest* answer   |




## Deadlock — the two-lock trap

```python
import threading

lock_a = threading.Lock()
lock_b = threading.Lock()

def worker_1():
    with lock_a:
        with lock_b:      # waiting for B
            ...

def worker_2():
    with lock_b:
        with lock_a:      # waiting for A
            ...
```

If worker_1 gets A while worker_2 gets B, both wait forever. That's a **deadlock**.

Four conditions must all hold (**Coffman conditions**):

1. **Mutual exclusion** — resources are exclusive.
2. **Hold and wait** — hold one while waiting for another.
3. **No preemption** — you can't force-release someone's lock.
4. **Circular wait** — a cycle in the wait graph.

Break any one to prevent deadlock. Practical rules:

- **Always acquire locks in the same order** everywhere.
- Prefer higher-level primitives (`queue.Queue`) over multiple locks.
- Use `Lock.acquire(timeout=…)` and give up cleanly if it times out.



## `ThreadPoolExecutor` — the simple API

```python
from concurrent.futures import ThreadPoolExecutor
import requests

def fetch(url):
    return requests.get(url, timeout=10).json()

urls = [
    f"https://jsonplaceholder.typicode.com/users/{i}"
    for i in range(1, 6)
]

with ThreadPoolExecutor(max_workers=5) as ex:
    results = list(ex.map(fetch, urls))

for r in results:
    print(r["name"])
```

---



# Part VII — Tool 3: `multiprocessing`



## Processes — true parallelism

Each process has its own interpreter and its own GIL, so processes run truly in parallel across CPU cores:

```python
import multiprocessing

def cpu_heavy(n: int) -> int:
    return sum(range(n))

if __name__ == "__main__":          # required — without it, children re-import and spawn forever
    procs = [
        multiprocessing.Process(target=cpu_heavy, args=(50_000_000,))
        for _ in range(4)
    ]
    for p in procs: p.start()
    for p in procs: p.join()
```



## More processes than cores?

If you launch 20 processes on a 10-core machine, the OS scheduler **time-slices** them onto the 10 hardware threads. You don't get 20-way parallelism; you get context-switching overhead and cache thrashing. Rule of thumb: `ProcessPoolExecutor()` defaults to `os.cpu_count()` workers for a reason.

## Fork vs Spawn — the platform difference that bites everyone


| Method       | Default on                                  | Behavior                                                                         |
| ------------ | ------------------------------------------- | -------------------------------------------------------------------------------- |
| `fork`       | Linux (until Python 3.14)                   | Child copies parent memory. Fast start. Dangerous with threads.                  |
| `spawn`      | Windows, macOS, **Linux from Python 3.14+** | Child starts a fresh interpreter and re-imports your module. Slower start. Safe. |
| `forkserver` | Optional on Linux                           | A dedicated server process forks children.                                       |


Set explicitly for portability:

```python
import multiprocessing as mp
mp.set_start_method("spawn", force=True)
```



## Sharing data between processes

Processes have **separate memory**. To share data, you pick one of:


| Primitive                                    | What it is                                | Best for                                   |
| -------------------------------------------- | ----------------------------------------- | ------------------------------------------ |
| `multiprocessing.Queue`                      | Thread- and process-safe FIFO             | Message passing between workers            |
| `multiprocessing.Pipe`                       | Two-endpoint connection                   | Simple parent ↔ child channel              |
| `multiprocessing.shared_memory.SharedMemory` | Raw bytes / numpy arrays with zero-copy   | Big numeric arrays without pickling        |
| `multiprocessing.Manager`                    | Server process hosting shared dicts/lists | Convenient, but slower (all access is RPC) |




## `ProcessPoolExecutor` — the simple API

```python
from concurrent.futures import ProcessPoolExecutor

def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return b

if __name__ == "__main__":
    with ProcessPoolExecutor() as ex:            # CPU-bound
        results = list(ex.map(fib, [300_000, 350_000, 400_000]))
    for r in results:
        print(str(r)[:15], "...")
```

Same interface as `ThreadPoolExecutor` — swap the executor to match the workload.

---



# Part VIII — The GIL (the reason everything above exists)



## What it is

The **Global Interpreter Lock** is a mutex in CPython that lets only **one thread execute Python bytecode at a time**. It exists because CPython's memory management (reference counting) is not thread-safe.

If you ran **Lab 0 Demo 2**, you already saw this: N threads, one core. The monitor doesn't lie.

## Consequences

- **Threads do NOT speed up CPU-bound Python code.** Two threads counting to 50 million are not faster than one — often *slower* due to contention (see "GIL thrashing" below).
- **Threads DO help IO-bound work.** When a thread does IO (network, disk, `sleep`), it **releases the GIL**, so other threads run.
- **Processes bypass the GIL entirely.** Each process has its own interpreter and its own GIL — real parallel execution.



## The escape hatch — C extensions release the GIL

`numpy`, `pandas`, `PyTorch`, `Pillow`, and most scientific libraries drop the GIL when they enter C code. That's why:

```python
# threading + numpy = actual parallel speedup
import numpy
from concurrent.futures import ThreadPoolExecutor

big_matrices = [numpy.random.rand(1000, 1000) for _ in range(4)]

with ThreadPoolExecutor() as ex:
    results = list(ex.map(numpy.linalg.svd, big_matrices))
```

*can* saturate multiple cores — the C code isn't executing Python bytecode.

## GIL history — the three eras (from David Beazley's PyCon 2010 talk)

David Beazley's [Understanding the Python GIL](https://www.youtube.com/watch?v=Obt-vMVdM8s) is the canonical GIL talk. Key findings:

1. **Old GIL (< Python 3.2)** — switched threads every 100 bytecodes. On multi-core machines, threads fought viciously for the lock — **GIL thrashing**. Two CPU-bound threads on a dual-core machine were often *slower* than one thread.
2. **New GIL (Python 3.2+)** — switches every 5 ms based on wall-clock, not bytecodes. Fixed the worst thrashing but introduced the **I/O convoy effect** — an I/O-ready thread can be forced to wait behind a CPU-bound thread that is monopolising the GIL.
3. **Free-threaded Python (3.14+)** — an optional build with no GIL at all.

The one-sentence takeaway for a Python developer: *the GIL punishes you for using threads for CPU work — always has, always will (until 3.14t).*

## Free-threaded Python 3.14 (PEP 703 + PEP 779)

Python 3.14 ships **two builds**:

- **Standard build** — GIL still on. This is what `python` runs by default.
- **Free-threaded build** (`python3.14t`) — GIL removed. Threads actually parallelise pure Python code.

Caveats: free-threaded Python is ~10% slower single-threaded, and many C extensions haven't been ported yet. It's officially supported (Phase II, PEP 779) but not the default. Treat it as "the future," not "today's production."

## Subinterpreters (PEP 734)

New in 3.14: run **multiple Python interpreters** in one OS process, each with its **own GIL**. Access via `concurrent.futures.InterpreterPoolExecutor`. Cheaper than `multiprocessing` (no separate process, faster startup, easier data transfer than pickling) but with strict isolation. Another future path to parallelism.

---



# Part IX — Decide and Practice



## The CPU vs IO Rule

The single most important concurrency decision:


| Task type | Examples                               | Solution                                     |
| --------- | -------------------------------------- | -------------------------------------------- |
| CPU-bound | Number crunching, image processing, ML | `multiprocessing`, `ProcessPoolExecutor`     |
| IO-bound  | API calls, DB queries, file reading    | `asyncio`, `threading`, `ThreadPoolExecutor` |




## Decision Tree — memorise this

```
Need concurrency?
├── IO-bound (network, disk, DB)?
│   ├── Whole codebase is async? → asyncio (TaskGroup, gather)
│   ├── Blocking libraries (requests, DB drivers)? → ThreadPoolExecutor
│   └── Mostly async but one blocking call? → asyncio.to_thread(...)
│
└── CPU-bound (computation)?
    ├── Uses numpy/pandas/PyTorch heavily? → threading MAY work (GIL released)
    ├── Pure Python compute? → ProcessPoolExecutor / multiprocessing
    └── Very short tasks? → often faster to stay sequential (fork/spawn overhead)
```

---



## Common Interview Questions

- **Concurrency vs parallelism?** Concurrency = many tasks *in progress* (structure). Parallelism = many tasks *at the same instant* (execution). Async is concurrent; multiprocessing can be parallel.
- **Preemptive vs cooperative multitasking?** Preemptive = OS forcibly pauses threads (`threading`). Cooperative = tasks yield voluntarily at `await` (`asyncio`).
- **What is the GIL?** A CPython mutex allowing only one thread to run Python bytecode at a time; it protects reference counting.
- **Do threads speed up CPU-bound code?** No — use multiprocessing. Threads only help IO-bound work (the GIL is released during IO).
- **What is GIL thrashing?** When multiple CPU-bound threads on multi-core machines fight over the GIL and spend more time on context switches than useful work. Fixed in Python 3.2+ but the I/O convoy effect replaced it.
- **What's a hardware thread vs a Python thread?** Hardware thread = a slot on a CPU core (Intel/AMD often 2 per core; Apple 1 per core). Python thread = a real OS thread — but only one runs Python bytecode at a time due to the GIL.
- **async vs threading?** Both handle IO; async is lighter and scales to thousands of coroutines. Use threading for blocking libraries.
- **Why does Python have three concurrency models?** Two different problems (IO wait vs CPU compute) plus the GIL — no single tool fits all workloads.
- **What is a coroutine?** A function created by `async def` that can pause at `await` and resume later. Lives inside one thread. Thousands can share one thread.
- **Is** `asyncio` **parallel?** No — one thread, one core. It's concurrent only.
- `gather` **vs** `TaskGroup`**?** `TaskGroup` (3.11+) gives structured concurrency: if one task fails, the group cancels the others cleanly.
- `fork` **vs** `spawn`**?** `fork` copies parent memory (fast, unsafe with threads, Linux default until 3.14). `spawn` restarts a fresh interpreter (slow, safe, Windows/macOS default and Linux from 3.14+).
- **How do you share state between processes?** `Queue`, `Pipe`, `shared_memory.SharedMemory`, or `Manager`.
- **What happens if you** `time.sleep()` **in async code?** You block the whole event loop; every other coroutine stalls. Use `await asyncio.sleep(...)`.
- **Race condition on** `counter += 1`**?** Yes — it's 3 bytecodes. Protect with `threading.Lock`.
- **Deadlock — the 4 Coffman conditions?** Mutual exclusion, hold-and-wait, no preemption, circular wait. Break any one.
- **Does Python 3.14 remove the GIL?** No — it adds an optional free-threaded build (`python3.14t`) that runs without the GIL. The default `python` still has it.
- **Why does numpy speed up under threading?** Its C code releases the GIL, so multiple threads can actually run in parallel.
- **What is Hyper-Threading?** Intel's SMT — one physical core exposes 2 hardware threads by keeping two contexts warm and switching when one stalls on memory. Apple Silicon does not have it.

---



## Where This Applies in Real Work

- **FastAPI:** `async def` endpoints handle thousands of concurrent requests without blocking.
- **AI agents:** call search, LLM, and database APIs concurrently instead of one-by-one (`asyncio.gather` / `TaskGroup`).
- **Web scraping / batch inference:** download or request hundreds of items at once with async or `ThreadPoolExecutor`.
- **Data pipelines & ML:** distribute CPU-heavy work across cores with `ProcessPoolExecutor` / `multiprocessing`.
- **Rate-limited APIs:** use `asyncio.Semaphore(N)` to cap in-flight requests.
- **Long-running services:** wrap risky calls in `asyncio.timeout(...)` to guarantee bounded latency.
- **Scientific computing:** `numpy` / `PyTorch` release the GIL, so `ThreadPoolExecutor` can genuinely parallelise matrix ops.

---



## Practice Assignment

Save as `concurrency.py` (or a folder with one file per task). Every snippet in this file is copy-paste runnable — start from those.

1. **Lab 0:** run `cpu-demo.py` demos 1–3. Screenshot or note the CPU % for each. Write one sentence explaining why Demo 2 and Demo 3 look different.
2. **Async:** write `simulate_api_call(name, delay)` (uses `asyncio.sleep`), then a `main()` that calls it three times sequentially vs. concurrently with `asyncio.gather`, printing both durations.
3. **TaskGroup:** rewrite #1 using `asyncio.TaskGroup` (3.11+) instead of `gather`. Add a task that raises an exception and observe how `TaskGroup` cancels the others.
4. **Threads:** use `ThreadPoolExecutor` to fetch `/users/1`–`/users/5` from JSONPlaceholder; compare to sequential `requests.get`.
5. **Race condition:** write the broken `counter += 1` example from above. Run it. Then fix it with `threading.Lock`.
6. **Processes:** use `ProcessPoolExecutor` to compute Fibonacci for `[100_000, 200_000, 300_000, 400_000]`; compare to sequential.
7. `asyncio.to_thread`**:** call `requests.get` from inside an async function without blocking the event loop.
8. In comments, answer: why do threads help #3 but not #5, and why does multiprocessing help #5? What is the GIL's role in each? Which of these is preemptive and which is cooperative?

---

