import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine('mysql+mysqlconnector://root:Aishu935359@localhost/hospital_db')

print("Verifying database setup...")
print("=" * 60)

# Count rows
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM patients")).fetchone()[0]
    print(f"✓ Total rows in patients table: {result:,}")

# Show sample data
df = pd.read_sql_query("SELECT * FROM patients LIMIT 3", engine)
print("\n✓ Sample data:")
print(df.to_string())

print("\n" + "=" * 60)
print("Database is ready!")
