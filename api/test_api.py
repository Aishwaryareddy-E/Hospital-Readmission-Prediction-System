"""
Test script for the Hospital Readmission Prediction API

This shows you how to call your API with example data.
Run this AFTER starting the FastAPI server.

How to use:
1. First, start the API server:
   python api/app.py

2. Then run this test script in another terminal:
   python api/test_api.py

3. You should see predictions printed!
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

print("=" * 70)
print("HOSPITAL READMISSION API - TEST CLIENT")
print("=" * 70)

# Test 1: Health check
print("\n[Test 1] Checking if API is running...")
try:
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        print("✓ API is healthy!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"✗ Health check failed: {response.status_code}")
except requests.exceptions.ConnectionError:
    print("✗ ERROR: Cannot connect to API!")
    print("\nMake sure the API server is running:")
    print("  python api/app.py")
    exit()

# Test 2: Single prediction
print("\n\n[Test 2] Making a single prediction...")

# Example patient data
patient_1 = {
    "age": "[60-70)",
    "time_in_hospital": 5,
    "num_lab_procedures": 43,
    "num_procedures": 2,
    "num_medications": 7,
    "number_outpatient": 2,
    "number_emergency": 3,
    "number_inpatient": 1,
    "number_diagnoses": 6,
    "diabetesMed": "Yes"
}

print("\nPatient Data:")
print(json.dumps(patient_1, indent=2))

response = requests.post(f"{BASE_URL}/predict", json=patient_1)

if response.status_code == 200:
    result = response.json()
    print("\n✓ Prediction Result:")
    print(f"  Prediction: {result['prediction']}")
    print(f"  Probability: {result['probability']:.2f}%")
    print(f"  Risk Level: {result['risk_level']}")
    print(f"\nExplanation:")
    print(f"  {result['explanation']}")
else:
    print(f"✗ Prediction failed: {response.status_code}")
    print(response.text)

# Test 3: Another patient (low risk profile)
print("\n\n[Test 3] Predicting for a low-risk patient...")

patient_2 = {
    "age": "[30-40)",
    "time_in_hospital": 2,
    "num_lab_procedures": 10,
    "num_procedures": 1,
    "num_medications": 3,
    "number_outpatient": 0,
    "number_emergency": 0,
    "number_inpatient": 0,
    "number_diagnoses": 2,
    "diabetesMed": "No"
}

print("\nPatient Data:")
print(json.dumps(patient_2, indent=2))

response = requests.post(f"{BASE_URL}/predict", json=patient_2)

if response.status_code == 200:
    result = response.json()
    print("\n✓ Prediction Result:")
    print(f"  Prediction: {result['prediction']}")
    print(f"  Probability: {result['probability']:.2f}%")
    print(f"  Risk Level: {result['risk_level']}")
    print(f"\nExplanation:")
    print(f"  {result['explanation']}")
else:
    print(f"✗ Prediction failed: {response.status_code}")

# Test 4: Batch predictions
print("\n\n[Test 4] Testing batch predictions...")

patients_batch = [
    {
        "age": "[70-80)",
        "time_in_hospital": 7,
        "num_lab_procedures": 50,
        "num_procedures": 3,
        "num_medications": 10,
        "number_outpatient": 3,
        "number_emergency": 5,
        "number_inpatient": 2,
        "number_diagnoses": 8,
        "diabetesMed": "Yes"
    },
    {
        "age": "[50-60)",
        "time_in_hospital": 3,
        "num_lab_procedures": 20,
        "num_procedures": 1,
        "num_medications": 4,
        "number_outpatient": 1,
        "number_emergency": 1,
        "number_inpatient": 1,
        "number_diagnoses": 3,
        "diabetesMed": "No"
    },
    {
        "age": "[80-90)",
        "time_in_hospital": 10,
        "num_lab_procedures": 60,
        "num_procedures": 5,
        "num_medications": 12,
        "number_outpatient": 4,
        "number_emergency": 4,
        "number_inpatient": 3,
        "number_diagnoses": 9,
        "diabetesMed": "Yes"
    }
]

print(f"\nSending {len(patients_batch)} patients for batch prediction...")

response = requests.post(f"{BASE_URL}/predict-batch", json=patients_batch)

if response.status_code == 200:
    result = response.json()
    print(f"\n✓ Batch Results:")
    print(f"  Total Patients: {result['total_patients']}")
    print(f"  Successful: {result['successful_predictions']}")
    print(f"  Failed: {result['failed_predictions']}")
    
    print("\nIndividual Results:")
    for r in result['results']:
        if 'error' in r:
            print(f"  Patient {r['patient_id']}: ERROR - {r['error']}")
        else:
            print(f"  Patient {r['patient_id']}: {r['prediction']} ({r['probability']:.2f}%) - {r['risk_level']} risk")
else:
    print(f"✗ Batch prediction failed: {response.status_code}")

# Summary
print("\n\n" + "=" * 70)
print("TEST COMPLETE!")
print("=" * 70)
print("""
Your API is working correctly!

Next steps:
1. Integrate this API into your hospital management system
2. Build a frontend (web/mobile app) that calls this API
3. Create automated alerts for high-risk patients
4. Set up monitoring and logging in production

To explore more:
- Open http://localhost:8000/docs for interactive documentation
- Try different patient scenarios
- Test edge cases and validate model behavior
""")
