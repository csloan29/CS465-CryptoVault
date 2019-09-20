# python module imports
import numpy as np

# local file imports
from AES.ff_math import *
from AES.constants import *


def expand_key(key_arr, nb, nk, nr):
    key_block = np.full((nb, (nr + 1) * 4), 0x00)

    # fill first key slice with original key
    key_index = 0
    for x in range(0, nk):
        for y in range(nb):
            key_block[y][x] = key_arr[key_index]
            key_index += 1

    # fill the rest of the expanded key array
    key_index = nk
    while key_index < (nb * (nr + 1)):
        temp_col = key_block[:, key_index - 1]
        if key_index % nk is 0:
            temp_col = rot_word(temp_col, nb)
            temp_col = sub_word(temp_col, nb)
            r_con_column = r_con[:, (int(key_index / nk))]
            for i in range(nb):
                temp_col[i] = ff_add(temp_col[i], r_con_column[i])

        elif (nk is 8) and ((key_index % nk) is 4):
            temp_col = sub_word(temp_col, nb)

        for i in range(nb):
            key_block[i][key_index] = ff_add(temp_col[i], key_block[i][key_index - nk])
        key_index += 1

    return key_block


def rot_word(key_column, nb):
    new_column = np.full((nb,), 0x00)
    for y in range(nb):
        new_column[y] = key_column[(y + 1) % 4]
    return new_column


def sub_word(key_column, nb):
    new_column = np.full((nb,), 0x00)
    for x in range(nb):
        # isolate first and second nibble of byte to get indices
        first_nibble = key_column[x] >> 4
        second_nibble = key_column[x] & 0x0f
        new_column[x] = s_box[first_nibble][second_nibble]
    return new_column
