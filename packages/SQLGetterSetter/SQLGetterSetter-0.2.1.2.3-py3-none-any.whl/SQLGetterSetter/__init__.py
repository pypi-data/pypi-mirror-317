from .main import hello
from mysql.connector import Error

class MainClass:
    def __init__(self, connection):
        self.connection = connection
        self.query = ""
        self.first_condition = True  # Flag to handle the placement of 'WHERE', 'AND', etc.
    
    # Helper methods for query construction
    def select(self, table, columns="*"):
        self.query += f"SELECT {columns} FROM {table} "
        return self

    def where(self, column):
        if self.first_condition:
            self.query += f"WHERE {column} "
            self.first_condition = False
        else:
            self.query += f"AND {column} "
        return self

    def like(self, pattern):
        self.query += f"LIKE '{pattern}' "
        return self

    def isnull(self):
        self.query += f"IS NULL "
        return self

    def between(self, start, end):
        self.query += f"BETWEEN {start} AND {end} "
        return self

    def and_operator(self):
        self.query += "AND "
        return self

    def or_operator(self):
        self.query += "OR "
        return self

    def distinct(self, table, *args):
        if args:
            self.query = f"SELECT DISTINCT {', '.join(args)} FROM {table} "
            return self
        else:
            print("Error: At least one column must be specified for DISTINCT.")
            return self

    def update(self, table, updates):
        set_clause = ", ".join([f"{column} = %s" for column in updates.keys()])
        self.query += f"UPDATE {table} SET {set_clause} "
        return self

    def delete(self, table):
        self.query += f"DELETE FROM {table} "
        return self

    # Method to execute the query using MySQL Connector
    def execute_query(self):
        cursor = self.connection.cursor()
        try:
            # If the query contains placeholders, we execute it with the actual data
            cursor.execute(self.query)
            if "SELECT" in self.query:
                rows = cursor.fetchall()
                print("Data retrieved successfully:")
                for row in rows:
                    print(row)
            else:
                self.connection.commit()
                print(f"Query executed successfully: {self.query}")
        except Exception as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()