-- ============================================================
-- WEEK 1, DAY 4 - Learning Your Data Through SQL
-- Each query answers a specific business question
-- Write down insights after each query in your notebook
-- ============================================================

-- QUERY 1: How many patients got readmitted?
-- This is the most basic question — what is the readmission rate overall?
SELECT 
    readmitted, 
    COUNT(*) as total_patients,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM patients), 2) as percentage
FROM patients
GROUP BY readmitted;

-- INSIGHT SPACE: What % of patients get readmitted?
-- If it is around 11-12%, that means the dataset is imbalanced
-- (Many more NO than YES) — this tells you SMOTE will be needed later


-- QUERY 2: Which age group has the highest readmission count?
SELECT 
    age, 
    COUNT(*) as total_patients,
    SUM(CASE WHEN readmitted = 'YES' THEN 1 ELSE 0 END) as readmitted_count,
    ROUND(SUM(CASE WHEN readmitted = 'YES' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as readmission_rate
FROM patients
GROUP BY age
ORDER BY readmission_rate DESC;

-- INSIGHT SPACE: Do older patients have higher readmission rates?
-- Business insight example: "Patients aged 70-80 have highest readmission rate of X%"


-- QUERY 3: Does longer hospital stay lead to more readmissions?
SELECT 
    readmitted,
    ROUND(AVG(time_in_hospital), 2) as avg_days_in_hospital,
    ROUND(AVG(num_medications), 2) as avg_medications,
    ROUND(AVG(number_diagnoses), 2) as avg_diagnoses
FROM patients
GROUP BY readmitted;

-- INSIGHT SPACE: Do readmitted patients stay longer? Take more medications?
-- This helps you understand which features will be good predictors


-- QUERY 4: Find the highest risk patients
-- These are patients with many emergency visits AND many inpatient stays AND many diagnoses
SELECT 
    age,
    readmitted,
    number_emergency,
    number_inpatient,
    number_diagnoses,
    num_medications
FROM patients
WHERE number_emergency >= 3 
    AND number_inpatient >= 3 
    AND number_diagnoses >= 5
ORDER BY number_emergency DESC, number_diagnoses DESC
LIMIT 20;

-- INSIGHT SPACE: What patterns do high-risk patients share?
-- This identifies your target population for intervention


-- QUERY 5: Impact of diabetes medication on readmission
SELECT 
    diabetesMed,
    COUNT(*) as total_patients,
    SUM(CASE WHEN readmitted = 'YES' THEN 1 ELSE 0 END) as readmitted_count,
    ROUND(SUM(CASE WHEN readmitted = 'YES' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as readmission_rate
FROM patients
GROUP BY diabetesMed;

-- INSIGHT SPACE: Does diabetes medication affect readmission rates?
-- This could be an important feature for your model


-- QUERY 6: Emergency visits impact analysis
SELECT 
    CASE 
        WHEN number_emergency = 0 THEN 'No Emergency Visits'
        WHEN number_emergency BETWEEN 1 AND 2 THEN '1-2 Emergency Visits'
        WHEN number_emergency BETWEEN 3 AND 5 THEN '3-5 Emergency Visits'
        ELSE '6+ Emergency Visits'
    END as emergency_category,
    COUNT(*) as total_patients,
    SUM(CASE WHEN readmitted = 'YES' THEN 1 ELSE 0 END) as readmitted_count,
    ROUND(SUM(CASE WHEN readmitted = 'YES' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as readmission_rate
FROM patients
GROUP BY emergency_category
ORDER BY readmission_rate DESC;

-- INSIGHT SPACE: Clear correlation between emergency visits and readmission
-- This will likely be one of your most important features


-- QUERY 7: Number of diagnoses distribution
SELECT 
    CASE 
        WHEN number_diagnoses BETWEEN 1 AND 3 THEN 'Low (1-3)'
        WHEN number_diagnoses BETWEEN 4 AND 6 THEN 'Medium (4-6)'
        WHEN number_diagnoses BETWEEN 7 AND 9 THEN 'High (7-9)'
        ELSE 'Very High (10+)'
    END as diagnosis_category,
    COUNT(*) as total_patients,
    SUM(CASE WHEN readmitted = 'YES' THEN 1 ELSE 0 END) as readmitted_count,
    ROUND(SUM(CASE WHEN readmitted = 'YES' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as readmission_rate
FROM patients
GROUP BY diagnosis_category
ORDER BY readmission_rate DESC;

-- INSIGHT SPACE: More diagnoses = higher readmission risk?
-- This validates our hypothesis about complexity of care


-- QUERY 8: Gender distribution (if available in your dataset)
-- Uncomment if your dataset has this column
-- SELECT 
--     gender,
--     COUNT(*) as total_patients,
--     SUM(CASE WHEN readmitted = 'YES' THEN 1 ELSE 0 END) as readmitted_count,
--     ROUND(SUM(CASE WHEN readmitted = 'YES' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as readmission_rate
-- FROM patients
-- GROUP BY gender;


-- QUERY 9: Payer code analysis (if available)
-- Shows which insurance types have highest readmission
-- SELECT 
--     payer_code,
--     COUNT(*) as total_patients,
--     SUM(CASE WHEN readmitted = 'YES' THEN 1 ELSE 0 END) as readmitted_count,
--     ROUND(SUM(CASE WHEN readmitted = 'YES' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as readmission_rate
-- FROM patients
-- GROUP BY payer_code
-- ORDER BY readmission_rate DESC;


-- QUERY 10: Medical specialty analysis (if available)
-- Which specialties see most readmissions
-- SELECT 
--     medical_specialty,
--     COUNT(*) as total_patients,
--     SUM(CASE WHEN readmitted = 'YES' THEN 1 ELSE 0 END) as readmitted_count,
--     ROUND(SUM(CASE WHEN readmitted = 'YES' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as readmission_rate
-- FROM patients
-- WHERE medical_specialty IS NOT NULL AND medical_specialty != '?'
-- GROUP BY medical_specialty
-- ORDER BY readmitted_count DESC
-- LIMIT 20;
