# DataVal Architecture Documentation

## Design Decisions

### Language Paradigm

**Decision**: Imperative, procedural language with first-class functions

**Rationale**:
- Familiar syntax for developers with Python/JavaScript background
- Procedural style is intuitive for validation workflows
- Functions allow code reuse for common validation patterns
- Simple enough to implement in limited timeframe

### Interpreter vs Compiler

**Decision**: Interpreter using tree-walking approach

**Rationale**:
- Faster to implement than a compiler
- Easier to debug during development
- Sufficient performance for database validation workloads
- Direct AST execution is straightforward
- No need for complex bytecode generation

### Parser Choice

**Decision**: Lark parser library

**Rationale**:
- Declarative grammar definition (easier to read and modify)
- Built-in tree construction
- Good error messages
- Well-documented and battle-tested
- Faster than writing parser from scratch
- LALR parser provides good performance

### Database Support

**Decision**: SQLite only (no SQLAlchemy)

**Rationale**:
- SQLite is built into Python (zero additional dependencies)
- Sufficient for hackathon demo and MVP
- Reduces complexity and setup time
- Easy to create test databases
- Can be extended later for other databases

### Comparison Strategy

**Decision**: In-memory comparison using dictionaries keyed by primary key

**Rationale**:
- Simple and fast for typical database sizes
- Dictionary lookup is O(1) for efficient comparison
- Primary key ensures unique row identification
- Auto-detection of primary key reduces user burden
- Fuzzy matching implemented through tolerance threshold

### Result Object Design

**Decision**: Dictionary-based result objects accessed via `result["key"]`

**Rationale**:
- Simpler than implementing custom object attribute access
- Python dictionaries are native and efficient
- Less interpreter complexity (no need for property access visitor)
- Familiar pattern for developers
- Extensible for future fields

### Error Handling Strategy

**Decision**: Try-catch blocks with descriptive error messages

**Rationale**:
- Graceful degradation instead of crashes
- Clear error messages help debugging
- Context-specific errors (syntax vs runtime vs database)
- Balances robustness with development time

## Architecture Overview

### Component Diagram
```
┌─────────────────┐
│   dataval.py    │  Entry point
│  (Main Driver)  │
└────────┬────────┘
         │
         ├──> ┌──────────────┐
         │    │ grammar.lark │  Language grammar
         │    └──────────────┘
         │
         ├──> ┌──────────────┐
         │    │  Lark Parser │  Parsing
         │    └──────┬───────┘
         │           │
         │           v
         │    ┌──────────────┐
         │    │ ast_nodes.py │  AST representation
         │    │ (Transformer)│
         │    └──────┬───────┘
         │           │
         │           v
         └──> ┌─────────────────┐
              │ interpreter.py  │  Execution engine
              │  (Visitor)      │
              └────────┬────────┘
                       │
                       ├──> ┌─────────────────┐
                       │    │ environment.py  │  Scope management
                       │    └─────────────────┘
                       │
                       ├──> ┌─────────────────┐
                       │    │  builtins.py    │  Built-in functions
                       │    └────────┬────────┘
                       │             │
                       │             ├──> ┌──────────────┐
                       │             │    │ database.py  │  DB operations
                       │             │    └──────────────┘
                       │             │
                       │             └──> ┌──────────────┐
                       │                  │ validator.py │  Comparison
                       │                  └──────────────┘
                       │
                       └──> Demo Program (.dv file)
```

### Execution Pipeline

1. **Lexing & Parsing**: Lark converts source code to parse tree
2. **AST Transformation**: Custom transformer converts parse tree to AST
3. **Interpretation**: Tree-walking interpreter executes AST nodes
4. **Built-in Execution**: Database operations and validation logic run
5. **Output**: Results printed to console

## Core Components

### 1. Lexer & Parser (Lark)

**Responsibility**: Convert source code text into structured parse tree

**Key Features**:
- Token recognition (keywords, operators, literals)
- Grammar rules for language constructs
- Error detection for syntax issues
- Automatic tree construction

### 2. AST (ast_nodes.py)

**Responsibility**: Represent program structure as typed tree nodes

**Key Classes**:
- `Program`: Root node containing all statements
- `VarDecl`, `Assignment`: Variable operations
- `FunctionDef`, `FunctionCall`: Function operations
- `IfStatement`, `ForLoop`: Control flow
- `BinaryOp`, `UnaryOp`: Expressions
- `Literal`, `Identifier`: Values

**Design Pattern**: Composite pattern for tree structure

### 3. Environment (environment.py)

**Responsibility**: Manage variable scoping and storage

**Key Features**:
- Variable definition and lookup
- Scope chaining (parent pointer)
- Nested scope support
- Closure capture for functions

**Design Pattern**: Chain of responsibility for scope lookup

### 4. Interpreter (interpreter.py)

**Responsibility**: Execute AST nodes and manage program flow

**Key Features**:
- Visitor pattern for node execution
- Expression evaluation
- Control flow handling
- Function call mechanism
- Environment management

