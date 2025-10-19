# DeltaQL# DataVal Language

A domain-specific language (DSL) for database validation and comparison.

## Overview

DataVal is a simple, intuitive programming language designed specifically for validating and comparing SQL databases. It provides built-in functions for connecting to databases, comparing tables, and generating validation reports.

## Features

- **Variables**: Store database paths, configuration values, and results
- **Functions**: Define reusable validation logic with parameters
- **Loops**: Iterate over lists of tables or validation results
- **Conditionals**: Make decisions based on validation outcomes
- **Built-in Database Operations**: Connect, query, and compare databases
- **Exact and Fuzzy Matching**: Support for strict and tolerance-based comparisons

## Installation

### Requirements

- Python 3.8 or higher
- Lark parser library

### Setup

1. Install dependencies:
```bash
pip install lark
```

2. Clone or download this repository

## Usage

Run a DataVal program:
```bash
python dataval.py <program.dv>
```

Example:
```bash
python dataval.py demo/demo.dv
```

## Language Syntax

### Variable Declaration
```
var database_path = "mydb.db"
var tolerance = 0.1
var tables = ["users", "orders"]
```

### Function Definition
```
function compare_databases(db1, db2, mode) {
    var conn1 = connect(db1)
    var conn2 = connect(db2)
    
    // Function body
    
    return result
}
```

### Control Flow

**If Statement:**
```
if condition {
    // then block
} else {
    // else block
}
```

**For Loop:**
```
for item in list {
    // loop body
}
```

### Built-in Functions

#### Utility Functions
- `print(value)` - Output to console
- `len(list)` - Get length of list
- `str(value)` - Convert to string
- `int(value)` - Convert to integer
- `float(value)` - Convert to float

#### Database Functions
- `connect(db_path)` - Connect to SQLite database
- `get_tables(connection)` - Get list of table names
- `table_exists(connection, table_name)` - Check if table exists
- `compare_table(conn1, conn2, table_name, mode, tolerance)` - Compare table between databases

### Comparison Modes

**Exact Mode**: Tables must match exactly (all rows and columns identical)

**Fuzzy Mode**: Numeric values can differ within tolerance threshold

### Result Object

The `compare_table()` function returns a dictionary with:

- `"table_name"` - Name of compared table
- `"passed"` - Boolean, true if tables match
- `"total_rows_db1"` - Row count in first database
- `"total_rows_db2"` - Row count in second database
- `"matching_rows"` - Number of matching rows
- `"match_rate"` - Percentage of rows that match (0-100)

## Example Program

See `demo/demo.dv` for a complete working example that demonstrates all language features.

## Database Requirements

DataVal works with SQLite databases. Your databases should:

- Have tables with primary keys (or at least one column to use as key)
- Use compatible schemas in both databases being compared
- Be accessible file paths

## Project Structure
```
dataval-language/
├── dataval.py          # Main interpreter entry point
├── grammar.lark        # Language grammar definition
├── ast_nodes.py        # AST node classes
├── interpreter.py      # Core interpreter logic
├── environment.py      # Variable scoping
├── builtins.py         # Built-in functions
├── database.py         # Database operations
├── validator.py        # Comparison logic
└── demo/
    └── demo.dv         # Demo program
```

## Error Handling

DataVal provides error messages for:

- Syntax errors (parser errors)
- Undefined variables or functions
- Type errors (e.g., calling non-functions)
- Database connection errors
- Table not found errors

## License

This project was created for the University of Victoria Engineering Competition 2025.

