def xor(a,b):
    return bytes([x^y for x,y in zip(a,b)])

class CustomRandom:
    def __init__(self, m, a=None, b=None, x=None) -> None:
        self.a = a
        self.b = b
        self.x = x
        self.m = m

    def next_bytes(self):
        self.x = (self.a*self.x + self.b) % self.m
        return int(bin(self.x)[2:].zfill(23)[-16:-9],2),int(bin(self.x)[2:].zfill(23)[-23:-16],2)

def crack_unknown_increment(states, modulus, multiplier):
    increment = (states[1] - states[0]*multiplier) % modulus
    return modulus, multiplier, increment

def crack_unknown_multiplier(states, modulus):
    multiplier = (states[2] - states[1]) * modinv(states[1] - states[0], modulus) % modulus
    return crack_unknown_increment(states, modulus, multiplier)

def modinv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n
    raise Exception

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)


x = 9014855307380235246
ct = open('../handout/flag.enc','rb').read()

X = list(xor(ct,[0x89,0x50,0x4E,0x47,0x0D,0x0A]))

x1,x2,x3 = [int((bin(X[i+1])[2:]+ bin(X[i])[2:].zfill(7)) + '0'*9,2) for i in range(0,len(X),2)]

pos_ks = ((x1 + i, x2 + j, x3 + k) for i in range(0x200) for j in range(0x200) for k in range(0x200))

for _,ks in enumerate(pos_ks):
    try:
        m,a,b = crack_unknown_multiplier(ks, 2**23)
    except Exception:
        pass
    else:
        if _%5000000 == 0:
            print(_,"tries")   
        r = CustomRandom(m,a,b,x)
        k = [val for _ in range(4) for val in r.next_bytes()]
        pt = xor(ct[:8],k)
        
        if pt == bytes([0x89,0x50,0x4E,0x47,0x0D,0x0A,0x1A,0x0A]):
            print(m,a,b,ks)
            k.extend((val for _ in range(len(ct)//2 - 3) for val in r.next_bytes()))  
            print(k[:20])          
            res = xor(ct,k)
            open("out.png",'wb').write(res)
            break

