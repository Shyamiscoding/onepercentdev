# Part 41 — Logging · Code Files (demo order)

Open and run these **in order** — each maps to one section of `notes.md`.

| # | File | Notes section | Run | Shows |
|---|------|---------------|-----|-------|
| 1 | `01_levels.py` | The Levels (the dial) | `python 01_levels.py` | the 5 severity levels; change `LOG_LEVEL` in `.env` to see more/less |
| 2 | `02_basic_config.py` | Configure It Once | `python 02_basic_config.py` | `basicConfig` writing to `logs/app_basic.log` |
| 3 | `03_module_logger.py` → `module_logger.py` + `main.py` | Module-Level Loggers | `uv run 03_module_logger.py`; then `uv run main.py` | run directly → `__main__`; `import 03_...` fails (digit rule); same code renamed → `module_logger.py`, imported by `main.py` → `module_logger` |
| 4 | `04_dial_in_action.py` | The Dial in Action | `python 04_dial_in_action.py` | DEBUG hidden at INFO; flip `LOG_LEVEL` in `.env` |
| 5 | `05_handlers.py` | Console AND File (handlers) | `python 05_handlers.py` | same log → screen (INFO) + `logs/handlers.log` (DEBUG) |
| 6 | `06_production.py` | Production Config · Redirection · Traceback | `python 06_production.py` | full app: `RotatingFileHandler` → `logs/app.log`, `logger.exception()` |
| 7 | `07_grafana_loki.py` | See Your Logs in a Grafana Dashboard | `python 07_grafana_loki.py` | push logs to Grafana Cloud / Loki (steps in the file) |

> File 3 ships as a **pair on purpose**: `03_module_logger.py` (numbered, like the rest — you can **run** it) and `module_logger.py` (the **same code**, renamed so it can be **imported** by `main.py`). You can't `import` a name that starts with a digit — Python identifiers must begin with a letter or underscore (Part 8's naming rule).

## Supporting files
- `.env` — holds `LOG_LEVEL` (the dial). Change `INFO` ↔ `DEBUG` and re-run.
- `logs/` — every file writes its log here: `app_basic.log`, `handlers.log`, `app.log`.

## Redirection demo (with File 06)
```bash
python 06_production.py > out.txt        # only print() output → file (logs stay on screen)
python 06_production.py 2> errs.txt      # only the logs → file (print output stays on screen)
python 06_production.py > all.txt 2>&1   # both channels → file
```

## Grafana dashboard (File 07)
Steps are in the comment block inside `07_grafana_loki.py`: install `python-logging-loki`,
get a free Loki URL from [grafana.com](https://grafana.com), add one handler, run it.
