# print(True)
# print(False)
# print(type(True))   # <class 'bool'>


a = True
b = True

print(id(a))        # 4345618736
print(id(b))        # 4345618736  — same id!
print(a is b)       # True — same object in heap

c = (10 > 5)        # comparison produces True
print(id(c))        # 4345618736  — still the same object!

# print(True + True)     # 2
# print(False + 1)       # 1
# print(True * 10)       # 10


# print(bool(1))       # True
# print(bool(0))       # False
# print(bool("False")) # True
# print(bool(""))      # False
# print(bool())        # False — no argument defaults to False

result = (10 > 5)
print(result)       # True
print(id(result))   # same id as every other True