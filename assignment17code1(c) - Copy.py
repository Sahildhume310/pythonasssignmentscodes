import Assignment17code1Module

def main():
    No1 = int(input("Enter first number : "))
    No2 = int(input("Enter second number : "))

    Res = Assignment17code1Module.Add(No1,No2)
    print("Addition is : ",Res)

    Res = Assignment17code1Module.Sub(No1,No2)
    print("Substraction is :",Res)

    Res = Assignment17code1Module.Div(No1,No2)
    print("Division is :",Res)

    Res = Assignment17code1Module.Mult(No1,No2)
    print("Multiplication is :",Res)

if __name__ == "__main__":
    main()