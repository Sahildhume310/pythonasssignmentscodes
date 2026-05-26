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

k = 3
neighbors = distances[:k]

red_count = 0
blue_count = 0

print("\nNearest Neighbors:")

for distance, point, label in neighbors:
    print(point, "- Distance:", round(distance, 2))

    if label == "Red":
        red_count += 1
    else:
        blue_count += 1

if red_count > blue_count:
    prediction = "Red"
else:
    prediction = "Blue"

print("\nPredicted Class:", prediction)