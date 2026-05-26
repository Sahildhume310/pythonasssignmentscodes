X = [1, 2, 3, 4, 5]
Y = [3, 4, 2, 4, 5]

m = 0.4
c = 2.4

# Step 1: Predicted values
Y_pred = [m * x + c for x in X]
print("Predicted Y values:", Y_pred)

# Step 2: MSE
errors = [(Y[i] - Y_pred[i]) ** 2 for i in range(len(Y))]
print("Squared errors:", errors)
MSE = sum(errors) / len(Y)
print(f"MSE = {MSE}")

# Step 3: R² Score
mean_y = sum(Y) / len(Y)
ss_tot = sum((y - mean_y) ** 2 for y in Y)
ss_res = sum((Y[i] - Y_pred[i]) ** 2 for i in range(len(Y)))
R2 = 1 - (ss_res / ss_tot)
print(f"R² Score = {R2}")