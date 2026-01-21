def chkGreater(a,b):
    print("greater no.")

    if a > b:
        return a
    
    else :
        return b
    


print("Enter first number: ")
a=int(input())
print("Enter second number:")
b=int(input())


result = chkGreater(a,b)


print("greater no is",result )


