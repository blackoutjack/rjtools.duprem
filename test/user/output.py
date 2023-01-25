'''End-to-end user tests for duplicate detection in duprem'''

import os

def prep(args):
    args.insert(0, "python3")
    args.insert(1, "-m")
    args.insert(2, "duprem")
    return args

TEST_DIR = os.path.join(os.path.dirname(__file__), "filetree")

def get_filepath(filename):
    return os.path.join(TEST_DIR, filename)

'''Basic test ensuring that empty files are detected as duplicates'''
run_basic = prep([get_filepath("empty1.txt"), get_filepath("empty2.txt")])

out_basic = '''Duplicate content:
0: %TESTDIR%/empty1.txt
1: %TESTDIR%/empty2.txt'''

'''Negative test showing that differing files are not detected as duplicates'''
run_no_dup = prep([get_filepath("empty1.txt"), get_filepath("basic.txt")])

out_no_dup = 'INFO: No duplicate files found.'

