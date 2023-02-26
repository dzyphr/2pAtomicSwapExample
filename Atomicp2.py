import random
from random import * 
import ast
import secrets
import hashlib
from ECC import *

def main():
    print("\nget rsG and ksG from p1\n enter them one at a time")
    print("\nrsG:")
    rsG = ast.literal_eval(input())
    print("\nksG:")
    ksG = ast.literal_eval(input())
    rr, kr, rrG, krG = pickScalarRandoms()
    e = issueChallenge(ksG, krG)
    sr, srG = startMultiSign(kr, e, rr)
    x, xG = generatePreImage()
    sr_ = blindedSignature(sr, x)
    print("\ne:\n", e, "\nsrG:\n", srG, "\nxG:\n", xG, "\nsr_:\n", sr_)
    print("you (p2) lock coins to secret value (x) that when multiplied by G == xG")
    print("\nsend e, srG, xG, and sr_ to p1\n then enter ss from p1")
    print("\nss:")
    ss = int(input())
    Q = completeMultiSign(sr, ss)
    print("\nyou (p2) are now broadcasting multisignature value:", Q, "to get your coins")


def pickScalarRandoms():
    rr = random.randrange(0, curve.n)
    kr = random.randrange(0, curve.n)
    krG = scalar_mult(kr, curve.g)
    rrG = scalar_mult(rr, curve.g)
    return rr, kr, krG, rrG

def issueChallenge(ksG, krG):
    message = "1000000000" #some public change output value 
    hashContent = message.encode() + str(ksG + krG).encode()
    sha256 = hashlib.sha256()
    sha256.update(hashContent)
    sha256 = hashlib.sha256()
    e = int(sha256.digest().hex(), 16)
    return e

def startMultiSign(kr, e, rr):
    sr = kr + (e * rr)
    srG = scalar_mult(sr, curve.g)
    return sr, srG

def generatePreImage():
    x = int.from_bytes(SystemRandom().getrandbits(128).to_bytes(16, 'little'), byteorder='little')
    xG = scalar_mult(x, curve.g)
    return x, xG

def blindedSignature(sr, x):
    sr_ = sr + x
    return sr_

def completeMultiSign(sr, ss):
    Q = sr + ss
    return Q


if __name__ == "__main__":
    main()
