import math
from Crypto.Util.number import getStrongPrime, getRandomInteger


def gcdExtended(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = gcdExtended(b % a, a)
        return gcd, y - (b//a) * x, x


def mod_exp_itr(x:int, y:int, N:int):
    z = 1
    while y:
        if y & 1:
            z = z * x % N
        y >>= 1
        x = x * x % N
    return z


def verify_good_num(e, n, d):
    for i in range(10):
        m = getRandomInteger(int(math.log2(n)))
        check_m = mod_exp_itr(mod_exp_itr(m, e, n), d, n)
        if check_m != m:
            return False
    return True


if __name__ == '__main__':
    # generate 2 512-bit prime numbers p and q
    # ensure high order bit is set
    # verify that (p-1)(q-1) is relatively prime to 65537
    # n = pq
    # e = 65537
    # calculate secret exponent d, such that e*d = 1 % phi(n)
    # verify that for numbers m less than n, ((m^e%n)^d)%n == m

    e = 65537
    while 1:
        p = getStrongPrime(512, e=e)
        # p value given to server
        p = 10427095057974209941173654150877419447711122572052721355253877621720075790853002901851378473192046987817607907515825457998769121189496955644542724094175737
        q = getStrongPrime(512, e=e)
        # q value given to server
        q = 12427810086996854817301661033053706211504596840666492719309517484350822922865354187730037588477595647499670921518663449310631711391299778566198029106400483
        phi_n = (p-1)*(q-1)
        gcd, d, z = gcdExtended(e, phi_n)
        if gcd == 1 and (e*d)%phi_n == 1:
            if d < 0:
                d += phi_n
            break
    n = p * q
    check = verify_good_num(e, n, d)

    message = 113406757685341391872236038790195831665610240074396859752550660555391707176481184593855909410550600467603868956243114390994831485161336145067609589322600826641
    print("\nreceived plaintext message:\n{}".format(message))
    crypto_text = mod_exp_itr(message, e, n)
    print("\nencrypted message:\n{}".format(crypto_text))
    encrypted_message = 6073311554187635318332648675924114193003022794880214359154193066247038549967201918744502039000705809027800861107336527231598379839673646655171590077963324466335407770220496623388953889458537376649747662441061621267955605684335504673443500199174750264589564523348702161297810360107136791287481508073727765882
    print("\nreceived encrypted message:\n{}".format(encrypted_message))
    decrypted_message = mod_exp_itr(encrypted_message, d, n)
    print("\ndecrypted message:\n{}".format(decrypted_message))
    print("\nDONE")
