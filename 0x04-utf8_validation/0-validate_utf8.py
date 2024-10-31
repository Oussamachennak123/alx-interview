#!/usr/bin/python3
"""UTF-8 validation module
"""


def validUTF8(data):
    """Checks if a list of integers are valid UTF-8 codepoints
    See <https://datatracker.ietf.org/doc/html/rfc3629#page-4>
    """
    skip = 0
    n = len(data)
    for a in range(n):
        if skip > 0:
            skip -= 1
            continue
        if type(data[a]) != int or data[a] < 0 or data[a] > 0x10ffff:
            return False
        elif data[a] <= 0x7f:
            skip = 0
        elif data[a] & 0b11111000 == 0b11110000:
            # 4-byte utf-8 character encoding
            span = 4
            if n - a >= span:
                next_body = list(map(
                    lambda x: x & 0b11000000 == 0b10000000,
                    data[a + 1: a + span],
                ))
                if not all(next_body):
                    return False
                skip = span - 1
            else:
                return False
        elif data[a] & 0b11110000 == 0b11100000:
            # 3-byte utf-8 character encoding
            span = 3
            if n - a >= span:
                next_body = list(map(
                    lambda x: x & 0b11000000 == 0b10000000,
                    data[a + 1: a + span],
                ))
                if not all(next_body):
                    return False
                skip = span - 1
            else:
                return False
        elif data[a] & 0b11100000 == 0b11000000:
            # 2-byte utf-8 character encoding
            span = 2
            if n - a >= span:
                next_body = list(map(
                    lambda x: x & 0b11000000 == 0b10000000,
                    data[a + 1: a + span],
                ))
                if not all(next_body):
                    return False
                skip = span - 1
            else:
                return False
        else:
            return False
    return True
