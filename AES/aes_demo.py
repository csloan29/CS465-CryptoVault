from AES.cipher import AESCipher
from AES.inverse_cipher import InverseAESCipher


def demo_aes():
    aes = AESCipher()
    cipher_input_text = '00112233445566778899aabbccddeeff'
    cipher_key_text_128 = '000102030405060708090a0b0c0d0e0f'
    cipher_key_text_192 = '000102030405060708090a0b0c0d0e0f1011121314151617'
    cipher_key_text_256 = '000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f'
    encrypted_text_128 = '69c4e0d86a7b0430d8cdb78070b4c55a'
    encrypted_text_192 = 'dda97ca4864cdfe06eaf70a0ec0d7191'
    encrypted_text_256 = '8ea2b7ca516745bfeafc49904b496089'

    aes = AESCipher()
    aes_inverse = InverseAESCipher()

    print("\nPLAINTEXT:        ", cipher_input_text)
    print("KEY:              ", cipher_key_text_128)
    aes.cipher(cipher_input_text, cipher_key_text_128)
    aes_inverse.inv_cipher(encrypted_text_128, cipher_key_text_128)

    print("\nPLAINTEXT:        ", cipher_input_text)
    print("KEY:              ", cipher_key_text_192)
    aes.cipher(cipher_input_text, cipher_key_text_192)
    aes_inverse.inv_cipher(encrypted_text_192, cipher_key_text_192)

    print("\nPLAINTEXT:        ", cipher_input_text)
    print("KEY:              ", cipher_key_text_256)
    aes.cipher(cipher_input_text, cipher_key_text_256)
    aes_inverse.inv_cipher(encrypted_text_256, cipher_key_text_256)


