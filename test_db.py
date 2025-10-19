import sqlite3

# Test database1
conn1 = sqlite3.connect('database1.db')
cursor1 = conn1.cursor()
cursor1.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables1 = cursor1.fetchall()
print("Tables in database1:", tables1)

cursor1.execute("SELECT COUNT(*) FROM users")
print("Users count in db1:", cursor1.fetchone()[0])

# Test database2
conn2 = sqlite3.connect('database2.db')
cursor2 = conn2.cursor()
cursor2.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables2 = cursor2.fetchall()
print("Tables in database2:", tables2)

cursor2.execute("SELECT COUNT(*) FROM users")
print("Users count in db2:", cursor2.fetchone()[0])

conn1.close()
conn2.close()

