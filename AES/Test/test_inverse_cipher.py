# library imports
from unittest import TestCase
import numpy as np

# local file imports
from AES.key_expansion import *
from AES.inverse_cipher import InverseAESCipher as invCipher


class TestInverseCipher(TestCase):

    def test_inv_cipher(self):
        # setup
        aes = invCipher()
        expected_output_text = '00112233445566778899aabbccddeeff'
        cipher_key_text_128 = '000102030405060708090a0b0c0d0e0f'
        cipher_key_text_192 = '000102030405060708090a0b0c0d0e0f1011121314151617'
        cipher_key_text_256 = '000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f'
        input_text_128 = '69c4e0d86a7b0430d8cdb78070b4c55a'
        input_text_192 = 'dda97ca4864cdfe06eaf70a0ec0d7191'
        input_text_256 = '8ea2b7ca516745bfeafc49904b496089'
        # test
        cipher_output_text = aes.inv_cipher(input_text_128, cipher_key_text_128)
        self.assertEqual(cipher_output_text, expected_output_text)
        cipher_output_text = aes.inv_cipher(input_text_192, cipher_key_text_192)
        self.assertEqual(cipher_output_text, expected_output_text)
        cipher_output_text = aes.inv_cipher(input_text_256, cipher_key_text_256)
        self.assertEqual(cipher_output_text, expected_output_text)

    def test_inv_sub_bytes(self):
        # setup
        aes = invCipher()
        state = np.array([[0xd4, 0xe0, 0xb8, 0x1e],
                                   [0x27, 0xbf, 0xb4, 0x41],
                                   [0x11, 0x98, 0x5d, 0x52],
                                   [0xae, 0xf1, 0xe5, 0x30]])
        expected_state = np.array([[0x19, 0xa0, 0x9a, 0xe9],
                                   [0x3d, 0xf4, 0xc6, 0xf8],
                                   [0xe3, 0xe2, 0x8d, 0x48],
                                   [0xbe, 0x2b, 0x2a, 0x08]])
        # test
        self.assert_(np.array_equal(aes.inv_sub_bytes(expected_state), state))

    def test_inv_shift_rows(self):
        # setup
        aes = invCipher()
        state = np.array([[0xd4, 0xe0, 0xb8, 0x1e],
                          [0xb4, 0x41, 0x27, 0xbf],
                          [0x11, 0x98, 0x5d, 0x52],
                          [0xe5, 0x30, 0xae, 0xf1]])
        expected_state = np.array([[0xd4, 0xe0, 0xb8, 0x1e],
                                   [0xbf, 0xb4, 0x41, 0x27],
                                   [0x5d, 0x52, 0x11, 0x98],
                                   [0x30, 0xae, 0xf1, 0xe5]])
        # test
        self.assert_(np.array_equal(aes.inv_shift_rows(state), expected_state))

    def test_inv_mix_columns(self):
        # setup
        aes = invCipher()
        state = np.array([[0x04, 0xe0, 0x48, 0x28],
                          [0x66, 0xcb, 0xf8, 0x06],
                          [0x81, 0x19, 0xd3, 0x26],
                          [0xe5, 0x9a, 0x7a, 0x4c]])
        expected_state = np.array([[0xd4, 0xe0, 0xb8, 0x1e],
                                   [0xbf, 0xb4, 0x41, 0x27],
                                   [0x5d, 0x52, 0x11, 0x98],
                                   [0x30, 0xae, 0xf1, 0xe5]])
        # test
        self.assert_(np.array_equal(aes.inv_mix_columns(state), expected_state))