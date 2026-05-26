from math import sqrt

dataset = [
    ("A", 1, 2, "Red"),
    ("B", 2, 3, "Red"),
    ("C", 3, 1, "Blue"),
    ("D", 6, 5, "Blue")
]

x = int(input("Enter X coordinate: "))
y = int(input("Enter Y coordinate: "))

distances = []

for point, px, py, label in dataset:
    distance = sqrt((x - px) ** 2 + (y - py) ** 2)
    distances.append((distance, point, label))

distances.sort()

print("\nPrediction Results")

for k in [1, 3, 4]:

    neighbors = distances[:k]

    red_count = 0
    blue_count = 0

    for distance, point, label in neighbors:

        if label == "Red":
            red_count += 1
        else:
            blue_count += 1

    if red_count > blue_count:
        prediction = "Red"
    else:
        prediction = "Blue"

    print("K =", k, "->", prediction)

print("\nExplanation:")
print("When K increases, more neighbors are considered.")
print("The majority class among neighbors may change.")
print("Small K focuses on nearby points, while large K considers more overall data.")