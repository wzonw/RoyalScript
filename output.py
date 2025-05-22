import sys


def Main():
    N = (
        lambda v: (
            int(v)
            if v.isdigit()
            else (
                print("Semantic Error: Invalid input value for treasures datatype.")
                or __import__("sys").exit()
            )
        )
    )(input("Enter number of Fibonacci Sequence to be displayed: \n\n").strip())
    A = 0
    B = 1
    I = 1
    while I <= N:
        print(
            str(A).replace("None", "phantom"),
            str(" ").replace("None", "phantom"),
            end="",
        )
        Temp = A
        A = B
        B = Temp + B
        I += 1
    return 0


if __name__ == "__main__":
    Main()
