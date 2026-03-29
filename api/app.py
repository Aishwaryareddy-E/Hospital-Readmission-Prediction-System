"""
WEEK 5 — FASTAPI DEPLOYMENT
Turning your ML model into a production-ready API

This allows any application (website, mobile app, hospital system)
to call your model and get predictions.

What is an API?
- Application Programming Interface
- Like a waiter in a restaurant - you give order, kitchen makes it, waiter brings food back
- You send patient data → API gives to model → model predicts → API sends back result

Why FastAPI?
- Modern, fast (one of the fastest Python frameworks)
- Automatic documentation (Swagger UI)
- Easy to use
- Industry standard for ML deployment
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
from typing import List, Optional

# Initialize FastAPI app
app = FastAPI(
    title="Hospital Readmission Prediction API",
    description="Predicts whether a patient will be readmitted within 30 days using advanced ML",
    version="1.0.0"
)

print("=" * 70)
print("FASTAPI APPLICATION STARTING...")
print("=" * 70)

# Load the trained model and preprocessing objects
print("\n[Step 1] Loading ML model and preprocessing objects...")
try:
    model = joblib.load('models/best_model.pkl')
    scaler = joblib.load('models/scaler.pkl')
    label_encoders = joblib.load('models/label_encoders.pkl')
    print("✓ Model loaded successfully!")
    print(f"  Model type: {type(model).__name__}")
    print("✓ Scaler loaded")
    print("✓ Label encoders loaded")
except Exception as e:
    print(f"✗ ERROR loading models: {e}")
    print("\nMake sure you have run the training notebooks first!")
    raise

# Define the expected input format
class PatientData(BaseModel):
    """
    Input model representing patient features
    
    Each field matches what the model expects:
    - age: Age group as string (e.g., "[60-70)")
    - time_in_hospital: Number of days in hospital
    - num_lab_procedures: Number of lab tests performed
    - num_procedures: Number of medical procedures
    - num_medications: Number of medications prescribed
    - number_outpatient: Outpatient visits in prior year
    - number_emergency: Emergency visits in prior year
    - number_inpatient: Inpatient visits in prior year
    - number_diagnoses: Number of diagnoses recorded
    - diabetesMed: Whether diabetes medication was prescribed ("Yes" or "No")
    """
    age: str
    time_in_hospital: int
    num_lab_procedures: int
    num_procedures: int
    num_medications: int
    number_outpatient: int
    number_emergency: int
    number_inpatient: int
    number_diagnoses: int
    diabetesMed: str


class PredictionResult(BaseModel):
    """
    Output model with prediction results
    
    Returns:
    - prediction: "YES" or "NO" for readmission
    - probability: Confidence score (0-100%)
    - risk_level: Low/Medium/High categorization
    - explanation: Brief interpretation
    """
    prediction: str
    probability: float
    risk_level: str
    explanation: str


@app.get("/")
async def root():
    """
    Root endpoint - API welcome message
    """
    return {
        "message": "Welcome to Hospital Readmission Prediction API",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "This welcome message",
            "GET /health": "Health check endpoint",
            "POST /predict": "Predict readmission risk for a single patient",
            "POST /predict-batch": "Predict readmission risk for multiple patients",
            "GET /docs": "Interactive API documentation (Swagger UI)"
        }
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    Used to verify API is running and model is loaded
    """
    return {
        "status": "healthy",
        "model_loaded": True,
        "model_type": type(model).__name__,
        "api_version": "1.0.0"
    }


