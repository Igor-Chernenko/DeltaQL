"""
Validation and comparison logic for DeltaQL language.
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
        Dictionary with comparison results including detailed differences
    """
    # Create dictionaries keyed by primary key
    dict1 = {row[primary_key]: row for row in rows1}
    dict2 = {row[primary_key]: row for row in rows2}
    
    # Get all keys
    all_keys = set(dict1.keys()) | set(dict2.keys())
    
    matching_rows = 0
    differences = []
    
    for key in all_keys:
        # Check if key exists in both
        if key not in dict1:
            differences.append({
                'type': 'extra_in_db2',
                'key': key,
                'row': dict2[key]
            })
            continue
        elif key not in dict2:
            differences.append({
                'type': 'missing_in_db2',
                'key': key,
                'row': dict1[key]
            })
            continue
        
        # Compare rows
        row1 = dict1[key]
        row2 = dict2[key]
        
        # Check if rows match exactly
        if row1 == row2:
            matching_rows += 1
        else:
            # Find specific column differences
            row_diffs = []
            for col in row1.keys():
                if row1[col] != row2[col]:
                    row_diffs.append({
                        'column': col,
                        'value_db1': row1[col],
                        'value_db2': row2[col]
                    })
            
            differences.append({
                'type': 'value_diff',
                'key': key,
                'column_diffs': row_diffs
            })
    
    # Calculate match rate
    total_rows_db1 = len(rows1)
    total_rows_db2 = len(rows2)
    
    # Use the number of keys that exist in both databases
    common_keys = set(dict1.keys()) & set(dict2.keys())
    total_comparable = len(common_keys)
    
    if total_comparable == 0:
        match_rate = 0.0
        passed = False
    else:
        match_rate = (matching_rows / total_comparable) * 100
        # Table passes if all comparable rows match AND row counts are the same
        passed = (matching_rows == total_comparable) and (total_rows_db1 == total_rows_db2)
    
    return {
        "passed": passed,
        "total_rows_db1": total_rows_db1,
        "total_rows_db2": total_rows_db2,
        "matching_rows": matching_rows,
        "match_rate": match_rate,
        "differences": differences
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
        Dictionary with comparison results including detailed differences
    """
    # Create dictionaries keyed by primary key
    dict1 = {row[primary_key]: row for row in rows1}
    dict2 = {row[primary_key]: row for row in rows2}
    
    # Get all keys
    all_keys = set(dict1.keys()) | set(dict2.keys())
    
    matching_rows = 0
    differences = []
    
    for key in all_keys:
        # Check if key exists in both
        if key not in dict1:
            differences.append({
                'type': 'extra_in_db2',
                'key': key,
                'row': dict2[key]
            })
            continue
        elif key not in dict2:
            differences.append({
                'type': 'missing_in_db2',
                'key': key,
                'row': dict1[key]
            })
            continue
        
        # Compare rows with fuzzy logic
        row1 = dict1[key]
        row2 = dict2[key]
        
        matches, row_diffs = fuzzy_rows_match_with_details(row1, row2, tolerance)
        
        if matches:
            matching_rows += 1
        else:
            differences.append({
                'type': 'value_diff',
                'key': key,
                'column_diffs': row_diffs
            })
    
    # Calculate match rate
    total_rows_db1 = len(rows1)
    total_rows_db2 = len(rows2)
    
    # Use the number of keys that exist in both databases
    common_keys = set(dict1.keys()) & set(dict2.keys())
    total_comparable = len(common_keys)
    
    if total_comparable == 0:
        match_rate = 0.0
        passed = False
    else:
        match_rate = (matching_rows / total_comparable) * 100
        # Table passes if all comparable rows match AND row counts are the same
        passed = (matching_rows == total_comparable) and (total_rows_db1 == total_rows_db2)
    
    return {
        "passed": passed,
        "total_rows_db1": total_rows_db1,
        "total_rows_db2": total_rows_db2,
        "matching_rows": matching_rows,
        "match_rate": match_rate,
        "differences": differences
    }


def fuzzy_rows_match_with_details(row1, row2, tolerance):
    """
    Check if two rows match with fuzzy comparison and return details.
    
    Args:
        row1: First row dictionary
        row2: Second row dictionary
        tolerance: Numeric tolerance
        
    Returns:
        Tuple of (matches: bool, differences: list)
    """
    # Check if they have the same columns
    if set(row1.keys()) != set(row2.keys()):
        return False, []
    
    differences = []
    
    # Compare each column
    for col in row1.keys():
        val1 = row1[col]
        val2 = row2[col]
        
        # Handle None/NULL values
        if val1 is None and val2 is None:
            continue
        elif val1 is None or val2 is None:
            differences.append({
                'column': col,
                'value_db1': val1,
                'value_db2': val2
            })
            continue
        
        # Numeric comparison with tolerance
        if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
            if abs(val1 - val2) > tolerance:
                differences.append({
                    'column': col,
                    'value_db1': val1,
                    'value_db2': val2
                })
        # Exact comparison for other types
        else:
            if val1 != val2:
                differences.append({
                    'column': col,
                    'value_db1': val1,
                    'value_db2': val2
                })
    
    return len(differences) == 0, differences

