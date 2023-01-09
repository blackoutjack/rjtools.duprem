import os

from duprem.file import find_duplicates, display_duplicates, display_failures, clear

TEST_DIR = os.path.dirname(__file__)

files_basic = [
        os.path.join(TEST_DIR, "filetree", "empty1.txt"),
        os.path.join(TEST_DIR, "filetree", "empty2.txt"),
    ]

def test_basic():
    clear()
    find_duplicates(files_basic)
    display_duplicates()
    return True

out_basic = """Duplicate content:
0: %TESTDIR%/filetree/empty1.txt
1: %TESTDIR%/filetree/empty2.txt"""

files_no_dups = [
        os.path.join(TEST_DIR, "filetree", "empty1.txt"),
        os.path.join(TEST_DIR, "filetree", "basic.txt"),
    ]

def test_no_dups():
    clear()
    find_duplicates(files_no_dups)
    display_duplicates()
    return True

out_no_dups = ""


files_jpeg_different_header = [
        os.path.join(TEST_DIR, "filetree", "pic1.jpg"),
        os.path.join(TEST_DIR, "filetree", "pic2.jpg"),
    ]

def test_jpeg_dup():
    clear()
    find_duplicates(files_jpeg_different_header)
    display_duplicates()
    return True

out_jpeg_dup = """Duplicate image content:
0: %TESTDIR%/filetree/pic1.jpg
1: %TESTDIR%/filetree/pic2.jpg"""


files_jpeg_different_image = [
        os.path.join(TEST_DIR, "filetree", "pic1.jpg"),
        os.path.join(TEST_DIR, "filetree", "pic3.jpg"),
    ]


def test_jpeg_diff():
    clear()
    find_duplicates(files_jpeg_different_image)
    display_duplicates()
    return True

out_jpeg_diff = ""

files_jpeg_extension = [
        os.path.join(TEST_DIR, "filetree", "pic1.jpg"),
        os.path.join(TEST_DIR, "filetree", "pic4.JPEG"),
    ]

def test_jpeg_extension():
    clear()
    find_duplicates(files_jpeg_extension)
    display_duplicates()
    return True

out_jpeg_extension = """Duplicate image content:
0: %TESTDIR%/filetree/pic1.jpg
1: %TESTDIR%/filetree/pic4.JPEG"""


files_failure = [
        os.path.join(TEST_DIR, "filetree", "badpic.jpg"),
    ]

def test_failure():
    clear()
    find_duplicates(files_failure)
    display_failures()
    return True

out_failure = """Failures:
  %TESTDIR%/filetree/badpic.jpg"""

err_failure = """WARNING: Unable to open JPEG (cannot identify image file '%TESTDIR%/filetree/badpic.jpg'): %TESTDIR%/filetree/badpic.jpg"""


files_twice = [
        os.path.join(TEST_DIR, "filetree", "basic.txt"),
        os.path.join(TEST_DIR, "filetree", "basic.txt"),
]

def test_twice():
    clear()
    find_duplicates(files_twice)
    display_duplicates()
    return True

out_twice = ""

