#!/usr/bin/env python3
ffiivVIxistivIX = "ironCTF{R0M4N_T1mes}"
blacklist = ' \t\n\r\v\f0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'*+,-./:;<=>?@\^_`{|}~[]'
print("WELCOME :)")
breakpoint = "breakpoint"
data = input()

if len(data) > 12:
    print("Too long...")
    exit()

for chars in blacklist:
    if chars in data:
        print("Blocked Character: ", chars)
        exit()
try:
    eval(data)
except Exception as e:
    print("Something went wrong\n", e)