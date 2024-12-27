from .main import hello
# from mysql.connector import Error
from mysql.connector import connect, Error

class MainClass:
    def __init__(self, connection=None, connection_params=None):
        self.connection = connection
        self.connection_params = connection_params  # Store connection params for reconnection
        self.query = ""

    def connect(self):
        """Reconnects if the connection is unavailable."""
        if not self.connection or not self.connection.is_connected():
            try:
                self.connection = connect(**self.connection_params)
                print("Reconnected to the database.")
            except Error as err:
                print(f"Error reconnecting: {err}")
                self.connection = None

    def select(self, *columns):
        self.query += "SELECT " + ", ".join(columns) if columns else "SELECT *"
        return self

    def distinct(self, *columns):
        self.query += " DISTINCT " + ", ".join(columns)
        return self

    def where(self, *condition, operator=None):
        if operator is None:
            self.query += " WHERE " + " ".join(condition)
        else:
            self.query += " WHERE " + f" {operator} ".join(condition)
        return self
    
    def orderby(self, *columns_with_order):
        order_str = ", ".join(
            f"{col} {ord}" if isinstance(col, tuple) else f"{col} ASC"
            for col, ord in columns_with_order
        )
        self.query += f" ORDER BY {order_str}"
        return self

    def like(self, pattern):
        # self.conditions.append(f"{self.current_column} LIKE '{pattern}'")
        self.query += f" LIKE {pattern}"
        return self

    def isnull(self):
        # self.conditions.append(f"{self.current_column} IS NULL")
        self.query += f" IS NULL"
        return self

    def between(self, start, end):
        # self.conditions.append(f"{self.current_column} BETWEEN {start} AND {end}")
        self.query += f" BETWEEN {start} AND {end}"
        return self

    def IN(self, *values):
        value_list = ', '.join(map(str, values))
        self.query += f" IN ({value_list})"
        return self

    def and_operator(self):
        self.query += " AND"
        return self

    def or_operator(self):
        self.query += " OR"
        return self

    def table(self, table_name):
        self.query += f" FROM {table_name}"
        return self
    
    def limit(self, n,offset = None):
        if offset is None:
            self.query += f" LIMIT {n}"
        else:
            self.query += f" LIMIT {n} OFFSET {offset}"
        return self
    
    def limit(self, n, offset=None):
        self.query += f" LIMIT {n}" if offset is None else f" LIMIT {n} OFFSET {offset}"
        return self

    def fetch(self, n, offset=None):
        if offset is not None:
            self.query += f" OFFSET {offset} ROWS"
        self.query += f" FETCH NEXT {n} ROWS ONLY"
        return self
    
    def top(self, n, percent=False):
        replacement = f"SELECT TOP {n}{' PERCENT' if percent else ''}"
        self.query = self.query.replace("SELECT", replacement, 1)  # Replace only the first occurrence
        return self
                        
            
    def exe(self):
        """Executes the constructed query."""
        self.connect()  # Ensure connection is available
        if not self.connection:
            print("Connection is unavailable. Query cannot be executed.")
            return None

        cursor = self.connection.cursor()
        try:
            cursor.execute(self.query + ';')
            print("Query Executed")
            if self.query.lower().startswith("select"):
                results = cursor.fetchall()  # Fetch all rows
            else:
                self.connection.commit()
                results = f"Query executed successfully, affected rows: {cursor.rowcount}"
            cursor.close()
            self.query = ""
            return results
        except Error as err:
            print(f"Error: {err}")
            self.query = ""
            return None