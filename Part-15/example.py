# user_input = input("Command: ")

# while user_input != "quit":
#     print(f"Processing: {user_input}")
#     user_input = input("Command: ")

# while True:
#     print("Running...")


# while True:
#     command = input("Enter command (quit to exit): ").strip().lower()
#     if command == "quit":
#         print("Goodbye!")
#         break
#     print(f"You entered: {command}")

# while True:
#     user_input = input("Enter a number (or 'done' to finish): ").strip()
    
#     if user_input.lower() == "done":
#         break
    
#     if not user_input.isdigit():
#         print("Please enter a valid number.")
#         continue
    
#     number = int(user_input)
#     print(f"You entered: {number}")

# print("Program finished.")


# total = 0
# count = 0

# while True:
#     value = input("Enter a number (or 'done'): ").strip()
#     if value.lower() == "done":
#         break
#     if not value.isdigit():
#         print("Invalid number, skipping.")
#         continue
    
#     total += int(value)
#     count += 1

# if count > 0:
#     print(f"Sum: {total}")
#     print(f"Count: {count}")
#     print(f"Average: {total / count:.2f}")
# else:
#     print("No numbers entered.")


target = 7
guess = 0

while guess < 5:
    attempt = int(input("Guess a number: "))
    guess += 1
    if attempt == target:
        print("Correct!")
        break
else:
    print("Out of attempts. The number was 7.")