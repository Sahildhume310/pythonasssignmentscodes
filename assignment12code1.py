def main():
    ch = input("Enter a character: ").lower()

    if ch in ['a', 'e', 'i', 'o', 'u']:
        print("Vowel")
    else:
        print("Consonant")

if __name__ == "__main__":
    main()