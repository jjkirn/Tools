#!/usr/bin/env python
# From: https://github.com/FedericoHeichou/RsaDecryptionCalculator/blob/master/RsaDecryptionCalculator.py

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

p = input("p: ")
q = input("q: ")
dp = input("dp: ")
dq = input("dq: ")
c = input("c: ")

qinv = modinv(q, p)
m1 = pow(c, dp, p)
m2 = pow(c, dq, q)
h = (qinv * (m1 - m2)) % p
m = m2 + h * q
txt = format(m, 'x')
print('')
print(''.join([chr(int(''.join(c), 16)) for c in zip(txt[0::2],txt[1::2])]))
