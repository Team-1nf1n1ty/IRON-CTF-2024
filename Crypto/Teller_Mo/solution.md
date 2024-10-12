### Teller Mo

This challenge invloves understanding the morellet cipher and its encoding scheme. To know more about the cipher, you can check https://codesandbox.io/p/sandbox/morellet-cipher-uzo6d?file=%2Fsrc%2FApp.vue this website out. Ideally how it works is, each letter is associated with a number and a corresponding color. The goal is find out the flag from the given number and image. The source code for the encoding scheme can be found at src>>components>>MorelletCroses.vue

# Approach 1:
For those who don't want to code and prefer using the interface directly, you can go through the source code and manually assign characters for the array given in the source code and get the answer by typing it in the webiste and checking it.

# Approach 2:
If you are person who believes in automation, then writing code is the way to go. This is the python solve script for the given challenge:


```huffmanian6 = {
  'A': "5",
  'B': "35",
  'C': "12",
  'D': "11",
  'E': "2",
  'F': "30",
  'G': "31",
  'H': "05",
  'I': "01",
  'J': "152",
  'K': "151",
  'L': "10",
  'M': "14",
  'N': "02",
  'O': "00",
  'P': "32",
  'Q': "155",
  'R': "04",
  'S': "03",
  'T': "4",
  'U': "13",
  'V': "150",
  'W': "33",
  'X': "153",
  'Y': "34",
  'Z': "154"
}
encoded="4052310010111200010201030501111120201024052350102"
inverse_huff={}
for key,value in huffmanian6.items():
    inverse_huff[value]=key

flag=""
i=0

while i<len(encoded):
    isFound=False
    for j in range(3,0,-1):
        coded=encoded[i:i+j]
        if coded in inverse_huff:
            flag+=inverse_huff[coded]
            i+=j
            isFound=True
            break
        
    if (not isFound):
        break

print(flag)```

flag: ironCTF{the_gold_coin_is_hidden_in_the_bin}






