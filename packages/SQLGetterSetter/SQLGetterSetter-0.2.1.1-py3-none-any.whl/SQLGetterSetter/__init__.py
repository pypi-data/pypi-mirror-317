from .main import hello


class MainClass:
    def __init__(self, connection):
        # pass
        self.connection = connection
    
    def select(self,key = None):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()
            print("Data retrieved successfully:")
            for row in rows:
                print(row)
        except Error as e:
            print(f"Error: {e}")
                
    def insert(self, data):
        cursor = self.connection.cursor()
        try:
            query = "INSERT INTO users (first_name, last_name, email, age) VALUES (%s, %s, %s, %s)"
            cursor.executemany(query, data)
            self.connection.commit()  # Commit the transaction
            print("Data inserted successfully.")
        except Error as e:
            print(f"Error: {e}")
            self.connection.rollback()  # Rollback in case of error
    def distinct(self, table, *args):
        if not args:
            raise ValueError("At least one column name must be provided for DISTINCT operation.")
        
        cursor = self.connection.cursor()
        query = ', '.join(args)
        
        try:
            cursor.execute(f"SELECT DISTINCT {query} FROM {table}")
            rows = cursor.fetchall()
            print("Data retrieved successfully:")
            for row in rows:
                print(row)
        except Error as e:
            print(f"Error: {e}")

    
    