"""
Matching basic patterns.
"""

from env.common.mktree import mktree
from env.common.run import run


def test(tmp_path):

    mktree(path=tmp_path, dir_number=1, file_number=1, depth=2)

    if 1:  # Test 1: A positive match for the `file0.txt` on its context level.

        (tmp_path / '.pylematch').write_text('file0.txt')

        test_cases = {
            'dirA/dirA/file0.txt': False,
            'dirA/file0.txt': False,
            'file0.txt': True,
        }

        run(tmp_path, test_cases, test_name='1')

    if 1:  # Test 2: A leading slash (/) is redundant.
        (tmp_path / '.pylematch').write_text('/file0.txt')

        test_cases = {
            'dirA/dirA/file0.txt': False,
            'dirA/file0.txt': False,
            'file0.txt': True,
        }

        run(tmp_path, test_cases, test_name='2')

    if 1:  # Test 3: Matching a directory pattern.
        (tmp_path / '.pylematch').write_text('dirA/')

        test_cases = {
            'dirA': True,
            'dirA/dirA': False,
            'dirA/file0.txt': False,
        }

        run(tmp_path, test_cases, test_name='3')

    if 1:  # Test 4: Checking for a trailing slashes (/) in directory matching.
        (tmp_path / '.pylematch').write_text('/dirA/')

        test_cases = {
            'dirA': True,
            'dirA/dirA': False,
            'dirA/file0.txt': False,
        }

        run(tmp_path, test_cases, test_name='4')

    mktree(path=tmp_path, dir_number=1, file_number=1, depth=1)

    if 1:  # Test 5: A negative match directory pattern against a file.
        (tmp_path / '.pylematch').write_text('file0.txt/')

        test_cases = {
            'file0.txt': False,
        }

        run(tmp_path, test_cases, test_name='5')

    (tmp_path / 'dirA/dirA').write_text('Ooops! It is a file!')
    if 1:  # Test 6: A negative match file pattern against a directory.
        (tmp_path / '.pylematch').write_text('dirA/dirA')

        test_cases = {
            'dirA/dirA': True,
        }

        run(tmp_path, test_cases, test_name='6')

    if 1:  # Test 7:  A negative match a directory-kind pattern against a file.
        (tmp_path / '.pylematch').write_text('dirA/dirA/')

        test_cases = {
            'dirA/dirA': False,
        }

        run(tmp_path, test_cases, test_name='7')
