"""
Part 41 · File 05 — Console AND File (handlers)
Notes section: "Console AND File (handlers)"

Send the SAME logs to two places, each with its own dial:
  - console (screen)  → INFO and above, kept clean
  - file (handlers.log) → EVERYTHING down to DEBUG, the full story

Key idea — two gates: a message passes the LOGGER's level first (master gate),
then each HANDLER's level. The logger is DEBUG so nothing is blocked early;
each handler then decides what it keeps.

Run it:
    python 05_handlers.py
Then open logs/handlers.log: the DEBUG line is in the file but never hit the screen.
"""

import logging
from pathlib import Path

LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)          # keep all logs in Part-41/logs/

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)        # MASTER gate — let every level through; handlers filter next

# Handler 1 → the screen: keep it clean, only the important lines
console = logging.StreamHandler()
console.setLevel(logging.INFO)        # screen shows INFO and above (hides DEBUG noise)

# Handler 2 → a file: keep the full story for later
file = logging.FileHandler(LOG_DIR / "handlers.log", encoding="utf-8")
file.setLevel(logging.DEBUG)          # file keeps EVERYTHING, down to DEBUG

# One shared format, attached to both handlers
fmt = logging.Formatter("%(asctime)s — %(levelname)s — %(name)s — %(message)s")
console.setFormatter(fmt)
file.setFormatter(fmt)

logger.addHandler(console)            # plug both handlers into the logger
logger.addHandler(file)

logger.debug("DEBUG — lands in handlers.log only (console dial is INFO)")
logger.info("INFO — appears on screen AND in the file")
logger.warning("WARNING — appears on screen AND in the file")

print("done — open logs/handlers.log to see the DEBUG line that never hit the screen")
