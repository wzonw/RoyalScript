import sys


def Main():
    N = int(input("Enter a number: \n"))
    if N == 0:
        print(
            str(N)
            .replace("True", "true")
            .replace("False", "false")
            .replace("None", "phantom"),
            str("is a ZERO Number\n")
            .replace("True", "true")
            .replace("False", "false")
            .replace("None", "phantom"),
            end="",
        )
    else:
        if N > 0:
            if N % 2 == 0:
                print(
                    str(N)
                    .replace("True", "true")
                    .replace("False", "false")
                    .replace("None", "phantom"),
                    str("is a POSITIVE EVEN Number\n")
                    .replace("True", "true")
                    .replace("False", "false")
                    .replace("None", "phantom"),
                    end="",
                )
            else:
                print(
                    str(N)
                    .replace("True", "true")
                    .replace("False", "false")
                    .replace("None", "phantom"),
                    str("is a POSITIVE ODD Number\n")
                    .replace("True", "true")
                    .replace("False", "false")
                    .replace("None", "phantom"),
                    end="",
                )
        elif N != 0:
            if N % 2 == 0:
                print(
                    str(N)
                    .replace("True", "true")
                    .replace("False", "false")
                    .replace("None", "phantom"),
                    str("is a NEGATIVE EVEN Number\n")
                    .replace("True", "true")
                    .replace("False", "false")
                    .replace("None", "phantom"),
                    end="",
                )
            else:
                print(
                    str(N)
                    .replace("True", "true")
                    .replace("False", "false")
                    .replace("None", "phantom"),
                    str("is a NEGATIVE ODD Number\n")
                    .replace("True", "true")
                    .replace("False", "false")
                    .replace("None", "phantom"),
                    end="",
                )
        else:
            print(
                str("Invalid Input\n")
                .replace("True", "true")
                .replace("False", "false")
                .replace("None", "phantom"),
                end="",
            )
    return 0


if __name__ == "__main__":
    Main()
