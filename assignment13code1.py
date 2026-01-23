def calculate_area(length, width):
    area = length * width
    print("Area of rectangle:", area)

def main():
    length = float(input("Enter the length of rectangle: "))
    width = float(input("Enter the width of rectangle: "))
    calculate_area(length, width)

if __name__ == "__main__":
    main()
