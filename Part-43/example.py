class BankAccount:
    bank_name = "OnePercent Bank"     # class data — shared by EVERY account
    interest_rate = 5                  # class data — shared by EVERY account
    count = 0                          # class data — how many exist so far

    def __init__(self, owner, balance):
        self.owner = owner             # instance data — one per account
        self.balance = balance
        BankAccount.count += 1         # each new account bumps the shared counter

    # ── INSTANCE · needs THIS account (self) ──
    def deposit(self, amount):
        self.balance += amount         # change ONE account's own data

    # ── CLASS · needs the class (cls), not one account ──
    @classmethod
    def savings(cls, owner):           # reason 1: another DOOR to create one
        return cls(owner, 0)               # cls(...) == BankAccount(...) → new object

    @classmethod
    def from_record(cls, line):        # reason 1: yet another door — "Alice,5000"
        owner, balance = line.split(",")
        return cls(owner, int(balance))

    @classmethod
    def set_interest_rate(cls, rate):  # reason 2: a setting shared by ALL accounts
        cls.interest_rate = rate

    @classmethod
    def total_accounts(cls):           # reason 3: a fact about the WHOLE class
        return cls.count

    # ── STATIC · needs neither self nor cls ──
    @staticmethod
    def is_valid_amount(amount):        # just numbers in → answer out
        return amount > 0


# ① create FIRST …
alice = BankAccount.savings("Alice")   # classmethod opens a fresh account
# ② … THEN use
alice.deposit(500)                       # instance method needs an existing account
print(alice.balance)                    # 500

BankAccount.set_interest_rate(7)         # affects EVERY account at once
print(BankAccount.total_accounts())    # 1 — a fact about the class
BankAccount.is_valid_amount(500)          # True — no account needed