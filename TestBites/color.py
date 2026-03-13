from collections.abc import Iterator
from random import sample


def gen_hex_color() -> Iterator[str]:
    while True:
        r, g, b = sample(range(256), 3)
        yield f'#{r:02x}{g:02x}{b:02x}'.upper()
