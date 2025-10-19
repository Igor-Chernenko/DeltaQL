#!/usr/bin/env python3
"""
Script to create sample databases for DataVal demo.
Run this before running the demo program.
"""

import sqlite3
import os

def create_database1():
    """Create database1.db with sample data."""
    # Remove if exists
    if os.path.exists('database1.db'):
        os.remove('database1.db')
    
    conn = sqlite3.connect('database1.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER,
            balance REAL
        )
    ''')
    
    # Insert users data
    users_data = [
        (1, 'Alice Johnson', 'alice@example.com', 28, 1500.50),
        (2, 'Bob Smith', 'bob@example.com', 35, 2300.75),
        (3, 'Charlie Brown', 'charlie@example.com', 42, 890.25),
        (4, 'Diana Prince', 'diana@example.com', 31, 5000.00),
        (5, 'Eve Anderson', 'eve@example.com', 26, 1200.00),
    ]
    cursor.executemany('INSERT INTO users VALUES (?, ?, ?, ?, ?)', users_data)
    
    # Create orders table
    cursor.execute('''
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            product_name TEXT,
            quantity INTEGER,
            total_price REAL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Insert orders data
    orders_data = [
        (101, 1, 'Laptop', 1, 999.99),
        (102, 2, 'Mouse', 2, 25.50),
        (103, 1, 'Keyboard', 1, 75.00),
        (104, 3, 'Monitor', 1, 299.99),
        (105, 4, 'Headphones', 1, 150.00),
    ]
    cursor.executemany('INSERT INTO orders VALUES (?, ?, ?, ?, ?)', orders_data)
    
    # Create products table
    cursor.execute('''
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT,
            price REAL,
            stock INTEGER
        )
    ''')
    
    # Insert products data
    products_data = [
        (1, 'Laptop', 'Electronics', 999.99, 50),
        (2, 'Mouse', 'Accessories', 12.99, 200),
        (3, 'Keyboard', 'Accessories', 75.00, 150),
        (4, 'Monitor', 'Electronics', 299.99, 75),
        (5, 'Headphones', 'Accessories', 150.00, 100),
    ]
    cursor.executemany('INSERT INTO products VALUES (?, ?, ?, ?, ?)', products_data)
    
    conn.commit()
    conn.close()
    print("✓ Created database1.db")


def create_database2():
    """Create database2.db with mostly matching data but some differences."""
    # Remove if exists
    if os.path.exists('database2.db'):
        os.remove('database2.db')
    
    conn = sqlite3.connect('database2.db')
    cursor = conn.cursor()
    
    # Create users table (same schema)
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER,
            balance REAL
        )
    ''')
    
    # Insert users data - DIFFERENCES:
    # - User 2: Different balance (2300.75 -> 2305.50) - within fuzzy tolerance
    # - User 3: Different email (charlie@example.com -> charlie.brown@example.com) - exact will fail
    # - User 5: Missing entirely - both will fail
    users_data = [
        (1, 'Alice Johnson', 'alice@example.com', 28, 1500.50),
        (2, 'Bob Smith', 'bob@example.com', 35, 2305.50),  # DIFFERENCE: balance changed
        (3, 'Charlie Brown', 'charlie.brown@example.com', 42, 890.25),  # DIFFERENCE: email changed
        (4, 'Diana Prince', 'diana@example.com', 31, 5000.00),
        # User 5 missing - DIFFERENCE: missing row
    ]
    cursor.executemany('INSERT INTO users VALUES (?, ?, ?, ?, ?)', users_data)
    
    # Create orders table (same schema)
    cursor.execute('''
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            product_name TEXT,
            quantity INTEGER,
            total_price REAL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Insert orders data - DIFFERENCES:
    # - Order 102: Price changed (25.50 -> 25.55) - within fuzzy tolerance
    # - Order 105: Missing entirely
    # - Order 106: Extra order not in database1
    orders_data = [
        (101, 1, 'Laptop', 1, 999.99),
        (102, 2, 'Mouse', 2, 25.55),  # DIFFERENCE: price changed slightly
        (103, 1, 'Keyboard', 1, 75.00),
        (104, 3, 'Monitor', 1, 299.99),
        # Order 105 missing - DIFFERENCE: missing row
        (106, 2, 'USB Cable', 3, 15.00),  # DIFFERENCE: extra row
    ]
    cursor.executemany('INSERT INTO orders VALUES (?, ?, ?, ?, ?)', orders_data)
    
    # Create products table - IDENTICAL to database1
    cursor.execute('''
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT,
            price REAL,
            stock INTEGER
        )
    ''')
    
    # Insert products data - NO DIFFERENCES (100% match)
    products_data = [
        (1, 'Laptop', 'Electronics', 999.99, 50),
        (2, 'Mouse', 'Accessories', 12.99, 200),
        (3, 'Keyboard', 'Accessories', 75.00, 150),
        (4, 'Monitor', 'Electronics', 299.99, 75),
        (5, 'Headphones', 'Accessories', 150.00, 100),
    ]
    cursor.executemany('INSERT INTO products VALUES (?, ?, ?, ?, ?)', products_data)
    
    conn.commit()
    conn.close()
    print("✓ Created database2.db")


if __name__ == '__main__':
    print("Creating sample databases for DataVal demo...")
    create_database1()
    create_database2()
    print("\n✓ Database creation complete!")
    print("\nDifferences between databases:")
    print("  users table:")
    print("    - User 2: balance differs by 4.75 (within tolerance of 0.1? NO)")
    print("    - User 3: email differs (exact match will fail)")
    print("    - User 5: missing in database2")
    print("  orders table:")
    print("    - Order 102: price differs by 0.05 (within tolerance of 0.1? YES)")
    print("    - Order 105: missing in database2")
    print("    - Order 106: extra in database2")
    print("  products table:")
    print("    - NO DIFFERENCES (100% match)")
    print("\nExpected results:")
    print("  Exact match: 1/3 tables pass (33.33%)")
    print("  Fuzzy match: 1/3 tables pass (33.33%)")

