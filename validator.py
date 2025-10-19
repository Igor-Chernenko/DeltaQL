"""
Validation and comparison logic for DataVal language.
Implements exact and fuzzy matching for database tables.
"""


def compare_tables(conn1, conn2, table_name, mode, tolerance):
    """
    Compare a table between two databases.
    
    Args:
        conn1: First DatabaseConnection
        conn2: Second DatabaseConnection
        table_name: Name of table to compare
        mode: "exact" or "fuzzy"
        tolerance: Numeric tolerance for fuzzy comparisons
        
    Returns:
        Dictionary with comparison results
    """
    # Get primary key
    pk1 = conn1.get_primary_key(table_name)
    pk2 = conn2.get_primary_key(table_name)
    
    if pk1 != pk2:
        raise ValueError(f"Primary keys differ: '{pk1}' vs '{pk2}'")
    
    primary_key = pk1
    
    # Fetch all data
    rows1 = conn1.get_table_data(table_name)
    rows2 = conn2.get_table_data(table_name)
    
    # Perform comparison based on mode
    if mode == "exact":
        result = exact_match_comparison(rows1, rows2, primary_key)
    elif mode == "fuzzy":
        result = fuzzy_match_comparison(rows1, rows2, primary_key, tolerance)
    else:
        raise ValueError(f"Invalid mode: {mode}")
    
    # Add table name to result
    result["table_name"] = table_name
    
    return result


def exact_match_comparison(rows1, rows2, primary_key):
    """
    Perform exact match comparison between two datasets.
    
    Args:
        rows1: List of row dictionaries from first database
        rows2: List of row dictionaries from second database
        primary_key: Name of primary key column
        
    Returns:
        Dictionary with comparison results
    """
    # Create dictionaries keyed by primary key
    dict1 = {row[primary_key]: row for row in rows1}
    dict2 = {row[primary_key]: row for row in rows2}
    
    # Get all keys
    all_keys = set(dict1.keys()) | set(dict2.keys())
    
    matching_rows = 0
    total_differences = 0
    
    for key in all_keys:
        # Check if key exists in both
        if key not in dict1 or key not in dict2:
            total_differences += 1
            continue
        
        # Compare rows
        row1 = dict1[key]
        row2 = dict2[key]
        
        # Check if rows match exactly
        if row1 == row2:
            matching_rows += 1
        else:
            total_differences += 1
    
    # Calculate match rate
    total_rows_db1 = len(rows1)
    total_rows_db2 = len(rows2)
    max_rows = max(total_rows_db1, total_rows_db2)
    
    if max_rows == 0:
        match_rate = 100.0
    else:
        match_rate = (matching_rows / max_rows) * 100
    
    # Determine if validation passed (100% match)
    passed = (match_rate == 100.0)
    
    return {
        "passed": passed,
        "total_rows_db1": total_rows_db1,
        "total_rows_db2": total_rows_db2,
        "matching_rows": matching_rows,
        "match_rate": match_rate
    }


def fuzzy_match_comparison(rows1, rows2, primary_key, tolerance):
    """
    Perform fuzzy match comparison with numeric tolerance.
    
    Args:
        rows1: List of row dictionaries from first database
        rows2: List of row dictionaries from second database
        primary_key: Name of primary key column
        tolerance: Numeric tolerance for comparisons
        
    Returns:
        Dictionary with comparison results
    """
    # Create dictionaries keyed by primary key
    dict1 = {row[primary_key]: row for row in rows1}
    dict2 = {row[primary_key]: row for row in rows2}
    
    # Get all keys
    all_keys = set(dict1.keys()) | set(dict2.keys())
    
    matching_rows = 0
    total_differences = 0
    
    for key in all_keys:
        # Check if key exists in both
        if key not in dict1 or key not in dict2:
            total_differences += 1
            continue
        
        # Compare rows with fuzzy logic
        row1 = dict1[key]
        row2 = dict2[key]
        
        if fuzzy_rows_match(row1, row2, tolerance):
            matching_rows += 1
        else:
            total_differences += 1
    
    # Calculate match rate
    total_rows_db1 = len(rows1)
    total_rows_db2 = len(rows2)
    max_rows = max(total_rows_db1, total_rows_db2)
    
    if max_rows == 0:
        match_rate = 100.0
    else:
        match_rate = (matching_rows / max_rows) * 100
    
    # Determine if validation passed (100% match with tolerance)
    passed = (match_rate == 100.0)
    
    return {
        "passed": passed,
        "total_rows_db1": total_rows_db1,
        "total_rows_db2": total_rows_db2,
        "matching_rows": matching_rows,
        "match_rate": match_rate
    }


def fuzzy_rows_match(row1, row2, tolerance):
    """
    Check if two rows match with fuzzy comparison.
    
    Args:
        row1: First row dictionary
        row2: Second row dictionary
        tolerance: Numeric tolerance
        
    Returns:
        Boolean indicating if rows match within tolerance
    """
    # Check if they have the same columns
    if set(row1.keys()) != set(row2.keys()):
        return False
    
    # Compare each column
    for col in row1.keys():
        val1 = row1[col]
        val2 = row2[col]
        
        # Handle None/NULL values
        if val1 is None and val2 is None:
            continue
        elif val1 is None or val2 is None:
            return False
        
        # Numeric comparison with tolerance
        if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
            if abs(val1 - val2) > tolerance:
                return False
        # Exact comparison for other types
        else:
            if val1 != val2:
                return False
    
    return True
### **9. demo/demo.dv** (Demo Program)
"""
// DataVal Demo Program
// Demonstrates all language features through database validation

// Variables: Store database paths and configuration

var db1_path = "database1.db"
var db2_path = "database2.db"
var tolerance = 0.1
var tables = ["users", "orders", "products"]

// Function: Compare two databases and return match percentage
function compare_databases(db_name_a, db_name_b, match_type) {
    // Open connections to both databases
    var conn1 = connect(db_name_a)
    var conn2 = connect(db_name_b)
    
    // Initialize counters
    var passed_count = 0
    var total_count = len(tables)
    
    // Loop: Iterate through all tables
    for table in tables {
        // Conditional: Check if table exists in both databases
        if table_exists(conn1, table) and table_exists(conn2, table) {
            // Call built-in compare_table function
            var result = compare_table(conn1, conn2, table, match_type, tolerance)
            
            // Conditional: Check if this table passed validation
            if result["passed"] {
                passed_count = passed_count + 1
            }
        }
    }
    
    // Calculate match percentage
    var percentage = (passed_count / total_count) * 100
    
    // Return the result
    return percentage
}

// Call function with exact matching mode
var exact_match_percentage = compare_databases(db1_path, db2_path, "exact")
print(exact_match_percentage)

// Call function with fuzzy matching mode
var fuzzy_match_percentage = compare_databases(db1_path, db2_path, "fuzzy")
print(fuzzy_match_percentage)

"""
