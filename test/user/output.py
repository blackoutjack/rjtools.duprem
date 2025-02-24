'''End-to-end user tests for duplicate detection in duprem'''

import os

from rjtools.util.testutil import Grep

def cmd(args):
    args.insert(0, "python3")
    args.insert(1, "-m")
    args.insert(2, "rjtools.duprem")
    return args

TEST_DIR = os.path.join(os.path.dirname(__file__), "filetree")

def path(filename):
    return os.path.join(TEST_DIR, filename)

run_full_dir = cmd(["-t", "1", TEST_DIR])

out_full_dir = """
Duplicate content:
0: %TESTDIR%/pic4.JPEG
1: %TESTDIR%/pic1.jpg
"""

run_hidden = cmd(["-H", TEST_DIR])

out_hidden = Grep("""Duplicate content:
0: %TESTDIR%/.hiddenrc
1: %TESTDIR%/.anotherhidden""")

run_empty = cmd(["-E", TEST_DIR])

out_empty = Grep("""Duplicate content:
0: %TESTDIR%/empty1.txt
1: %TESTDIR%/empty2.txt""")

'''Basic test ensuring that empty files are processed when user says so'''
run_basic = cmd([path("empty1.txt"), path("empty2.txt")])

out_basic = '''
Duplicate content:
0: %TESTDIR%/empty1.txt
1: %TESTDIR%/empty2.txt'''

'''Negative test showing that differing files are not detected as duplicates'''
run_no_dup = cmd([path("empty1.txt"), path("basic.txt")])

out_no_dup = 'No duplicate files found.'

run_force_no_remove = cmd(["--force", path("empty1")])

code_force_no_remove = 2

err_force_no_remove = Grep("Cannot force removal without --remove")
