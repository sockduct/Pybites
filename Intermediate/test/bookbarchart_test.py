from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from bookbarchart import create_chart

expected_lines = """02-13 ...........
02-14 ..............
02-15 .................
02-16 ............
02-19 🐍.......🐍
02-20 ...
02-21 ..............🐍
02-22 🐍...................""".split('\n')

def test_valid_output(capfd):
    create_chart()
    out, _ = capfd.readouterr()
    for line in expected_lines:
        assert line in out, f'"{line}" should be in output of create_chart'
