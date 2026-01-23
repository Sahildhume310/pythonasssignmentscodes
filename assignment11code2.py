def count_digits(n):
    count = 0
    while n > 0:
        count += 1
    return count

def main():
    num = int(input("Enter a number: "))
    print("Number of digits:", count_digits(num))

if __name__ == "__main__":
    main()

