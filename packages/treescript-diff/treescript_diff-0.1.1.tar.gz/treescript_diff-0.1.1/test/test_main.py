"""Testing Main Module.
"""
import pytest
from pathlib import Path

from treescript_diff.__main__ import main


def test_main_():
    from sys import argv, orig_argv
    argv.clear()
    argv.append('treescript-diff')
    argv.append('original')
    argv.append('updated')

    # Mock files
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'read_text', lambda _: "src/")
        main()


    argv.clear()
    for i in orig_argv:
        argv.append(i)
