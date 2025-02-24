import os

def cmd(args):
    args.insert(0, "python3")
    args.insert(1, "-m")
    args.insert(2, "rjtools.duprem")
    args.insert(3, "--plugin")
    args.insert(4, "image")
    return args

TEST_DIR = os.path.join(os.path.dirname(__file__), "filetree")

def path(filename):
    return os.path.join(TEST_DIR, filename)


run_full_dir = cmd(["-t", "1", TEST_DIR])

out_full_dir = """
Duplicate image content:
0: %TESTDIR%/pic4.JPEG
1: %TESTDIR%/pic1.bmp
2: %TESTDIR%/pic1.jpg
3: %TESTDIR%/pic1.tiff
Duplicate image content:
0: %TESTDIR%/pic2.bmp
1: %TESTDIR%/pic2.tiff
Failures:
%TESTDIR%/badpic2.jpg
"""

err_full_dir = "ERROR: Failure to extract JPEG data (broken data stream when reading image file): %TESTDIR%/badpic2.jpg"


run_same_file = cmd([path("pic1.bmp"), path("pic1.bmp")])

out_same_file = "No duplicate files found."


run_same_content = cmd([path("pic1.bmp"), path("pic1.tiff")])

out_same_content = """
Duplicate image content:
0: %TESTDIR%/pic1.bmp
1: %TESTDIR%/pic1.tiff
"""

run_different_content = cmd([path("pic1.bmp"), path("pic2.bmp")])

out_different_content = "No duplicate files found."


run_same_content_three = cmd([path("pic2.bmp"), path("pic2.tiff"), path("pic2.jpg")])

# %%% Implement perceptual hashing to pick up the jpg.
out_same_content_three = """
Duplicate image content:
0: %TESTDIR%/pic2.bmp
1: %TESTDIR%/pic2.tiff
"""

# %%% Expected output until perceptual hashing is implemented.
out_same_content_three = """
Duplicate image content:
0: %TESTDIR%/pic2.bmp
1: %TESTDIR%/pic2.tiff
"""
