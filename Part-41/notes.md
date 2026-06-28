# Part 41 — Logging (Production Mindset)

In Part 40 you debugged by *watching* — tracebacks, `print()`, the VS Code debugger. That works while you sit in front of the code. But in production you can't: the program runs on a server, ran days ago, with nobody watching. Logging is how a program tells you what happened — *after* it happened.

> **The one idea:** logging is `print()` with a **volume dial.** You leave all the messages in your code permanently, each tagged with a severity level, and one setting controls how much you see — everything in development, only the important parts in production.

---

## Why print() Isn't Enough


| `print()` problem                           | Logging fixes it with                           |
| ------------------------------------------- | ----------------------------------------------- |
| no severity — can't tell info from disaster | 5 levels: DEBUG, INFO, WARNING, ERROR, CRITICAL |
| no timestamp — when did it happen?          | `%(asctime)s`                                   |
| all-or-nothing — can't filter               | the level dial                                  |
| vanishes when the program exits             | write to a file                                 |
| must hunt and delete every debug print      | leave them in; the dial hides them              |


---

## The Levels (the dial)

Every message gets a severity, from lowest to highest:


| Level      | Value | Use for                                               |
| ---------- | ----- | ----------------------------------------------------- |
| `DEBUG`    | 10    | detailed diagnostics (development only)               |
| `INFO`     | 20    | normal events — started, user logged in               |
| `WARNING`  | 30    | unexpected but not broken — low disk, deprecated call |
| `ERROR`    | 40    | something failed, app continues — API call failed     |
| `CRITICAL` | 50    | severe — app may not continue — database down         |


```python
import logging

logging.debug("x = 42")
logging.info("user 'alice' logged in")
logging.warning("config missing, using defaults")
logging.error("failed to save record")
logging.critical("database is down")
```

**The dial = the lowest level you want to see. It shows that level and everything above it.** So lowering the dial shows *more*, not fewer errors:


| Dial set to           | You see                                                   |
| --------------------- | --------------------------------------------------------- |
| `DEBUG`               | everything — DEBUG, INFO, WARNING, ERROR, CRITICAL        |
| `INFO`                | INFO and above (errors still show — only DEBUG is hidden) |
| `WARNING` *(default)* | WARNING, ERROR, CRITICAL                                  |
| `ERROR`               | ERROR, CRITICAL only                                      |


Two things to lock in: the **default** dial is `WARNING` (so INFO and DEBUG are hidden until you lower it), and setting the dial to `INFO` **never hides your errors** — ERROR is higher than INFO, so it always gets through. The dial only ever hides the *less serious* levels below it.

---

## Configure It Once

```python
import logging

logging.basicConfig(
    level=logging.INFO,                                  # the dial
    format="%(asctime)s — %(levelname)s — %(message)s",
    filename="app.log",                                  # omit this → log to console
    filemode="a",                                        # append (default)
    encoding="utf-8",
)

logging.info("Application started")
# 2026-03-19 14:30:15 — INFO — Application started
```

Main knobs: `level` (the dial), `format`, and `filename`/`filemode` (file vs console).

Common format placeholders: `%(asctime)s` time · `%(levelname)s` level · `%(name)s` logger · `%(message)s` text · `%(filename)s` / `%(lineno)d` source location.

> **Gotcha:** a bare `filename="app.log"` is created in the **current working directory** — wherever you *ran* `python` from, not where the `.py` file lives (the Part 38 path lesson). For anything real, give an absolute path (often from an env var like `LOG_FILE`). `basicConfig` is also for simple scripts — it only configures logging *once*; see the production setup below.

---

## Module-Level Loggers (the pro pattern)

Above we called `logging.info()` directly — that uses the one shared **root** logger. Real projects instead give every file its own logger, named after the module:

```python
# utils.py
import logging

logger = logging.getLogger(__name__)   # name becomes "utils"
```

Now each line shows *which module* produced it — essential when 50 files all log into one place. Use `getLogger(__name__)` at the top of every module; never call `logging.info()` directly in real code.

---

## The Dial in Action — Replace print() with logging

This is the direct upgrade from Part 40. Using the module logger from above, the debug lines now stay in the code **forever**:

```python
import logging

logger = logging.getLogger(__name__)

def calculate_total(items):
    logger.debug(f"items received: {items}")     # shown only when dial = DEBUG
    total = sum(i["price"] * i["quantity"] for i in items)
    logger.info(f"calculated total: {total}")    # shown in production too
    return total
```

Development → set the dial to `DEBUG`, see everything. Production → set it to `INFO`, the debug lines are silently skipped. **No code changes, no deleting prints.**

---

## Console AND File (handlers)

Want full debug detail in a file but only important lines on screen? **Handlers** route messages to different places, each with its **own dial**:

