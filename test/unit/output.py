'''In-memory unit tests for duplicate detection in duprem'''

import os

from duprem.engine import DupEngine
from duprem.plugin import image

TEST_DIR = os.path.join("/", "topdir")
TEST_FILE_TREE = os.path.join(TEST_DIR, "filetree")

engine = DupEngine([image])

def get_filepath(filename):
    return os.path.join(TEST_FILE_TREE, filename)

image_files = [
        get_filepath("pic1.bmp"),
        get_filepath("pic1.jpg"),
        get_filepath("pic1.tiff"),
        get_filepath("pic2.bmp"),
        get_filepath("pic2.jpg"),
        get_filepath("pic2.tiff"),
        get_filepath("pic3.jpg"),
        get_filepath("pic4.JPEG"),
        # This one has the image header, but bad data
        get_filepath("badpic2.jpg"),
    ]

non_image_files = [
        get_filepath("basic.txt"),
        get_filepath("notapic.jpg"),
    ]

def test_is_image():
    '''Test that image detection categorizes files appropriately'''
    result = True
    for file in image_files:
        result &= engine.plugins[0].can_handle(file)
    for file in non_image_files:
        result &= not engine.plugins[0].can_handle(file)
    return result

files_basic = [
        get_filepath("empty1.txt"),
        get_filepath("empty2.txt"),
    ]

def test_basic():
    '''Test basic duplicate file detection'''
    engine.clear()
    foundDups = engine.find_duplicates(files_basic)
    engine.display_duplicates()
    return foundDups

out_basic = """Duplicate content:
0: %TESTDIR%/filetree/empty1.txt
1: %TESTDIR%/filetree/empty2.txt"""

files_no_dups = [
        get_filepath("empty1.txt"),
        get_filepath("basic.txt"),
    ]

def test_no_dups():
    '''Test a negative case for duplicate file detection'''
    engine.clear()
    foundDups = engine.find_duplicates(files_no_dups)
    engine.display_duplicates()
    return not foundDups

out_no_dups = ""


files_jpeg_different_header = [
        get_filepath("pic1.jpg"),
        get_filepath("pic2.jpg"),
    ]

def test_jpeg_dup():
    '''Test a case of duplicate JPEG detection with differing headers'''
    engine.clear()
    foundDups = engine.find_duplicates(files_jpeg_different_header)
    engine.display_duplicates()
    return foundDups

out_jpeg_dup = """Duplicate image content:
0: %TESTDIR%/filetree/pic1.jpg
1: %TESTDIR%/filetree/pic2.jpg"""


files_jpeg_different_image = [
        get_filepath("pic1.jpg"),
        get_filepath("pic3.jpg"),
    ]

def test_jpeg_diff():
    '''Test a negative case for duplicate JPEG detection'''
    engine.clear()
    foundDups = engine.find_duplicates(files_jpeg_different_image)
    engine.display_duplicates()
    return not foundDups

out_jpeg_diff = ""


files_jpeg_extension = [
        get_filepath("pic1.jpg"),
        get_filepath("pic4.JPEG"),
    ]

def test_jpeg_extension():
    '''Test duplicate JPEG detection when the files have different extensions'''
    engine.clear()
    foundDups = engine.find_duplicates(files_jpeg_extension)
    engine.display_duplicates()
    return foundDups

out_jpeg_extension = """Duplicate image content:
0: %TESTDIR%/filetree/pic1.jpg
1: %TESTDIR%/filetree/pic4.JPEG"""


files_jpg_text = [
        get_filepath("notapic.jpg"),
    ]

def test_jpg_text():
    '''Ensure a text file with JPEG extension does not cause a failure'''
    engine.clear()
    foundDups = engine.find_duplicates(files_jpg_text)
    engine.display_failures()
    return not foundDups

out_jpg_text = ""

err_jpg_text = ""


files_twice = [
        get_filepath("basic.txt"),
        get_filepath("basic.txt"),
]

def test_twice():
    '''Test that processing one file twice is not reported as a duplicate'''
    engine.clear()
    foundDups = engine.find_duplicates(files_twice)
    engine.display_duplicates()
    return not foundDups

out_twice = ""


# This file contains valid headers but bad image data.
files_data_failure = [
        get_filepath("badpic2.jpg"),
    ]

def test_data_failure():
    '''Test a JPEG file with corrupt data, and the resulting error'''
    engine.clear()
    foundDups = engine.find_duplicates(files_data_failure)
    engine.display_failures()
    return not foundDups

out_data_failure = """Failures:
  %TESTDIR%/filetree/badpic2.jpg"""

err_data_failure = """ERROR: Failure to extract JPEG data (broken data stream when reading image file): %TESTDIR%/filetree/badpic2.jpg"""


files_bmp_dup = [
        get_filepath("pic1.bmp"),
        get_filepath("pic2.bmp"),
    ]

def test_bmp_dup():
    '''Test detection of duplicate BMP data'''
    engine.clear()
    foundDups = engine.find_duplicates(files_bmp_dup)
    engine.display_duplicates()
    return foundDups

out_bmp_dup = """Duplicate image content:
0: %TESTDIR%/filetree/pic1.bmp
1: %TESTDIR%/filetree/pic2.bmp"""


files_bmp_jpg = [
        get_filepath("pic1.bmp"),
        get_filepath("pic1.jpg"),
    ]

def test_bmp_jpg():
    '''Test detection of duplicate image data in JPEG and BMP files'''
    engine.clear()
    foundDups = engine.find_duplicates(files_bmp_jpg)
    engine.display_duplicates()
    return foundDups

out_bmp_jpg = """Duplicate image content:
0: %TESTDIR%/filetree/pic1.bmp
1: %TESTDIR%/filetree/pic1.jpg"""


files_tiff_dup = [
        get_filepath("pic1.tiff"),
        get_filepath("pic2.tiff"),
    ]

def test_tiff_dup():
    '''Test detection of duplicate image data in TIFF files'''
    engine.clear()
    foundDups = engine.find_duplicates(files_tiff_dup)
    engine.display_duplicates()
    return foundDups

out_tiff_dup = """Duplicate image content:
0: %TESTDIR%/filetree/pic1.tiff
1: %TESTDIR%/filetree/pic2.tiff"""


files_tiff_jpg = [
        get_filepath("pic1.tiff"),
        get_filepath("pic1.jpg"),
    ]

def test_tiff_jpg():
    '''Test detection of duplicate image data in TIFF and JPEG files'''
    engine.clear()
    foundDups = engine.find_duplicates(files_tiff_jpg)
    engine.display_duplicates()
    return foundDups

out_tiff_jpg = """Duplicate image content:
0: %TESTDIR%/filetree/pic1.tiff
1: %TESTDIR%/filetree/pic1.jpg"""


