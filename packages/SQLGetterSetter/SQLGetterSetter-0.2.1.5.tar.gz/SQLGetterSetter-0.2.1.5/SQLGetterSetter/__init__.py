from mysql.connector import connect, Error

class MainClass:
    def __init__(self, connection=None, connection_params=None):
        """Initialize the object with Connection and new empty Query."""
        self.connection = connection
        self.connection_params = connection_params  # Store connection params for reconnection
        self.query = ""

    def connect(self):
        """Establize New Connection and Reconnects if the connection is unavailable."""
        if not self.connection or not self.connection.is_connected():
            try:
                self.connection = connect(**self.connection_params)
                print("Reconnected to the database.")
            except Error as err:
                print(f"Error reconnecting: {err}")
                self.connection = None

    def select(self, *columns):
        """SELECT the coloumns and Default to '*' ."""
        self.query += "SELECT " + ", ".join(columns) if columns else "SELECT *"
        return self

    def distinct(self, *columns):
        """DISTINCT is used to retrive the unique data , Parameters are single and multiple column_names."""
        self.query += " DISTINCT " + ", ".join(columns)
        return self

    def where(self, *condition, operator=None):
        """WHERE is used to retrive the data with certain conditions, Parameters are normal condition as string or multiple condition with logical operation."""
        if operator is None:
            self.query += " WHERE " + " ".join(condition)
        else:
            self.query += " WHERE " + f" {operator} ".join(condition)
        return self
    
    def orderby(self, *columns_with_order):
        """ORDERBY is used to arrange the result orderly, Parameters are passed as an tuples containing of (column_name, order). default is column name which assigned as ASC."""
        order_str = ", ".join(
            f"{col} {ord}" if isinstance(col, tuple) else f"{col} ASC"
            for col, ord in columns_with_order
        )
        self.query += f" ORDER BY {order_str}"
        return self

    def like(self, pattern):
        """LIKE is used to filter the data that are matches the pattern, Parameter is passed as string pattern."""        
        self.query += f" LIKE {pattern}"
        return self

    def isnull(self):
        """ISNULL is used to check the data's of the column is Null or not, No Parameters are passed."""
        self.query += f" IS NULL"
        return self

    def between(self, start, end):
        """BETWEEN is used to retrive the data from certain range, Parameters are starting value and ending."""
        self.query += f" BETWEEN {str(start)} AND {str(end)}"
        return self

    def IN(self, *values):
        """IN is used to check the multiple columns, Parameter are column_names passed as tuple."""
        value_list = ', '.join(map(str, values))
        self.query += f" IN ({value_list})"
        return self

    def and_operator(self):
        """It is an AND operator the added between the query is user's wish to."""
        self.query += " AND"
        return self

    def or_operator(self):
        """It is an OR operator the added between the query is user's wish to."""
        self.query += " OR"
        return self

    def table(self, table_name):
        """Assign the table name to the query."""
        self.query += f" FROM {table_name}"
        return self
    
    def limit(self, n, offset=None):
        """LIMIT is used to retrive the certain number of data from table, Parameters are no.of.rows and OFFSET to skip the no.of.begging_rows -> default to None."""
        self.query += f" LIMIT {n}" if offset is None else f" LIMIT {n} OFFSET {offset}"
        return self

    def fetch(self, n, offset=None):
        """FETCH is used in sql_server to fetch certain amount of data, Parameters are no.of.rows and OFFSET to skip the no.of.begging_rows -> default to None."""
        if offset is not None:
            self.query += f" OFFSET {offset} ROWS"
        self.query += f" FETCH NEXT {n} ROWS ONLY"
        return self
    
    def top(self, n, percent=False):
        """TOP is used in sql_server to retrive the begging data at certain percentage or number, Parameters are no.of.rows and percentage default -> None."""
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
            # print("Query Executed")
            if self.query.lower().startswith("select"): #Need to return the Resulted data
                results = cursor.fetchall()  
            else:
                self.connection.commit()
                results = f"Query executed successfully, affected rows: {cursor.rowcount}"
            cursor.close()
            self.query = ""
            return results #Return as List or String
        except Error as err:
            print(f"Error: {err}")
            self.query = ""
            return None