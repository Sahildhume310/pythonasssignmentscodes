
def factorial(num):
    fact = 1
    for i in range(1, num + 1):
        fact = fact * i
    return fact

def main():
    n = int(input("Enter a number: "))
    result = factorial(n)
    print("Factorial of", n, "is:", result)


    
    

if __name__=="__main__":
    main()

