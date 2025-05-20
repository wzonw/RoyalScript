import sys


def Multiplication(A, B):
    print(str(A * B).replace("None", "phantom"), end="")


def Division(A, B):
    if B != 0:
        print(str(A / B).replace("None", "phantom"), end="")
    else:
        print(str("Cannot divide by zero!").replace("None", "phantom"), end="")


def Addition(A, B):
    print(str(A + B).replace("None", "phantom"), end="")


def Subtraction(A, B):
    print(str(A - B).replace("None", "phantom"), end="")


def Calculate(Operation, A, B):
    if Operation == 1:
        Multiplication(A, B)
    elif Operation == 2:
        Division(A, B)
    elif Operation == 3:
        Addition(A, B)
    elif Operation == 4:
        Subtraction(A, B)
    else:
        print(str("Invalid operation choice!").replace("None", "phantom"), end="")


def Main():
    print(
        str(
            "Welcome to MDAS operations (Multiplication, Division, Addition, Subtraction)!\n"
        ).replace("None", "phantom"),
        end="",
    )
    print(str("Choose an operation:\n").replace("None", "phantom"), end="")
    print(str("1. Multiplication\n").replace("None", "phantom"), end="")
    print(str("2. Division\n").replace("None", "phantom"), end="")
    print(str("3. Addition\n").replace("None", "phantom"), end="")
    print(str("4. Subtraction\n").replace("None", "phantom"), end="")
    Operation = (
        lambda v: (
            int(v)
            if v.isdigit()
            else (
                print("Semantic Error: Invalid input value for treasures datatype.")
                or __import__("sys").exit()
            )
        )
    )(input("Enter the number for the operation: \n\n").strip())
    A = (
        lambda v: (
            float(v)
            if (
                v.count(".") == 1
                and v.replace(".", "", 1).replace("-", "", 1).isdigit()
                and v != "."
                and v != "-."
                and v[0] != "."
                and v != "-0."
                and v[0] in "-0123456789"
                and not v.replace(".", "", 1).replace("-", "", 1).isdigit()
                == v.lstrip("-")
            )
            else (
                print("Semantic Error: Invalid input value for ocean datatype.")
                or __import__("sys").exit()
            )
        )
    )(input("Enter the first number: \n\n").strip())
    B = (
        lambda v: (
            float(v)
            if (
                v.count(".") == 1
                and v.replace(".", "", 1).replace("-", "", 1).isdigit()
                and v != "."
                and v != "-."
                and v[0] != "."
                and v != "-0."
                and v[0] in "-0123456789"
                and not v.replace(".", "", 1).replace("-", "", 1).isdigit()
                == v.lstrip("-")
            )
            else (
                print("Semantic Error: Invalid input value for ocean datatype.")
                or __import__("sys").exit()
            )
        )
    )(input("Enter the second number: \n\n").strip())
    Calculate(Operation, A, B)
    return 0


if __name__ == "__main__":
    Main()