```python
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)        # MASTER gate — let every level through; handlers filter next

# Handler 1 → the screen: keep it clean, only the important lines
console = logging.StreamHandler()
console.setLevel(logging.INFO)        # screen shows INFO and above (hides DEBUG noise)

# Handler 2 → a file: keep the full story for later
file = logging.FileHandler("app.log", encoding="utf-8")
file.setLevel(logging.DEBUG)          # file keeps EVERYTHING, down to DEBUG

# One shared format, attached to both handlers
fmt = logging.Formatter("%(asctime)s — %(levelname)s — %(name)s — %(message)s")
console.setFormatter(fmt)
file.setFormatter(fmt)

logger.addHandler(console)            # plug both handlers into the logger
logger.addHandler(file)
```

**Why two different levels?** Every message passes through **two gates**: first the **logger's** level, then each **handler's** level. The logger is the *master* gate — set it to `DEBUG` so nothing is blocked early; then each handler decides what *it* keeps. That's how the **same** `logger.debug(...)` line can land in the file but stay off the screen: the file handler's dial is `DEBUG`, the console handler's is `INFO`.

> If you set the *logger* to `INFO`, DEBUG messages die at the first gate and never reach the file — even though the file handler asked for DEBUG. **Master gate first, handler gates second.**

---

## Where Your Logs Go — stdout, stderr, and Redirection

Before sending logs anywhere fancy, understand where they go *right now* when you run the script. Your program doesn't write to "the screen" — it writes to two numbered channels the OS hands every program (remember Part 36: `print()` really writes to `sys.stdout`, a file connected to your terminal — and Part 38's `f.fileno()` returns that channel's number):


| Channel    | Number | Carries                    | Written by            |
| ---------- | ------ | -------------------------- | --------------------- |
| **stdout** | 1      | the program's real results | `print()`             |
| **stderr** | 2      | errors, warnings, **logs** | `logging`, tracebacks |


Both show on screen by default, so they look the same — until you **redirect** them by number:

```bash
python 06_production.py > out.txt        # channel 1 only — just print() output (logs stay on screen)
python 06_production.py 2> errs.txt      # channel 2 only — just the logs (print output stays on screen)
python 06_production.py > all.txt 2>&1   # both — "send channel 2 to wherever channel 1 goes"
```

> **Gotcha:** Python's logging writes to **stderr (2)**, not stdout. So a plain `> out.txt` captures your `print()` results but **not** your logs — you need `2>` or `2>&1` for those.

**Why this matters next:** in the cloud you never type `>` by hand. Your app just writes to stdout/stderr, and the platform captures **both** automatically (like a built-in `2>&1`) and ships them away. That one idea — *the app just writes; something outside decides where it goes* — is the whole foundation of the production setup below.

---

## Production Configuration

`basicConfig` is fine for scripts. Real apps need two more things, and there are two standard patterns.

**Problem 1 — a plain log file grows forever and fills the disk.** Fix: a **rotating** handler that caps the size and keeps a few old files:

```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    "/var/log/myapp/app.log",      # absolute path, not CWD
    maxBytes=10_000_000,           # 10 MB per file
    backupCount=5,                 # keep 5 old files, then delete the oldest
    encoding="utf-8",
)
```

**Problem 2 — configuring handlers by hand gets messy.** Fix: `dictConfig` — one dictionary (often loaded from a YAML/JSON file, your Part 39 skills) that defines levels, formats, and handlers in one place. This is the production standard.

**The two real-world patterns** (which one you pick depends on *where* the app runs):


