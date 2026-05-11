# def fibonacci(n):
#     if n == 0:                                  # Base case 1
#         return 0
#     if n == 1:                                  # Base case 2
#         return 1
#     return fibonacci(n - 1) + fibonacci(n - 2)  # Recursive case — two calls!

# print(fibonacci(10)) 


# call_count = 0

# def fibonacci(n):
#     global call_count
#     call_count += 1
#     if n == 0:
#         return 0
#     if n == 1:
#         return 1
#     return fibonacci(n - 1) + fibonacci(n - 2)

# fibonacci(30)
# print(f"Calls: {call_count}") 

cache = {}
call_count = 0

def fibonacci(n):
    global call_count
    call_count += 1
    if n in cache:
        return cache[n]
    if n == 0:
        return 0
    if n == 1:
        return 1

    result = fibonacci(n - 1) + fibonacci(n - 2)
    cache[n] = result
    return result

print(fibonacci(50))        # 12586269025 — instant
print(f"Calls: {call_count}")  # Calls: 99

call_count = 0
print(fibonacci(100))       # 354224848179261915075 — still instant
print(f"Calls: {call_count}")  # Calls: 99 (51 to 100, rest from cache)