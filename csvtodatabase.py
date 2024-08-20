import pandas as pd
import psycopg2
import os

# Database connection parameters
db_name = "concourse"
db_user = "concourse_user"
db_password = "concourse_pass"
db_host = "192.168.3.109"  
db_port = "5432"

# Path to the CSV file
csv_file_path = "profit_loss_data/profit_loss_data.csv"

# Connect to PostgreSQL database
try:
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS relianceprofitlost (
        "Parameters" TEXT,
        "Mar 2013" TEXT,
        "Mar 2014" TEXT,
        "Mar 2015" TEXT,
        "Mar 2016" TEXT,
        "Mar 2017" TEXT,
        "Mar 2018" TEXT,
        "Mar 2019" TEXT,
        "Mar 2020" TEXT,
        "Mar 2021" TEXT,
        "Mar 2022" TEXT,
        "Mar 2023" TEXT,
        "Mar 2024" TEXT,
        "TTM" TEXT
    )
    """
    cursor.execute(create_table_query)
    
    # Read the CSV file into a DataFrame, skipping the index column if present
    df = pd.read_csv(csv_file_path, index_col=0)
    
    # Remove any leading/trailing spaces from column names
    df.columns = [col.strip() for col in df.columns]
    
    # Insert data into the table
    insert_query = """
        INSERT INTO relianceprofitlost ({})
        VALUES ({})
    """.format(
        ', '.join(f'"{col}"' for col in df.columns),
        ', '.join(['%s'] * len(df.columns))
    )

    for index, row in df.iterrows():
        cursor.execute(insert_query, row.tolist())
    
    # Commit changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()
    
    print("Data inserted successfully into PostgreSQL!")
except Exception as e:
    print(f"Database connection failed: {e}")
