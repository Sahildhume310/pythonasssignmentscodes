def convert_to_binary(n):
    binary = ""

    while n > 0:
        remainder = n % 2
        binary = str(remainder) + binary
        n = n // 2

    print("Binary equivalent is:", binary)

def main():
    num = int(input("Enter a number: "))
    convert_to_binary(num)

if __name__ == "__main__":
    main()
