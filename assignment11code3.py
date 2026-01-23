def sum_of_digits(n):
    total = 0
    for i in range(len(str(n))):
        digit = int(str(n)[i])
        total = total + digit
    return total

def main():
    num = int(input("Enter a number: "))
    print("Sum of digits:", sum_of_digits(num))

if __name__ == "__main__":
    main()

