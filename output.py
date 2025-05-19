import sys


def Main():
    N = int(input("Enter number of Fibonacci Sequence to be displayed: \n\n"))
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