**Design Pattern**: Visitor pattern

### 5. Built-ins (builtins.py)

**Responsibility**: Provide native functions to DataVal programs

**Categories**:
- Utility functions (print, len, conversions)
- Database functions (connect, get_tables, table_exists)
- Validation functions (compare_table)

**Integration**: Registered in global environment at startup

### 6. Database (database.py)

**Responsibility**: Wrap SQLite operations in clean interface

**Key Features**:
- Connection management
- Table introspection
- Primary key detection
- Data fetching as dictionaries

**Design Pattern**: Wrapper/Adapter pattern

### 7. Validator (validator.py)

**Responsibility**: Implement comparison logic

**Algorithms**:
- Exact matching: Row-by-row equality check
- Fuzzy matching: Numeric tolerance + exact for other types

**Strategy**: Dictionary-based comparison for O(1) lookups

## Tradeoffs

### Simplicity vs Features

**Choice**: Focused DSL over general-purpose language

**Tradeoff**:
- ✅ Faster to implement
- ✅ Easier to learn
- ✅ Clear use case
- ❌ Less flexible
- ❌ Not Turing-complete in practical terms

### Performance vs Development Time

**Choice**: Tree-walking interpreter over compiler

**Tradeoff**:
- ✅ Much faster to build
- ✅ Easier to debug
- ✅ Sufficient for typical database sizes
- ❌ Slower than compiled code
- ❌ No optimization passes

### Flexibility vs Complexity

**Choice**: Dictionary result objects over custom objects

**Tradeoff**:
- ✅ Simpler interpreter
- ✅ Less code to maintain
- ✅ Familiar pattern
- ❌ No dot notation (must use `result["key"]`)
- ❌ Less type safety

### Database Support

**Choice**: SQLite only vs multiple databases

**Tradeoff**:
- ✅ Zero dependencies beyond Lark
- ✅ Easier testing and demos
- ✅ Faster implementation
- ❌ Limited to SQLite databases
- ❌ Would need refactoring to add other databases

## Extension Points

### Future Enhancements

1. **Additional Database Support**: Add MySQL/PostgreSQL via connection string parsing
2. **Report Generation**: Add file-based reporting with templates
3. **Schema Validation**: Compare table structures, not just data
4. **Advanced Fuzzy Matching**: String similarity, custom rules
5. **Performance**: Add parallel comparison for multiple tables
6. **Debugger**: Add step-through debugging capabilities
7. **Standard Library**: More built-in utilities (date functions, math, etc.)

### How to Extend

**Adding Built-in Functions**:
1. Implement function in `builtins.py`
2. Add to `get_builtins()` dictionary
3. Document in language spec

**Adding Language Features**:
1. Update `grammar.lark`
2. Add AST node class in `ast_nodes.py`
3. Update transformer in `ast_nodes.py`
4. Add visitor method in `interpreter.py`

**Adding Database Operations**:
1. Add method to `DatabaseConnection` class
2. Wrap in built-in function if needed
3. Test with sample databases

## Testing Strategy

### Unit Testing (Recommended)

- Test each AST node type independently
- Test environment scope chaining
- Test comparison algorithms with known data
- Test built-in functions in isolation

### Integration Testing

- Test complete programs end-to-end
- Test with various database schemas
- Test error handling paths
- Test edge cases (empty tables, missing keys)

### Demo Testing

- Run demo program with sample databases
- Verify output matches expectations
- Test both exact and fuzzy modes
- Ensure clean error messages

## Performance Characteristics

### Time Complexity

- **Parsing**: O(n) where n is source code length
- **Execution**: O(n) where n is number of AST nodes
- **Table Comparison**: O(m) where m is max(rows_db1, rows_db2)
- **Overall**: Linear in both code size and data size

### Space Complexity

- **AST**: O(n) for parse tree
- **Environment**: O(v) where v is number of variables in scope
- **Comparison**: O(m) for dictionary storage of rows
- **Overall**: Linear in variables and data size

### Scalability

**Suitable For**:
- Small to medium databases (< 1M rows per table)
- Validation scripts (not production workloads)
- One-time or periodic comparisons

**Not Suitable For**:
- Real-time validation
- Very large databases (> 10M rows)
- High-frequency comparisons

## Security Considerations

### SQL Injection

**Risk**: Medium (table names are not parameterized in some queries)

**Mitigation**: Validate table names against schema before querying

### File Access

**Risk**: Users can connect to any SQLite file accessible to the process

**Mitigation**: Run interpreter with limited file system permissions

### Resource Exhaustion

**Risk**: Large databases could consume excessive memory

**Mitigation**: Add row limits or streaming comparison for production use

## Conclusion

DataVal's architecture prioritizes simplicity, correctness, and rapid development. The design choices favor ease of implementation and debugging over raw performance, making it ideal for a hackathon MVP. The modular structure allows for future enhancements while keeping the core interpreter clean and maintainable.

