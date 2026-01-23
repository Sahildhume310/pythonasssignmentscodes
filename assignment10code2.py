def sum_of_natural_numbers(n):
    total = 0
    for i in range(1, n + 1):
        total = total + i
    return total

def main():
    n = int(input("Enter a number: "))
    result = sum_of_natural_numbers(n)
    print("Sum of first", n, "natural numbers is:", result)

main()
