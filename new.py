

import sys

def Main():
    Year = int(input("Enter a year:"))
    if ( Year % 4 == 0 and Year % 100 != 0 ) or Year % 400 == 0:
        print("Leap Year"); sys.stdout.flush()
    else:
        print("Not a Leap Year"); sys.stdout.flush()
    return 0

Main()