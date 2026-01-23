def main():
    num = int(input("Enter a number: "))

    print("Factors are:")
    for i in range(1, num + 1):
        if num % i == 0:
            print(i, end=" ")

if __name__=="__main__":
    main()