
def bit_len(int_type):
    length = 0
    while int_type:
        int_type >>= 1
        length += 1
    return length


def ff_add(*fields):
    final = 0x00
    for field in fields:
        final = final ^ field
    return final


def x_time(field):
    field = field << 1
    if field >= 0x100:
        field = ff_add(field, 0x11b)
    return field


def ff_multiply(field1, field2):
    final = exponent = intermediate = 0x00
    while 1:
        # step 1: calculate intermediate
        if intermediate:
            intermediate = x_time(intermediate)
        else:
            intermediate = field1
        # step 2: decide whether to xor add intermediate to final value
        if 2**exponent & field2:
            final = ff_add(final, intermediate)
        # step 3: increment exponent (bit in field 2) and test whether this bit is larger than field2
        exponent += 1
        if 2**exponent > field2:
            break
    return final
