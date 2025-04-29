import sys


def Main():
    Num1 = int(input("Number 1: \n"))
    Num2 = int(input("Number 2: \n"))
    Num3 = int(input("Number 3: \n"))
    Num4 = int(input("Number 4: \n"))
    Num5 = int(input("Number 5: \n"))
    Num = [Num1, Num2, Num3, Num4, Num5]
    Choice = input("Sort in (i)ncreasing or (d)ecreasing order? (i/d): \n")
    I = 0
    while I < 4:
        J = 0
        while J < 4 - I:
            K = J + 1
            Temp = 0
            if Choice == "i" or Choice == "i":
                if Num[J] > Num[K]:
                    Temp = Num[J]
                    Num[J] = Num[K]
                    Num[K] = Temp
            elif Choice == "d" or Choice == "D":
                if Num[J] < Num[K]:
                    Temp = Num[J]
                    Num[J] = Num[K]
                    Num[K] = Temp
            J += 1
        I += 1
    if Choice == "i" or Choice == "i":
        print(
            str("Numbers in increasing order: \n")
            .replace("True", "true")
            .replace("False", "false")
            .replace("None", "phantom"),
            end="",
        )
    elif Choice == "d" or Choice == "D":
        print(
            str("Numbers in decreasing order: \n")
            .replace("True", "true")
            .replace("False", "false")
            .replace("None", "phantom"),
            end="",
        )
    else:
        print(
            str("Invalid choice. Sorted in increasing order by default: \n")
            .replace("True", "true")
            .replace("False", "false")
            .replace("None", "phantom"),
            end="",
        )
    L = 0
    while L < 5:
        print(
            str(str(Num[L]) + " ")
            .replace("True", "true")
            .replace("False", "false")
            .replace("None", "phantom"),
            end="",
        )
        L += 1
    print(
        str("\n")
        .replace("True", "true")
        .replace("False", "false")
        .replace("None", "phantom"),
        end="",
    )
    return 0


if __name__ == "__main__":
    Main()
