import sys


def RTriangle():
    print("====== Right Triangle ======\n", end="")
    Row = int(input("Enter rows: \n"))
    I = 1
    while I <= Row:
        J = 1
        while J <= I:
            print("*", end="")
            J += 1
        print("\n", end="")
        I += 1


def ITriangle():
    print("====== Isoceles Triangle ======\n", end="")
    Row = int(input("Enter rows: \n"))
    I = 1
    while I <= Row:
        J = 1
        while J <= Row - I:
            print(" ", end="")
            J += 1
        K = 1
        while K <= 2 * I - 1:
            print("*", end="")
            K += 1
        print("\n", end="")
        I += 1


def Square():
    print("========= Square =========\n", end="")
    Sides = int(input("Enter sides: \n"))
    I = 1
    while I <= Sides:
        J = 1
        while J <= Sides:
            print(" *", end="")
            J += 1
        print("\n", end="")
        I += 1


def Rectangle():
    print("========= Square =========\n", end="")
    Length = int(input("Enter length: \n"))
    Width = int(input("Enter width: \n"))
    I = 1
    while I <= Width:
        J = 1
        while J <= Length:
            print(" *", end="")
            J += 1
        print("\n", end="")
        I += 1


def Main():
    print("A. Square\nB. Rectangle\nC. Isoceles Triangle\nD. Right Triangle\n", end="")
    Letter = input("Enter a Letter:\n")[:1]
    if Letter == "A":
        Square()
    elif Letter == "B":
        Rectangle()
    elif Letter == "C":
        ITriangle()
    elif Letter == "D":
        RTriangle()
    else:
        print("Invalid Letter", end="")
    return 0


if __name__ == "__main__":
    Main()
