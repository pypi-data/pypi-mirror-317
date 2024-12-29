from mysql.connector import connect, Error

class MainClass:
    def __init__(self, connection=None, connection_params=None):
        """Initialize the object with Connection and new empty Query."""
        self.connection = connection
        self.connection_params = connection_params  # Store connection params for reconnection
        self.query = ""
        self.sub_query_count = 0

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
        self.sub_query_count += 1
        if self.sub_query_count == 2:
            self.query += " (SELECT " + ", ".join(columns) if columns else " (SELECT "
        else:
            self.query += "SELECT " + ", ".join(columns) if columns else "SELECT *"
        return self

    def distinct(self, *columns):
        """DISTINCT is used to retrive the unique data , 
        Parameters are single and multiple column_names."""
        self.query += " DISTINCT " + ", ".join(columns)
        return self

    def where(self, *condition, operator=None):
        """WHERE is used to retrive the data with certain conditions, 
        Parameters are normal condition as string or multiple condition with logical operation."""
        if operator is None:
            self.query += " WHERE " + " ".join(condition)
        else:
            self.query += " WHERE " + f" {operator} ".join(condition)
        return self
    
    def orderby(self, *columns_with_order):
        """ORDERBY is used to arrange the result orderly, P
        arameters are passed as an tuples containing of (column_name, order). 
        default is column name which assigned as ASC."""
        order_str = ", ".join(
            f"{col} {ord}" if isinstance(col, tuple) else f"{col} ASC"
            for col, ord in columns_with_order
        )
        self.query += f" ORDER BY {order_str}"
        return self

    def like(self, pattern):
        """LIKE is used to filter the data that are matches the pattern, 
        Parameter is passed as string pattern."""        
        self.query += f" LIKE {pattern}"
        return self

    def isnull(self):
        """ISNULL is used to check the data's of the column is Null or not, 
        No Parameters are passed."""
        self.query += f" IS NULL"
        return self

    def between(self, start, end):
        """BETWEEN is used to retrive the data from certain range, 
        Parameters are starting value and ending."""
        self.query += f" BETWEEN {str(start)} AND {str(end)}"
        return self

    def IN(self, *values):
        """IN is used to check the multiple columns, 
        Parameter are column_names passed as tuple."""
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
    def avg(self, value):
        self.query += f" AVG({value})"
        return self

    def table(self, table_name):
        """Assign the table name to the query."""
        self.query += f" FROM {table_name}"
        return self
    
    def limit(self, n, offset=None):
        """LIMIT is used to retrive the certain number of data from table, 
        Parameters are no.of.rows and OFFSET to skip the no.of.begging_rows -> default to None."""
        self.query += f" LIMIT {n}" if offset is None else f" LIMIT {n} OFFSET {offset}"
        return self

    def fetch(self, n, offset=None):
        """FETCH is used in sql_server to fetch certain amount of data, 
        Parameters are no.of.rows and OFFSET to skip the no.of.begging_rows -> default to None."""
        if offset is not None:
            self.query += f" OFFSET {offset} ROWS"
        self.query += f" FETCH NEXT {n} ROWS ONLY"
        return self
    
    def top(self, n, percent=False):
        """TOP is used in sql_server to retrive the begging data at certain percentage or number, 
        Parameters are no.of.rows and percentage default -> None."""
        replacement = f"SELECT TOP {n}{' PERCENT' if percent else ''}"
        self.query = self.query.replace("SELECT", replacement, 1)  # Replace only the first occurrence
        return self
        
    def insert(self, table_name, values, columns=None):
        """
        Constructs an INSERT INTO SQL query for single or multiple rows.
    
        :param table_name: Name of the table to insert data into.
        :param values: List of values (single row as a tuple or multiple rows as a list of tuples).
        :param columns: List of column names (optional).
        """
        columns_part = f" ({', '.join(columns)})" if columns else ""        
        if isinstance(values, list):
            values_part = ", ".join(f"({', '.join(map(str, row))})" for row in values)
        else:
            values_part = f"({', '.join(map(str, values))})"
        
        self.query = f"INSERT INTO {table_name}{columns_part} VALUES {values_part}"
        return self

    def insert_into_select(self, source, destination, source_columns=None, destination_columns=None):
        """
        Constructs an INSERT INTO SELECT SQL query.

        :param source: Source table to select data from.
        :param destination: Destination table to insert data into.
        :param source_columns: List of source column names (optional).
        :param destination_columns: List of destination column names (optional).
        """
        source_columns_part = f" ({', '.join(source_columns)})" if source_columns else "*"
        destination_columns_part = f" ({', '.join(destination_columns)})" if destination_columns else ""
        self.query = f"INSERT INTO {destination}{destination_columns_part} SELECT {source_columns_part} FROM {source}"
        return self
            
    def update(self, table_name, changes):
        """
        Constructs an UPDATE SQL query.
        :param table_name: Name of the table to update.
        :param changes: List of tuples containing column name and new value (e.g., [('column1', 'value1'), ('column2', 'value2')]).
        """
        if not isinstance(changes, list):
            raise ValueError("Changes must be a list of tuples: [('column1', 'value1'), ...]")

        def format_value(value):
            if isinstance(value, str):
                return f"'{value.replace('\'', '\\\'')}'"
            return str(value)

        changes_part = ", ".join(f"{col} = {format_value(val)}" for col, val in changes)
        self.query = f"UPDATE {table_name} SET {changes_part}"
        # print(self.query)    
        return self

    def delete(self, table_name):
        """
        Constructs a DELETE SQL query.
        :param table_name: Name of the table to delete records from.
        :param condition: Optional condition for the WHERE clause (e.g., "id = 1").
        """
        self.query = f"DELETE FROM {table_name}"
        # print(self.query)
        return self

    def select_into(self, source, destination, source_columns=None):
        """
        Constructs a SELECT INTO SQL query.
        :param source: Source table to select data from.
        :param destination: Destination table to insert data into.
        :param source_columns: List of column names to select (optional).
        """
        columns_part = ", ".join(source_columns) if source_columns else "*"
        self.query = f"SELECT {columns_part} INTO {destination} FROM {source}"
        # print(self.query)
        return self

            
    def exe(self):
        """Executes the constructed query."""
        self.connect()  # Ensure connection is available
        if not self.connection:
            print("Connection is unavailable. Query cannot be executed.")
            return None

        cursor = self.connection.cursor()
        try:
            if self.sub_query_count == 2:
                cursor.execute(self.query + ');')
            else:
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