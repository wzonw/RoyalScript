import sys


def GCD(A, B):
    while B != 0:
        Temp = B
        B = A % B
        A = Temp
    return A


def LCD(A, B):
    Lcd = (A * B) / GCD(A, B)
    return (A * B) / GCD(A, B)


def Main():
    N1 = int(input("Enter 1st Denominator: \n"))
    N2 = int(input("Enter 2nd Denominator: \n"))
    print("LCD: ", LCD(N1, N2), "\n", end="")
    return 0


if __name__ == "__main__":
    Main()
