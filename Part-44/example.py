class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner            # data
        self._balance = balance        # data

    def deposit(self, amount):        # action
        self._balance += amount

    def withdraw(self, amount):       # action + rule
        if amount > self._balance:
            raise ValueError("Not enough money")
        self._balance -= amount

acc = BankAccount("Alice", 5000)   # __init__ runs here, automatically
acc.deposit(500)
print(acc.owner, acc._balance)        # Alice 5500

acc._balance = -9999                  # no error! the withdraw rule got skipped
print(acc._balance)                   # -9999  ← data is corrupted, nobody stopped it


# ============================================================
# Version 2 — same account, now PROTECTED (information hiding + property)
# ============================================================
# class BankAccount:
#     def __init__(self, owner, balance):
#         self.owner = owner             # public  — safe to read / change
#         self._balance = balance        # hidden  — "_" means "don't touch directly"

#     def deposit(self, amount):         # action
#         self._balance += amount

#     def withdraw(self, amount):        # action + rule
#         if amount > self._balance:
#             raise ValueError("Not enough money")
#         self._balance -= amount

#     @property                          # safe READ  -> acc.balance   (no parentheses)
#     def balance(self):
#         return self._balance

#     @balance.setter                    # guarded WRITE -> the rule CANNOT be skipped
#     def balance(self, value):
#         if value < 0:
#             raise ValueError("Balance cannot be negative")
#         self._balance = value


# acc = BankAccount("Alice", 5000)
# acc.deposit(500)
# print(acc.owner, acc.balance)        # Alice 5500  (balance read through the property)

# acc.balance = 3000                   # allowed — goes through the setter's check
# print(acc.balance)                   # 3000

# # acc.balance = -9999                # ValueError! blocked now (in Version 1 it silently worked)