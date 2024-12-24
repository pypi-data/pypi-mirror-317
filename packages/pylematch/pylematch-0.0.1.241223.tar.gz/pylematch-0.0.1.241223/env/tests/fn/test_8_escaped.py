"""
Escaped patterns test.
"""

import os

from env.common.run import run
from env.common.mktree import mktree


def test(tmp_path):
    # Create test directories and .pylematch rules
    mktree(path=tmp_path, dir_number=1, file_number=1, depth=1)

    if 1:  # Test 1: A positive match for an escaped asterisk (*).
        (tmp_path / '.pylematch').write_text(r'\*')
        (tmp_path / '*').write_text('')

        test_cases = {
            '*': True,
            'file0.txt': False,
        }

        run(tmp_path, test_cases, test_name='1')

    if 1:  # Test 2: A positive match for an escaped double asterisk (**).
        (tmp_path / '.pylematch').write_text(r'\*\*')
        (tmp_path / '**').write_text('')

        test_cases = {
            '**': True,
            'file0.txt': False,
        }

        run(tmp_path, test_cases, test_name='2')

    if 1:  # Test 3: Another positive match for an escaped double asterisk (**).
        (tmp_path / '.pylematch').write_text(r'file\*\*.txt')
        (tmp_path / 'file**.txt').write_text('')

        test_cases = {
            'file**.txt': True,
            'file0.txt': False,
        }

        run(tmp_path, test_cases, test_name='3')

    if 1:  # Test 4: One more positive match for an escaped asterisk used as a directory contents (*).
        (tmp_path / '.pylematch').write_text(r'dirA/\*/')
        os.makedirs(tmp_path / 'dirA/*', exist_ok=True)

        test_cases = {
            'dirA': False,
            'dirA/*': True,
        }

        run(tmp_path, test_cases, test_name='4')

    if 1:  # Test 5: A positive match for an escaped exclamation mark (!).
        (tmp_path / '.pylematch').write_text(r'\!file.txt')
        (tmp_path / '!file.txt').write_text('')

        test_cases = {
            '!file.txt': True,
            'file0.txt': False,
        }

        run(tmp_path, test_cases, test_name='5')

    if 1:  # Test 6: A positive match for an escaped hash (#)
        (tmp_path / '.pylematch').write_text(r'\#file.txt')
        (tmp_path / '#file.txt').write_text('')

        test_cases = {
            '#file.txt': True,
            'file0.txt': False,
        }

        run(tmp_path, test_cases, test_name='6')
