import sqlite3
from contextlib import contextmanager

@contextmanager
def transaction(connection):
    """Commit on success, roll back on any error."""
    try:
        yield connection
        connection.commit()          # all statements succeeded -> save them
        print("Transaction committed")
    except Exception:
        connection.rollback()        # something failed -> undo everything
        print("Transaction rolled back")
        raise

# A real (in-memory) database
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE accounts (name TEXT, balance INTEGER)")
conn.execute("INSERT INTO accounts VALUES ('Alice', 100)")
conn.execute("INSERT INTO accounts VALUES ('Bob', 0)")
conn.commit()

def show(msg):
    rows = conn.execute("SELECT name, balance FROM accounts ORDER BY name").fetchall()
    print(msg, dict(rows))

show("Start:      ")

# 1) A transfer that SUCCEEDS -> committed
with transaction(conn):
    conn.execute("UPDATE accounts SET balance = balance - 50 WHERE name='Alice'")
    conn.execute("UPDATE accounts SET balance = balance + 50 WHERE name='Bob'")
show("After OK:   ")

# 2) A transfer that FAILS midway -> rolled back (Alice is NOT charged)
try:
    with transaction(conn):
        conn.execute("UPDATE accounts SET balance = balance - 30 WHERE name='Alice'")
        raise ValueError("network dropped mid-transfer!")   # something breaks
        conn.execute("UPDATE accounts SET balance = balance + 30 WHERE name='Bob'")
except ValueError as e:
    print("Error:", e)
show("After fail: ")