| Where it runs                           | What you do                                                                                      | Read more                                                                                                                               |
| --------------------------------------- | ------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| Containers / cloud (Docker, Kubernetes) | log to the **console** (no file); the platform collects stdout — the idea from the section above | [12-Factor logs](https://12factor.net/logs) · [Kubernetes logging](https://kubernetes.io/docs/concepts/cluster-administration/logging/) |
| Traditional server                      | write to an **absolute path** with a `RotatingFileHandler` so the disk never fills               | [RotatingFileHandler docs](https://docs.python.org/3/library/logging.handlers.html#rotatingfilehandler)                                 |


And the dial stays in config, not code — `level=os.getenv("LOG_LEVEL", "INFO")` — so you change it and restart, no redeploy.

### The tools that collect those logs

As we just saw, in the cloud your app only writes to the console (stdout) — it **doesn't open log files**. A log platform then grabs every line, stores it, and lets you search, filter, and alert across thousands of servers in one place. The big ones:

- **[Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)** — AWS's built-in logging service. If your app runs on AWS, your console output lands here automatically; you search and set alarms in the AWS console.
- **[Datadog](https://www.datadoghq.com/product/log-management/)** — a paid all-in-one monitoring platform (logs + metrics + traces). Cloud-agnostic; popular in companies for dashboards and alerting.
- **[Grafana Loki](https://grafana.com/oss/loki/)** — yes, the Grafana one. Open-source log aggregator; you view and query the logs inside **[Grafana](https://grafana.com/)** dashboards. The free/self-hosted favourite.

All three do the same core job: **take your console logs and organize them** so you can search and alert — no SSH-ing into servers to read files.

---

## The Whole Journey at a Glance

Read this top to bottom — each row adds one piece, from your bare script to a fully monitored production app:


| Stage                               | What you add                                                                                                                                 | Who sends the logs / data                                                        | What you get                                        |
| ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | --------------------------------------------------- |
| **1. Your code**                    | the script itself (`06_production.py`)                                                                                                       | nobody — `print()` only                                                          | output flashes on screen, then it's gone            |
| **2. Logging**                      | Python `logging` (levels + handlers)                                                                                                         | the app writes to **console + `logs/app.log`**                                   | timestamped, leveled logs saved to a file           |
| **3. + Grafana Loki (you push)**    | the `python-logging-loki` library                                                                                                            | the **app itself pushes** logs to Loki                                           | logs in an online **Grafana** dashboard, searchable |
| **4. Production (an agent pushes)** | an **agent: [Promtail](https://grafana.com/docs/loki/latest/send-data/promtail/) / [Grafana Alloy**](https://grafana.com/docs/alloy/latest/) | the app just writes to the **console**; the **agent** reads it and sends to Loki | same dashboard — but the app stays fast & safe      |
| **5a. Beyond logs — metrics**       | **[Prometheus](https://prometheus.io/)**                                                                                                     | it collects *numbers* from your app (CPU, requests/sec)                          | graphs of how the system is performing              |
| **5b. Beyond logs — errors**        | **[Sentry](https://sentry.io/)**                                                                                                             | it catches *exceptions / crashes* with the full traceback                        | instant alerts — "what broke, where, and how often" |


**Three signals, three tools:** **Loki** = logs (text) · **Prometheus** = metrics (numbers) · **Sentry** = errors (crashes) — all viewed around Grafana. The next sections walk through stages 3 and 4; stages 5a/5b are a future topic — monitoring.

---

## See Your Logs in a Grafana Dashboard

So far our logs live on screen and in `logs/app.log`. In real teams they land in a **web dashboard** you can search and filter. The journey is always the same three stops:

```
your code  ──►  Loki (stores the logs)  ──►  Grafana (the dashboard you search)
```

**Loki** is the storage; **Grafana** is the screen. The only thing that changes between a simple setup and production is **who delivers the logs to Loki.**

### Sending logs to Grafana yourself — the app pushes them

There's a tiny library that turns "send to Loki" into just **another handler** (the same `addHandler` pattern from Files 05/06). The runnable version is `07_grafana_loki.py`.

**Step 1 — install the library:**

```bash
uv add python-logging-loki        # or: pip install python-logging-loki
```

**Step 2 — get your Loki URL + User (inside Grafana):** sign up / log in at [grafana.com](https://grafana.com) (free tier), then open your Grafana stack and go to **[Connections → Data sources](https://grafana.com/docs/grafana/latest/datasources/)**:

1. Click your Loki data source (named like `grafanacloud-<stack>-logs`).
2. **Connection → URL** = `https://logs-prod-XXX.grafana.net` → your push URL is that **+ `/loki/api/v1/push`**.
3. **Authentication → Basic auth → User** = a number (e.g. `1660256`) — this is your username.

**Step 3 — create the token (grafana.com portal):** go to **[Security → Access Policies](https://grafana.com/docs/grafana-cloud/security-and-account-management/authentication-and-permissions/access-policies/)**:

1. **Create access policy** → name it → add the `**logs:write`** scope → **Create**.
2. On that policy → **Add token** → name it → **Create token** → **copy it once** (it's shown only one time).

> Watch out: don't use the **Grafana instance ID** — Loki has its own numeric **User** shown on the data-source page. Keep the token in `.env` (`LOKI_TOKEN`), not hard-coded.

**Step 4 — add the handler** (the runnable file reads these from `.env`):

```python
import logging_loki

logging_loki.emitter.LokiEmitter.level_tag = "level"   # so Grafana color-codes by level
loki = logging_loki.LokiHandler(
    url="https://logs-prod-XXX.grafana.net/loki/api/v1/push",  # URL + /loki/api/v1/push
    tags={"app": "part41"},                                     # query later with {app="part41"}
    auth=("USER_ID", "API_TOKEN"),                              # (numeric User, access-policy token)
    version="1",
)
logger.addHandler(loki)
```

**Step 5 — run it and look:** `uv run 07_grafana_loki.py`, then in Grafana → **Explore** → pick your Loki data source → set the time picker to **Last 15 minutes** → run a query:


| Use case    | Query                            |
| ----------- | -------------------------------- |
| All logs    | `{app="part41"}`                 |
| Errors only | `{app="part41"} | level="error"` |
| Search text | `{app="part41"} |= "some text"`  |


The same `INFO`/`ERROR` lines appear online, searchable.

Here the **app itself** opens a connection and pushes every log — quick to set up, but the app is now doing delivery work too.

### How production does it — the app just writes; a separate agent delivers

In production we flip it. The app **does not** push to Loki. It only writes to **stdout** (the `2>&1` idea above) and forgets. A **separate program — an agent — reads that output and ships it to Loki.** The app never waits on the network.

```
You push it:   app ──(pushes over HTTP itself)──► Loki ──► Grafana
Production:    app ──writes to stdout──► [agent] ──► Loki ──► Grafana
                                          a separate program, not your code
```

The agent is a ready-made tool you install and run **next to** your app — you don't write it:

- **[Promtail](https://grafana.com/docs/loki/latest/send-data/promtail/)** — Grafana's classic log agent for Loki.
- **[Grafana Alloy](https://grafana.com/docs/alloy/latest/)** — Grafana's newer all-in-one agent (the recommended one today).

**Why flip it?** Three plain reasons:


|                 | App pushes its own logs                    | Production (agent delivers)                                   |
| --------------- | ------------------------------------------ | ------------------------------------------------------------- |
| **Speed**       | every log = an HTTP call inside the app    | writing to stdout is instant; the agent does the network work |
| **Safety**      | if Loki is down, the app's logging suffers | the agent buffers & retries; the app keeps running            |
| **Flexibility** | change log system → change app code        | swap Loki for Datadog → the app never changes                 |


> **Name trap:** the log agent is **Promtail / Alloy** — *not* **Prometheus**. Prometheus is the **metrics** (numbers) sibling — CPU %, requests/sec — and it also feeds Grafana, but it has nothing to do with shipping your text logs. Same family, different jobs.

**The one line for it all:** *who delivers the logs — the app, or a separate agent?* When you push them yourself, the app does it. In production, an agent does it. Everything else (Loki, Grafana, searching, filtering) is identical.

---

## Logging Errors with the Traceback

Inside an `except` block (Parts 33–35), `logger.exception()` logs your message **plus the full traceback** from Part 40 — the single most useful line in production:

```python
def process_file(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        logger.error(f"file not found: {path}")               # message only — expected case
        return None
    except Exception:
        logger.exception(f"unexpected error reading {path}")  # message + full traceback
        raise
```

The log then contains the exact bottom-up traceback you learned to read in Part 40 — but captured automatically, with no one watching:

```
2026-03-19 14:30:15 — ERROR — unexpected error reading data.csv
Traceback (most recent call last):
  File "app.py", line 9, in process_file
    return f.read()
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff ...
```

`logger.exception()` only works inside an `except` block. Anywhere else, use `logger.error("...", exc_info=True)`.

---

## Three Rules for Good Logs

```python
# 1. Include context — what, who, why
logger.error(f"request failed — user_id={uid}, endpoint={url}, status={code}")

# 2. Match the level to the severity
logger.info("user logged in")          # not WARNING
logger.critical("database is down")    # not WARNING

# 3. NEVER log secrets
logger.debug(f"api key: {api_key[:4]}****")   # masked, never the full key
```

Passwords, tokens, API keys, personal data — never in logs. Logs are shared and stored where many people can read them.

---

## Where This Applies in Real Work

- **Production monitoring:** tools scan logs for `ERROR`/`CRITICAL` and fire alerts.
- **API request tracing:** tag each request with an ID, log it at every step, search by ID when a user reports a bug.
- **AI / data pipelines:** log each stage's start, counts, and failures to catch model drift and silent data loss.
- **Debugging without access:** in production you can't attach a debugger — logs are your only window, and their quality decides how fast you fix things.

---

## Practice Assignment

Add logging to your note app from Part 36:

1. `add_note()` → `INFO`; `view_notes()` → `DEBUG` (note count); `clear_notes()` → `WARNING` (destructive); file-not-found → `ERROR`; unexpected errors → `logger.exception()`.
2. Send logs to **both** console (`INFO`) and file `notes_app.log` (`DEBUG`), using a module-level logger.
3. Format: `%(asctime)s — %(levelname)s — %(message)s`.
4. Run it, then open `notes_app.log` and confirm: DEBUG appears only in the file, INFO and above in both, and the log tells the complete story of the run.

Save as `src/notes_app_logged.py`.

---

> **Phase 4 complete.** Your code now handles errors, reads/writes every file format (text, JSON, JSONL, CSV, Markdown, PDF, Excel, images), debugs systematically, and logs for production.

