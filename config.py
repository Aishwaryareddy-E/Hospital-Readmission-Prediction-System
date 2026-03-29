"""
Configuration File for Hospital Readmission Project

Update the settings below to match your system setup.
This file is imported by other scripts to avoid hardcoding passwords.
"""

# ============================================================
# DATABASE CONFIGURATION
# ============================================================

# MySQL Database Settings
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,           # Default MySQL port
    'database': 'hospital_db',
    'user': 'root',
    'password': 'Aishu935359'  # Your MySQL root password
}

# Connection string format for SQLAlchemy
def get_connection_string():
    """
    Creates MySQL connection string for SQLAlchemy
    
    Returns:
        str: Connection string in format: mysql+mysqlconnector://user:pass@host:port/database
    """
    return f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"


# ============================================================
# FILE PATHS
# ============================================================

import os

# Get absolute path to project root directory
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Data paths
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
RAW_DATA_FILE = os.path.join(DATA_DIR, 'hospital_data.csv')

# Notebook paths
NOTEBOOKS_DIR = os.path.join(PROJECT_ROOT, 'notebooks')

# API paths
API_DIR = os.path.join(PROJECT_ROOT, 'api')

# Models paths
MODELS_DIR = os.path.join(PROJECT_ROOT, 'models')

# Plots paths
PLOTS_DIR = os.path.join(PROJECT_ROOT, 'plots')

# Report paths
REPORT_DIR = os.path.join(PROJECT_ROOT, 'report')

# Dashboard paths
DASHBOARD_DIR = os.path.join(PROJECT_ROOT, 'dashboard')


# ============================================================
# MODEL CONFIGURATION
# ============================================================

# Features to use in modeling
FEATURE_COLUMNS = [
    'age_encoded', 
    'time_in_hospital', 
    'num_lab_procedures', 
    'num_procedures',
    'num_medications', 
    'number_outpatient', 
    'number_emergency',
    'number_inpatient', 
    'number_diagnoses', 
    'diabetesMed_encoded'
]

# Target variable name
TARGET_COLUMN = 'readmitted_binary'

# Test set size (20% of data)
TEST_SIZE = 0.2

# Random seed for reproducibility
RANDOM_SEED = 42

# SMOTE parameters
SMOTE_K_NEIGHBORS = 5


# ============================================================
# API CONFIGURATION
# ============================================================

# API server settings
API_HOST = '0.0.0.0'
API_PORT = 8000
API_DEBUG = False

# Risk level thresholds
RISK_THRESHOLDS = {
    'low': 0.3,      # < 30% = Low risk
    'medium': 0.6    # 30-60% = Medium risk, > 60% = High risk
}


# ============================================================
# VISUALIZATION SETTINGS
# ============================================================

# Plot settings
PLOT_DPI = 300  # Resolution for saved plots
PLOT_FORMAT = 'png'  # Can also use 'jpg', 'svg', etc.
PLOT_STYLE = 'seaborn-v0_8-darkgrid'

# Color palettes
COLOR_PALETTE = {
    'primary': '#2E86AB',
    'secondary': '#A23B72', 
    'success': '#28A745',
    'warning': '#FFC107',
    'danger': '#DC3545',
    'info': '#17A2B8'
}


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def verify_setup():
    """
    Verify that all required directories and files exist.
    
    Returns:
        bool: True if everything is set up correctly, False otherwise
    """
    import os
    
    print("Verifying project setup...")
    print("=" * 60)
    
    all_good = True
    
    # Check directories
    required_dirs = [
        DATA_DIR,
        NOTEBOOKS_DIR,
        API_DIR,
        MODELS_DIR,
        PLOTS_DIR,
        REPORT_DIR,
        DASHBOARD_DIR
    ]
    
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            print(f"✗ Missing directory: {dir_path}")
            all_good = False
        else:
            print(f"✓ Directory exists: {os.path.basename(dir_path)}")
    
    # Check critical files
    required_files = [
        RAW_DATA_FILE,
        os.path.join(NOTEBOOKS_DIR, '01_eda.ipynb'),
        os.path.join(API_DIR, 'app.py')
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"✗ Missing file: {file_path}")
            all_good = False
        else:
            print(f"✓ File exists: {os.path.basename(file_path)}")
    
    # Check database connection
    try:
        from sqlalchemy import create_engine
        engine = create_engine(get_connection_string())
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        print("✓ Database connection successful")
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        print("  → Check if MySQL is running and password is correct")
        all_good = False
    
    print("=" * 60)
    if all_good:
        print("✓ All checks passed! Setup is complete.")
    else:
        print("⚠ Some checks failed. Please fix the issues above.")
    
    return all_good


def print_project_structure():
    """
    Print the project directory structure.
    """
    import os
    
    structure = """
hospital-readmission-project/
│
├── data/                      # Data storage
│   ├── hospital_data.csv     # Raw dataset
│   └── ...                   # Processed data files
│
├── notebooks/                 # Jupyter notebooks
│   ├── 01_eda.ipynb          # Exploratory analysis
│   ├── 02_preprocessing.py   # Data preprocessing
│   ├── 03_model_training.py  # ML model training
│   └── 04_shap_analysis.py   # Model explainability
│
├── api/                       # FastAPI application
│   ├── app.py                # Main API server
│   └── test_api.py           # API testing
│
├── models/                    # Trained models
│   ├── best_model.pkl        # Best performing model
│   ├── scaler.pkl            # Feature scaler
│   └── ...                   # Other models
│
├── plots/                     # Visualizations
│   └── ...                   # Generated plots
│
├── dashboard/                 # Tableau dashboard
│   └── (Add your workbook here)
│
├── report/                    # Reports
│   ├── eda_insights.txt      # EDA findings
│   ├── shap_insights.txt     # SHAP analysis
│   └── final_report.pdf      # Final report
│
├── config.py                  # This configuration file
├── requirements.txt           # Python dependencies
├── README.md                  # Main documentation
└── QUICKSTART.md             # Quick start guide
    """
    print(structure)


# ============================================================
# MAIN (for testing configuration)
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("HOSPITAL READMISSION PROJECT - CONFIGURATION CHECK")
    print("=" * 70)
    
    # Print current configuration
    print("\nCurrent Configuration:")
    print(f"  Database: {DB_CONFIG['database']}")
    print(f"  Host: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    print(f"  User: {DB_CONFIG['user']}")
    print(f"  Password: {'*' * len(DB_CONFIG['password'])}")
    print(f"  Test Size: {TEST_SIZE}")
    print(f"  Random Seed: {RANDOM_SEED}")
    print(f"  API Port: {API_PORT}")
    
    # Verify setup
    print("\n")
    verify_setup()
    
    # Show project structure
    print("\nProject Structure:")
    print_project_structure()
    
    print("\n" + "=" * 70)
    print("Configuration check complete!")
    print("=" * 70)
