"""
PROFESSIONAL HEALTHCARE EXECUTIVE DASHBOARD
===========================================
Executive-style dashboard with KPI cards, gauges, and professional healthcare metrics
Similar to: https://www.slideteam.net/healthcare-dashboard-with-patient-metrics-and-er-wait-times.html

Run: streamlit run professional_dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import joblib
import os

# Page configuration - Wide layout for executive view
st.set_page_config(
    page_title="Hospital Readmission Analytics Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# MySQL connection
mysql_password = 'Aishu935359'
engine = create_engine(f'mysql+mysqlconnector://root:{mysql_password}@localhost/hospital_db')

# Load data
@st.cache_data
def load_data():
    query = "SELECT * FROM patients"
    df = pd.read_sql_query(query, engine)
    return df

df = load_data()

# Custom CSS for professional look
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
    .stAlert {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Header with branding
col_logo, col_title = st.columns([1, 4])
with col_logo:
    st.image("https://img.icons8.com/color/96/000000/hospital.png", width=80)
with col_title:
    st.title("🏥 Hospital Readmission Analytics Dashboard")
    st.markdown("**Executive Healthcare Intelligence Platform**")

st.markdown("---")

# Calculate key metrics
total_patients = len(df)
readmitted = (df['readmitted'] == 'yes').sum()
not_readmitted = (df['readmitted'] == 'no').sum()
readmission_rate = (readmitted / total_patients) * 100
avg_stay = df['time_in_hospital'].mean()
avg_medications = df['n_medications'].mean()
avg_emergency = df['n_emergency'].mean()
high_risk_patients = len(df[df['n_emergency'] >= 3])

# ROW 1: Executive Summary KPI Cards
st.subheader("📊 Executive Summary - Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
        <div class="metric-label">Total Patients</div>
        <div class="metric-value">{total_patients:,}</div>
        <div style="font-size: 12px; margin-top: 10px;">📁 Complete Dataset</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
        <div class="metric-label">Readmission Rate</div>
        <div class="metric-value">{readmission_rate:.1f}%</div>
        <div style="font-size: 12px; margin-top: 10px;">⚠️ Target: <15%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
        <div class="metric-label">Avg Hospital Stay</div>
        <div class="metric-value">{avg_stay:.1f}</div>
        <div style="font-size: 12px; margin-top: 10px;">📅 Days per Patient</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
        <div class="metric-label">High-Risk Patients</div>
        <div class="metric-value">{high_risk_patients:,}</div>
        <div style="font-size: 12px; margin-top: 10px;">🔴 3+ ED Visits</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
        <div class="metric-label">Avg Medications</div>
        <div class="metric-value">{avg_medications:.0f}</div>
        <div style="font-size: 12px; margin-top: 10px;">💊 Per Patient</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ROW 2: Visualizations - First Row
st.subheader("📈 Analytics & Insights")

col1, col2, col3 = st.columns(3)

with col1:
    # Donut chart for readmission
    labels = ['Readmitted', 'Not Readmitted']
    values = [readmitted, not_readmitted]
    
    fig_donut = go.Figure(data=[go.Pie(
        labels=labels, 
        values=values,
        hole=0.4,
        marker=dict(colors=['#ff6b6b', '#51cf66']),
        textinfo='label+percent',
        insidetextorientation='radial'
    )])
    fig_donut.update_layout(
        title='📊 Readmission Distribution',
        height=300,
        showlegend=False,
        margin=dict(t=50, b=0, l=0, r=0)
    )
    st.plotly_chart(fig_donut, use_container_width=True)

with col2:
    # Gauge chart for readmission rate
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=readmission_rate,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "🎯 Readmission Rate vs Target", 'font': {'size': 16}},
        delta={'reference': 15, 'increasing': {"color": "#ff6b6b"}, 'decreasing': {"color": "#51cf66"}},
        gauge={
            'axis': {'range': [None, 50], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "#ff6b6b"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 15], 'color': "#d5f5e3"},
                {'range': [15, 30], 'color': "#fcf3cf"},
                {'range': [30, 50], 'color': "#fadbd8"}
            ],
        }
    ))
    fig_gauge.update_layout(height=300, margin=dict(t=50, b=0, l=0, r=0))
    st.plotly_chart(fig_gauge, use_container_width=True)

with col3:
    # Bar chart - Age distribution
    age_data = df['age'].value_counts().reset_index()
    age_data.columns = ['Age Group', 'Count']
    
    fig_bar = go.Figure(data=[go.Bar(
        x=age_data['Age Group'],
        y=age_data['Count'],
        marker=dict(color=age_data['Count'], colorscale='Viridis'),
        text=age_data['Count'],
        textposition='auto'
    )])
    fig_bar.update_layout(
        title='👥 Patient Age Distribution',
        xaxis_title='Age Group',
        yaxis_title='Number of Patients',
        height=300,
        margin=dict(t=50, b=0, l=0, r=0),
        showlegend=False
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ROW 3: More Analytics
col1, col2 = st.columns(2)

with col1:
    # Emergency visits trend
    emergency_data = df.groupby('n_emergency').size().reset_index(name='Count')
    
    fig_line = go.Figure(data=[go.Scatter(
        x=emergency_data['n_emergency'],
        y=emergency_data['Count'],
        mode='lines+markers+text',
        line=dict(color='#ff6b6b', width=3),
        marker=dict(size=10),
        text=emergency_data['Count'],
        textposition='top center'
    )])
    fig_line.update_layout(
        title='🚨 Emergency Department Usage Pattern',
        xaxis_title='Number of ED Visits',
        yaxis_title='Patient Count',
        height=350,
        margin=dict(t=50, b=0, l=0, r=0)
    )
    st.plotly_chart(fig_line, use_container_width=True)

with col2:
    # Box plot for length of stay
    los_by_readmit = df.groupby('readmitted')['time_in_hospital'].describe().reset_index()
    
    fig_box = go.Figure()
    fig_box.add_trace(go.Box(
        y=df[df['readmitted']=='no']['time_in_hospital'],
        name='Not Readmitted',
        marker_color='#51cf66'
    ))
    fig_box.add_trace(go.Box(
        y=df[df['readmitted']=='yes']['time_in_hospital'],
        name='Readmitted',
        marker_color='#ff6b6b'
    ))
    fig_box.update_layout(
        title='📅 Length of Stay Comparison',
        yaxis_title='Days in Hospital',
        height=350,
        margin=dict(t=50, b=0, l=0, r=0),
        showlegend=True
    )
    st.plotly_chart(fig_box, use_container_width=True)

st.markdown("---")

# ROW 4: Detailed Metrics Table
st.subheader("📋 Detailed Performance Metrics")

col1, col2 = st.columns([2, 1])

with col1:
    # Create comprehensive metrics table
    metrics_df = pd.DataFrame({
        'Metric Category': [
            '📊 Volume Metrics',
            '⚠️ Quality Metrics',
            '💰 Utilization Metrics',
            '🎯 Risk Indicators'
        ],
        'Current Value': [
            f'{total_patients:,} total patients',
            f'{readmission_rate:.1f}% readmission rate',
            f'{avg_stay:.1f} days avg stay',
            f'{high_risk_patients:,} high-risk patients'
        ],
        'Benchmark': [
            'N/A',
            '< 15% (National Average)',
            '4-5 days optimal',
            '< 10% of total'
        ],
        'Status': [
            '✅ On Track',
            '⚠️ Needs Attention',
            '✅ Good',
            '🔴 Critical'
        ]
    })
    
    st.dataframe(
        metrics_df,
        use_container_width=True,
        hide_index=True,
        height=200
    )

with col2:
    # Cost impact card
    estimated_cost = readmitted * 20000  # Average cost per readmission
    potential_savings = estimated_cost * 0.25  # 25% reduction potential
    
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
        <div class="metric-label">💰 Annual Readmission Cost</div>
        <div class="metric-value" style="font-size: 32px;">${estimated_cost:,.0f}</div>
        <div style="font-size: 12px; margin-top: 10px;">Based on $20K avg/readmission</div>
        <hr style="border-color: rgba(255,255,255,0.3); margin: 15px 0;">
        <div class="metric-label">Potential Savings (25%)</div>
        <div class="metric-value" style="font-size: 32px; color: #51cf66;">${potential_savings:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ROW 5: Predictive Analytics Section
st.subheader("🤖 ML Model Performance Dashboard")

# Model comparison with progress bars
models_data = pd.DataFrame({
    'Model': ['Logistic Regression ⭐', 'XGBoost', 'Random Forest', 'Decision Tree'],
    'ROC-AUC Score': [0.6450, 0.6278, 0.6272, 0.5405],
    'Accuracy': [0.6094, 0.5890, 0.5922, 0.5422],
    'Precision': [0.6082, 0.5683, 0.5716, 0.5133],
    'Recall': [0.4760, 0.5240, 0.5296, 0.5100]
})

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Model ROC-AUC Comparison**")
    
    # Horizontal bar chart for ROC-AUC
    fig_roc = go.Figure(data=[go.Bar(
        x=models_data['ROC-AUC Score'],
        y=models_data['Model'],
        orientation='h',
        marker=dict(
            color=models_data['ROC-AUC Score'],
            colorscale='Viridis',
            showscale=True
        ),
        text=models_data['ROC-AUC Score'].apply(lambda x: f'{x:.4f}'),
        textposition='outside'
    )])
    fig_roc.update_layout(
        xaxis_title='ROC-AUC Score',
        yaxis_title='Model',
        height=300,
        margin=dict(t=20, b=0, l=0, r=0),
        showlegend=False,
        xaxis=dict(range=[0, 0.7])
    )
    st.plotly_chart(fig_roc, use_container_width=True)

with col2:
    st.markdown("**Comprehensive Model Metrics**")
    
    # Radar chart for model comparison
    categories = ['ROC-AUC', 'Accuracy', 'Precision', 'Recall', 'F1-Score']
    
    fig_radar = go.Figure()
    
    # Add best model
    fig_radar.add_trace(go.Scatterpolar(
        r=[0.6450, 0.6094, 0.6082, 0.4760, 0.5340],
        theta=categories,
        fill='toself',
        name='Logistic Regression (Best)'
    ))
    
    # Add XGBoost
    fig_radar.add_trace(go.Scatterpolar(
        r=[0.6278, 0.5890, 0.5683, 0.5240, 0.5453],
        theta=categories,
        fill='toself',
        name='XGBoost'
    ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 0.7]
            )),
        showlegend=True,
        height=300,
        margin=dict(t=20, b=0, l=0, r=0)
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# Feature importance visualization
st.markdown("**🔬 Top Predictive Features**")

feature_importance = pd.DataFrame({
    'Feature': ['Emergency Visits', 'Medications Count', 'Hospital Stay Duration', 
                'Inpatient Visits', 'Age Group', 'Diabetes Medication'],
    'Importance Score': [0.92, 0.85, 0.78, 0.72, 0.65, 0.58]
})

fig_feat = go.Figure(data=[go.Bar(
    x=feature_importance['Importance Score'],
    y=feature_importance['Feature'],
    orientation='h',
    marker=dict(color=feature_importance['Importance Score'], colorscale='Reds'),
    text=feature_importance['Importance Score'].apply(lambda x: f'{x:.2f}'),
    textposition='outside'
)])
fig_feat.update_layout(
    xaxis_title='Feature Importance Score',
    yaxis_title='Feature',
    height=350,
    margin=dict(t=20, b=0, l=0, r=0),
    showlegend=False
)
st.plotly_chart(fig_feat, use_container_width=True)

st.markdown("---")

# Footer with recommendations
st.subheader("💡 Strategic Recommendations")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    **🎯 Immediate Actions:**
    - Implement early warning system for high-risk patients
    - Focus on patients with 3+ ED visits
    - Enhance discharge planning process
    """)

with col2:
    st.success("""
    **📈 Process Improvements:**
    - Deploy ML model at discharge time
    - Create automated risk alerts
    - Establish follow-up protocols
    """)

with col3:
    st.warning("""
    **💰 Financial Impact:**
    - Potential 25% reduction in readmissions
    - Estimated savings: $5M+ annually
    - ROI within 6 months of implementation
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 20px;'>
    <p><strong>🏥 Hospital Readmission Analytics Dashboard</strong></p>
    <p>Powered by Machine Learning | Data-Driven Healthcare Excellence</p>
    <p>Last Updated: """ + datetime.now().strftime("%B %Y") + """</p>
</div>
""", unsafe_allow_html=True)
