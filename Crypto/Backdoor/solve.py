from sage.all import *
from curve_operations import *  # Using this because sage gets angry when i try to do curve operations on a singular curve
from Crypto.Util.number import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

class Dual_EC:

    def __init__(self):
        p = 229054522729978652250851640754582529779
        a = -75
        b = -250
        self.curve = Curve(p,a,b)
        self.P = Point(97396093570994028423863943496522860154 , 2113909984961319354502377744504238189)
        self.Q = Point(137281564215976890139225160114831726699 , 111983247632990631097104218169731744696)

    def set_state(self, state):
        self.state = state

    def set_next_state(self):
        self.state = self.curve.scalar_multiply(self.P, self.state).x

    def gen_rand_num(self):
        rand_point = self.curve.scalar_multiply(self.Q, self.state)
        rand_num = rand_point.x
        self.set_next_state()
        return rand_num

# Credit to : https://github.com/jvdsn/crypto-attacks/blob/master/attacks/ecc/singular_curve.py 
def attack(p, a2, a4, a6, Gx, Gy, Px, Py):
    """
    Solves the discrete logarithm problem on a singular curve (y^2 = x^3 + a2 * x^2 + a4 * x + a6).
    :param p: the prime of the curve base ring
    :param a2: the a2 parameter of the curve
    :param a4: the a4 parameter of the curve
    :param a6: the a6 parameter of the curve
    :param Gx: the base point x value
    :param Gy: the base point y value
    :param Px: the point multiplication result x value
    :param Py: the point multiplication result y value
    :return: l such that l * G == P
    """
    x = GF(p)["x"].gen()
    f = x ** 3 + a2 * x ** 2 + a4 * x + a6
    roots = f.roots()

    # Singular point is a cusp.
    if len(roots) == 1:
        alpha = roots[0][0]
        u = (Gx - alpha) / Gy
        v = (Px - alpha) / Py
        return int(v / u)

    # Singular point is a node.
    if len(roots) == 2:
        if roots[0][1] == 2:
            alpha = roots[0][0]
            beta = roots[1][0]
        elif roots[1][1] == 2:
            alpha = roots[1][0]
            beta = roots[0][0]
        else:
            raise ValueError("Expected root with multiplicity 2.")

        t = (alpha - beta).sqrt()
        u = (Gy + t * (Gx - alpha)) / (Gy - t * (Gx - alpha))
        v = (Py + t * (Px - alpha)) / (Py - t * (Px - alpha))
        return int(v.log(u))

    raise ValueError(f"Unexpected number of roots {len(roots)}.")
    
def main():
    p = 229054522729978652250851640754582529779
    a2 = 0
    a4 = -75
    a6 = -250
    Px = 97396093570994028423863943496522860154
    Py = 2113909984961319354502377744504238189
    Gx = 137281564215976890139225160114831726699
    Gy = 111983247632990631097104218169731744696
    backdoor = attack(p, a2, a4, a6, Gx, Gy, Px, Py)

    sample_rand_num_x = 222485190245526863452994827085862802196
    F = GF(p)
    y2 = F(sample_rand_num_x**3 + a4*sample_rand_num_x + a6)
    sample_rand_num_y = int(sqrt(y2))
    sample_rand_num = Point(sample_rand_num_x, sample_rand_num_y)

    prng = Dual_EC()
    next_state = prng.curve.scalar_multiply(sample_rand_num, backdoor).x
    prng.set_state(next_state)

    key = long_to_bytes((prng.gen_rand_num() << 128) + prng.gen_rand_num())
    iv = long_to_bytes(prng.gen_rand_num())
    enc_flag = b'o\x8f\xfd\x06\x07C\x04$\xf2\x9e\xe1\x1a\x80g\xec\x9eN\xe05\xc8~ M\x9c\x02g\xc6YY!\x92Z7\xdf\xcf\xe3%]\xb0\x0c)\xc8\xf4\x88\x03\x1f\xe4\x92'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    flag = unpad(cipher.decrypt(enc_flag), AES.block_size)
    print("FLAG : ", flag)

if __name__ == "__main__":
    main()
