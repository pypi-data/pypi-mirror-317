"""
Nested patterns hierarchy test.
"""

from env.common.run import run
from env.common.mktree import mktree


def test(tmp_path):
    if 1:  # Test 1: Checking the sequence of rule application.
        mktree(path=tmp_path, dir_number=2, file_number=1, depth=2)

        (tmp_path / 'dirA/.pylematch').write_text('file0.txt')

        test_cases = {
            'dirA/file0.txt': True,
            'dirA/dirA/file0.txt': False,
            'dirB/file0.txt': False,
            'file0.txt': False,
        }

        run(tmp_path, test_cases, test_name='1')

    if 1:  # Test 2: Checking the sequence of rule application.
        mktree(path=tmp_path, dir_number=2, file_number=1, depth=2)

        (tmp_path / 'dirA/.pylematch').write_text('dirA/')

        test_cases = {
            'dirA': False,
            'dirA/dirA': True,
            'dirA/dirA/file0.txt': False,
            'dirB/dirA': False,
        }

        run(tmp_path, test_cases, test_name='2')

    if 1:  # Test 3: Checking the sequence of rule application.
        mktree(path=tmp_path, dir_number=1, file_number=1, depth=2)

        (tmp_path / '.pylematch').write_text('dirA/file0.txt')

        test_cases = {
            'dirA/file0.txt': True,
            'dirA/dirA/file0.txt': False,
        }

        run(tmp_path, test_cases, test_name='3')

    if 1:  # Test 4: Checking the sequence of rule application.
        mktree(path=tmp_path, dir_number=1, file_number=0, depth=3)

        (tmp_path / '.pylematch').write_text('dirA/dirA/')

        test_cases = {
            'dirA/dirA': True,
            'dirA/dirA/dirA': False,
        }

        run(tmp_path, test_cases, test_name='4')

    if 1:  # Test 5: Checking the sequence of rule application.
        mktree(path=tmp_path, dir_number=1, file_number=0, depth=2)

        (tmp_path / '.pylematch').write_text('dirA/file0.txt')
        (tmp_path / 'dirA/.pylematch').write_text('!file0.txt')

        test_cases = {
            'dirA/file0.txt': False,
        }

        run(tmp_path, test_cases, test_name='5')
