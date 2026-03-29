"""
WEEK 2, DAY 4-5 — DATA PREPROCESSING
Converting raw data into machine learning-ready format

What we do:
1. Clean the data (handle missing values)
2. Convert text to numbers (encoding)
3. Scale features (normalization)
4. Fix class imbalance (SMOTE)
5. Split into train/test sets
6. Save everything for later use
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from imblearn.over_sampling import SMOTE
import joblib
import os

# Create models directory if it doesn't exist
os.makedirs('models', exist_ok=True)

print("=" * 70)
print("DATA PREPROCESSING PIPELINE")
print("=" * 70)

# CELL 1: Connect to database
print("\n[Step 1] Connecting to MySQL database...")
engine = create_engine('mysql+mysqlconnector://root:yourpassword@localhost/hospital_db')
print("✓ Connected!")

# CELL 2: Load data
print("\n[Step 2] Loading data from MySQL...")
query = """
    SELECT * FROM patients
    WHERE readmitted IS NOT NULL
"""
df = pd.read_sql_query(query, engine)
print(f"✓ Loaded {len(df):,} rows × {len(df.columns)} columns")

# CELL 3: Drop unnecessary columns
print("\n[Step 3] Selecting relevant features...")
columns_to_keep = [
    'age', 'time_in_hospital', 'num_lab_procedures', 'num_procedures',
    'num_medications', 'number_outpatient', 'number_emergency',
    'number_inpatient', 'number_diagnoses', 'diabetesMed', 'readmitted'
]

df = df[columns_to_keep].copy()
print(f"✓ Selected {len(columns_to_keep)} important features")
print(f"  New shape: {df.shape}")

# CELL 4: Handle '?' values - replace with NaN
print("\n[Step 4] Handling '?' missing value markers...")
df = df.replace('?', np.nan)
print("✓ Replaced '?' with NaN")

missing_after = df.isnull().sum()
if missing_after.sum() > 0:
    print(f"\nMissing values after replacement:")
    print(missing_after[missing_after > 0])

# CELL 5: Convert numerical columns to proper types
print("\n[Step 5] Converting numerical columns...")
numeric_cols = ['time_in_hospital', 'num_lab_procedures', 'num_procedures',
                'num_medications', 'number_outpatient', 'number_emergency',
                'number_inpatient', 'number_diagnoses']

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

print("✓ Converted all numerical columns")

# CELL 6: Handle missing values - use median imputation
print("\n[Step 6] Imputing missing values with median...")
for col in numeric_cols:
    median_val = df[col].median()
    df[col] = df[col].fillna(median_val)
    
print("✓ Median imputation completed")
print(f"  Remaining missing values: {df.isnull().sum().sum()}")

# CELL 7: Encode target variable (YES/NO → 1/0)
print("\n[Step 7] Encoding target variable (readmitted)...")
df['readmitted_binary'] = df['readmitted'].apply(lambda x: 1 if x == 'YES' else 0)
print("✓ Target encoded: YES=1, NO=0")

target_dist = df['readmitted_binary'].value_counts()
print(f"\nTarget distribution:")
print(f"  Not Readmitted (0): {target_dist.get(0, 0):,} ({target_dist.get(0, 0)/len(df)*100:.2f}%)")
print(f"  Readmitted (1): {target_dist.get(1, 0):,} ({target_dist.get(1, 0)/len(df)*100:.2f}%)")

# CELL 8: Encode categorical features
print("\n[Step 8] Encoding categorical features...")
label_encoders = {}

# Encode age
le_age = LabelEncoder()
df['age_encoded'] = le_age.fit_transform(df['age'])
label_encoders['age'] = le_age
print(f"✓ Age encoded ({len(le_age.classes_)} unique categories)")

# Encode diabetesMed
le_diabetes = LabelEncoder()
df['diabetesMed_encoded'] = le_diabetes.fit_transform(df['diabetesMed'])
label_encoders['diabetesMed'] = le_diabetes
print(f"✓ DiabetesMed encoded ({len(le_diabetes.classes_)} unique categories)")

# Show encoding mappings
print("\nAge encoding mapping:")
for i, label in enumerate(le_age.classes_):
    print(f"  {label} → {i}")

print(f"\nDiabetesMed encoding mapping:")
for i, label in enumerate(le_diabetes.classes_):
    print(f"  {label} → {i}")

# CELL 9: Prepare final feature set
print("\n[Step 9] Preparing feature matrix...")
feature_columns = [
    'age_encoded', 'time_in_hospital', 'num_lab_procedures', 'num_procedures',
    'num_medications', 'number_outpatient', 'number_emergency',
    'number_inpatient', 'number_diagnoses', 'diabetesMed_encoded'
]

X = df[feature_columns].copy()
y = df['readmitted_binary'].copy()

print(f"✓ Feature matrix shape: {X.shape}")
print(f"✓ Target vector shape: {y.shape}")
print(f"\nFeatures:")
for i, col in enumerate(feature_columns):
    print(f"  {i+1}. {col}")

# CELL 10: Feature scaling
print("\n[Step 10] Scaling features (StandardScaler)...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled = pd.DataFrame(X_scaled, columns=feature_columns)

print("✓ Features scaled to mean=0, std=1")
print(f"\nScaled features statistics:")
print(X_scaled.describe().round(2))

# CELL 11: Train-test split
print("\n[Step 11] Splitting into training and test sets...")
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

print(f"✓ Training set: {len(X_train):,} samples ({len(X_train)/len(X)*100:.1f}%)")
print(f"✓ Test set: {len(X_test):,} samples ({len(X_test)/len(X)*100:.1f}%)")

print(f"\nTraining target distribution BEFORE SMOTE:")
train_dist = y_train.value_counts()
print(f"  Class 0 (Not Readmitted): {train_dist.get(0, 0):,} ({train_dist.get(0, 0)/len(y_train)*100:.2f}%)")
print(f"  Class 1 (Readmitted): {train_dist.get(1, 0):,} ({train_dist.get(1, 0)/len(y_train)*100:.2f}%)")
print(f"  ⚠ Imbalance ratio: {train_dist.get(0, 0)/train_dist.get(1, 1):.2f}:1")

# CELL 12: Apply SMOTE to handle class imbalance
print("\n[Step 12] Applying SMOTE to fix class imbalance...")
smote = SMOTE(random_state=42, k_neighbors=5)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

print(f"✓ SMOTE applied successfully!")
print(f"\nTraining set AFTER SMOTE:")
print(f"  Original size: {len(X_train):,} samples")
print(f"  New size: {len(X_train_resampled):,} samples")
print(f"  SMOTE added: {len(X_train_resampled) - len(X_train):,} synthetic samples")

print(f"\nTarget distribution AFTER SMOTE:")
resampled_dist = pd.Series(y_train_resampled).value_counts()
print(f"  Class 0 (Not Readmitted): {resampled_dist.get(0, 0):,} ({resampled_dist.get(0, 0)/len(y_train_resampled)*100:.2f}%)")
print(f"  Class 1 (Readmitted): {resampled_dist.get(1, 0):,} ({resampled_dist.get(1, 0)/len(y_train_resampled)*100:.2f}%)")
print(f"  ✓ Perfect balance achieved! (1:1 ratio)")

# CELL 13: Save processed data and preprocessing objects
print("\n[Step 13] Saving processed data and preprocessing objects...")

# Save scaler
joblib.dump(scaler, 'models/scaler.pkl')
print("✓ Saved: models/scaler.pkl")

# Save label encoders
joblib.dump(label_encoders, 'models/label_encoders.pkl')
print("✓ Saved: models/label_encoders.pkl")

# Save SMOTE object
joblib.dump(smote, 'models/smote.pkl')
print("✓ Saved: models/smote.pkl")

# Save datasets
X_train_resampled.to_csv('data/X_train_processed.csv', index=False)
print("✓ Saved: data/X_train_processed.csv")

X_test.to_csv('data/X_test_processed.csv', index=False)
print("✓ Saved: data/X_test_processed.csv")

pd.Series(y_train_resampled).to_csv('data/y_train_processed.csv', index=False)
print("✓ Saved: data/y_train_processed.csv")

pd.Series(y_test).to_csv('data/y_test_processed.csv', index=False)
print("✓ Saved: data/y_test_processed.csv")

# CELL 14: Final summary
print("\n" + "=" * 70)
print("PREPROCESSING COMPLETE! ✓")
print("=" * 70)

print(f"""
SUMMARY:
--------
✓ Raw data loaded: {len(df):,} patient records
✓ Missing values handled: '?' replaced with median imputation
✓ Categorical features encoded: age, diabetesMed
✓ Features scaled: All numerical features standardized
✓ Class imbalance fixed: SMOTE applied (1:1 balanced ratio)
✓ Data split: 80% training, 20% testing
✓ All objects saved for deployment

TRAINING DATA READY FOR ML MODELS:
----------------------------------
Training samples: {len(X_train_resampled):,}
Test samples: {len(X_test):,}
Features: {len(feature_columns)}
Target: Binary (0=Not Readmitted, 1=Readmitted)

NEXT STEP: Run '02_model_training.ipynb' to build ML models!
""")
