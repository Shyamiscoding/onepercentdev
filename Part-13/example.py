# if "hello":         # bool("hello") → True → runs
#     print("truthy")

# if 0:               # bool(0) → False → skipped
#     print("never")

# if [1, 2, 3]:       # bool([1,2,3]) → True (non-empty) → runs
#     print("has items")

score = 85

if score >= 90:
    print("Grade: A")
elif score >= 80:
    print("Grade: B")
elif score >= 70:
    print("Grade: C")
elif score >= 60:
    print("Grade: D")
else:
    print("Grade: F")