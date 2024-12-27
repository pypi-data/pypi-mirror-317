from .main import hello
from mysql.connector import Error

class MainClass:
    def __init__(self, connection):
        self.connection = connection
        self.query = ""  # This will hold the entire query
        self.conditions = []  # List to store conditions
        self.is_where_added = False  # To check if WHERE is already added

    # Helper methods for query construction
    def where(self, column):
        self.current_column = column  # Store the current column
        if not self.is_where_added:
            self.query += " WHERE "
            self.is_where_added = True
        return self  # Return self for chaining methods

    def like(self, pattern):
        self.conditions.append(f"{self.current_column} LIKE '{pattern}'")  # Add condition to the list
        self.query += f"{self.current_column} LIKE '{pattern}'"
        return self  # Return self for chaining methods

    def isnull(self):
        self.conditions.append(f"{self.current_column} IS NULL")  # Add IS NULL condition
        self.query += f"{self.current_column} IS NULL"
        return self

    def between(self, start, end):
        self.conditions.append(f"{self.current_column} BETWEEN {start} AND {end}")  # Add BETWEEN condition
        self.query += f"{self.current_column} BETWEEN {start} AND {end}"
        return self

    def IN(self, *values):
        value_list = ', '.join(map(str, values))  # Join values with commas
        self.conditions.append(f"{self.current_column} IN ({value_list})")  # Add IN condition
        self.query += f"{self.current_column} IN ({value_list})"
        return self

    def and_operator(self):
        self.conditions.append("AND")  # Add AND operator
        self.query += " AND "
        return self

    def or_operator(self):
        self.conditions.append("OR")  # Add OR operator
        self.query += " OR "
        return self

    # Query execution methods
    def select(self, table, columns="*"):
        self.query = f"SELECT {columns} FROM {table}"
        return self  # Return self to allow chaining

    def insert(self, table, columns, data):
        column_str = ", ".join(columns)
        values_placeholder = ", ".join(["%s"] * len(columns))
        self.query = f"INSERT INTO {table} ({column_str}) VALUES ({values_placeholder});"
        cursor = self.connection.cursor()
        try:
            cursor.executemany(self.query, data)
            self.connection.commit()
            print("Data inserted successfully.")
        except Exception as e:
            print(f"Error: {e}")
            self.connection.rollback()

    def distinct(self, table, *args):
        if not args:
            raise ValueError("At least one column name must be provided for DISTINCT operation.")
        self.query = f"SELECT DISTINCT {', '.join(args)} FROM {table}"
        return self  # Return self to allow chaining

    def update(self, table, updates):
        update_clause = ", ".join([f"{column} = %s" for column in updates.keys()])
        self.query = f"UPDATE {table} SET {update_clause}"
        return self  # Return self to allow chaining

    def delete(self, table):
        self.query = f"DELETE FROM {table}"
        return self  # Return self to allow chaining

    def execute_query(self):
        if not self.query:
            print("No query to execute.")
            return
        cursor = self.connection.cursor()
        try:
            cursor.execute(self.query)
            rows = cursor.fetchall()
            print("Data retrieved successfully:")
            for row in rows:
                print(row)
            return rows
        except Exception as e:
            print(f"Error: {e}")
