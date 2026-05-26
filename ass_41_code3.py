from math import sqrt

dataset = [
    (2, 60, "Fail"),
    (5, 80, "Pass"),
    (6, 85, "Pass"),
    (1, 50, "Fail")
]

study_hours = int(input("Enter Study Hours: "))
attendance = int(input("Enter Attendance Percentage: "))

distances = []

for sh, att, result in dataset:

    distance = sqrt((study_hours - sh) ** 2 +
                    (attendance - att) ** 2)

    distances.append((distance, result, sh, att))

distances.sort()

k = 3

neighbors = distances[:k]

pass_count = 0
fail_count = 0

print("\nNearest Neighbors:")

for distance, result, sh, att in neighbors:

    print("Study Hours:", sh,
          "Attendance:", att,
          "Result:", result,
          "Distance:", round(distance, 2))

    if result == "Pass":
        pass_count += 1
    else:
        fail_count += 1

if pass_count > fail_count:
    prediction = "Pass"
else:
    prediction = "Fail"

print("\nPredicted Result:", prediction)