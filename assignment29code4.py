import os
import sys

def FileCompare(FileName1, FileName2):
    # Check if both files exist
    if not os.path.exists(FileName1):
        print(f"{FileName1} does not exist!")
        return
    if not os.path.exists(FileName2):
        print(f"{FileName2} does not exist!")
        return

    # Open both files safely using 'with' (auto-closes files)
    with open(FileName1, "r") as f1, open(FileName2, "r") as f2:
        # Read files in chunks to handle large files efficiently
        chunk_size = 1024
        same = True
        while True:
            data1 = f1.read(chunk_size)
            data2 = f2.read(chunk_size)
            
            if data1 != data2:
                same = False
                break
            
            if not data1:  # End of file reached
                break

    # Print comparison result
    if same:
        print("\nSuccess")
        print(f"{FileName1} and {FileName2} contain the same content.\n")
    else:
        print("\nFailure")
        print(f"{FileName1} and {FileName2} do not contain the same content.\n")

def main():
    border = "-"*57
    print(border)
    print("---------------- Marvellous File Compare ----------------")
    print(border)

    # Check command-line arguments
    if len(sys.argv) != 3:
        print("Invalid Number Of Arguments!")
        print("Please specify two file names:")
        print("Example: python assignment29code4.py file1.txt file2.txt")
        return

    FileCompare(sys.argv[1], sys.argv[2])

    print(border)
    print("------------------ END OF APPLICATION -------------------")
    print(border)

if __name__ == "__main__":
    main()
