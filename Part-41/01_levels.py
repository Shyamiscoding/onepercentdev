"""
Part 41 · File 01 — The Levels (the dial)
Notes section: "The Levels (the dial)"

Every log message has a severity. The "dial" (level) sets the cutoff: it shows
that level and everything ABOVE it. Lower the dial → see MORE.

Run it:
    python 01_levels.py

Then change LOG_LEVEL in .env (INFO → DEBUG) and run again to watch the hidden
DEBUG line appear. The default dial is WARNING, so INFO and DEBUG stay hidden
until you lower it.
"""

import logging
import os
from pathlib import Path

try:
    from dotenv import load_dotenv          # pip install python-dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass

LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)      

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),   # the dial — read from .env
    format="%(asctime)s — %(levelname)s — %(message)s",
    filename=LOG_DIR / "app.log",                                  # omit this → log to console
    filemode="a",                                        # append (default)
    encoding="utf-8"
)

logging.debug("debug — detailed diagnostics (value 10, lowest)")
logging.info("info — normal events (value 20)")
logging.warning("warning — something unexpected (value 30)")
logging.error("error — something failed (value 40)")
logging.critical("critical — severe failure (value 50, highest)")
