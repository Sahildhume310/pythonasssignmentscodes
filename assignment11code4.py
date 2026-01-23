def reverse_number(n):
    rev = ""
    for i in str(n):
        rev = i + rev
    return rev

def main():
    num = int(input("Enter a number: "))
    print("Reverse of number:", reverse_number(num))

if __name__ == "__main__":
    main()

