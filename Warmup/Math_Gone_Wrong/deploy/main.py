#!/usr/bin/python3
with open('/chal/flag.txt', 'rb') as f:
    FLAG = f.read()
try:
    n1 = float(input("Enter frist number (n1) > "))
    n2 = float(input("Enter second number (n2) > "))
    if n1*10+n2*10 != (n1+n2)*10:
        print(FLAG)
    else:
        print("n1*10+n2*10 != (n1+n2)*10\nabove condition is false so no flag")
except ValueError:
    print("Not a valid number!")