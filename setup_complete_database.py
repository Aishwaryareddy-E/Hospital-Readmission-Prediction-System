"""
Complete Database Setup Script
This will:
1. Read the CSV file
2. Create the patients table in MySQL
3. Load all data into the database
4. Verify everything loaded correctly
"""

import pandas as pd
from sqlalchemy import create_engine

print("=" * 70)
print("HOSPITAL READMISSION DATABASE - COMPLETE SETUP")
print("=" * 70)

# Your MySQL credentials
mysql_password = 'Aishu935359'

try:
    # Step 1: Read the CSV file
    print("\n[Step 1] Reading hospital_data.csv...")
    df = pd.read_csv('data/hospital_data.csv')
    
    print(f"✓ CSV file loaded successfully!")
    print(f"  Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"\n  Columns found:")
    for i, col in enumerate(df.columns[:10], 1):  # Show first 10 columns
        print(f"    {i}. {col}")
    if len(df.columns) > 10:
        print(f"    ... and {len(df.columns) - 10} more columns")
    
    # Step 2: Create database connection
    print("\n[Step 2] Connecting to MySQL database...")
    engine = create_engine(f'mysql+mysqlconnector://root:{mysql_password}@localhost/hospital_db')
    print("✓ Connected to MySQL")
    
    # Step 3: Load data into MySQL
    print("\n[Step 3] Loading data into 'patients' table...")
    print("  This may take 30-60 seconds...")
    
    df.to_sql('patients', con=engine, if_exists='replace', index=False)
    
    print("✓ Data loaded successfully!")
    
    # Step 4: Verify the data
    print("\n[Step 4] Verifying data...")
    
    # Count total rows
    count_query = "SELECT COUNT(*) FROM patients"
    with engine.connect() as conn:
        result = conn.execute(count_query).fetchone()[0]
    
    print(f"✓ Total rows in database: {result:,}")
    
    # Sample some data
    sample_query = "SELECT * FROM patients LIMIT 3"
    with engine.connect() as conn:
        sample_df = pd.read_sql_query(sample_query, conn)
    
    print("\n✓ Sample data (first 3 rows):")
    print(sample_df.to_string())
    
    # Step 5: Summary
    print("\n" + "=" * 70)
    print("DATABASE SETUP COMPLETE! ✓")
    print("=" * 70)
    print(f"""
SUMMARY:
--------
✓ Database: hospital_db
✓ Table: patients
✓ Rows loaded: {result:,}
✓ Columns: {len(df.columns)}

NEXT STEPS:
-----------
1. Run Exploratory Data Analysis:
   jupyter notebook notebooks/01_eda.ipynb

2. Or run preprocessing and model training:
   python notebooks/02_preprocessing.py
   python notebooks/03_model_training.py

3. Or deploy the API:
   python api/app.py

Your data is now ready for analysis!
""")
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    print("\nTroubleshooting:")
    print("1. Make sure MySQL service is running")
    print("2. Check if password is correct: Aishu935359")
    print("3. Verify CSV file exists in data\\hospital_data.csv")
