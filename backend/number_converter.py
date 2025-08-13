# -*- coding: utf-8 -*-
"""
A robust and correct implementation for converting integers to Chinese numerals.
"""

NUM_MAP = {0: "零", 1: "一", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 7: "七", 8: "八", 9: "九"}
UNIT_MAP = {
    1: "",
    10: "十",
    100: "百",
    1000: "千",
}

def to_chinese_numeral(num):
    """
    Converts an integer (0-9999) to its idiomatic Chinese numeral representation.
    """
    if not isinstance(num, int) or not 0 <= num <= 9999:
        raise ValueError("Input must be an integer between 0 and 9999.")

    if num == 0:
        return NUM_MAP[0]

    s = str(num)
    length = len(s)
    res = ""
    zero_added = False

    for i, digit_char in enumerate(s):
        digit = int(digit_char)
        unit_power = 10 ** (length - 1 - i)

        if digit == 0:
            # If the digit is 0, we might need to add a "零".
            # We add "零" only if we haven't just added one.
            if not zero_added:
                # We only add "零" if it's not the last digit.
                # e.g., for 110, we don't say "一百一十零".
                if i < length - 1:
                    res += NUM_MAP[0]
                    zero_added = True
        else:
            # If the digit is not 0, append the digit and its unit.
            # Special case for "一十" (yī shí) which should be "十" (shí).
            if digit == 1 and unit_power == 10 and i == 0:
                 res += UNIT_MAP[unit_power]
            else:
                 res += NUM_MAP[digit] + UNIT_MAP[unit_power]
            zero_added = False

    # Cleanup: If the result ends with "零", remove it.
    if res.endswith(NUM_MAP[0]):
        res = res[:-1]

    return res
