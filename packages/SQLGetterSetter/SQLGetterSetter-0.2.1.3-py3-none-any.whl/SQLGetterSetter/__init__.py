from .main import hello
from mysql.connector import Error

class MainClass:
    def __init__(self, connection=None):
        self.connection = connection
        self.query = ""

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
    def exe(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute(self.query)
            print("Query Executed")
            if self.query.lower().startswith("select"):
                results = cursor.fetchall()  # Fetch all rows
                cursor.close()
                self.connection.close()
                print(self.query)
                self.query = ""
                return results 
                
            else:
                self.connection.commit()
                cursor.close()
                self.connection.close()
                print(self.query)
                self.query = ""
                return f"Query executed successfully, affected rows: {cursor.rowcount}"
                
        except Error as err:
            print(f"Error: {err}")
            if self.connection.self.cs_Connectionected():
                self.connection.close()
            print(self.query)
            self.query = ""
            return None  # Return None if there was an error

