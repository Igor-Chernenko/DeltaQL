# Documentation
## Declaring Variables
var local_db_path = "./database1.db" //saves as string type
var tables = ["users", "orders", "products"] //Uses python Lists
var some_variable = 0.1 //saves as a Floating integer
## Database connectionsa
var conn1 = connect(db_path_a) // uses SQLite3 Connection cursors as pointers to data
Built-In Functions
var tables = get_tables(connection) // Returns a list of SQLite3 Connection Cursors pointed at tables

table_exists(connection, table) // Boolean check to see if a table exists in another database
var table_length = len(tables) // Gets the length of a table

var report_file = generate_html_report(results, match_type, conn1, conn2) // creates an HTML report that visualizes all the changes

## Compare
Fuzzy
compare_table(conn1, conn2, table, Fuzzy, tolerance) //Checks if two tables are equal, using fuzzy matching with tolerance

Exact
compare_table(conn1, conn2, table, Fuzzy)  //Checks if two tables are equal, using exact matching


## Crediting
We acknowledge the use of Anthropic’s Claude Sonnet 4.5 during development. It assisted in drafting the initial HTML report scaffolding and refining example snippets that informed our Lark grammar documentation. We reviewed, tested, and modified all generated code to meet our project’s requirements and quality standards. Any remaining mistakes or omissions are ours alone.
