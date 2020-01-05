import math
from DiffieHellman.prime_handler import generate_prime_number


def mod_exp(gen, exp, P):
    if exp == 0:
        return 1
    z = mod_exp(gen, math.floor(exp / 2), P)
    if int(exp % 2) == 0:
        return int(pow(z, 2) % P)
    return int(gen * pow(z, 2) % P)


if __name__ == '__main__':
    # shared prime
    # p = generate_prime_number(500)
    p = 2938192068135735487832132082799769579209915267450700112901467455524835247767278585098697694218175236715252251265099872958529065604537556650562482834889

    # shared base generator
    g = 5

    # my secret number
    # a = getrandbits(500)
    a = 79505044317324984596554989831332494254822943070172895958780993254644639027798499470329417617409321511361937221743507293074764227684614218228021979509

    # received from server after sharing publicly found g^aModP
    b_mod_exp = 122172084358076338942870484871056909413570047973270265496852071992562946545066899582058860901307049243828445758652897905582036883382069065785083450849

    # DEBUG: server's secret number & found secret key
    # b = 1998286638065473057944506344030256054916203227381748916180906390214373930105605405985818224246280726328877245115163209963634633681313092395058312190549
    # secret_key = 966130539454179826524240128814614683966279904048767619022742393878023821171889202297599366932336685608154447502700560809186245521243679552883813290778

    print("\nDiffie-Hellman Key Exchange")
    print("My chosen secret exponent \"a\":     ", a)
    print("Chosen prime \"p\":                  ", p)
    print("My publicly exchanged value:       ", mod_exp(g, a, p))

    # DEBUG INFORMATION
    # print("Server's secret exponent \"b\": ", b)
    # print("\nServer's found secret key: ", secret_key)
    print("Server's publicly exchanged value: ", b_mod_exp)
    print("My Found Secret Key:               ", mod_exp(b_mod_exp, a, p))

    print("\nDONE")





