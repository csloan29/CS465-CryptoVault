from Crypto.PublicKey import RSA


# Python program to demonstrate working of extended
# Euclidean Algorithm

# function for extended Euclidean Algorithm
def gcdExtended(a, b, x, y):
    # Base Case
    if a == 0:
        x = 0
        y = 1
        return b

    x1 = 1
    y1 = 1  # To store results of recursive call
    gcd = gcdExtended(b % a, a, x1, y1)

    # Update x and y using results of recursive
    # call
    x = y1 - (b / a) * x1
    y = x1

    return gcd


if __name__ == '__main__':
    p = 1
    q = 1
    a = 35
    b = 15
    g = gcdExtended(a, b, p, q)
    print("gcd(", a, ",", b, ") = ", g)

