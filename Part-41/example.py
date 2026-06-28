"""
Part 41 — Where Your Logs Go: stdout vs stderr.

Two kinds of output leave this program on TWO different channels:
  - print()  → stdout (channel 1): the program's RESULTS
  - logging  → stderr (channel 2): the LOGS, warnings, and tracebacks

Because they are separate channels, you can send them to separate files:

    python example.py > out.txt 2> errs.txt
        out.txt  = the report (print output)
        errs.txt = the logs (INFO lines + the error traceback)

Run normally (both show on screen):
    python example.py
"""

import logging

logging.basicConfig(                       # no filename → logs go to the CONSOLE (stderr)
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)

students = [
    {"name": "Alice", "scores": [80, 90, 85]},
    {"name": "Bob", "scores": [70, 65, 72]},
    {"name": "Charlie", "scores": []},      # the empty list that broke Part 40
]


def calculate_summary(scores):
    logger.debug(f"scores received: {scores}")
    total = sum(scores)
    average = total / len(scores)            # fails when a student has an empty score list
    return {"total": total, "average": average, "count": len(scores)}


def generate_report(students):
    report = []
    for student in students:
        try:
            summary = calculate_summary(student["scores"])
            logger.info(f"{student['name']} summarized: avg={summary['average']:.1f}")
            report.append(f"{student['name']}: avg={summary['average']:.1f}")
        except ZeroDivisionError:
            logger.exception(f"could not summarize {student['name']}")   # traceback → stderr
    return report


def main():
    logger.info("report started")
    for line in generate_report(students):
        print(line)                          # the RESULT → stdout
    logger.info("report finished")


if __name__ == "__main__":
    main()

# Split the two channels into separate files:
#   python example.py > out.txt              # results only (print) → out.txt; logs stay on screen
#   python example.py 2> errs.txt            # logs only (stderr)   → errs.txt; results stay on screen
#   python example.py > out.txt 2> errs.txt  # results → out.txt AND logs → errs.txt (two files!)
