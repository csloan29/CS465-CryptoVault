import numpy as np


def extract_state_from_text(state_text, nb):
    data_arr = np.full((nb, nb), 0x00)
    # fill state array by column order, starting with leftmost column first
    index = 0
    for y in range(0, nb):
        for x in range(0, nb):
            data_arr[x][y] = int(state_text[index:index+2], 16)
            index += 2
    return data_arr


def extract_key_from_text(key_text, key_length):
    key_arr = np.full(key_length >> 1, 0x00)
    index = 0
    for x in range(0, key_length >> 1):
        key_arr[x] = int(key_text[index:index+2], 16)
        index += 2
    return key_arr


def return_state_array_to_text(state_array, nb):
    state_string = ''
    for y in range(nb):
        for x in range(nb):
            cell_string = hex(state_array[x][y])[2:4]
            if len(cell_string) < 2:
                cell_string = '0' + cell_string
            state_string = state_string + cell_string
    return state_string


def return_key_array_to_text(key_array, nb):
    key_string = ''
    for y in range(nb):
        for x in range(nb):
            cell_string = hex(key_array[x][y])[2:4]
            if len(cell_string) < 2:
                cell_string = '0' + cell_string
            key_string = key_string + cell_string
    return key_string

