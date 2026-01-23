def print_odd_numbers(n):
    for i in range(1, n + 1, 2):
        print(i)

def main():
    num = int(input("Enter a number: "))
    print("odd numbers till", num, "are:")
    print_odd_numbers(num)

if __name__=="__main__":
    main()
