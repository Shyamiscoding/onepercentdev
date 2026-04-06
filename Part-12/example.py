# age = 25
# has_id = True

# print(age >= 18 and has_id)   # True
# print(age >= 18 and not has_id)  # Would be False if has_id was False

print("hello" and "world")   # "world"  — NOT True
print("" and "world")        # ""       — NOT False
print("hello" or "world")    # "hello"  — NOT True
print("" or "world")         # "world"  — NOT True
print(0 or 42)               # 42       — NOT True
print(None or "default")     # "default"