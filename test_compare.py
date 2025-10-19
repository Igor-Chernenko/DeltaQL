from database import DatabaseConnection
from validator import compare_tables

# Connect to both databases
conn1 = DatabaseConnection("database1.db")
conn2 = DatabaseConnection("database2.db")

# Test comparing the products table (should be 100% match)
result = compare_tables(conn1, conn2, "products", "exact", 0.1)

print("Products table comparison:")
print(f"  Passed: {result['passed']}")
print(f"  Total rows db1: {result['total_rows_db1']}")
print(f"  Total rows db2: {result['total_rows_db2']}")
print(f"  Matching rows: {result['matching_rows']}")
print(f"  Match rate: {result['match_rate']}%")
print()

# Test comparing the users table (has differences)
result2 = compare_tables(conn1, conn2, "users", "exact", 0.1)

print("Users table comparison:")
print(f"  Passed: {result2['passed']}")
print(f"  Total rows db1: {result2['total_rows_db1']}")
print(f"  Total rows db2: {result2['total_rows_db2']}")
print(f"  Matching rows: {result2['matching_rows']}")
print(f"  Match rate: {result2['match_rate']}%")

