"""
MySQL Database Setup and Verification Script
This will:
1. Test MySQL connection with your password
2. Create the database if it doesn't exist
3. Verify everything is working
"""

import mysql.connector
from mysql.connector import Error

print("=" * 70)
print("MYSQL CONNECTION TEST")
print("=" * 70)

# Your MySQL credentials
mysql_password = 'Aishu935359'

try:
    # Step 1: Connect to MySQL server (without specifying database)
    print("\n[Step 1] Connecting to MySQL server...")
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password=mysql_password
    )
    
    if connection.is_connected():
        print("✓ SUCCESS! Connected to MySQL server")
        
        # Get server info
        db_info = connection.get_server_info()
        print(f"  MySQL Server Version: {db_info}")
        
        # Step 2: Create database if it doesn't exist
        print("\n[Step 2] Creating hospital_db database...")
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS hospital_db")
        print("✓ Database 'hospital_db' created (or already exists)")
        
        # Step 3: Use the database
        print("\n[Step 3] Selecting hospital_db database...")
        cursor.execute("USE hospital_db")
        print("✓ Using database: hospital_db")
        
        # Step 4: Check if patients table exists
        print("\n[Step 4] Checking for patients table...")
        cursor.execute("SHOW TABLES LIKE 'patients'")
        result = cursor.fetchone()
        
        if result:
            print("✓ Table 'patients' already exists")
            
            # Count rows
            cursor.execute("SELECT COUNT(*) FROM patients")
            count = cursor.fetchone()[0]
            print(f"  Rows in table: {count:,}")
            
            if count == 0:
                print("\n⚠ Table is EMPTY - Need to load data from CSV")
            else:
                print("\n✓ Data already loaded!")
        else:
            print("⊠ Table 'patients' does not exist yet")
            print("\nNext step: Run setup_database.sql to create the table structure")
        
        cursor.close()
        connection.close()
        print("\n" + "=" * 70)
        print("MYSQL CONNECTION TEST COMPLETE ✓")
        print("=" * 70)
        
except Error as e:
    print(f"\n✗ ERROR connecting to MySQL: {e}")
    print("\nTroubleshooting:")
    print("1. Make sure MySQL service is running")
    print("   - Press Win+R, type: services.msc")
    print("   - Look for MySQL80 service")
    print("   - Right-click → Start (if not running)")
    print("\n2. Verify password is correct: Aishu935359")
    print("\n3. Check if MySQL is installed correctly")
    print("   - Open MySQL Workbench")
    print("   - Try connecting with root and your password")
