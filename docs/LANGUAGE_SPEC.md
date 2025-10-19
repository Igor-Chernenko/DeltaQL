# DataVal Language Specification

## Grammar

### Tokens

**Keywords**: `var`, `function`, `for`, `in`, `if`, `else`, `return`, `true`, `false`, `and`, `or`, `not`

**Literals**:
- Numbers: `123`, `45.67`
- Strings: `"hello"`, `'world'`
- Booleans: `true`, `false`
- Lists: `[1, 2, 3]`, `["a", "b"]`

**Operators**:
- Arithmetic: `+`, `-`, `*`, `/`
- Comparison: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Logical: `and`, `or`, `not`

**Identifiers**: `[a-zA-Z_][a-zA-Z0-9_]*`

### Statements

**Variable Declaration**:
```
var <identifier> = <expression>
```

**Assignment**:
```
<identifier> = <expression>
```

**Function Definition**:
```
function <identifier>(<parameters>) {
    <statements>
}
```

**If Statement**:
```
if <expression> {
    <statements>
} else {
    <statements>
}
```

**For Loop**:
```
for <identifier> in <expression> {
    <statements>
}
```

**Return Statement**:
```
return <expression>
```

### Expressions

**Binary Operations**:
```
<expression> <operator> <expression>
```

**Unary Operations**:
```
<operator> <expression>
```

**Function Call**:
```
<identifier>(<arguments>)
```

**List Literal**:
```
[<expression>, <expression>, ...]
```

### Operator Precedence

From highest to lowest:

1. Unary operators: `not`, `-`
2. Multiplication and division: `*`, `/`
3. Addition and subtraction: `+`, `-`
4. Comparison: `<`, `>`, `<=`, `>=`, `==`, `!=`
5. Logical AND: `and`
6. Logical OR: `or`

### Comments

Single-line comments start with `//`:
```
// This is a comment
var x = 5  // This is also a comment
```

## Data Types

### Primitive Types

- **Number**: Integer or floating-point (e.g., `42`, `3.14`)
- **String**: Text in quotes (e.g., `"hello"`, `'world'`)
- **Boolean**: `true` or `false`

### Composite Types

- **List**: Ordered collection (e.g., `[1, 2, 3]`)
- **Dictionary**: Result objects from built-in functions (accessed with `dict["key"]`)

### Special Types

- **DatabaseConnection**: Returned by `connect()` function
- **Function**: User-defined or built-in functions

## Scoping Rules

- Variables are lexically scoped
- Function parameters create new bindings in function scope
- Loop variables are scoped to the loop body
- Inner scopes can access outer scope variables
- Variable shadowing is allowed

## Type Coercion

- String concatenation: Any type + String = String concatenation
- Numeric operations: Integers and floats can be mixed
- Boolean context: `0`, `""`, `[]`, `false` are falsy; everything else is truthy

## Built-in Functions Reference

### `print(...values)`
Prints values to console, separated by spaces.

**Example**:
```
print("Hello", "World")  // Output: Hello World
```

### `len(list)`
Returns the length of a list or string.

**Example**:
```
var count = len([1, 2, 3])  // count = 3
```

### `str(value)`
Converts a value to string.

**Example**:
```
var text = str(123)  // text = "123"
```

### `int(value)`
Converts a value to integer.

**Example**:
```
var num = int("42")  // num = 42
```

### `float(value)`
Converts a value to float.

**Example**:
```
var num = float("3.14")  // num = 3.14
```

### `connect(db_path)`
Connects to a SQLite database and returns a connection object.

**Parameters**:
- `db_path` (string): Path to SQLite database file

**Returns**: DatabaseConnection object

**Example**:
```
var conn = connect("mydb.db")
```

### `get_tables(connection)`
Returns list of all table names in the database.

**Parameters**:
- `connection`: DatabaseConnection object

**Returns**: List of strings (table names)

**Example**:
```
var tables = get_tables(conn)
```

### `table_exists(connection, table_name)`
Checks if a table exists in the database.

**Parameters**:
- `connection`: DatabaseConnection object
- `table_name` (string): Name of table to check

**Returns**: Boolean

**Example**:
```
if table_exists(conn, "users") {
    // Table exists
}
```

### `compare_table(conn1, conn2, table_name, mode, tolerance)`
Compares a table between two databases.

**Parameters**:
- `conn1`: First DatabaseConnection object
- `conn2`: Second DatabaseConnection object
- `table_name` (string): Name of table to compare
- `mode` (string): `"exact"` or `"fuzzy"`
- `tolerance` (number): Numeric tolerance for fuzzy comparisons

**Returns**: Dictionary with:
- `"table_name"` (string)
- `"passed"` (boolean)
- `"total_rows_db1"` (number)
- `"total_rows_db2"` (number)
- `"matching_rows"` (number)
- `"match_rate"` (number, 0-100)

**Example**:
```
var result = compare_table(conn1, conn2, "users", "fuzzy", 0.1)
if result["passed"] {
    print("Table matches!")
}
```

## Examples

### Basic Variables and Arithmetic
```
var x = 10
var y = 20
var sum = x + y
print(sum)  // Output: 30
```

### Functions
```
function add(a, b) {
    return a + b
}

var result = add(5, 3)
print(result)  // Output: 8
```

### Loops
```
var numbers = [1, 2, 3, 4, 5]
var sum = 0

for num in numbers {
    sum = sum + num
}

print(sum)  // Output: 15
```

### Conditionals
```
var age = 18

if age >= 18 {
    print("Adult")
} else {
    print("Minor")
}
```

### Database Validation
```
var conn1 = connect("db1.db")
var conn2 = connect("db2.db")

var result = compare_table(conn1, conn2, "users", "exact", 0)

if result["passed"] {
    print("Tables match!")
} else {
    print("Differences found")
    print("Match rate:", result["match_rate"])
}
```

