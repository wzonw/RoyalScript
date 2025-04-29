import sys


def RTriangleL():
    print(str("*\n").replace("None", "phantom"), end="")
    print(str("**\n").replace("None", "phantom"), end="")
    print(str("***\n").replace("None", "phantom"), end="")
    print(str("****\n").replace("None", "phantom"), end="")
    print(str("*****\n").replace("None", "phantom"), end="")
    print(str("******\n").replace("None", "phantom"), end="")
    print(str("*******\n").replace("None", "phantom"), end="")
    print(str("********\n").replace("None", "phantom"), end="")
    print(str("*********\n").replace("None", "phantom"), end="")


def RTriangleR():
    print(str("        *\n").replace("None", "phantom"), end="")
    print(str("       **\n").replace("None", "phantom"), end="")
    print(str("      ***\n").replace("None", "phantom"), end="")
    print(str("     ****\n").replace("None", "phantom"), end="")
    print(str("    *****\n").replace("None", "phantom"), end="")
    print(str("   ******\n").replace("None", "phantom"), end="")
    print(str("  *******\n").replace("None", "phantom"), end="")
    print(str(" ********\n").replace("None", "phantom"), end="")
    print(str("*********\n").replace("None", "phantom"), end="")


def ITriangle():
    print(str("     *\n").replace("None", "phantom"), end="")
    print(str("    ***\n").replace("None", "phantom"), end="")
    print(str("   *****\n").replace("None", "phantom"), end="")
    print(str("  *******\n").replace("None", "phantom"), end="")
    print(str(" *********\n").replace("None", "phantom"), end="")
    print(str("***********\n").replace("None", "phantom"), end="")


def Square():
    print(str("* * * * * * * * * *\n").replace("None", "phantom"), end="")
    print(str("* * * * * * * * * *\n").replace("None", "phantom"), end="")
    print(str("* * * * * * * * * *\n").replace("None", "phantom"), end="")
    print(str("* * * * * * * * * *\n").replace("None", "phantom"), end="")
    print(str("* * * * * * * * * *\n").replace("None", "phantom"), end="")
    print(str("* * * * * * * * * *\n").replace("None", "phantom"), end="")
    print(str("* * * * * * * * * *\n").replace("None", "phantom"), end="")
    print(str("* * * * * * * * * *\n").replace("None", "phantom"), end="")
    print(str("* * * * * * * * * *\n").replace("None", "phantom"), end="")
    print(str("* * * * * * * * * *\n").replace("None", "phantom"), end="")


def Rectangle():
    print(str("******************\n").replace("None", "phantom"), end="")
    print(str("******************\n").replace("None", "phantom"), end="")
    print(str("******************\n").replace("None", "phantom"), end="")
    print(str("******************\n").replace("None", "phantom"), end="")
    print(str("******************\n").replace("None", "phantom"), end="")


def Main():
    print(str("========== SHAPES =========\n").replace("None", "phantom"), end="")
    print(
        str(
            "A. Square\nB. Rectangle\nC. Isoceles Triangle\nD. Right Triangle(Left)\nE. Right Triangle(Right)\n"
        ).replace("None", "phantom"),
        end="",
    )
    Letter = input("Enter a Letter:\n")[:1]
    if Letter == "A":
        Square()
    elif Letter == "B":
        Rectangle()
    elif Letter == "C":
        ITriangle()
    elif Letter == "D":
        RTriangleL()
    elif Letter == "E":
        RTriangleR()
    else:
        print(str("Invalid Letter").replace("None", "phantom"), end="")
    return 0


if __name__ == "__main__":
    Main()
