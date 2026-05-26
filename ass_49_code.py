import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (accuracy_score, confusion_matrix,
                             precision_score, recall_score,
                             f1_score, classification_report)

# ─────────────────────────────────────────
# STEP 1: Get Data
# ─────────────────────────────────────────
data = {
    'Pregnancies':              [6,1,8,1,0,5,3,10,2,8,4,10,10],
    'Glucose':                  [148,85,183,89,137,116,78,115,197,125,110,168,139],
    'BloodPressure':            [72,66,64,66,40,74,50,0,70,96,92,74,80],
    'SkinThickness':            [35,29,0,23,35,0,32,0,45,0,0,0,0],
    'Insulin':                  [0,0,0,94,168,0,88,0,543,0,0,0,0],
    'BMI':                      [33.6,26.6,23.3,28.1,43.1,25.6,31,35.3,30.5,0,37.6,38,27.1],
    'DiabetesPedigreeFunction': [0.627,0.351,0.672,0.167,2.288,0.201,0.248,0.134,0.158,0.232,0.191,0.537,1.441],
    'Age':                      [50,31,32,21,33,30,26,29,53,54,30,34,57],
    'Outcome':                  [1,0,1,0,1,0,1,0,1,1,0,1,0]
}
# For full dataset use:
# df = pd.read_csv('diabetes.csv')
df = pd.DataFrame(data)

print("=== Dataset ===")
print(df)
print(f"\nShape: {df.shape}")

# ─────────────────────────────────────────
# STEP 2: Data Preprocessing
# ─────────────────────────────────────────

# Replace 0s with NaN in medically invalid columns
zero_cols = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
df[zero_cols] = df[zero_cols].replace(0, np.nan)

print("\n=== Missing Values (after replacing 0s) ===")
print(df.isnull().sum())

# Fill NaN with column mean
df.fillna(df.mean(numeric_only=True), inplace=True)
print("\n=== After Filling Missing Values ===")
print(df)

# Split features and target
X = df.drop('Outcome', axis=1)
y = df['Outcome']

# Feature Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-Test Split (80/20)
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)
print(f"\nTrain: {len(X_train)} | Test: {len(X_test)}")

# ─────────────────────────────────────────
# STEP 3: Model Building
# ─────────────────────────────────────────
models = {
    'Logistic Regression': LogisticRegression(max_iter=1000),
    'KNN (K=3)':           KNeighborsClassifier(n_neighbors=3),
    'Decision Tree':       DecisionTreeClassifier(random_state=42)
}

results = {}

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    results[name] = {
        'model':     model,
        'y_pred':    y_pred,
        'accuracy':  accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, zero_division=0),
        'recall':    recall_score(y_test, y_pred, zero_division=0),
        'f1':        f1_score(y_test, y_pred, zero_division=0),
        'cm':        confusion_matrix(y_test, y_pred)
    }

# ─────────────────────────────────────────
# STEP 4: Model Evaluation
# ─────────────────────────────────────────
print("\n" + "="*55)
print(f"{'Model':<25} {'Acc':>6} {'Prec':>6} {'Rec':>6} {'F1':>6}")
print("="*55)
for name, r in results.items():
    print(f"{name:<25} {r['accuracy']:>6.2f} {r['precision']:>6.2f} "
          f"{r['recall']:>6.2f} {r['f1']:>6.2f}")

# Confusion Matrix plots
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for ax, (name, r) in zip(axes, results.items()):
    sns.heatmap(r['cm'], annot=True, fmt='d', cmap='Blues',
                xticklabels=['No Diabetes','Diabetes'],
                yticklabels=['No Diabetes','Diabetes'], ax=ax)
    ax.set_title(f'{name}\nAccuracy: {r["accuracy"]:.2f}')
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')
plt.tight_layout()
plt.savefig('confusion_matrices.png')
plt.show()
print("\nConfusion matrix plot saved.")

# Detailed classification report
for name, r in results.items():
    print(f"\n=== {name} — Classification Report ===")
    print(classification_report(y_test, r['y_pred'],
          target_names=['No Diabetes', 'Diabetes'], zero_division=0))

# ─────────────────────────────────────────
# STEP 5: Final Output — Predictions + CSV
# ─────────────────────────────────────────
best_model_name = max(results, key=lambda n: results[n]['accuracy'])
best_pred = results[best_model_name]['y_pred']

print(f"\n=== Best Model: {best_model_name} ===")
print(f"{'Index':<8} {'Predicted':>12} {'Actual':>10}")
print("-" * 32)
for i, (pred, actual) in enumerate(zip(best_pred, y_test)):
    label_p = "Diabetic" if pred == 1 else "Not Diabetic"
    label_a = "Diabetic" if actual == 1 else "Not Diabetic"
    print(f"{i:<8} {label_p:>12} {label_a:>10}")

# Save predictions to CSV
output_df = pd.DataFrame(X_test, columns=df.drop('Outcome', axis=1).columns)
output_df['Actual']    = y_test.values
output_df['Predicted'] = best_pred
output_df.to_csv('diabetes_predictions.csv', index=False)
print("\nPredictions saved to diabetes_predictions.csv")