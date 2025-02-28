#! /usr/bin/env python3.13
'''
Convert rgb tuple (128, 128, 0) to hexadecimal equivalent: #808000
Check each r, g and b int is [0 - 255] or raise ValueError
'''


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    """Receives (r, g, b)  tuple, checks if each rgb int is within RGB
       boundaries (0, 255) and returns its converted hex, for example:
       Silver: input tuple = (192,192,192) -> output hex str = #C0C0C0"""
    min_val = 0
    max_val = 255
    if not all(min_val <= val <= max_val for val in rgb):
        raise ValueError(f'Expected all components in the range 0 - 255, got: {rgb}')

    # return f'#{"".join(hex(val)[2:].zfill(2).upper() for val in rgb)}'
    # Better:
    return '#' + ''.join(f'{val:02x}' for val in rgb).upper()


if __name__ == '__main__':
    assert rgb_to_hex((128, 128, 0)) == '#808000', 'Incorrect value from rgb_to_hex'
