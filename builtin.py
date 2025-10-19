"""
Built-in functions for DeltaQL language.
Includes utility functions and database operations.
"""

from database import DatabaseConnection
from validator import compare_tables
from datetime import datetime


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
        Dictionary with comparison results
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


def builtin_generate_html_report(results, mode, conn1, conn2):
    """
    Generate an HTML report from comparison results.
    File is overwritten if it already exists.
    
    Args:
        results: List of comparison result dictionaries
        mode: Comparison mode ("exact" or "fuzzy")
        conn1: First DatabaseConnection object
        conn2: Second DatabaseConnection object
        
    Returns:
        Filename of generated report
    """
    if not isinstance(conn1, DatabaseConnection):
        raise TypeError("generate_html_report() expects DatabaseConnection for conn1")
    if not isinstance(conn2, DatabaseConnection):
        raise TypeError("generate_html_report() expects DatabaseConnection for conn2")
    
    # Generate filename
    filename = f"{conn1.db_name}_vs_{conn2.db_name}_{mode}_report.html"
    
    # Calculate summary statistics
    total_tables = len(results)
    passed_tables = sum(1 for r in results if r["passed"])
    failed_tables = total_tables - passed_tables
    pass_rate = (passed_tables / total_tables * 100) if total_tables > 0 else 0
    
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Build HTML content
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Database Validation Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f7fa;
            padding: 20px;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .header {{
            background: white;
            color: #333;
            padding: 40px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            color: #333;
        }}
        
        .header h2 {{
            font-size: 1.5em;
            font-weight: normal;
            color: #666;
        }}
        
        .header p {{
            margin-top: 10px;
            color: #666;
        }}
        
        .summary {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-bottom: 30px;
        }}
        
        .summary h2 {{
            margin-bottom: 20px;
            color: #333;
        }}
        
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .summary-card {{
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        
        .summary-card.total {{
            background: #e3f2fd;
            border-left: 4px solid #2196f3;
        }}
        
        .summary-card.passed {{
            background: #e8f5e9;
            border-left: 4px solid #4caf50;
        }}
        
        .summary-card.failed {{
            background: #ffebee;
            border-left: 4px solid #f44336;
        }}
        
        .summary-card h3 {{
            font-size: 2em;
            margin-bottom: 5px;
        }}
        
        .summary-card p {{
            color: #666;
            font-size: 0.9em;
        }}
        
        .section {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-bottom: 30px;
        }}
        
        .section h2 {{
            margin-bottom: 20px;
            color: #333;
            border-bottom: 2px solid #333;
            padding-bottom: 10px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        
        thead {{
            background: #f8f9fa;
        }}
        
        th {{
            padding: 12px;
            text-align: left;
            font-weight: 600;
            color: #333;
            border-bottom: 2px solid #dee2e6;
        }}
        
        td {{
            padding: 12px;
            border-bottom: 1px solid #dee2e6;
        }}
        
        tr:hover {{
            background: #f8f9fa;
        }}
        
        .status-icon {{
            font-size: 1.3em;
            margin-right: 8px;
        }}
        
        .passed-row {{
            color: #28a745;
        }}
        
        .failed-row {{
            color: #dc3545;
        }}
        
        .table-detail {{
            margin-bottom: 40px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #dc3545;
        }}
        
        .table-detail h3 {{
            color: #dc3545;
            margin-bottom: 15px;
        }}
        
        .table-name-label {{
            color: #666;
            font-weight: normal;
            font-size: 0.9em;
        }}
        
        .table-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin: 15px 0;
        }}
        
        .stat-item {{
            background: white;
            padding: 10px;
            border-radius: 5px;
        }}
        
        .stat-label {{
            color: #666;
            font-size: 0.85em;
            margin-bottom: 5px;
        }}
        
        .stat-value {{
            font-size: 1.2em;
            font-weight: bold;
            color: #333;
        }}
        
        .diff-table {{
            margin-top: 20px;
            background: white;
        }}
        
        .diff-type {{
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.85em;
            font-weight: bold;
        }}
        
        .diff-type.missing {{
            background: #ffebee;
            color: #c62828;
        }}
        
        .diff-type.extra {{
            background: #fff3e0;
            color: #e65100;
        }}
        
        .diff-type.value {{
            background: #fce4ec;
            color: #880e4f;
        }}
        
        .diff-highlight {{
            background: #fff9c4;
            padding: 2px 6px;
            border-radius: 3px;
            font-weight: bold;
        }}
        
        .no-differences {{
            text-align: center;
            padding: 40px;
            color: #28a745;
            font-size: 1.2em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Database Validation Report</h1>
            <h2>{conn1.db_name} vs {conn2.db_name}</h2>
            <p>Comparison Mode: <strong>{mode.upper()}</strong> | Generated: {timestamp}</p>
        </div>
        
        <div class="summary">
            <h2>Summary</h2>
            <div class="summary-grid">
                <div class="summary-card total">
                    <h3>{total_tables}</h3>
                    <p>Total Tables</p>
                </div>
                <div class="summary-card passed">
                    <h3>{passed_tables}</h3>
                    <p>Tables Passed</p>
                </div>
                <div class="summary-card failed">
                    <h3>{failed_tables}</h3>
                    <p>Tables Failed</p>
                </div>
            </div>
            <div style="text-align: center; margin-top: 30px; font-size: 1.5em;">
                <strong>Overall Pass Rate: {pass_rate:.2f}%</strong>
            </div>
        </div>
        
        <div class="section">
            <h2>Tables Tested</h2>
            <table>
                <thead>
                    <tr>
                        <th>Table Name</th>
                        <th>Status</th>
                        <th>Match Rate</th>
                        <th>Rows (DB1 / DB2)</th>
                    </tr>
                </thead>
                <tbody>
"""
    
    # Add table rows
    for result in results:
        status_class = "passed-row" if result["passed"] else "failed-row"
        status_icon = "✓" if result["passed"] else "✗"
        status_text = "PASSED" if result["passed"] else "FAILED"
        
        html += f"""                    <tr>
                        <td><span class="status-icon {status_class}">{status_icon}</span>{result["table_name"]}</td>
                        <td class="{status_class}"><strong>{status_text}</strong></td>
                        <td>{result["match_rate"]:.1f}%</td>
                        <td>{result["total_rows_db1"]} / {result["total_rows_db2"]}</td>
                    </tr>
"""
    
    html += """                </tbody>
            </table>
        </div>
        
        <div class="section">
            <h2>Failed Table Details</h2>
"""
    
    # Add failed table details
    failed_results = [r for r in results if not r["passed"]]
    
    if not failed_results:
        html += """            <div class="no-differences">
                <h3>🎉 All tables passed validation!</h3>
                <p>No differences found between the databases.</p>
            </div>
"""
    else:
        for result in failed_results:
            html += f"""            <div class="table-detail">
                <h3><span class="table-name-label">Table Name:</span> {result["table_name"]}</h3>
                <div class="table-stats">
                    <div class="stat-item">
                        <div class="stat-label">Rows in {conn1.db_name}</div>
                        <div class="stat-value">{result["total_rows_db1"]}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Rows in {conn2.db_name}</div>
                        <div class="stat-value">{result["total_rows_db2"]}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Matching Rows</div>
                        <div class="stat-value">{result["matching_rows"]}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Match Rate</div>
                        <div class="stat-value">{result["match_rate"]:.1f}%</div>
                    </div>
                </div>
                
                <h4>Row Differences:</h4>
                <table class="diff-table">
                    <thead>
                        <tr>
                            <th>Row ID</th>
                            <th>Issue Type</th>
                            <th>Details</th>
                        </tr>
                    </thead>
                    <tbody>
"""
            
            # Add difference details
            for diff in result["differences"]:
                if diff["type"] == "missing_in_db2":
                    html += f"""                        <tr>
                            <td><strong>{diff["key"]}</strong></td>
                            <td><span class="diff-type missing">MISSING IN DB2</span></td>
                            <td>Row exists in {conn1.db_name} but not in {conn2.db_name}</td>
                        </tr>
"""
                elif diff["type"] == "extra_in_db2":
                    html += f"""                        <tr>
                            <td><strong>{diff["key"]}</strong></td>
                            <td><span class="diff-type extra">EXTRA IN DB2</span></td>
                            <td>Row exists in {conn2.db_name} but not in {conn1.db_name}</td>
                        </tr>
"""
                elif diff["type"] == "value_diff":
                    for col_diff in diff["column_diffs"]:
                        html += f"""                        <tr>
                            <td><strong>{diff["key"]}</strong></td>
                            <td><span class="diff-type value">VALUE DIFFERS</span></td>
                            <td>
                                <strong>{col_diff["column"]}:</strong> 
                                {col_diff["value_db1"]} 
                                → 
                                <span class="diff-highlight">{col_diff["value_db2"]}</span>
                            </td>
                        </tr>
"""
            
            html += """                    </tbody>
                </table>
            </div>
"""
    
    html += """        </div>
    </div>
</body>
</html>
"""
    
    # Write HTML to file (using 'w' mode to overwrite existing file)
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        
        # Also print summary to console
        print(f"\n{'='*60}")
        print(f"HTML Report Generated: {filename}")
        print(f"{'='*60}")
        print(f"Database: {conn1.db_name} vs {conn2.db_name}")
        print(f"Mode: {mode.upper()}")
        print(f"Total Tables: {total_tables}")
        print(f"Passed: {passed_tables} ✓")
        print(f"Failed: {failed_tables} ✗")
        print(f"Pass Rate: {pass_rate:.2f}%")
        print(f"{'='*60}\n")
        
        return filename
    except Exception as e:
        raise RuntimeError(f"Failed to write HTML report: {e}")


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
        'generate_html_report': builtin_generate_html_report,
    }

