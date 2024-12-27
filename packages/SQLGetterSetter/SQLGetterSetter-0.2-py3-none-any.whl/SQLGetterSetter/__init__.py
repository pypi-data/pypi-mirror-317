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
        query = ','.join(list(args))
        cursor = self.connection.cursor()
        try :
            cursor.execute("SELECT DISTINCT "+query+f" FROM {table}")
        except Error as e:
            print(f"Error: {e}")
    
    