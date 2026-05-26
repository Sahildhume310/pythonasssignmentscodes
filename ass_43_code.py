import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


data = {
    'Wether':      ['Sunny','Sunny','Overcast','Rainy','Rainy',
                    'Rainy','Overcast','Sunny','Sunny','Rainy'],
    'Temperature': ['Hot','Hot','Hot','Mild','Cool',
                    'Cool','Cool','Mild','Cool','Mild'],
    'Play':        ['No','No','Yes','Yes','Yes',
                    'No','Yes','No','Yes','Yes']
}

df = pd.DataFrame(data)
# If loading from CSV instead, use:
# df = pd.read_csv('MarvellousInfosystems_PlayPredictor.csv')

print("=== Original Dataset ===")
print(df)

# ─────────────────────────────────────────
# STEP 2: Clean, Prepare and Manipulate Data
# ─────────────────────────────────────────
le_wether      = LabelEncoder()
le_temperature = LabelEncoder()
le_play        = LabelEncoder()

df['Wether_enc']      = le_wether.fit_transform(df['Wether'])
df['Temperature_enc'] = le_temperature.fit_transform(df['Temperature'])
df['Play_enc']        = le_play.fit_transform(df['Play'])

print("\n=== Encoded Dataset ===")
print(df)

print("\nWether mapping     :", dict(zip(le_wether.classes_,
                                         le_wether.transform(le_wether.classes_))))
print("Temperature mapping:", dict(zip(le_temperature.classes_,
                                        le_temperature.transform(le_temperature.classes_))))
print("Play mapping       :", dict(zip(le_play.classes_,
                                        le_play.transform(le_play.classes_))))

X = df[['Wether_enc', 'Temperature_enc']]
y = df['Play_enc']

# ─────────────────────────────────────────
# STEP 3: Train Data (whole dataset, K=3)
# ─────────────────────────────────────────
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X, y)
print("\n=== Model trained on full dataset with K=3 ===")

# ─────────────────────────────────────────
# STEP 4: Test Data — predict for new input
# ─────────────────────────────────────────
def predict_play(wether, temperature):
    w_enc = le_wether.transform([wether])[0]
    t_enc = le_temperature.transform([temperature])[0]
    pred  = knn.predict([[w_enc, t_enc]])[0]
    result = le_play.inverse_transform([pred])[0]
    print(f"\nInput  → Wether: {wether}, Temperature: {temperature}")
    print(f"Result → Play: {result}")
    return result

predict_play('Sunny', 'Cool')
predict_play('Rainy', 'Mild')
predict_play('Overcast', 'Hot')

# ─────────────────────────────────────────
# STEP 5: CheckAccuracy() — split 50/50, vary K
# ─────────────────────────────────────────
def CheckAccuracy():
    print("\n=== Accuracy Check (50/50 split) ===")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.5, random_state=42
    )

    for k in range(1, 6):
        model = KNeighborsClassifier(n_neighbors=k)
        model.fit(X_train, y_train)
        y_pred    = model.predict(X_test)
        accuracy  = accuracy_score(y_test, y_pred) * 100
        print(f"K={k}  →  Accuracy: {accuracy:.1f}%")

CheckAccuracy()