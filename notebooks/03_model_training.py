"""
WEEK 3 — MACHINE LEARNING MODEL TRAINING
Training multiple models and comparing their performance

Models we will train:
1. Logistic Regression (baseline)
2. Decision Tree
3. Random Forest
4. XGBoost (most powerful)
5. Support Vector Machine (optional)

We will:
- Train each model on our preprocessed data
- Evaluate using accuracy, precision, recall, F1-score
- Compare ROC-AUC scores
- Select the best model
- Save it for deployment
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.svm import SVC
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                             f1_score, roc_auc_score, classification_report, 
                             confusion_matrix)
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
import os

# Create models directory if it doesn't exist
os.makedirs('models', exist_ok=True)

print("=" * 70)
print("MACHINE LEARNING MODEL TRAINING")
print("=" * 70)

# CELL 1: Load preprocessed data
print("\n[Step 1] Loading preprocessed data...")
X_train = pd.read_csv('data/X_train_processed.csv')
X_test = pd.read_csv('data/X_test_processed.csv')
y_train = pd.read_csv('data/y_train_processed.csv').squeeze()
y_test = pd.read_csv('data/y_test_processed.csv').squeeze()

print(f"✓ Training data: {X_train.shape}")
print(f"✓ Test data: {X_test.shape}")

# CELL 2: Define models to compare
print("\n[Step 2] Initializing machine learning models...")

models = {
    'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000, n_jobs=-1),
    'Decision Tree': DecisionTreeClassifier(random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
    'XGBoost': XGBClassifier(n_estimators=100, random_state=42, n_jobs=-1, use_label_encoder=False, eval_metric='logloss')
}

print("✓ Models initialized:")
for name in models.keys():
    print(f"  - {name}")

# CELL 3: Train and evaluate each model
print("\n[Step 3] Training and evaluating models...\n")

results = []

for name, model in models.items():
    print(f"{'='*70}")
    print(f"Training: {name}")
    print(f"{'='*70}")
    
    # Train the model
    print("  Training...", end=" ")
    model.fit(X_train, y_train)
    print("✓")
    
    # Make predictions
    print("  Predicting on test set...", end=" ")
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    print("✓")
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba)
    
    print(f"\n  Results:")
    print(f"    Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"    Precision: {precision:.4f} ({precision*100:.2f}%)")
    print(f"    Recall:    {recall:.4f} ({recall*100:.2f}%)")
    print(f"    F1-Score:  {f1:.4f} ({f1*100:.2f}%)")
    print(f"    ROC-AUC:   {roc_auc:.4f} ({roc_auc*100:.2f}%)")
    
    # Store results
    results.append({
        'Model': name,
        'Accuracy': accuracy,
        'Precision': precision,
        'Recall': recall,
        'F1-Score': f1,
        'ROC-AUC': roc_auc,
        'Model_Object': model,
        'Predictions': y_pred,
        'Predictions_Proba': y_pred_proba
    })
    
    print()

# CELL 4: Create comparison dataframe
print("\n[Step 4] Creating model comparison table...")
results_df = pd.DataFrame(results)
comparison_df = results_df[['Model', 'Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC']]

print("\n" + "=" * 70)
print("MODEL COMPARISON TABLE")
print("=" * 70)
print(comparison_df.to_string(index=False))

# CELL 5: Visualize model performance
print("\n\n[Step 5] Creating visualization plots...")

# Bar chart comparison
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# Accuracy comparison
axes[0, 0].barh(comparison_df['Model'], comparison_df['Accuracy'], color='steelblue', edgecolor='black')
axes[0, 0].set_xlabel('Accuracy', fontsize=12)
axes[0, 0].set_title('Model Accuracy Comparison', fontsize=14, fontweight='bold')
axes[0, 0].set_xlim([0, 1])
for i, v in enumerate(comparison_df['Accuracy']):
    axes[0, 0].text(v + 0.01, i, f'{v:.4f}', va='center', fontsize=10, fontweight='bold')

# ROC-AUC comparison
axes[0, 1].barh(comparison_df['Model'], comparison_df['ROC-AUC'], color='coral', edgecolor='black')
axes[0, 1].set_xlabel('ROC-AUC Score', fontsize=12)
axes[0, 1].set_title('Model ROC-AUC Comparison', fontsize=14, fontweight='bold')
axes[0, 1].set_xlim([0, 1])
for i, v in enumerate(comparison_df['ROC-AUC']):
    axes[0, 1].text(v + 0.01, i, f'{v:.4f}', va='center', fontsize=10, fontweight='bold')

# F1-Score comparison
axes[1, 0].barh(comparison_df['Model'], comparison_df['F1-Score'], color='green', edgecolor='black')
axes[1, 0].set_xlabel('F1-Score', fontsize=12)
axes[1, 0].set_title('Model F1-Score Comparison', fontsize=14, fontweight='bold')
axes[1, 0].set_xlim([0, 1])
for i, v in enumerate(comparison_df['F1-Score']):
    axes[1, 0].text(v + 0.01, i, f'{v:.4f}', va='center', fontsize=10, fontweight='bold')

# Recall comparison
axes[1, 1].barh(comparison_df['Model'], comparison_df['Recall'], color='purple', edgecolor='black')
axes[1, 1].set_xlabel('Recall', fontsize=12)
axes[1, 1].set_title('Model Recall Comparison', fontsize=14, fontweight='bold')
axes[1, 1].set_xlim([0, 1])
for i, v in enumerate(comparison_df['Recall']):
    axes[1, 1].text(v + 0.01, i, f'{v:.4f}', va='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('plots/model_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Saved: plots/model_comparison.png")
plt.show()

# CELL 6: Identify best model
print("\n[Step 6] Identifying best performing model...")
best_model_idx = results_df['ROC-AUC'].idxmax()
best_model_info = results_df.loc[best_model_idx]

print(f"\n🏆 BEST MODEL: {best_model_info['Model']}")
print(f"   ROC-AUC Score: {best_model_info['ROC-AUC']:.4f} ({best_model_info['ROC-AUC']*100:.2f}%)")
print(f"   Accuracy: {best_model_info['Accuracy']:.4f} ({best_model_info['Accuracy']*100:.2f}%)")
print(f"   Precision: {best_model_info['Precision']:.4f}")
print(f"   Recall: {best_model_info['Recall']:.4f}")
print(f"   F1-Score: {best_model_info['F1-Score']:.4f}")

best_model = best_model_info['Model_Object']

# CELL 7: Detailed analysis of best model
print("\n[Step 7] Detailed evaluation of best model...")
best_predictions = best_model_info['Predictions']

print("\nClassification Report:")
print(classification_report(y_test, best_predictions, target_names=['Not Readmitted', 'Readmitted']))

# Confusion matrix
cm = confusion_matrix(y_test, best_predictions)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False,
            xticklabels=['Not Readmitted', 'Readmitted'],
            yticklabels=['Not Readmitted', 'Readmitted'])
plt.title(f'Confusion Matrix - {best_model_info["Model"]}', fontsize=14, fontweight='bold')
plt.ylabel('Actual', fontsize=12)
plt.xlabel('Predicted', fontsize=12)
plt.savefig('plots/confusion_matrix_best_model.png', dpi=300, bbox_inches='tight')
print("\n✓ Saved: plots/confusion_matrix_best_model.png")
plt.show()

print(f"\nConfusion Matrix Breakdown:")
print(f"  True Negatives (Correct NO): {cm[0, 0]}")
print(f"  False Positives (Wrong YES): {cm[0, 1]}")
print(f"  False Negatives (Wrong NO): {cm[1, 0]}")
print(f"  True Positives (Correct YES): {cm[1, 1]}")

# CELL 8: Feature importance (if available)
print("\n[Step 8] Analyzing feature importance...")

if hasattr(best_model, 'feature_importances_'):
    feature_names = X_train.columns.tolist()
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': best_model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    print("\nTop 10 Most Important Features:")
    print(importance_df.head(10).to_string(index=False))
    
    # Plot feature importance
    plt.figure(figsize=(10, 8))
    plt.barh(importance_df['Feature'], importance_df['Importance'], color='steelblue', edgecolor='black')
    plt.xlabel('Importance', fontsize=12)
    plt.title(f'Feature Importance - {best_model_info["Model"]}', fontsize=14, fontweight='bold')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig('plots/feature_importance.png', dpi=300, bbox_inches='tight')
    print("\n✓ Saved: plots/feature_importance.png")
    plt.show()
else:
    print("⊠ Feature importance not available for this model type")

# CELL 9: Save the best model
print("\n[Step 9] Saving the best model...")
joblib.dump(best_model, 'models/best_model.pkl')
print("✓ Saved: models/best_model.pkl")

# Also save all models for experimentation
for name, model in models.items():
    filename = f"models/{name.replace(' ', '_').lower()}.pkl"
    joblib.dump(model, filename)
    print(f"✓ Saved: {filename}")

# CELL 10: Final summary
print("\n" + "=" * 70)
print("MODEL TRAINING COMPLETE! ✓")
print("=" * 70)

print(f"""
SUMMARY:
--------
✓ Models trained: {len(models)}
  - Logistic Regression
  - Decision Tree
  - Random Forest
  - XGBoost

✓ Best model selected: {best_model_info['Model']}
✓ Performance metrics calculated:
  - Accuracy: {best_model_info['Accuracy']:.4f}
  - Precision: {best_model_info['Precision']:.4f}
  - Recall: {best_model_info['Recall']:.4f}
  - F1-Score: {best_model_info['F1-Score']:.4f}
  - ROC-AUC: {best_model_info['ROC-AUC']:.4f}

✓ All models saved for experimentation
✓ Best model ready for deployment

NEXT STEP: Run '03_shap_analysis.ipynb' to understand WHY your model makes predictions!
""")
