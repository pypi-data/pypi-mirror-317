"""
Various tests.
"""

from env.common.run import run
from env.common.mktree import mktree


def test(tmp_path):
    mktree(path=tmp_path, dir_number=3, file_number=1, depth=3)

    if 1:  # Test 1: A test for a rule sequence via negation.
        (tmp_path / '.fls').write_text('**')
        (tmp_path / 'dirA/.fls').write_text('!**/*.log')
        (tmp_path / 'dirA/dirA/.fls').write_text('!.fls')
        (tmp_path / 'dirA/dirA/dirA/.fls').write_text('*.log')
        (tmp_path / 'dirA/dirB/.fls').write_text('!.fls')
        (tmp_path / 'dirB/.fls').write_text('!*')
        (tmp_path / 'dirB/dirB/.fls').write_text('!.fls')
        (tmp_path / 'dirB/dirB/dirB/.fls').write_text('!*.txt')
        (tmp_path / 'dirC/.fls').write_text('*.*')
        (tmp_path / 'dirC/dirC/.fls').write_text('!*.*')
        (tmp_path / 'dirC/dirC/dirC/.fls').write_text('*.*')

        test_cases = {
            'dirA': True,
            'dirA/file0.log': True,
            'dirA/file0.txt': True,
            'dirA/dirA/.fls': False,
            'dirA/dirA/file0.log': False,
            'dirA/dirA/file0.txt': True,
            'dirA/dirA/dirA/file0.log': True,
            'dirA/dirB/file0.log': False,
            'dirA/dirB/file0.txt': True,
            'dirB': True,
            'dirB/dirA/file0.txt': True,
            'dirB/dirB/dirB/file0.txt': False,
            'dirB/dirB/file0.txt': True,
            'dirB/dirB/.fls': False,
            'dirB/file0.txt': False,
            'dirC/dirC/file0.txt': False,
            'dirC/dirC/dirC/file0.txt': True,
            'dirC/.fls': True,
            'dirC/file0.txt': True,
            'file0.log': True,
            'file0.txt': True,
        }

        run(tmp_path, test_cases, test_name='4')
