import math

def calculate_area(radius):
    area = math.pi * radius * radius
    print("Area of circle:", area)

def main():
    r = float(input("Enter the radius of the circle: "))
    calculate_area(r)

if __name__ == "__main__":
    main()
