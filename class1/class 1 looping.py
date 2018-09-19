"""Matt Scott
Looping for class 1"""

i = input("Enter an integer!")

while i.isdigit() == False:
    i = input("Try again!  That wasn't an integer!!!")

i = int(i)
x = -1

while x < i:
    x += 1
    print(x)


