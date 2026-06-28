"""
Part 41 · File 06 — Production setup + the full program (run this one)
Notes sections: "Production Configuration" · "Where Your Logs Go" · "Logging Errors with the Traceback"

Everything from Files 01–05 put together the way a real app does it:
  - the dial read from .env (LOG_LEVEL)
  - a NAMED logger — getLogger(__name__)
  - two handlers: console (your dial) + a RotatingFileHandler (full DEBUG, never grows forever)
  - logger.exception() to capture the full traceback when something breaks

It runs the same students-and-scores program you debugged in Part 40.

Run it:
    python 06_production.py
Then open logs/app.log for the complete record (including the traceback).
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

try:
    from dotenv import load_dotenv          # pip install python-dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass

# ── one-time logging setup (in a real project this lives in its own config file) ──
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)                          # keep all logs in Part-41/logs/
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()    # the dial, from .env

root = logging.getLogger()
root.setLevel(logging.DEBUG)                          # MASTER gate — handlers filter below

fmt = logging.Formatter("%(asctime)s — %(levelname)s — %(name)s — %(message)s")

console = logging.StreamHandler()                     # screen: only your dial level and above
console.setLevel(LOG_LEVEL)
console.setFormatter(fmt)

file = RotatingFileHandler(                           # file: keep everything, never grow forever
    LOG_DIR / "app.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8"
)
file.setLevel(logging.DEBUG)
file.setFormatter(fmt)

root.addHandler(console)
root.addHandler(file)
# ──────────────────────────────────────────────────────────────────────────────

logger = logging.getLogger(__name__)   # this module's own logger

students = [
    {"name": "Alice", "scores": [80, 90, 85]},
    {"name": "Bob", "scores": [70, 65, 72]},
    {"name": "Charlie", "scores": []},      # the empty list that broke Part 40
]


def calculate_summary(scores):
    logger.debug(f"scores received: {scores}")     # only in the file (console dial is INFO)
    total = sum(scores)
    if len(scores) == 0:
        raise ZeroDivisionError("No scores to calculate average")
    average = total / len(scores)                  # fails when a student has an empty score list
    return {"total": total, "average": average, "count": len(scores)}


def generate_report(students):
    report = []
    for student in students:
        try:
            summary = calculate_summary(student["scores"])
            logger.info(f"{student['name']} summarized: avg={summary['average']:.1f}")
            report.append(f"{student['name']}: avg={summary['average']:.1f}")
        except ZeroDivisionError:
            logger.exception(f"could not summarize {student['name']}")   # message + full traceback
    return report


def main():
    logger.info("report started")
    for line in generate_report(students):
        print(line)
    logger.info("report finished — open logs/app.log to see the full record")


if __name__ == "__main__":
    main()

# Redirect the two output channels (stdout=1 = print, stderr=2 = logs):
#   python 06_production.py > out.txt        # only print() output → file; logs stay on screen
#   python 06_production.py 2> errs.txt      # only the logs → file; print() output stays on screen
#   python 06_production.py > all.txt 2>&1   # both channels → file (what cloud platforms capture)
