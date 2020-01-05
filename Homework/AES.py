from Crypto.Cipher import AES


def pad(m):
    return m + chr(16 - len(m) % 16) * (16 - len(m) % 16)

def unpad(ct):
    return ct[:-ct[-1]]

def encrypt(mode, key, iv, pt_text):
    if len(key) % 16 != 0:
        key = pad(key)
    if len(iv) % 16 != 0:
        iv = pad(iv)
    if len(pt_text) % 16 != 0:
        pt_text = pad(pt_text)

    cipher = AES.new(key, mode, iv)
    cipher_text = cipher.encrypt(pt_text)
    return cipher_text

def decrypt(mode, key, iv, cipher_text):
    if len(key) % 16 != 0:
        key = pad(key)
    if len(iv) % 16 != 0:
        iv = pad(iv)

    cipher = AES.new(key, mode, iv)
    cipher_output = cipher.decrypt(cipher_text)
    return unpad(cipher_output)


if __name__ == '__main__':

    pt_file = open('/Users/Carter/Desktop/aes-text.txt', 'r')
    file_text = pt_file.read()
    my_key = 'This is a key123'
    my_iv = 'This is an IV456'

    mode = AES.MODE_CBC
    encryption_text = encrypt(mode, my_key, my_iv, file_text)
    print(encryption_text)
    decryption_text = decrypt(mode, my_key, my_iv, encryption_text)
    print(decryption_text)

    mode = AES.MODE_CFB
    encryption_text = encrypt(mode, my_key, my_iv, file_text)
    print(encryption_text)
    decryption_text = decrypt(mode, my_key, my_iv, encryption_text)
    print(decryption_text)

    print('DONE')
