"""
Part 40 — Debugging practice.

This script has a bug. Use it to practice the debugging workflow:

1. Run it. It crashes. Read the traceback BOTTOM-UP:
   the last line is what broke, the line above is where, the lines higher up
   show who called whom.

2. The traceback points to calculate_summary(). Set a breakpoint there
   (click the left margin next to a line number -> a red dot appears) and run again.

3. While paused, inspect the program:
     - Variables panel   -> see scores, total, count change as you step.
     - Watch panel       -> track total and len(scores).
     - Call Stack panel  -> main -> generate_report -> calculate_summary.
     - F10 (Step Over)   -> run the current line, stay in this function.
     - F11 (Step Into)   -> go inside a function call.
     - Shift+F11 (Out)   -> finish this function, return to the caller.

4. Find the cause (an empty score list divided by its length) and fix it.
"""

students = [
    {"name": "Alice", "scores": [80, 90, 85]},
    {"name": "Bob", "scores": [70, 65, 72]},
    {"name": "Charlie", "scores": []},
]


def calculate_summary(scores):
    total = 0
    for score in scores:
        total += score
    # breakpoint()                      # pause here to inspect total and scores in the terminal
    # if len(scores) == 0:
    #     return {"total": total, "average": 0, "count": 0}
    average = total / len(scores)        # fails when a student has an empty score list
    return {"total": total, "average": average, "count": len(scores)}
    

def generate_report(students):
    report = []
    for student in students:
        summary = calculate_summary(student["scores"])
        report.append(f"{student['name']}: avg={summary['average']:.1f}")
    return report


def main():
    for line in generate_report(students):
        print(line)


if __name__ == "__main__":
    main()
