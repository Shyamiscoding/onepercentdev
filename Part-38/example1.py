from pathlib import Path

data = Path("data")
total = 0
for f in data.rglob("*.txt"):
    words = len(f.read_text(encoding="utf-8").split())
    total += words
    print(f.name, words)        # notes.txt 120

print("Total:", total)