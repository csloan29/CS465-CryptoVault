# python modules
from hashlib import sha1
import binascii
from bitarray import bitarray


def hash_string_to_crop(input_image: str, bit_length: int) -> str:
    assert((bit_length % 4) == 0)
    sha_obj = sha1()
    sha_obj.update(input_image.encode('utf-8'))
    full_hex = sha_obj.hexdigest()
    return full_hex[:int(bit_length / 4)]


