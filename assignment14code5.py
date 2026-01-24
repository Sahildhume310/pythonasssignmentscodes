def even(No):
    return No % 2 == 0

def main():
    No = int(input("Enter a No : "))
    Ret = even(No)
    print(Ret)

if __name__ == "__main__":
    main()
