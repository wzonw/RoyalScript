import sys


def Main():
    Letter = input("Enter: \n")
    L = len(Letter)
    print(str(L).replace("None", "phantom"), end="")
    return 0


if __name__ == "__main__":
    Main()
