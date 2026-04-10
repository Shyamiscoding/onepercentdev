# while True:
#     line = input("Type something (or 'quit' to exit): ")
#     if line == "quit":
#         break
#     print(f"You typed: {line}")


# for _ in iter(int, 1):
#     line = input("Type something (or 'quit' to exit): ")
#     if line == "quit":
#         break
#     print(f"You typed: {line}")

# for i in range(2, 7):
#     print(i)
# print("--------------------------------")
# for i in range(0, 10):
#     print(i)

# text = "Python"
# for i in range(len(text)):
#     print(i, text[i])


# for i in range(10):
#     if i == 5:
#         print("Found 5, stopping")
#         break
#     print(i)

# for i in range(10):
#     if i % 3 == 0:
#         continue
#     print(i)

# target = "P"
# text = "Python"

# for char in text:
#     if char == target:
#         print(f"Found '{target}'!")
#         break
# else:
#     print(f"'{target}' not found in '{text}'")

for i in range(1, 4):
    for j in range(1, 4):
        print(f"{i} x {j} = {i * j}")
    print("--------------------------------")