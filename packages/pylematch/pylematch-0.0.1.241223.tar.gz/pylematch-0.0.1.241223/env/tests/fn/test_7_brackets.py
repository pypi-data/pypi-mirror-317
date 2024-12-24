"""
Brackets-based patterns test.
"""

from env.common.run import run
from env.common.mktree import mktree


def test(tmp_path):
    mktree(path=tmp_path, dir_number=3, file_number=5, depth=3)

    if 1:  # Test 1: Any file matching the pattern "file?.txt" where the "?" is a digit from 0 to 2.
        (tmp_path / '.pylematch').write_text('file[0-2].txt')

        test_cases = {
            'file0.txt': True,
            'file1.txt': True,
            'file2.txt': True,
        }

        run(tmp_path, test_cases, test_name='1')

    if 1:  # Test 2: Any file matching the pattern "file?.txt" where the "?" is a digit 0 or 2.
        (tmp_path / '.pylematch').write_text('file[02].txt')

        test_cases = {
            'file0.txt': True,
            'file1.txt': False,
            'file2.txt': True,
        }

        run(tmp_path, test_cases, test_name='2')

    if 1:  # Test 3: Any file matching the pattern "file?.txt" where the "?" is any character except those from 0 to 2.
        (tmp_path / '.pylematch').write_text('file[!0-2].txt')

        test_cases = {
            'file0.txt': False,
            'file1.txt': False,
            'file2.txt': False,
            'file3.txt': True,
        }

        run(tmp_path, test_cases, test_name='3')

    if 1:  # Test 4: Any file matching the pattern "file?.txt"  where the "?" is neither "0" nor "1".
        (tmp_path / '.pylematch').write_text('file[!01].txt')

        test_cases = {
            'file0.txt': False,
            'file1.txt': False,
            'file2.txt': True,
        }

        run(tmp_path, test_cases, test_name='4')

    if 1:  # Test 5: Any directory matching the pattern "dir?/" where the "?" is "A".
        (tmp_path / '.pylematch').write_text('dir[A]/')

        test_cases = {
            'dirA': True,
            'dirA/dirA': False,
            'dirB': False,
        }

        run(tmp_path, test_cases, test_name='5')

    if 1:  # Test 6: Any directory matching the pattern "dir?/", where "?" is any character except those from "C" to "Z".
        (tmp_path / '.pylematch').write_text('dir[!C-Z]/')

        test_cases = {
            'dirA': True,
            'dirB': True,
            'dirC': False,
        }

        run(tmp_path, test_cases, test_name='6')

    if 1:  # Test 7: Any path matching the pattern "dir?/file0.txt", where the "?" is either "A" or "C".
        (tmp_path / '.pylematch').write_text('dir[AC]/file0.txt')

        test_cases = {
            'dirA/file0.txt': True,
            'dirB/file0.txt': False,
            'dirC/file0.txt': True,
        }

        run(tmp_path, test_cases, test_name='7')

    if 1:  # Test 8: Any path matching the pattern "dir?/file0.txt", where the "?" is neither "B" nor "Z".
        (tmp_path / '.pylematch').write_text('dir[!BZ]/file0.txt')

        test_cases = {
            'dirA/file0.txt': True,
            'dirB/file0.txt': False,
            'dirC/file0.txt': True,
        }

        run(tmp_path, test_cases, test_name='8')
