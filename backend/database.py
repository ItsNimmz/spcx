from sqlalchemy import create_engine
import pandas as pd
import os

current_dir = os.path.dirname(__file__)
folder_path = os.path.join(current_dir, 'data')

# Replace with your MySQL credentials
USERNAME = "root"
PASSWORD = "root"
HOST = "localhost"  # Change if your database is hosted remotely
DATABASE = "spacexv1"

# Create MySQL database connection using SQLAlchemy
engine = create_engine(f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}")

# SQL query to execute (replace with your actual query)
query = "CREATE DATABASE IF NOT EXISTS spacexv1;"


try:
    # Use engine to connect to the database
    with engine.connect() as connection:
        # Execute the query
        connection.execute(query)
        print("Query executed successfully.")
except Exception as e:
    # If an error occurs, print the error
    print(f"An error occurred: {e}")

print("Connected to MySQL successfully!")


def create_table():
    query = """
    CREATE TABLE IF NOT EXISTS launches (
        id INT AUTO_INCREMENT PRIMARY KEY,
        mission_name VARCHAR(255),
        launch_date_utc TIMESTAMP,
        launch_success BOOLEAN,
        launch_year INT,
        launch_site_name VARCHAR(255),
        rocket_name VARCHAR(255),
        rocket_type VARCHAR(255),
        payload_mass_kg FLOAT,
        payload_type VARCHAR(255),
        manufacturer VARCHAR(255),
        reused BOOLEAN
    );
    """

    try:
        # Use engine to connect to the database
        with engine.connect() as connection:
            # Execute the query
            connection.execute(query)
            print("Query executed successfully.")
    except Exception as e:
        # If an error occurs, print the error
        print(f"An error occurred: {e}")
    
    print("✅ Table 'launches' created or already exists.")

    file_path = os.path.join(folder_path, 'after_clean.xlsx')
    insert_excel_to_mysql(file_path) 


def insert_excel_to_mysql(file_path, table_name="launches"):
    """Reads Excel file and inserts data into MySQL table."""
    
    # Read Excel file
    df = pd.read_excel(file_path, sheet_name="Sheet1")

    # Insert into MySQL
    df.to_sql(table_name, con=engine, if_exists="append", index=False)
    print(f"🚀 Data from {file_path} inserted successfully into '{table_name}'!")

    # 5️⃣ Main Execution
if __name__ == "__main__":
    create_table()  # Ensure table exists
    # insert_excel_to_mysql("after_clean.xlsx") 