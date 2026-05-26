import pandas as pd
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report

# ─────────────────────────────────────────
# STEP 1: Get Data
# ─────────────────────────────────────────
wine = load_wine()

df = pd.DataFrame(wine.data, columns=wine.feature_names)
df['Class'] = wine.target

print("=== Wine Dataset (first 5 rows) ===")
print(df.head())
print(f"\nShape : {df.shape}")
print(f"Classes : {wine.target_names}")

# ─────────────────────────────────────────
# STEP 2: Clean, Prepare and Manipulate Data
# ─────────────────────────────────────────
X = df.drop('Class', axis=1)   # 13 features
y = df['Class']                 # Target: 0, 1, 2

print("\n=== Features ===")
print(list(X.columns))
print(f"\nClass distribution:\n{y.value_counts()}")

# ─────────────────────────────────────────
# STEP 3: Train Model (80/20 split)
# ─────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\nTraining samples : {len(X_train)}")
print(f"Testing  samples : {len(X_test)}")

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)
print("\n=== Model Trained (KNN, K=3) ===")

# ─────────────────────────────────────────
# STEP 4: Test Data
# ─────────────────────────────────────────
y_pred = knn.predict(X_test)

# ─────────────────────────────────────────
# STEP 5: Improve — Accuracy & Report
# ─────────────────────────────────────────
print("\n=== Predicted vs Expected ===")
print(f"{'Index':<8} {'Expected':>10} {'Predicted':>12} {'Correct?':>10}")
print("-" * 44)
for i, (exp, pred) in enumerate(zip(y_test, y_pred)):
    match = "✓" if exp == pred else "✗"
    print(f"{X_test.index[i]:<8} {wine.target_names[exp]:>10} "
          f"{wine.target_names[pred]:>12} {match:>10}")

accuracy = accuracy_score(y_test, y_pred) * 100
print(f"\n=== Accuracy: {accuracy:.2f}% ===")

print("\n=== Classification Report ===")
print(classification_report(y_test, y_pred, target_names=wine.target_names))

# Bonus: Try different K values
print("=== Accuracy for different K values ===")
for k in range(1, 8):
    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test)) * 100
    print(f"K={k}  →  Accuracy: {acc:.2f}%")