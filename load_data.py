"""
WEEK 1, DAY 3 - Loading Data into MySQL
This script loads the hospital data CSV file into MySQL database.
"""

import pandas as pd
from sqlalchemy import create_engine

print("=" * 60)
print("HOSPITAL READMISSION PROJECT - DATA LOADING")
print("=" * 60)

# Read the CSV file into a pandas DataFrame
print("\n[Step 1] Reading CSV file...")
df = pd.read_csv('data/hospital_data.csv')

# Print the shape to confirm it loaded correctly
print(f"✓ Data loaded successfully!")
print(f"  Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")

# Print first 5 rows to see the data
print("\n[Step 2] Preview of data (first 5 rows):")
print(df.head())

# Create the connection to MySQL
print("\n[Step 3] Connecting to MySQL database...")
# IMPORTANT: Replace 'yourpassword' with your actual MySQL password
# Your MySQL password: Aishu935359
engine = create_engine('mysql+mysqlconnector://root:Aishu935359@localhost/hospital_db')

# Load the entire DataFrame into MySQL
print("[Step 4] Loading data into MySQL 'patients' table...")
df.to_sql('patients', con=engine, if_exists='replace', index=False)

print("\n✓✓✓ SUCCESS! ✓✓✓")
print(f"Total rows loaded into MySQL: {len(df):,}")
print("\nNext step: Open MySQL Workbench and run:")
print("  USE hospital_db;")
print("  SELECT COUNT(*) FROM patients;")
