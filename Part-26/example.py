# ============================================
# PART 1: What we learned yesterday (Part 25)
# ============================================

# 1. Default arguments
# def greet(name, greeting="Hello"):
#     print(f"{greeting}, {name}!")

# greet("Shyam")              # Hello, Shyam!
# greet("Shyam", "Namaste")   # Namaste, Shyam!

# 2. *args — accept any number of positional arguments
# def total(*numbers):
#     return sum(numbers)

# print(total(1, 2, 3))       # 6
# print(total(10, 20))        # 30

# 3. **kwargs — accept any number of keyword arguments
# def show_info(**details):
#     for key, value in details.items():
#         print(f"{key}: {value}")

# show_info(name="Shyam", role="dev")


# ============================================
# PART 2: What is recursion?
# ============================================

# A function that calls ITSELF.
# More importantly — breaking a problem into a SMALLER VERSION of the same problem.

# You already know how to do this with a loop:

def countdown_loop(n):
    for i in range(n, 0, -1):
        print(i)
    print("Done!")

# countdown_loop(5)
# Output: 5, 4, 3, 2, 1, Done!

# Here's the SAME thing with recursion:

def countdown(n):
    if n == 0:
        print("Done!")
        return
    print(n)
    countdown(n - 1)

# countdown(5)
# Output: 5, 4, 3, 2, 1, Done!

# Same result. Different approach.
# The loop does ALL the work in one place.
# The recursive version does ONE step (print n), then delegates the rest to itself.

# Two parts every recursive function MUST have:
#   1. BASE CASE      — where it stops (n == 0 above)
#   2. RECURSIVE CASE  — where it calls itself with smaller input (n - 1 above)


# ============================================
# PART 3: Why do we need recursion?
# ============================================

# Loops work on FLAT data — one level, left to right.
# numbers = [1, 2, 3, 4, 5]
# total = 0
# for n in numbers:
#     total += n
# print(total)   # 15   — easy, loop handles it.

# But what about NESTED data?

data = [1, [2, [3, [4, [5]]]]]

# Try with a loop:
# total = 0
# for item in data:
#     if isinstance(item, list):
#         for sub_item in item:
#             if isinstance(sub_item, list):
#                 for sub_sub_item in sub_item:
#                     # ... how deep do we go?!
#                     pass
#     else:
#         total += item

# You DON'T KNOW how deep the nesting goes.
# 1 level? 5 levels? 100 levels? You'd need infinite for-loops.

# With recursion — it just works:

def nested_sum(data):
    total = 0
    for item in data:
        if isinstance(item, list):
            total += nested_sum(item)   # list? same problem, smaller.
        else:
            total += item
    return total

print(nested_sum([1, [2, [3, [4, [5]]]]]))   # 15
print(nested_sum([1, 2, [3, 4], [5, [6, [7]]]]))  # 28


# ============================================
# PART 4: Factorial — base case & recursive case
# ============================================

# 5! = 5 × 4 × 3 × 2 × 1 = 120

def factorial(n):
    if n == 0 or n == 1:       # base case
        return 1
    return n * factorial(n - 1)  # recursive case

print(factorial(5))   # 120
print(factorial(0))   # 1

# What happens without a base case?
# def infinite(n):
#     return n * infinite(n - 1)   # never stops!
# infinite(5)   # RecursionError: maximum recursion depth exceeded


# ============================================
# PART 5: Tracing the call stack
# ============================================

def factorial_trace(n, depth=0):
    indent = "  " * depth
    print(f"{indent}factorial({n}) called")

    if n == 0 or n == 1:
        print(f"{indent}factorial({n}) returns 1")
        return 1

    result = n * factorial_trace(n - 1, depth + 1)
    print(f"{indent}factorial({n}) returns {result}")
    return result

# factorial_trace(5)

# Output:
# factorial(5) called
#   factorial(4) called
#     factorial(3) called
#       factorial(2) called
#         factorial(1) called
#         factorial(1) returns 1
#       factorial(2) returns 2
#     factorial(3) returns 6
#   factorial(4) returns 24
# factorial(5) returns 120

# Goes DOWN (calling) then comes back UP (returning).
# That's the call stack — frames stacking up, then unwinding.
