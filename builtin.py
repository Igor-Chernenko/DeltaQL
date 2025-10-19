"""
Built-in functions for DataVal language.
Includes utility functions and database operations.
"""

from database import DatabaseConnection
from validator import compare_tables


def builtin_print(*args):
    """Print values to console."""
    output = " ".join(str(arg) for arg in args)
    print(output)


def builtin_len(value):
    """Return length of a list or string."""
    if not isinstance(value, (list, str)):
        raise TypeError(f"len() expects list or string, got {type(value).__name__}")
    return len(value)


def builtin_str(value):
    """Convert value to string."""
    return str(value)


def builtin_int(value):
    """Convert value to integer."""
    try:
        return int(value)
    except (ValueError, TypeError) as e:
        raise TypeError(f"Cannot convert {value} to int: {e}")


def builtin_float(value):
    """Convert value to float."""
    try:
        return float(value)
    except (ValueError, TypeError) as e:
        raise TypeError(f"Cannot convert {value} to float: {e}")


def builtin_connect(db_path):
    """
    Connect to a SQLite database.
    
    Args:
        db_path: Path to database file
        
    Returns:
        DatabaseConnection object
    """
    try:
        return DatabaseConnection(db_path)
    except Exception as e:
        raise RuntimeError(f"Failed to connect to database '{db_path}': {e}")


def builtin_get_tables(connection):
    """
    Get list of table names in a database.
    
    Args:
        connection: DatabaseConnection object
        
    Returns:
        List of table names
    """
    if not isinstance(connection, DatabaseConnection):
        raise TypeError("get_tables() expects DatabaseConnection object")
    
    try:
        return connection.get_tables()
    except Exception as e:
        raise RuntimeError(f"Failed to get tables: {e}")


def builtin_table_exists(connection, table_name):
    """
    Check if a table exists in the database.
    
    Args:
        connection: DatabaseConnection object
        table_name: Name of table to check
        
    Returns:
        Boolean indicating if table exists
    """
    if not isinstance(connection, DatabaseConnection):
        raise TypeError("table_exists() expects DatabaseConnection object")
    
    try:
        return connection.table_exists(table_name)
    except Exception as e:
        raise RuntimeError(f"Failed to check table existence: {e}")


def builtin_compare_table(conn1, conn2, table_name, mode, tolerance):
    """
    Compare a table between two databases.
    
    Args:
        conn1: First DatabaseConnection object
        conn2: Second DatabaseConnection object
        table_name: Name of table to compare
        mode: Comparison mode ("exact" or "fuzzy")
        tolerance: Tolerance for fuzzy numeric comparisons
        
    Returns:
        Dictionary with comparison results:
        {
            "table_name": str,
            "passed": bool,
            "total_rows_db1": int,
            "total_rows_db2": int,
            "matching_rows": int,
            "match_rate": float (0-100)
        }
    """
    if not isinstance(conn1, DatabaseConnection):
        raise TypeError("compare_table() expects DatabaseConnection for first argument")
    if not isinstance(conn2, DatabaseConnection):
        raise TypeError("compare_table() expects DatabaseConnection for second argument")
    if mode not in ["exact", "fuzzy"]:
        raise ValueError(f"Invalid comparison mode: '{mode}'. Must be 'exact' or 'fuzzy'")
    
    try:
        return compare_tables(conn1, conn2, table_name, mode, tolerance)
    except Exception as e:
        raise RuntimeError(f"Failed to compare table '{table_name}': {e}")


def get_builtins():
    """
    Return dictionary of all built-in functions.
    
    Returns:
        Dictionary mapping function names to function objects
    """
    return {
        'print': builtin_print,
        'len': builtin_len,
        'str': builtin_str,
        'int': builtin_int,
        'float': builtin_float,
        'connect': builtin_connect,
        'get_tables': builtin_get_tables,
        'table_exists': builtin_table_exists,
        'compare_table': builtin_compare_table,
    }

