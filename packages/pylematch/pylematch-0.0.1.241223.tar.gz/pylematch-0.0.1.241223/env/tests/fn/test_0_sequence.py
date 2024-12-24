"""
Checking the hierarchical consistency of the rules.
"""

from env.common.run import run
from env.common.mktree import mktree


def test(tmp_path):
    mktree(path=tmp_path, dir_number=3, file_number=1, depth=3)

    if 1:  # Test 1: Checking the sequence of rule application.

        (tmp_path / 'dirA/.pylematch').write_text('file0.txt')

        test_cases = {
            'dirA/dirB/dirC/file0.txt': False,
            'dirA/dirB/file0.txt': False,
            'dirA/file0.txt': True,
            'dirB/file0.txt': False,
            'file0.txt': False,
            'file0.log': False,
        }

        run(tmp_path, test_cases, test_name='1')

    if 1:  # Test 2: Checking the sequence of rule application.
        (tmp_path / 'dirA/.pylematch').write_text('/file0.txt')

        test_cases = {
            'dirA/dirB/dirC/file0.txt': False,
            'dirA/dirB/file0.txt': False,
            'dirA/file0.txt': True,
            'dirB/file0.txt': False,
            'file0.txt': False,
            'file0.log': False,
        }

        run(tmp_path, test_cases, test_name='2')
        (tmp_path / 'dirA/.pylematch').write_text('')  # clear

    if 1:  # Test 3: Checking the sequence of rule application.
        (tmp_path / 'dirA/dirA/.pylematch').write_text('file0.txt')

        test_cases = {
            'dirA/dirA/file0.txt': True,
            'dirA/file0.txt': False,
            'file0.txt': False,
        }

        run(tmp_path, test_cases, test_name='3')