@app.post("/predict", response_model=PredictionResult)
async def predict_readmission(patient: PatientData):
    """
    Predict whether a patient will be readmitted within 30 days
    
    **Request Body:**
    - Patient data including demographics, hospital stay info, and medical history
    
    **Response:**
    - prediction: YES (will be readmitted) or NO (won't be readmitted)
    - probability: Confidence score from 0% to 100%
    - risk_level: Low (<30%), Medium (30-60%), or High (>60%)
    - explanation: Human-readable interpretation
    
    **Example:**
    ```json
    {
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
    ```
    """
    
    try:
        # Step 1: Prepare the input data
        input_data = {
            'age': patient.age,
            'time_in_hospital': patient.time_in_hospital,
            'num_lab_procedures': patient.num_lab_procedures,
            'num_procedures': patient.num_procedures,
            'num_medications': patient.num_medications,
            'number_outpatient': patient.number_outpatient,
            'number_emergency': patient.number_emergency,
            'number_inpatient': patient.number_inpatient,
            'number_diagnoses': patient.number_diagnoses,
            'diabetesMed': patient.diabetesMed
        }
        
        # Convert to DataFrame
        df_input = pd.DataFrame([input_data])
        
        # Step 2: Encode categorical variables
        # Age encoding
        if 'age' in label_encoders:
            le_age = label_encoders['age']
            # Handle unseen categories
            try:
                df_input['age_encoded'] = le_age.transform(df_input['age'])
            except ValueError:
                # If age category not seen during training, use most common
                df_input['age_encoded'] = le_age.transform([le_age.classes_[0]])[0]
        
        # DiabetesMed encoding
        if 'diabetesMed' in label_encoders:
            le_diabetes = label_encoders['diabetesMed']
            try:
                df_input['diabetesMed_encoded'] = le_diabetes.transform(df_input['diabetesMed'])
            except ValueError:
                df_input['diabetesMed_encoded'] = le_diabetes.transform([le_diabetes.classes_[0]])[0]
        
        # Step 3: Select features in the correct order
        feature_columns = [
            'age_encoded', 'time_in_hospital', 'num_lab_procedures', 'num_procedures',
            'num_medications', 'number_outpatient', 'number_emergency',
            'number_inpatient', 'number_diagnoses', 'diabetesMed_encoded'
        ]
        
        X_input = df_input[feature_columns]
        
        # Step 4: Scale the features
        X_scaled = scaler.transform(X_input)
        
        # Step 5: Make prediction
        prediction = model.predict(X_scaled)[0]
        probability = model.predict_proba(X_scaled)[0][1]
        
        # Step 6: Determine risk level
        if probability < 0.3:
            risk_level = "Low"
        elif probability < 0.6:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        # Step 7: Create explanation
        prediction_text = "WILL be readmitted" if prediction == 1 else "will NOT be readmitted"
        explanation = (
            f"Based on the patient's characteristics, our model predicts they "
            f"{prediction_text} within 30 days with {probability:.1%} confidence. "
            f"Risk Level: {risk_level}. "
            f"Key factors likely influencing this prediction include emergency visits, "
            f"number of diagnoses, and medication count."
        )
        
        # Return the result
        return PredictionResult(
            prediction="YES" if prediction == 1 else "NO",
            probability=round(probability * 100, 2),
            risk_level=risk_level,
            explanation=explanation
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.post("/predict-batch")
async def predict_batch(patients: List[PatientData]):
    """
    Predict readmission risk for multiple patients at once
    
    Useful for batch processing of patient records
    
    **Returns:**
    - List of predictions with same structure as /predict endpoint
    """
    
    results = []
    
    for i, patient in enumerate(patients):
        try:
            # Reuse the single prediction logic
            input_data = {
                'age': patient.age,
                'time_in_hospital': patient.time_in_hospital,
                'num_lab_procedures': patient.num_lab_procedures,
                'num_procedures': patient.num_procedures,
                'num_medications': patient.num_medications,
                'number_outpatient': patient.number_outpatient,
                'number_emergency': patient.number_emergency,
                'number_inpatient': patient.number_inpatient,
                'number_diagnoses': patient.number_diagnoses,
                'diabetesMed': patient.diabetesMed
            }
            
            df_input = pd.DataFrame([input_data])
            
            # Encode
            if 'age' in label_encoders:
                le_age = label_encoders['age']
                try:
                    df_input['age_encoded'] = le_age.transform(df_input['age'])
                except ValueError:
                    df_input['age_encoded'] = le_age.transform([le_age.classes_[0]])[0]
            
            if 'diabetesMed' in label_encoders:
                le_diabetes = label_encoders['diabetesMed']
                try:
                    df_input['diabetesMed_encoded'] = le_diabetes.transform(df_input['diabetesMed'])
                except ValueError:
                    df_input['diabetesMed_encoded'] = le_diabetes.transform([le_diabetes.classes_[0]])[0]
            
            # Select features
            feature_columns = [
                'age_encoded', 'time_in_hospital', 'num_lab_procedures', 'num_procedures',
                'num_medications', 'number_outpatient', 'number_emergency',
                'number_inpatient', 'number_diagnoses', 'diabetesMed_encoded'
            ]
            
            X_input = df_input[feature_columns]
            X_scaled = scaler.transform(X_input)
            
            # Predict
            prediction = model.predict(X_scaled)[0]
            probability = model.predict_proba(X_scaled)[0][1]
            
            # Risk level
            if probability < 0.3:
                risk_level = "Low"
            elif probability < 0.6:
                risk_level = "Medium"
            else:
                risk_level = "High"
            
            results.append({
                "patient_id": i + 1,
                "prediction": "YES" if prediction == 1 else "NO",
                "probability": round(probability * 100, 2),
                "risk_level": risk_level
            })
            
        except Exception as e:
            results.append({
                "patient_id": i + 1,
                "error": str(e)
            })
    
    return {
        "total_patients": len(patients),
        "successful_predictions": sum(1 for r in results if "error" not in r),
        "failed_predictions": sum(1 for r in results if "error" in r),
        "results": results
    }


# Run the server
if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "=" * 70)
    print("STARTING FASTAPI SERVER...")
    print("=" * 70)
    print("""
Server will start at: http://localhost:8000

Available endpoints:
  • http://localhost:8000          - Welcome message
  • http://localhost:8000/health   - Health check
  • http://localhost:8000/predict  - Single prediction
  • http://localhost:8000/docs     - Interactive documentation (Swagger UI)
  • http://localhost:8000/redoc    - Alternative documentation (ReDoc)

To test the API:
1. Open browser and go to: http://localhost:8000/docs
2. Or use Postman to send POST requests to /predict
3. Or use the example code in test_api.py

Press CTRL+C to stop the server
""")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
