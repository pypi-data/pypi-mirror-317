"""
Question-mark-based patterns test.
"""

from env.common.run import run
from env.common.mktree import mktree


def test(tmp_path):
    mktree(path=tmp_path, dir_number=2, file_number=2, depth=3)

    if 1:  # Test 1: A positive match for filename where the "?" represents exactly one character excepting a slash (/).
        (tmp_path / '.pylematch').write_text('file?.txt')

        test_cases = {
            'file0.txt': True,
            'file1.txt': True,
        }

        run(tmp_path, test_cases, test_name='1')

    if 1:  # Test 2:  A negative match because "the `?` represents exactly one character".
        (tmp_path / '.pylematch').write_text('file0?.txt')

        test_cases = {
            'file0.txt': False,
        }

        run(tmp_path, test_cases, test_name='2')

    if 1:  # Test 3:  A negative match because "other than a slash (/)"..
        (tmp_path / '.pylematch').write_text('dirA?file0.txt')

        test_cases = {
            'dirA/file0.txt': False,
        }

        run(tmp_path, test_cases, test_name='3')

    if 1:  # Test 4: A positive match of multiple question marks.
        (tmp_path / '.pylematch').write_text('f???????t')

        test_cases = {
            'file0.txt': True,
            'file1.txt': True,
        }

        run(tmp_path, test_cases, test_name='4')
