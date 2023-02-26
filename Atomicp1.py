import ast
import secrets
import hashlib
from ECC import *

def main():
    rs, ks, rsG, ksG = pickScalarRandoms()
    print("\nrsG:\n", rsG, "\nksG:\n", ksG)
    print("\nget e, srG, xG, and sr_ from p2\nenter values one at a time.")
    print("\ne:")
    e = int(input())
    print("\nsrG:")
    srG = ast.literal_eval(input())
    print("\nxG:")
    xG = ast.literal_eval(input())
    print("\nsr_:")
    sr_ = int(input())
    checkP2Math(srG, xG, sr_)
    print("now you (p1) lock coins to a multisig that requires ss + rs to spend as well as public values ksG + krG")
    ss = blessMultiSign(ks, e, rs)
    print("\nss:", ss)
    print("\nsend ss to p2 to finalize the swap agreement. \nGet Q (multisignature value) from p2's broadcasted tx")
    print("\nQ:")
    Q = int(input())
    sr = extractSignature(Q, ss)
    x = extractPreImage(sr, sr_)
    print("\nyou (p1) can now get your coins with x:", x)


def pickScalarRandoms():
    rs = random.randrange(0, curve.n)#BOTH rs AND ks SHOULD NOT BE REUSED BY ONE SIGNER
    ks = random.randrange(0, curve.n)
    rsG = scalar_mult(rs, curve.g)
    ksG = scalar_mult(ks, curve.g)
    return rs, ks, rsG, ksG

def checkP2Math(srG, xG, sr_): #xG should also be the coordinates locking up funds on p2's chain
    sigma = add_points(srG, xG)
    sr_G = scalar_mult(sr_, curve.g)
    assert(sigma == sr_G)

def blessMultiSign(ks, e, rs):
    ss = ks + (e * rs)
    return ss #p1 makes a script locked to (ss + sr | ksG krG) #script can check that entered ss and sr val multiplied by G == ssG srG

def extractSignature(Q, ss):
    sr = Q - ss
    return sr

def extractPreImage(sr, sr_):
    x = sr_ - sr
    return x


if __name__ == "__main__":
    main()
