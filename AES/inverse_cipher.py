# python module imports
import numpy as np

# local file imports
from AES.cipher_io import *
from AES.constants import *
from AES.key_expansion import *
from AES.ff_math import *


class InverseAESCipher:
    # AES CONSTANTS

    # NB - number of rows and columns in state
    NB = 4

    # NK - number of 32-bit words in key
    # (equivalent to number of columns in key with 4 byte height)
    # Possible Key bit-length values: 128, 192, 256
    # Possible NK values: 4, 6, 8
    # Actual value is extracted from key input to cipher below
    # Default is 4
    NK = 4

    # NR - number of rounds
    # NR is a function of NK: [NR=10 if NK=4], [NR=12 if NK=6], [NR=14 if NK=8]
    # Actual value is extracted from key input to cipher below
    # Default is 10
    NR = 10

    def inv_cipher(self, data_in, key):
        # Verbose Details
        print("\nCIPHER  (DECRYPT):")
        print("round[ 0].iinput   ", data_in)

        # adjust NR and NK according to given key length
        key_length = len(key)
        if key_length is 48:
            self.NK = 6
            self.NR = 12
        elif key_length is 64:
            self.NK = 8
            self.NR = 14

        # fill state and key & expand key
        state = extract_state_from_text(data_in, self.NB)
        key_arr = extract_key_from_text(key, key_length)
        # expand key
        expanded_key = expand_key(key_arr, self.NB, self.NK, self.NR)

        # Round 0
        round_key = expanded_key[:, (self.NR * self.NB):((self.NR + 1) * self.NB)]
        state = self.add_round_key(state, round_key)
        # Verbose Details
        print("round[ {}].ik_sch    {}".format(0, return_key_array_to_text(round_key, self.NB)))

        # round tracker for expanded key needed for particular round of encryption
        cipher_round = self.NR - 1

        # iterate through rounds of encryption
        while cipher_round is not 0:
            print("round[ {}].istart    {}".format(self.NR - cipher_round, return_state_array_to_text(state, self.NB)))

            state = self.inv_shift_rows(state)
            print("round[ {}].is_row    {}".format(self.NR - cipher_round, return_state_array_to_text(state, self.NB)))

            state = self.inv_sub_bytes(state)
            print("round[ {}].is_box    {}".format(self.NR - cipher_round, return_state_array_to_text(state, self.NB)))

            round_key = expanded_key[:, (cipher_round * self.NB):((cipher_round + 1) * self.NB)]
            state = self.add_round_key(state, round_key)
            print("round[ {}].ik_sch    {}".format(self.NR - cipher_round, return_key_array_to_text(round_key, self.NB)))
            print("round[ {}].ik_add    {}".format(self.NR - cipher_round, return_state_array_to_text(state, self.NB)))

            state = self.inv_mix_columns(state)

            cipher_round -= 1

        # do final iteration
        state = self.inv_sub_bytes(state)
        print("round[ {}].is_box    {}".format(self.NR - cipher_round, return_state_array_to_text(state, self.NB)))

        state = self.inv_shift_rows(state)
        print("round[ {}].is_row    {}".format(self.NR - cipher_round, return_state_array_to_text(state, self.NB)))

        round_key = expanded_key[:, :self.NB]
        state = self.add_round_key(state, round_key)
        print("round[ {}].ik_sch    {}".format(self.NR - cipher_round, return_state_array_to_text(state, self.NB)))

        # send encrypted data out
        print("round[ {}].ioutput    {}".format(self.NR - cipher_round, return_state_array_to_text(state, self.NB)))
        return return_state_array_to_text(state, self.NB)

    def add_round_key(self, state, key):
        for x in range(self.NB):
            for y in range(self.NB):
                state[x][y] = ff_add(state[x][y], key[x][y])
        return state

    def inv_sub_bytes(self, state):
        for x in range(0, self.NB):
            for y in range(0, self.NB):
                # isolate first and second nibble of byte to get indices
                first_nibble = state[x][y] >> 4
                second_nibble = state[x][y] & 0x0f
                state[x][y] = invert_s_box[first_nibble][second_nibble]
        return state

    def inv_shift_rows(self, state):
        offset = 3
        # start at row index 1 (row 0 does not shift)
        for x in range(1, self.NB):
            new_row = np.full(self.NB, 0x00)
            for y in range(0, self.NB):
                new_row[y] = state[x][(y + offset) % self.NB]
            state[x] = new_row
            offset -= 1
        return state

    def inv_mix_columns(self, state):
        new_arr = np.full((self.NB, self.NB), 0x00)
        # for each column in state
        for y in range(0, self.NB):
            # for each item within the state column
            for x in range(0, self.NB):
                count = 0
                while count < self.NB:
                    new_arr[x][y] = ff_add(new_arr[x][y], ff_multiply(
                        state[count][y], static_invert_mix_arr[x][count]))
                    count += 1
        return new_arr
