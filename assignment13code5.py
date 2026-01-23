def display_grade(marks):
    if marks >= 75:
        print("Distinction")
    elif marks >= 60:
        print("First Class")
    elif marks >= 50:
        print("Second Class")
    elif marks >= 40:
        print("Pass")
    else:
        print("Fail")

def main():
    marks = int(input("Enter marks: "))
    display_grade(marks)

if __name__ == "__main__":
    main()
