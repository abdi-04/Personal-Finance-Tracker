import mysql.connector
from database.config import DB_CONFIG

## This function checks if the database file already exists, 
# and if not it creates the database and tables 
# by executing the SQL commands in database/setup.sql.

def init_database():
    try:
        temp_config = DB_CONFIG.copy() # Make a copy of the config so we don't modify the original
        # Remove and save the database name — we can't connect to it yet if it doesn't exist
        db_name = temp_config.pop("database") # returns finance_tracker and removes it from temp_config 
        
        # Connect to MySQL without specifying a database, so we can create it if it doesn't exist
        conn = mysql.connector.connect(**temp_config)  
        cursor = conn.cursor() 

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}") # Create the database only if it doesn't already exist
        cursor.execute(f"USE {db_name}") 


        with open("database/setup.sql", "r") as f: # Open the SQL file that contains the table definitions
            schema = f.read() # Read the entire contents of the SQL file as a string
            for statement in schema.split(";"): # Split the file into individual SQL statements(table)
                if statement.strip():
                    cursor.execute(statement) # Run each SQL statement to create the tables

        conn.commit()
        cursor.close()
        conn.close()

        print("Database initialized successfully!")

    except Exception as e:
        print(f"Database initialization error: {e}")


# Open and return a fresh connection to the database 
# This function is used by the query functions in database/queries 
# to get a connection to the database whenever they need to run a query.
def get_connection():
    return mysql.connector.connect(**DB_CONFIG) 