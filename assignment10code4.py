def print_even_numbers(n):
    for i in range(2, n + 1, 2):
        print(i)

def main():
    num = int(input("Enter a number: "))
    print("Even numbers till", num, "are:")
    print_even_numbers(num)


if __name__=="__main__":
    main()

