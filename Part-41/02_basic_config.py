"""
Part 41 · File 02 — Configure It Once (basicConfig)
Notes section: "Configure It Once"

logging.basicConfig() is the one-call way to set up logging for a simple
script: pick the dial (level), the format, and optionally a file. This is the
BASIC setup — start here, then move to handlers (File 05) and the production
setup (File 06).

Run it:
    python 02_basic_config.py
Then open logs/app_basic.log to see the lines that were written.
"""

import logging
from pathlib import Path

LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)                              # keep all logs in Part-41/logs/

logging.basicConfig(
    level=logging.INFO,                                   # the dial — show INFO and above
    format="%(asctime)s — %(levelname)s — %(name)s — %(message)s",
    filename=LOG_DIR / "app_basic.log",                   # omit this line → logs to the console instead
    filemode="a",                                         # "a" = append (default) · "w" = overwrite each run
    encoding="utf-8",
)

# What each format placeholder fills in (no need to run it to see this):
#   %(asctime)s   → 2026-06-24 00:31:08,123      the timestamp
#   %(levelname)s → INFO                          the severity level
#   %(name)s      → root                          the logger name (root here, because we call
#                                                  logging.info() directly; a named logger shows __main__)
#   %(message)s   → Application started           your text
#
# So one log line renders as:
#   2026-06-24 00:31:08,123 — INFO — root — Application started

logging.info("Application started")     # written — INFO == the dial
logging.warning("low disk space")       # written — WARNING is above the dial
logging.debug("x = 42")                 # skipped — DEBUG is below the dial

print("done — open logs/app_basic.log to see the two lines that were written")
