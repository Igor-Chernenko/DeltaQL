"""
Database operations for DataVal language.
Handles SQLite connections and queries.
"""

import sqlite3


class DatabaseConnection:
    """Wrapper for SQLite database connections."""
    
    def __init__(self, db_path):
        """
        Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row  # Enable column access by name
    
    def get_tables(self):
        """
        Get list of all table names in the database.
        
        Returns:
            List of table names
        """
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        tables = [row[0] for row in cursor.fetchall()]
        return tables
    
    def table_exists(self, table_name):
        """
        Check if a table exists in the database.
        
        Args:
            table_name: Name of table to check
            
        Returns:
            Boolean indicating if table exists
        """
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM sqlite_master 
            WHERE type='table' AND name=?
        """, (table_name,))
        count = cursor.fetchone()[0]
        return count > 0
    
    def get_primary_key(self, table_name):
        """
        Get the primary key column name for a table.
        If no primary key, returns the first column.
        
        Args:
            table_name: Name of table
            
        Returns:
            Primary key column name
        """
        cursor = self.connection.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        # Find primary key column
        for col in columns:
            if col[5] == 1:  # col[5] is the pk flag
                return col[1]  # col[1] is the column name
        
        # If no primary key, return first column
        if columns:
            return columns[0][1]
        
        raise ValueError(f"Table '{table_name}' has no columns")
    
    def get_table_data(self, table_name):
        """
        Get all rows from a table as list of dictionaries.
        
        Args:
            table_name: Name of table
            
        Returns:
            List of dictionaries, each representing a row
        """
        cursor = self.connection.cursor()
        
        # Get primary key for ordering
        primary_key = self.get_primary_key(table_name)
        
        # Fetch all rows ordered by primary key
        cursor.execute(f"SELECT * FROM {table_name} ORDER BY {primary_key}")
        rows = cursor.fetchall()
        
        # Convert to list of dictionaries
        result = []
        for row in rows:
            row_dict = {}
            for key in row.keys():
                row_dict[key] = row[key]
            result.append(row_dict)
        
        return result
    
    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
    
    def __del__(self):
        """Ensure connection is closed when object is destroyed."""
        self.close()

