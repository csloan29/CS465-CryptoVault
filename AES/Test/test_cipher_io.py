from unittest import TestCase
from AES.cipher_io import *


class TestCipherIO(TestCase):

    def test_extract_state_from_text(self):
        # setup
        nb = 4
        state_text = '00112233445566778899aabbccddeeff'
        expected_output = np.array([[0x00, 0x44, 0x88, 0xcc],
                                    [0x11, 0x55, 0x99, 0xdd],
                                    [0x22, 0x66, 0xaa, 0xee],
                                    [0x33, 0x77, 0xbb, 0xff]])
        # test
        self.assert_(np.array_equal(extract_state_from_text(state_text, nb), expected_output))

    def test_extract_key_from_text(self):
        # setup
        key_text = '000102030405060708090a0b0c0d0e0f'
        key_length = 32
        expected_output = np.array([0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
                                    0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f])
        # test
        self.assert_(np.array_equal(extract_key_from_text(key_text, key_length), expected_output))

    def test_return_state_array_to_text(self):
        # setup
        nb = 4
        state = np.array([[0x19, 0xa0, 0x9a, 0xe9],
                          [0x3d, 0xf4, 0xc6, 0xf8],
                          [0xe3, 0xe2, 0x8d, 0x48],
                          [0xbe, 0x2b, 0x2a, 0x08]])
        expected_output = '193de3bea0f4e22b9ac68d2ae9f84808'
        # test
        self.assertEqual(return_state_array_to_text(state, nb), expected_output)
