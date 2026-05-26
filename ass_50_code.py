import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, confusion_matrix,
                             classification_report, roc_auc_score,
                             roc_curve)

# ─────────────────────────────────────────
# STEP 1: Load and Explore Dataset
# ─────────────────────────────────────────
data = {
    'age':       [30, 33, 35, 30, 59, 35, 36, 39, 41, 43,
                  39, 43, 36, 20, 31, 40, 56, 30, 29, 45],
    'job':       ['admin.','technician','services','admin.','admin.',
                  'management','self-employed','technician','admin.','services',
                  'admin.','technician','management','student','technician',
                  'admin.','retired','admin.','admin.','services'],
    'marital':   ['married','married','married','married','married',
                  'single','married','married','married','married',
                  'married','married','single','single','married',
                  'married','married','married','single','married'],
    'education': ['secondary','secondary','secondary','secondary','secondary',
                  'tertiary','tertiary','secondary','secondary','secondary',
                  'secondary','secondary','tertiary','secondary','secondary',
                  'secondary','secondary','secondary','secondary','secondary'],
    'default':   ['no']*20,
    'balance':   [1787,4789,1350,1476,0,747,307,147,221,61,
                  -88,1258,309,199,55,168,529,393,189,600],
    'housing':   ['no','yes','yes','yes','yes','no','yes','no',
                  'yes','yes','yes','yes','yes','yes','yes','yes',
                  'yes','yes','no','yes'],
    'loan':      ['no']*20,
    'contact':   ['cellular','cellular','cellular','unknown','unknown',
                  'cellular','cellular','cellular','cellular','unknown',
                  'cellular','cellular','cellular','cellular','cellular',
                  'cellular','cellular','cellular','cellular','cellular'],
    'day':       [19,11,16,3,5,23,14,6,14,17,
                  20,9,24,4,17,21,25,12,5,9],
    'month':     ['oct','may','apr','jun','may','feb','may','may','may','apr',
                  'feb','jan','feb','feb','apr','oct','aug','dec','feb','may'],
    'duration':  [79,220,185,199,226,141,341,151,57,182,
                  38,79,59,101,339,126,154,120,172,133],
    'campaign':  [1,1,1,4,1,2,1,2,2,1,
                  1,2,1,1,2,3,1,3,1,1],
    'previous':  [0]*20,
    'poutcome':  ['unknown']*20,
    'y':         ['no','no','no','no','no','no','no','no',
                  'no','no','no','no','no','no','no','no',
                  'yes','yes','yes','yes']
}

df = pd.DataFrame(data)

print("=== Dataset Info ===")
print(df.shape)
print(df.head())

# Handle 'unknown' values
df = df.replace('unknown', np.nan)

print("\n=== Missing Values ===")
print(df.isnull().sum())

# Fill categorical NaN with mode (pandas 2.x compatible)
cat_cols = df.select_dtypes(include='object').columns.tolist()
for col in cat_cols:
    mode_val = df[col].mode()
    if not mode_val.empty:
        df[col] = df[col].fillna(mode_val.iloc[0])

# Class distribution
print("\n=== Target Distribution ===")
print(df['y'].value_counts())

plt.figure(figsize=(5, 3))
df['y'].value_counts().plot(kind='bar', color=['steelblue','coral'])
plt.title('Class Distribution (y)')
plt.xlabel('Subscribed')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig('class_distribution.png')
plt.show()

# ─────────────────────────────────────────
# STEP 2: Preprocess the Data
# ─────────────────────────────────────────
le = LabelEncoder()

for col in cat_cols:
    df[col] = le.fit_transform(df[col].astype(str))

print("\n=== After Encoding ===")
print(df.head())

X = df.drop('y', axis=1)
y = df['y']

# Scale numeric features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ─────────────────────────────────────────
# STEP 3: Split the Data (80/20)
# ─────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)
print(f"\nTrain: {len(X_train)} | Test: {len(X_test)}")

# ─────────────────────────────────────────
# STEP 4: Train Classification Models
# ─────────────────────────────────────────
models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'KNN (K=5)':           KNeighborsClassifier(n_neighbors=5),
    'Random Forest':       RandomForestClassifier(n_estimators=100, random_state=42)
}

results = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    results[name] = {
        'model':    model,
        'y_pred':   y_pred,
        'y_prob':   y_prob,
        'accuracy': accuracy_score(y_test, y_pred),
        'roc_auc':  roc_auc_score(y_test, y_prob),
        'cm':       confusion_matrix(y_test, y_pred)
    }

# ─────────────────────────────────────────
# STEP 5: Evaluate the Models
# ─────────────────────────────────────────
print("\n" + "="*60)
print(f"{'Model':<25} {'Accuracy':>10} {'ROC-AUC':>10}")
print("="*60)
for name, r in results.items():
    print(f"{name:<25} {r['accuracy']:>10.4f} {r['roc_auc']:>10.4f}")

for name, r in results.items():
    print(f"\n=== {name} — Classification Report ===")
    print(classification_report(y_test, r['y_pred'],
                                target_names=['No', 'Yes'],
                                zero_division=0))

# ─────────────────────────────────────────
# STEP 6: Visualize Results
# ─────────────────────────────────────────

# Confusion Matrices
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for ax, (name, r) in zip(axes, results.items()):
    sns.heatmap(r['cm'], annot=True, fmt='d', cmap='Blues',
                xticklabels=['No', 'Yes'],
                yticklabels=['No', 'Yes'], ax=ax)
    ax.set_title(f'{name}\nAcc={r["accuracy"]:.2f} | AUC={r["roc_auc"]:.2f}')
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')
plt.tight_layout()
plt.savefig('confusion_matrices.png')
plt.show()

# ROC Curves
plt.figure(figsize=(8, 5))
for name, r in results.items():
    fpr, tpr, _ = roc_curve(y_test, r['y_prob'])
    plt.plot(fpr, tpr, label=f"{name} (AUC={r['roc_auc']:.2f})")

plt.plot([0, 1], [0, 1], 'k--', label='Random')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curves — Bank Marketing')
plt.legend()
plt.tight_layout()
plt.savefig('roc_curves.png')
plt.show()

# Feature Importance (Random Forest)
rf_model = results['Random Forest']['model']
feat_imp = pd.Series(rf_model.feature_importances_,
                     index=df.drop('y', axis=1).columns)
feat_imp.sort_values().plot(kind='barh', figsize=(8, 5), color='teal')
plt.title('Feature Importance — Random Forest')
plt.tight_layout()
plt.savefig('feature_importance.png')
plt.show()

print("\nAll plots saved successfully.")