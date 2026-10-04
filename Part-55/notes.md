# Part 55 — Performance 1 (Big-O Thinking)

In Part 54, you learned how to make programs do multiple things at once with async, threads, and processes. Now we zoom into a different performance question: how does your code scale as data grows?

## Why Performance Intuition Matters

Two developers solve the same problem. One's solution takes 0.01 seconds. The other takes 45 minutes. Both produce the correct answer. The difference is not intelligence — it is knowing how code scales.

Big-O is not academic theory. It is practical intuition that determines whether your code can handle real-world data.

---



## The Four Patterns You Need



### O(1) — Constant Time

The operation takes the same time regardless of data size:

```python
scores = {"Alice": 95, "Bob": 87, "Charlie": 92}

score = scores["Alice"]   # O(1) — instant, whether dict has 10 or 10 million entries
```

```python
numbers = {1, 2, 3, 4, 5}

exists = 3 in numbers   # O(1) — set membership is instant
```

Dict lookup and set membership are O(1). This is why choosing the right data structure matters.

### O(n) — Linear Time

Time grows proportionally with data size:

```python
def find_max(numbers: list[int]) -> int:
    maximum = numbers[0]
    for num in numbers:   # Visits every element once
        if num > maximum:
            maximum = num
    return maximum
```

10 items → 10 operations. 1 million items → 1 million operations. Proportional growth.

### O(n²) — Quadratic Time

Time grows with the **square** of data size. This is where most performance bugs live:

```python
def has_duplicate_slow(items: list) -> bool:
    for i in range(len(items)):           # n iterations
        for j in range(i + 1, len(items)):  # n iterations (nested)
            if items[i] == items[j]:
                return True
    return False
```

10 items → ~50 comparisons. 1,000 items → ~500,000. 100,000 items → ~5 billion. This does not scale.

### O(log n) — Logarithmic Time

Each step cuts the problem in half:

```python
def binary_search(sorted_list: list[int], target: int) -> int:
    low, high = 0, len(sorted_list) - 1

    while low <= high:
        mid = (low + high) // 2
        if sorted_list[mid] == target:
            return mid
        elif sorted_list[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1
```

1,000 items → ~10 steps. 1,000,000 items → ~20 steps. Extremely efficient for sorted data.

---



## Quick Reference


| Big-O      | Name         | 1,000 items | 1,000,000 items   | Example       |
| ---------- | ------------ | ----------- | ----------------- | ------------- |
| O(1)       | Constant     | 1           | 1                 | Dict lookup   |
| O(log n)   | Logarithmic  | 10          | 20                | Binary search |
| O(n)       | Linear       | 1,000       | 1,000,000         | Single loop   |
| O(n log n) | Linearithmic | 10,000      | 20,000,000        | Sorting       |
| O(n²)      | Quadratic    | 1,000,000   | 1,000,000,000,000 | Nested loops  |


---



## Typical Performance Traps



### Trap 1: Nested Loops When a Set Would Work

```python
# BAD: O(n²) — checking membership in a list inside a loop
def find_common_slow(list1: list, list2: list) -> list:
    common = []
    for item in list1:           # O(n)
        if item in list2:        # O(n) — list membership is linear!
            common.append(item)
    return common                # Total: O(n²)

# GOOD: O(n) — convert to set first
def find_common_fast(list1: list, list2: list) -> list:
    set2 = set(list2)            # O(n) one-time conversion
    common = []
    for item in list1:           # O(n)
        if item in set2:         # O(1) — set membership is constant!
            common.append(item)
    return common                # Total: O(n)
```

With 100,000 items: the slow version takes minutes, the fast version takes milliseconds.

### Trap 2: Using `in` on a List vs a Set

```python
# SLOW: O(n) per lookup
users_list = ["alice", "bob", "charlie", ...]   # 100,000 names
"zoe" in users_list   # Scans all 100,000 elements

# FAST: O(1) per lookup
users_set = set(users_list)   # One-time conversion
"zoe" in users_set   # Instant hash lookup
```



### Trap 3: String Concatenation in a Loop

```python
# BAD: O(n²) — each += creates a new string
result = ""
for word in words:
    result += word + " "   # Creates a new string every iteration

# GOOD: O(n) — join builds the string once
result = " ".join(words)
```

Strings are immutable. Each `+=` creates a new string object and copies all previous characters. With 100,000 words, the slow version copies billions of characters.

---



## Data Structure Choice Eliminates Algorithms

The right data structure often makes the problem trivial:

```python
# Problem: Count frequency of each word in a large text

# Without knowing dict: nested loops, complex logic, O(n²)
# With dict: simple and O(n)
from collections import Counter

word_counts = Counter(words)   # One line, O(n)
```

```python
# Problem: Remove duplicates while preserving order

# Without knowing set: nested loops, O(n²)
# With set: track seen items, O(n)
def deduplicate(items: list) -> list:
    seen: set = set()
    result: list = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
```

---



## Interview Pattern: Two-Sum

Given a list of numbers and a target, find two numbers that add up to the target.

```python
# O(n²) — brute force
def two_sum_slow(numbers: list[int], target: int) -> tuple[int, int] | None:
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] + numbers[j] == target:
                return (numbers[i], numbers[j])
    return None

# O(n) — using a set
def two_sum_fast(numbers: list[int], target: int) -> tuple[int, int] | None:
    seen: set[int] = set()
    for num in numbers:
        complement = target - num
        if complement in seen:
            return (complement, num)
        seen.add(num)
    return None
```

The interviewer does not want the brute force. They want to see if you can recognize the O(n) pattern using a set.

---



## How to Analyze Your Code

1. **Count the loops:** One loop = O(n). Nested loops = O(n²). Loop inside a loop inside a loop = O(n³).
2. **Check what is inside the loop:** `if item in list` inside a loop = O(n²). `if item in set` inside a loop = O(n).
3. **Identify the bottleneck:** The slowest part determines the overall complexity.
4. **Ask: "What happens when n is 1 million?"** If the answer is "it crashes" or "it takes hours," you need a better approach.

---



## Where This Applies in Real Work

- **API response time:** An endpoint that is O(n²) on a list of 100 users works fine. When the user base grows to 100,000, the response takes minutes. This is a production outage.
- **Database queries:** Fetching all records and filtering in Python (O(n)) vs using a database index (O(log n)) — the difference can be 1000x.
- **Data pipelines:** Processing a CSV with 10 million rows. An O(n²) approach is impossible. An O(n) approach takes seconds.
- **AI inference:** Preprocessing input for a model. If preprocessing is O(n²), scaling to larger inputs becomes impractical.
- **Interviews:** Big-O is the language of technical interviews. Every coding question expects you to analyze and optimize time complexity.

---



## Practice Assignment

1. Given a list of 100,000 random integers:

```python
import random
numbers = [random.randint(1, 1_000_000) for _ in range(100_000)]
```

1. Find all pairs that sum to a target value (e.g., 500,000):
  - Write the O(n²) brute-force solution
  - Write the O(n) set-based solution
2. Time both using `timeit` (or `time.time()` for rough comparison)
3. Write an O(n) duplicate finder using a set
4. Write an O(n) word frequency counter using `dict` or `Counter`
5. For each solution, write a comment stating the Big-O complexity

Save as `performance_basics.py`.

---



