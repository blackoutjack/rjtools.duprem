import os

def prep(args):
    args.insert(0, "python3")
    args.insert(1, "-m")
    args.insert(2, "duprem")
    return args

TEST_DIR=os.path.dirname(os.path.dirname(__file__))
TEST_FILE_TREE = os.path.join(TEST_DIR, "filetree")

def get_filepath(filename):
    return os.path.join(TEST_FILE_TREE, filename)

run_basic = prep([get_filepath("empty1.txt"), get_filepath("empty2.txt")])

out_basic = '''Duplicate content:
0: %TESTDIR%/filetree/empty1.txt
1: %TESTDIR%/filetree/empty2.txt'''

