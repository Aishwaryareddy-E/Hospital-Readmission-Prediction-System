-- ============================================================
-- QUICK START - MySQL Database Setup
-- Copy and paste these commands into MySQL Workbench
-- ============================================================

-- Step 1: Create the database
CREATE DATABASE IF NOT EXISTS hospital_db;

-- Step 2: Use the database
USE hospital_db;

-- Step 3: Create the patients table
CREATE TABLE patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    age VARCHAR(20),
    time_in_hospital INT,
    num_lab_procedures INT,
    num_procedures INT,
    num_medications INT,
    number_outpatient INT,
    number_emergency INT,
    number_inpatient INT,
    number_diagnoses INT,
    diabetesMed VARCHAR(5),
    readmitted VARCHAR(5)
);

-- Step 4: Verify table was created
DESCRIBE patients;

-- Step 5: Check how many rows (should be 0 initially)
SELECT COUNT(*) FROM patients;

-- After running this file, run load_data.py to populate the table
-- ============================================================
