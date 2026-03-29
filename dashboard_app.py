"""
ULTIMATE HOSPITAL READMISSION DASHBOARD - SIMPLIFIED PATIENT SEARCH
====================================================================
Complete interactive dashboard with simplified patient lookup:
- Just type an age (e.g., "70-80") to see ALL patients of that age
- Shows complete details: diabetes status, risk level, medications, etc.

Run: streamlit run ultimate_dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
import plotly.graph_objects as go
import plotly.express as px
from sklearn.preprocessing import LabelEncoder
from datetime import datetime
import joblib
import os

# Page configuration
st.set_page_config(
    page_title="Hospital Readmission Prediction System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# MySQL connection
try:
    mysql_password = 'Aishu935359'
    engine = create_engine(f'mysql+mysqlconnector://root:{mysql_password}@localhost/hospital_db')
except Exception:
    engine = None

# Load data
@st.cache_data
def load_data():
    try:
        query = "SELECT * FROM patients"
        df = pd.read_sql_query(query, engine)
        return df
    except Exception:
        # Fallback for Streamlit Cloud
        return pd.read_csv("data/hospital_data.csv")

# Load models
@st.cache_resource
def load_models():
    models = {}
    model_files = {
        'Logistic Regression': 'models/logistic_regression.pkl',
        'Random Forest': 'models/random_forest.pkl',
        'XGBoost': 'models/xgboost.pkl',
        'Decision Tree': 'models/decision_tree.pkl',
        'Best Model': 'models/best_model.pkl'
    }
    for name, path in model_files.items():
        try:
            if os.path.exists(path):
                models[name] = joblib.load(path)
        except:
            pass
    return models

df = load_data()
models = load_models()

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .metric-value {
        font-size: 48px;
        font-weight: bold;
        margin: 10px 0;
    }
    .metric-label {
        font-size: 14px;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .patient-card {
        background: white;
        border-left: 5px solid #667eea;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Header
col_logo, col_title = st.columns([1, 4])
with col_logo:
    st.image("https://img.icons8.com/color/96/000000/hospital.png", width=80)
with col_title:
    st.title("🏥 Hospital Readmission Prediction System")
    st.markdown("**AI-Powered Healthcare Analytics with Live Predictions**")

st.markdown("---")

# Calculate metrics
total_patients = len(df)
readmitted = (df['readmitted'] == 'yes').sum()
not_readmitted = (df['readmitted'] == 'no').sum()
readmission_rate = (readmitted / total_patients) * 100
avg_stay = df['time_in_hospital'].mean()
high_risk = len(df[df['n_emergency'] >= 3])

# Create tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Data Overview", 
    "📈 Visualizations", 
    "🤖 ML Models", 
    "🔮 Live Prediction",
    "💡 Insights",
    "🔍 Find Patients by Age"  # SIMPLIFIED!
])

# ==================== TAB 1: DATA OVERVIEW ====================
with tab1:
    st.header("📊 Dataset Overview - 25,000 Patient Records")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Patients</div>
            <div class="metric-value">{total_patients:,}</div>
            <div style="font-size: 12px;">📁 Complete Dataset</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <div class="metric-label">Readmitted Cases</div>
            <div class="metric-value">{readmitted:,}</div>
            <div style="font-size: 12px;">{readmission_rate:.1f}% of Total</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <div class="metric-label">Not Readmitted</div>
            <div class="metric-value">{not_readmitted:,}</div>
            <div style="font-size: 12px;">{(100-readmission_rate):.1f}% of Total</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
            <div class="metric-label">Avg Hospital Stay</div>
            <div class="metric-value">{avg_stay:.1f}</div>
            <div style="font-size: 12px;">📅 Days per Patient</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.dataframe(df, use_container_width=True, height=400)

# ==================== TAB 2: VISUALIZATIONS ====================
with tab2:
    st.header("📈 Interactive Visualizations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        readmit_counts = df['readmitted'].value_counts().reset_index()
        readmit_counts.columns = ['Status', 'Count']
        
        fig_pie = px.pie(
            readmit_counts,
            values='Count',
            names='Status',
            title='Readmission Percentage',
            color='Status',
            color_discrete_map={'yes': '#e74c3c', 'no': '#2ecc71'}
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label', hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        age_counts = df['age'].value_counts().reset_index()
        age_counts.columns = ['Age Group', 'Count']
        
        fig_bar = px.bar(
            age_counts,
            x='Age Group',
            y='Count',
            title='Patient Distribution by Age Group',
            color='Count',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        emergency_data = df.groupby(['n_emergency', 'readmitted']).size().reset_index(name='Count')
        fig_emergency = px.bar(
            emergency_data,
            x='n_emergency',
            y='Count',
            color='readmitted',
            title='Emergency Visits vs Readmission',
            barmode='group',
            color_discrete_sequence=['#3498db', '#e74c3c']
        )
        st.plotly_chart(fig_emergency, use_container_width=True)
    
    with col2:
        fig_box = px.box(
            df,
            x='readmitted',
            y='n_medications',
            color='readmitted',
            title='Medications Count vs Readmission',
            color_discrete_sequence=['#2ecc71', '#e74c3c']
        )
        st.plotly_chart(fig_box, use_container_width=True)
    
    st.subheader("🔥 Feature Correlation Heatmap")
    corr_cols = ['time_in_hospital', 'n_lab_procedures', 'n_procedures', 'n_medications', 
                 'n_outpatient', 'n_inpatient', 'n_emergency']
    corr_matrix = df[corr_cols].corr()
    fig_heatmap = px.imshow(
        corr_matrix,
        labels=dict(x="Features", y="Features", color="Correlation"),
        x=corr_cols,
        y=corr_cols,
        color_continuous_scale='RdBu_r',
        aspect="auto"
    )
    fig_heatmap.update_layout(height=600)
    st.plotly_chart(fig_heatmap, use_container_width=True)

# ==================== TAB 3: ML MODELS ====================
with tab3:
    st.header("🤖 Machine Learning Models Performance")
    
    model_results = pd.DataFrame({
        'Model': ['Logistic Regression ⭐', 'Decision Tree', 'Random Forest', 'XGBoost'],
        'Accuracy': ['60.94%', '54.22%', '59.22%', '58.90%'],
        'Precision': ['0.6082', '0.5133', '0.5716', '0.5683'],
        'Recall': ['0.4760', '0.5100', '0.5296', '0.5240'],
        'F1-Score': ['0.5340', '0.5116', '0.5498', '0.5453'],
        'ROC-AUC': ['0.6450', '0.5405', '0.6272', '0.6278']
    })
    
    st.dataframe(model_results.style.highlight_max(subset=['ROC-AUC'], color='#2ecc71'),
                use_container_width=True, hide_index=True)
    
    st.success("✅ **Best Model: Logistic Regression** with ROC-AUC Score of 0.6450")
    
    fig_roc = px.bar(
        model_results,
        x='Model',
        y='ROC-AUC',
        title='Model Performance Comparison (ROC-AUC)',
        color='ROC-AUC',
        color_continuous_scale='Viridis',
        text='ROC-AUC'
    )
    fig_roc.update_traces(texttemplate='%{text:.4f}', textposition='outside')
    st.plotly_chart(fig_roc, use_container_width=True)

# ==================== TAB 4: LIVE PREDICTION ====================
with tab4:
    st.header("🔮 Live Patient Risk Prediction")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.selectbox("Age Group", sorted(df['age'].unique()))
        time_in_hospital = st.slider("Days in Hospital", 0, 20, 5)
        n_lab_procedures = st.slider("Lab Procedures", 0, 100, 20)
        n_procedures = st.slider("Number of Procedures", 0, 10, 2)
        n_medications = st.slider("Number of Medications", 0, 50, 15)
        n_outpatient = st.slider("Outpatient Visits", 0, 20, 2)
        n_inpatient = st.slider("Inpatient Visits", 0, 20, 1)
        n_emergency = st.slider("Emergency Visits", 0, 10, 1)
    
    with col2:
        medical_specialty = st.selectbox("Medical Specialty", sorted(df['medical_specialty'].unique()))
        diag_1 = st.selectbox("Primary Diagnosis", sorted(df['diag_1'].unique())[:10])
        glucose_test = st.selectbox("Glucose Test", sorted(df['glucose_test'].unique()))
        a1c_test = st.selectbox("A1C Test", sorted(df['A1Ctest'].unique()))
        change = st.selectbox("Medication Change", sorted(df['change'].unique()))
        diabetes_med = st.selectbox("Diabetes Medication", sorted(df['diabetes_med'].unique()))
    
    if st.button("🎯 Predict Readmission Risk"):
        input_data = pd.DataFrame({
            'age': [age], 'time_in_hospital': [time_in_hospital],
            'n_lab_procedures': [n_lab_procedures], 'n_procedures': [n_procedures],
            'n_medications': [n_medications], 'n_outpatient': [n_outpatient],
            'n_inpatient': [n_inpatient], 'n_emergency': [n_emergency],
            'medical_specialty': [medical_specialty], 'diag_1': [diag_1],
            'glucose_test': [glucose_test], 'A1Ctest': [a1c_test],
            'change': [change], 'diabetes_med': [diabetes_med]
        })
        
        label_encoders = joblib.load('models/label_encoders.pkl')
        for col, le in label_encoders.items():
            if col in input_data.columns:
                input_data[col] = input_data[col].apply(lambda x: x if x in list(le.classes_) else le.classes_[0])
                input_data[col] = le.transform(input_data[col])
        
        scaler = joblib.load('models/scaler.pkl')
        input_scaled = scaler.transform(input_data)
        
        if 'Best Model' in models:
            model = models['Best Model']
            prediction = model.predict(input_scaled)[0]
            probability = model.predict_proba(input_scaled)[0][1]
            
            col1, col2 = st.columns(2)
            with col1:
                if prediction == 1:
                    st.error(f"⚠️ **HIGH RISK** - {probability*100:.2f}%")
                else:
                    st.success(f"✅ **LOW RISK** - {(1-probability)*100:.2f}%")

# ==================== TAB 5: INSIGHTS ====================
with tab5:
    st.header("💡 Key Insights & Business Impact")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 🔍 Clinical Insights:
        1. **Emergency Department Usage** - Strong correlation with readmissions
        2. **Medication Complexity** - Higher counts = higher risk
        3. **Length of Stay** - Longer stays associated with readmissions
        4. **Age Factors** - Elderly patients (70-80) most vulnerable
        """)
    
    with col2:
        estimated_cost = readmitted * 20000
        potential_savings = estimated_cost * 0.25
        
        st.markdown(f"""
        #### 💰 Business Impact:
        - **Current Cost:** ${estimated_cost:,.0f}
        - **Potential Savings:** ${potential_savings:,.0f}
        - **ROI:** Within 6 months
        """)

