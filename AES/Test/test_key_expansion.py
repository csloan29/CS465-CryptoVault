# library imports
from unittest import TestCase
import numpy as np

# local file imports
from AES.key_expansion import *


class TestKeyExpansion(TestCase):

    def test_expand_key(self):
        # setup
        nb = 4
        nk = 4
        nr = 10
        key = np.array([0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6,
                        0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c])

        expected_expanded_key = np.array([[0x2b, 0x28, 0xab, 0x09, 0xa0, 0x88, 0x23, 0x2a, 0xf2, 0x7a, 0x59, 0x73],
                                          [0x7e, 0xae, 0xf7, 0xcf, 0xfa, 0x54, 0xa3, 0x6c, 0xc2, 0x96, 0x35, 0x59],
                                          [0x15, 0xd2, 0x15, 0x4f, 0xfe, 0x2c, 0x39, 0x76, 0x95, 0xb9, 0x80, 0xf6],
                                          [0x16, 0xa6, 0x88, 0x3c, 0x17, 0xb1, 0x39, 0x05, 0xf2, 0x43, 0x7a, 0x7f]])

        expanded_key = expand_key(key, nb, nk, nr)
        # check if the first three keys are correct (didn't want to type out whole expanded key for test)
        self.assert_(np.array_equal(expanded_key[:, :12], expected_expanded_key))

    def test_sub_word(self):
        # setup
        nb = 4
        input_column = np.array([0x19, 0xa0, 0x9a, 0xe9])
        expected_output_column = np.array([0xd4, 0xe0, 0xb8, 0x1e])
        # test
        self.assertTrue(np.array_equal(sub_word(input_column, nb), expected_output_column))

    def test_rot_word(self):
        # setup
        nb = 4
        input_column = np.array([[0x2b], [0x28], [0xab], [0x09]])
        expected_output_column = np.array([0x28, 0xab, 0x09, 0x2b])
        # test
        self.assertTrue(np.array_equal(rot_word(input_column, nb), expected_output_column))


