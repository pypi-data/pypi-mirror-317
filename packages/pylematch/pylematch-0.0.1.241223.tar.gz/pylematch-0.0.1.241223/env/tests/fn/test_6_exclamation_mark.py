"""
Exclamation-mark-based patterns test.
"""

from env.common.run import run
from env.common.mktree import mktree


def test(tmp_path):
    mktree(path=tmp_path, dir_number=3, file_number=2, depth=3)

    if 1:  # Test 1.
        (tmp_path / '.pylematch').write_text('file0.txt')
        (tmp_path / 'dirA/.pylematch').write_text('!file0.txt')

        test_cases = {
            'dirA/dirA/file0.txt': False,
            'dirA/file0.txt': False,
            'file0.txt': True,
        }

        run(tmp_path, test_cases, test_name='1')

        (tmp_path / 'dirA/.pylematch').write_text('')

    if 1:  # Test 2.
        (tmp_path / '.pylematch').write_text('!file0.txt\n!file1.log')
        (tmp_path / 'dirA/dirA/.pylematch').write_text('file0.txt')
        (tmp_path / 'dirB/dirB/.pylematch').write_text('file1.log')

    if 1:  # Test 3.
        (tmp_path / '.pylematch').write_text('*\n!file*.*')

        test_cases = {
            'dirA': True,
            'dirB': True,
            'file0.txt': False,
            'file0.log': False,
        }

        run(tmp_path, test_cases, test_name='3')

        (tmp_path / 'dirA/dirB/.pylematch').write_text('')

    if 1:  # Test 4.
        (tmp_path / '.pylematch').write_text('**')
        (tmp_path / 'dirA/dirA/.pylematch').write_text('!**')

        test_cases = {
            'dirA': True,
            'dirA/dirA': True,
            'dirA/dirA/dirA': False,
            'dirA/dirA/dirA/file0.txt': False,
            'dirA/dirA/file0.txt': False,
            'dirA/file0.txt': True,
            'file0.log': True,
        }

        run(tmp_path, test_cases, test_name='4')
