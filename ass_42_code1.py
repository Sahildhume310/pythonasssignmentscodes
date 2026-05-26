X = [1, 2, 3, 4, 5]
Y = [3, 4, 2, 4, 5]

n = len(X)

mean_x = sum(X) / n
mean_y = sum(Y) / n

numerator = sum((X[i] - mean_x) * (Y[i] - mean_y) for i in range(n))
denominator = sum((X[i] - mean_x) ** 2 for i in range(n))

m = numerator / denominator
c = mean_y - m * mean_x

print(f"Mean of X = {mean_x}")
print(f"Mean of Y = {mean_y}")
print(f"Slope (m) = {m}")
print(f"Intercept (c) = {c}")
print(f"Regression Equation: Y = {m}X + {c}")
print(f"Predicted Y for X = 6 : {m * 6 + c}")