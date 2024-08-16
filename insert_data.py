import pandas as pd
from sqlalchemy import create_engine

# Load the DataFrame from CSV
df = pd.read_csv('profit_loss_data.csv')

# Database connection parameters
db_user = 'concourse_user'
db_password = 'concourse_pass'
db_host = 'localhost'  # Adjust if necessary
db_port = '5432'
db_name = 'concourse'

# Create a SQLAlchemy engine
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

# Write data to PostgreSQL
df.to_sql('profit_loss', engine, if_exists='replace', index=False)
print("Data inserted into PostgreSQL successfully!")
