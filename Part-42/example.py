class Waiter:                      # the ROLE (class) — defines data + actions
    def __init__(self, name):
        self.name = name           # each waiter's own data
    def take_order(self, dish):    # what every waiter can DO
        print(f"{self.name} is taking order: {dish}")

ravi = Waiter("Ravi")              # an OBJECT — a real waiter hired into the role
anil = Waiter("Anil")              # another object, same role, own data
anil.take_order("Dosa")            # Ravi is taking order: Dosa