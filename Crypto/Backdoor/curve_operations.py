# Core components of the code have been taken from Cryptohack. Then I modified the code a bit.

from Crypto.Util.number import inverse
from sympy import gcd

class Point:
    def __init__(self, x=None, y=None, origin=False):
        self.x = x
        self.y = y
        self.origin = origin

class Curve:
    def __init__(self, p, a, b):
        self.p = p
        self.a = a
        self.b = b
    
    def is_on_curve(self, P):
        if P.origin:
            return True
        else:
            return (P.y**2 - (P.x**3 + self.a*P.x + self.b)) % self.p == 0 and 0 <= P.x < self.p and 0 <= P.y < self.p
    
    def point_inverse(self, P):
        if P.origin:
            return P
        return Point(P.x, -P.y % self.p)
    
    def point_addition(self, P, Q):
        if P.origin:
            return Q
        elif Q.origin:
            return P
        elif Q == self.point_inverse(P):
            return Point(origin=True)
        else:
            try:
                if P.x == Q.x and P.y == Q.y:
                    if(gcd(2*P.y , self.p) != 1):
                        lam = (3*P.x**2 + self.a)*pow(2*P.y,-1, gcd(2*P.y , self.p))
                        lam%=gcd(2*P.y , self.p)
                    else:
                        lam = (3*P.x**2 + self.a)*pow(2*P.y,-1, self.p)
                        lam %= self.p
                else:
                    if(gcd((Q.x - P.x),self.p)!=1):
                        lam = (Q.y - P.y) * pow((Q.x - P.x),-1, gcd((Q.x - P.x)))
                        lam %= gcd((Q.x - P.x))
                    else:
                        lam = (Q.y - P.y) * pow((Q.x - P.x),-1, self.p)
                        lam %= self.p
            except ValueError:
                R = Point(origin=True)
                return R
        Rx = (lam**2 - P.x - Q.x) % self.p
        Ry = (lam*(P.x - Rx) - P.y) % self.p
        R = Point(Rx, Ry)
        assert self.is_on_curve(R)
        return R

    def scalar_multiply(self, P, n):
        Q = P
        R = Point(origin=True)
        while n > 0:
            if n % 2 == 1:
                R = self.point_addition(R, Q)
            Q = self.point_addition(Q, Q)
            n = n // 2
        assert self.is_on_curve(R)
        return R