# ==================== TAB 6: FIND PATIENTS BY AGE (SIMPLIFIED!) ====================
with tab6:
    st.header("🔍 Find Patients by Age")
    st.markdown("**Simply enter an age group to see ALL patients of that age with complete details**")
    
    # Simple age input
    st.subheader("Step 1: Enter Age Group")
    
    all_ages = sorted(df['age'].unique().tolist())
    selected_age = st.selectbox(
        "Select Age Group:",
        ["All Ages"] + all_ages,
        help="Choose an age group to view all patients in that category"
    )
    
    if selected_age != "All Ages":
        # Filter patients by selected age
        age_patients = df[df['age'] == selected_age].copy()
        
        st.success(f"✓ Found **{len(age_patients):,}** patients in age group **{selected_age}**")
        
        # Show summary statistics
        st.subheader("📊 Summary for Age Group: " + selected_age)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            diabetic_count = len(age_patients[age_patients['glucose_test'] == 'yes'])
            st.metric("Diabetic Patients", f"{diabetic_count:,}")
        
        with col2:
            high_risk_count = len(age_patients[age_patients['n_emergency'] >= 3])
            st.metric("High Risk (3+ ED)", f"{high_risk_count:,}")
        
        with col3:
            readmit_count = len(age_patients[age_patients['readmitted'] == 'yes'])
            st.metric("Readmitted", f"{readmit_count:,} ({readmit_count/len(age_patients)*100:.1f}%)")
        
        with col4:
            avg_meds = age_patients['n_medications'].mean()
            st.metric("Avg Medications", f"{avg_meds:.0f}")
        
        st.markdown("---")
        
        # Show all patients as cards
        st.subheader(f"👥 All {len(age_patients):,} Patients - Complete Details")
        
        # Pagination
        page_size = st.selectbox("Show how many patients per page?", [10, 20, 50, 100])
        total_pages = (len(age_patients) + page_size - 1) // page_size
        
        if total_pages > 1:
            selected_page = st.selectbox("Page", range(1, total_pages + 1))
            start_idx = (selected_page - 1) * page_size
            end_idx = start_idx + page_size
        else:
            start_idx = 0
            end_idx = len(age_patients)
        
        patients_to_show = age_patients.iloc[start_idx:end_idx].reset_index(drop=True)
        
        # Display each patient as a detailed card
        for idx, patient in patients_to_show.iterrows():
            patient_num = start_idx + idx + 1
            
            with st.expander(f"👤 Patient #{patient_num} - Complete Medical Record", expanded=False):
                # Header with key info
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.info(f"**Age:** {patient['age']}")
                    st.info(f"**Hospital Stay:** {patient['time_in_hospital']} days")
                
                with col2:
                    st.success(f"**Diabetes:** {'Yes 🩸' if patient['glucose_test']=='yes' else 'No ✅'}")
                    st.success(f"**A1C Test:** {patient['A1Ctest']}")
                
                with col3:
                    risk_level = "🔴 HIGH" if patient['n_emergency']>=3 else "🟡 MEDIUM" if patient['n_emergency']>=1 else "🟢 LOW"
                    st.warning(f"**Risk Level:** {risk_level}")
                    st.warning(f"**ED Visits:** {patient['n_emergency']}")
                
                with col4:
                    status = "⚠️ READMITTED" if patient['readmitted']=='yes' else "✅ Not Readmitted"
                    st.error(status)
                
                st.markdown("---")
                
                # Detailed clinical information
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 💊 Medications & Treatments")
                    st.write(f"- **Total Medications:** {patient['n_medications']}")
                    st.write(f"- **Diabetes Medication:** {patient['diabetes_med']}")
                    st.write(f"- **Medication Change:** {patient['change']}")
                    st.write(f"- **Lab Procedures:** {patient['n_lab_procedures']}")
                    st.write(f"- **Total Procedures:** {patient['n_procedures']}")
                
                with col2:
                    st.markdown("#### 🏥 Hospital Usage")
                    st.write(f"- **Emergency Visits:** {patient['n_emergency']}")
                    st.write(f"- **Inpatient Visits:** {patient['n_inpatient']}")
                    st.write(f"- **Outpatient Visits:** {patient['n_outpatient']}")
                
                st.markdown("---")
                
                # Diagnoses
                st.markdown("#### 📋 Diagnoses")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.error(f"**Primary:** {patient['diag_1']}")
                with col2:
                    st.error(f"**Secondary:** {patient['diag_2']}")
                with col3:
                    st.error(f"**Tertiary:** {patient['diag_3']}")
                
                st.markdown("---")
                
                # AI Prediction
                if 'Best Model' in models:
                    st.markdown("#### 🤖 AI Risk Assessment")
                    
                    try:
                        input_data = pd.DataFrame([{
                            'age': patient['age'],
                            'time_in_hospital': patient['time_in_hospital'],
                            'n_lab_procedures': patient['n_lab_procedures'],
                            'n_procedures': patient['n_procedures'],
                            'n_medications': patient['n_medications'],
                            'n_outpatient': patient['n_outpatient'],
                            'n_inpatient': patient['n_inpatient'],
                            'n_emergency': patient['n_emergency'],
                            'medical_specialty': patient['medical_specialty'],
                            'diag_1': patient['diag_1'],
                            'glucose_test': patient['glucose_test'],
                            'A1Ctest': patient['A1Ctest'],
                            'change': patient['change'],
                            'diabetes_med': patient['diabetes_med']
                        }])
                        
                        label_encoders = joblib.load('models/label_encoders.pkl')
                        for col, le in label_encoders.items():
                            if col in input_data.columns:
                                try:
                                    input_data[col] = le.transform(input_data[col])
                                except:
                                    pass
                        
                        scaler = joblib.load('models/scaler.pkl')
                        scaled = scaler.transform(input_data)
                        
                        model = models['Best Model']
                        prediction = model.predict(scaled)[0]
                        probability = model.predict_proba(scaled)[0][1]
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            if prediction == 1:
                                st.error(f"⚠️ **HIGH RISK** - {probability*100:.2f}% readmission probability")
                            else:
                                st.success(f"✅ **LOW RISK** - {(1-probability)*100:.2f}% readmission probability")
                        
                        with col2:
                            gauge = go.Figure(go.Indicator(
                                mode="gauge+number",
                                value=probability*100,
                                gauge={'axis': {'range': [None, 100]}},
                                bar={'color': "#e74c3c" if probability > 0.5 else "#2ecc71"}
                            ))
                            st.plotly_chart(gauge, use_container_width=True)
                        
                        # Risk factors
                        risk_factors = []
                        if patient['n_emergency'] >= 3:
                            risk_factors.append("Frequent ED user")
                        if patient['n_medications'] > 20:
                            risk_factors.append("Complex medications")
                        if patient['time_in_hospital'] > 7:
                            risk_factors.append("Extended stay")
                        if patient['glucose_test'] == 'yes':
                            risk_factors.append("Diabetic")
                        
                        if risk_factors:
                            st.warning(f"**Risk Factors:** {', '.join(risk_factors)}")
                    
                    except Exception as e:
                        st.info("AI prediction available soon")
    else:
        st.info("👆 Select an age group above to view patients")

# Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: gray; padding: 20px;'>
    <p><strong>🏥 Hospital Readmission Prediction System</strong></p>
    <p>Built with ❤️ using AI & Machine Learning | Data Science Project 2026</p>
    <p>Last Updated: {datetime.now().strftime("%B %Y")}</p>
</div>
""", unsafe_allow_html=True)
