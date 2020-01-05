import binascii
from hashlib import sha1
from struct import pack, unpack


def chunks(l, n):
    return [l[i:i + n] for i in range(0, len(l), n)]


def rol(n, b):
    return ((n << b) | (n >> (32 - b))) & 0xffffffff


def padding(msglen):
    padding = [128]
    padding.extend([0] * (55 - msglen % 64))
    if msglen % 64 > 55:
        padding.extend([0] * (64 + 55 - msglen % 64))
    return bytes(padding) + pack('>Q', 8 * msglen)


def sha1_homebrew(data: bytes, iv=[0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0], original_len=0):
    # set initialization vector
    h0 = iv[0]
    h1 = iv[1]
    h2 = iv[2]
    h3 = iv[3]
    h4 = iv[4]

    padded_data = data + padding(len(data) + original_len)

    chunk_arr = [padded_data[i:i + 64] for i in range(0, len(padded_data), 64)]
    for chunk in chunk_arr:
        w = list(unpack('>16L', chunk)) + [0] * 64
        for i in range(16, 80):
            w[i] = rol((w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16]), 1)

        a, b, c, d, e = h0, h1, h2, h3, h4

        #Main loop
        for i in range(0, 80):
            if 0 <= i <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            elif 60 <= i <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = rol(a, 5) + f + e + k + w[i] & 0xffffffff
            e = d
            d = c
            c = rol(b, 30)
            b = a
            a = temp

        h0 = h0 + a & 0xffffffff
        h1 = h1 + b & 0xffffffff
        h2 = h2 + c & 0xffffffff
        h3 = h3 + d & 0xffffffff
        h4 = h4 + e & 0xffffffff

    return h0.to_bytes(4, 'big') + \
           h1.to_bytes(4, 'big') + \
           h2.to_bytes(4, 'big') + \
           h3.to_bytes(4, 'big') + \
           h4.to_bytes(4, 'big')


def run_passoff():
    secret_len = 16
    message = b'No one has completed lab 2 so give them all a 0'
    extension = b'except for Carter Sloan. Give him 100.'
    mac = 'f4b645e89faaec2ff8e443c595009c16dbdfba4b'
    macA = int(mac[0:8], 16)
    macB = int(mac[8:16], 16)
    macC = int(mac[16:24], 16)
    macD = int(mac[24:32], 16)
    macE = int(mac[32:40], 16)
    macs = [macA, macB, macC, macD, macE]

    orig_padding = padding(secret_len + len(message))
    extended_message_digest = sha1_homebrew(extension, iv=macs, original_len=(secret_len + len(message) + len(orig_padding)))
    padded_extended_message = message + orig_padding + extension
    extended_digest_hex = binascii.hexlify(extended_message_digest)
    extended_message_hex = binascii.hexlify(padded_extended_message)
    print("DIG: ", extended_digest_hex)
    print("MSG: ", extended_message_hex)


def run_test():
    secret = b'0000000000000000'
    message = b'This is a test message'
    extension = b'hopefully this works!'

    sha_obj = sha1()
    sha_obj.update(secret + message)
    default_mac = binascii.unhexlify(sha_obj.hexdigest())
    mac = sha1_homebrew(secret + message)
    assert(default_mac == mac)

    macs = list(unpack('>5L', mac))

    orig_padding = padding(len(secret) + len(message))
    padded_extended_message = message + orig_padding + extension
    extended_message_digest = sha1_homebrew(extension, iv=macs, original_len=(len(secret) + len(message) + len(orig_padding)))
    compare_sha1 = sha1_homebrew(secret + padded_extended_message)
    sha_obj = sha1()
    sha_obj.update(secret + padded_extended_message)
    compare_sha2 = binascii.unhexlify(sha_obj.hexdigest())
    assert(compare_sha1 == compare_sha2 == extended_message_digest)


if __name__ == '__main__':
    run_test()
    run_passoff()


