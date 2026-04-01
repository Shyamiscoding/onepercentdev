# import threading
# print(threading.stack_size())

# ulimit -s

# import resource
# print(resource.getrlimit(resource.RLIMIT_STACK))

x = 10
# print(f"x = {x}")
# print(f"id(x) = {id(x)}")

y = x
print(f"x = {x}")
print(f"y = {y}")
print(f"id(x) = {id(x)}")
print(f"id(y) = {id(y)}")
print(f"Same id? {id(x) == id(y)}")

x = 20
print(f"x = {x}")
print(f"y = {y}")
print(f"id(x) = {id(x)}")
print(f"id(y) = {id(y)}")
print(f"Same id? {id(x) == id(y)}")