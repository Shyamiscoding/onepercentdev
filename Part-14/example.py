# age = 20

# # # Standard if-else:
# # if age >= 18:
# #     status = "adult"
# # else:
# #     status = "minor"

# status = "adult" if age >= 18 else "minor"

# print(status)


# command = input("Enter command: ")

# match command:
#     case "start":
#         print("Starting...")
#     case "stop":
#         print("Stopping...")
#     case "restart":
#         print("Restarting...")
#     case _:
#         print(f"Unknown command: {command}")

age = 25

match age:
    case n if n < 0:
        print("Invalid age")
    case n if n < 18:
        print(f"Minor, age {n}")
    case n if n < 65:
        print(f"Adult, age {n}")
    case n:
        print(f"Senior, age {n}")