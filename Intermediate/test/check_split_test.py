from pathlib import Path
import sys

import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent))

from check_split import check_split


@pytest.mark.parametrize("args, expected", [
    (('$8.68', '4.75%', '10%', 3), '$10.00'),
    (('$8.44', '6.75%', '11%', 3), '$10.00'),
    (('$9.99', '3.25%', '10%', 2), '$11.34'),
    (('$186.70', '6.75%', '18%', 6), '$235.17'),
    (('$191.57', '6.75%', '15%', 6), '$235.18'),
    (('$0.00', '0%', '0%', 1), '$0.00'),
    (('$100.03', '0%', '0%', 4), '$100.03'),
    (('$141.86', '2%', '18%', 9), '$170.75'),
    (('$16.99', '10%', '20%', 1), '$22.43'),
    (('$16.99', '10%', '20%', 2), '$22.43'),
    (('$16.99', '10%', '20%', 3), '$22.43'),
    (('$16.99', '10%', '20%', 4), '$22.43'),
])
def test_check_split(args, expected):
    grand_total, splits = check_split(*args)
    assert grand_total == expected
    assert grand_total == f'${sum(splits)}'
