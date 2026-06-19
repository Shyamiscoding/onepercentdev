import csv

rows = [{"name": "Alice", "age": 20}, {"name": "Bob", "age": 21}]

with open("out.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["name", "age"])
    w.writeheader()
    w.writerows(rows)