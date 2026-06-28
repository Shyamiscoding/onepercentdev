"""
Part 41 · File 03 — Module-Level Loggers (getLogger(__name__))
Notes section: "Module-Level Loggers (the pro pattern)"

The pro pattern: every file makes its OWN logger, named after the module. The
name comes from __name__ — and it changes with HOW the file is used:
  - run this file directly   → __name__ is "__main__"
  - import it (see main.py)  → __name__ is "module_logger" (the file's name)

Run it directly:
    uv run module_logger.py
Or import it from main.py to watch the name change:
    uv run main.py

This is the SAME code as 03_module_logger.py — only the filename changed. No
digit prefix on purpose: Python can only `import` names that start with a letter
or underscore, never a digit. So 03_module_logger can be RUN but not IMPORTED;
module_logger can be both.
"""

import logging
from pathlib import Path

LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)                              # keep all logs in Part-41/logs/

logging.basicConfig(
    level=logging.INFO,                                   # the dial — show INFO and above
    format="%(asctime)s — %(levelname)s — %(name)s — %(message)s",
    filename=LOG_DIR / "app_basic_1.log",                   # omit this line → logs to the console instead
    filemode="a",                                         # "a" = append (default) · "w" = overwrite each run
    encoding="utf-8",
)

# One named logger per file — its name is whatever __name__ is right now
logger = logging.getLogger(__name__)

logger.info(f"module logger speaking — my __name__ is '{__name__}'")

print("Hello this is print statement")