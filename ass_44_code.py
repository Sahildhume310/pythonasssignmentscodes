import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# ─────────────────────────────────────────
# STEP 1: Get Data
# ─────────────────────────────────────────
data = {
    'TV':        [230.1, 44.5, 17.2, 151.5, 180.8, 8.7,  57.5, 120.2, 8.6,  199.8],
    'radio':     [37.8,  39.3, 45.9, 41.3,  10.8,  48.9, 32.8, 19.6,  2.1,  2.6],
    'newspaper': [69.2,  45.1, 69.3, 58.5,  58.4,  75.0, 23.5, 11.6,  1.0,  21.2],
    'sales':     [22.1,  10.4, 9.3,  18.5,  12.9,  7.2,  11.8, 13.2,  4.8,  10.6]
}

df = pd.DataFrame(data)
# If loading from CSV instead, use:
# df = pd.read_csv('MarvellousAdvertising.csv')

print("=== Dataset ===")
print(df)

# ─────────────────────────────────────────
# STEP 2: Clean, Prepare and Manipulate Data
# ─────────────────────────────────────────
X = df[['TV', 'radio', 'newspaper']]   # Features
y = df['sales']                         # Target

print("\n=== Features (X) ===")
print(X)
print("\n=== Target (y) ===")
print(y)

# ─────────────────────────────────────────
# STEP 3: Train Data (50/50 split)
# ─────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.5, random_state=42
)

print(f"\nTraining samples : {len(X_train)}")
print(f"Testing  samples : {len(X_test)}")

model = LinearRegression()
model.fit(X_train, y_train)

print("\n=== Model Trained Successfully ===")
print(f"Coefficients : TV={model.coef_[0]:.4f}, "
      f"radio={model.coef_[1]:.4f}, "
      f"newspaper={model.coef_[2]:.4f}")
print(f"Intercept    : {model.intercept_:.4f}")

# ─────────────────────────────────────────
# STEP 4: Test Data
# ─────────────────────────────────────────
y_pred = model.predict(X_test)

# ─────────────────────────────────────────
# STEP 5: Display Predicted vs Expected
# ─────────────────────────────────────────
print("\n=== Predicted vs Expected Sales ===")
print(f"{'Index':<8} {'Expected':>10} {'Predicted':>12}")
print("-" * 32)
for i, (exp, pred) in enumerate(zip(y_test, y_pred)):
    print(f"{X_test.index[i]:<8} {exp:>10.1f} {pred:>12.2f}")

# Bonus: Model accuracy (R² Score)
from sklearn.metrics import r2_score, mean_squared_error
r2  = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
print(f"\nR² Score : {r2:.4f}")
print(f"MSE      : {mse:.4f}")