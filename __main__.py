#
# Identify files containing duplicate content within a filesystem location.
# Intended for use with media files such as images or audio.
#

import sys
import os
import io
import hashlib
import exifread
# Pillow requires (at least some of) the following Cygwin packages
#    mingw-w64-x86_64-libjpeg-turbo \
#    mingw-w64-x86_64-zlib \
#    mingw-w64-x86_64-tiff \
#    mingw-w64-x86_64-freetype \
#    mingw-w64-x86_64-lcms2 \
#    mingw-w64-x86_64-libwebp \
#    mingw-w64-x86_64-openjpeg2 \
#    mingw-w64-x86_64-libimagequant \
#    mingw-w64-x86_64-libraq
#    jpeg
#    python39-devel
from PIL import Image, UnidentifiedImageError
from optparse import OptionParser

# My custom utility module
from util.msg import set_debug, dbg, info, warn, err

BUF_SIZE = 65536

content_paths = {}
image_content_paths = {}
failures = []

# Print a zero-indexed list of paths
def display_paths(paths):
    for idx, path in enumerate(paths):
        print("%d: %s" % (idx, path))

# Unlink (i.e. delete) the given files, except for the one at the given index.
def unlink_files_except(paths, keep):
    # Check and prep arguments
    if type(keep) is int:
        # Make a single-item list to allow consistent processing.
        keep = [keep]
    elif type(keep) is list:
        # Type check
        for item in keep:
            if not type(item) is int:
                raise ValueError("Unhandled type for keep values: %r" % item)
    else:
        raise ValueError("Unhandled type for keep value: %r" % keep)
        
    for idx, path in enumerate(paths):
        if idx not in keep:
            print("> Deleting: %s" % path)
            os.unlink(path)
        else:
            print(">  Keeping: %s" % path)

def remove_paths(paths, force, desc):
    if len(paths) <= 1:
        return True

    print("Duplicate %s content:" % desc)

    if force:
        # Delete all files except for the first.
        unlink_files_except(paths, 0)
            
    else:
        # Get input from the user for which file to retain.
        choice = None
        display_paths(paths)
        print("k: Keep all")
        while True:
            choice = input("Retain which %s(s) (comma-separated)? " % desc)
            choice = choice.strip()
            if choice == "k":
                break
            if choice == "q":
                # Tell the calling function to quit.
                return False
            try:
                choices = choice.split(",")
                dbg("CHOICES: %r" % choices)    
                keep = []
                for c in choices:
                    dbg("C: %r" % c)
                    num = int(c.strip())
                    dbg("NUM: %d" % num)
                    if num < 0 or num >= len(paths):
                        raise ValueError
                    keep.append(num)
                dbg("KEEP: %r")
                unlink_files_except(paths, keep)
                break
            except ValueError as ex:
                dbg("E: %s" % str(ex))
                # Redo the input
                pass

    return True

# For each set of duplicate files, ask the user which to keep.
def remove_duplicates(force):
    for paths in content_paths.values():
        keepgoing = remove_paths(paths, force, "file")
        if not keepgoing: return

    for image_paths in image_content_paths.values():
        keepgoing = remove_paths(image_paths, force, "image")
        if not keepgoing: return

def display_failures():
    if len(failures) > 0:
        print("Failures:")
        for filepath in failures:
            print("  %s" % filepath)
                    
# Output sets of paths that contain duplicate content.
def display_duplicates():
    for paths in content_paths.values():
        if len(paths) > 1:
            print("Duplicate content:")
            display_paths(paths)

    for image_paths in image_content_paths.values():
        if len(image_paths) > 1:
            print("Duplicate image content:")
            display_paths(image_paths)

def update_hashmap(hashmap, key, value):
    if key not in hashmap:
        hashmap[key] = []
    dbg("%s => %s" % (key, value))
    hashmap[key].append(value)

def hash_file_bytes(fl, hashfn):
    while True:
        data = fl.read(BUF_SIZE)
        if not data:
            break
        hashfn.update(data)

# Create a hash of the contents of a general file.
def hash_file(filepath):
    hashfn = hashlib.sha1()
    
    _, ext = os.path.splitext(filepath)
    ext = ext.lower()
    if ext == ".jpg" or ext == ".jpeg":
        hash_jpeg(hashfn, filepath)
    else:
        # Read the file and pass to the hash function.
        # Buffer the file to limit memory use.
        with open(filepath, 'rb') as f:
            hash_file_bytes(f, hashfn)
            update_hashmap(content_paths, hashfn.hexdigest(), filepath)

# Create a hash of the image data in a JPEG. Don't include EXIF headers
# and canonicalize by converting to BMP data.
def hash_jpeg(hashfn, filepath):
    # Use pillow module to convert to BMP.
    try:
        with Image.open(filepath) as jpg:
            imagebytes = io.BytesIO()
            try:
                jpg.save(imagebytes, format='BMP')
                imagebytes.seek(0)
                hash_file_bytes(imagebytes, hashfn)
                update_hashmap(image_content_paths, hashfn.hexdigest(), filepath)
            except OSError as ex:
                warn("Failure to convert JPEG to BMP (%s): %s" % (str(ex), filepath))
                failures.append(filepath)
    except UnidentifiedImageError as ex:
        warn("Unable to open JPEG (%s): %s" % (str(ex), filepath))
        failures.append(filepath)
        

# Recursively walk a directory to generate file hashes.
def walk_dir(basedir):
    for subdir, dirs, files in os.walk(basedir):
        for file in files:
            filepath = os.path.join(subdir, file)
            filehash = hash_file(filepath)

def handle_duplicates(remove, force):
    if remove:
        remove_duplicates(force)
    else:
        display_duplicates()

    display_failures()

def main():
    parser = OptionParser(usage="python3 -m duprem [-rfg] DIR")
    parser.add_option(
        "-g", "--debug", dest="debug", action="store_true",
        help="Enable debug output")
    parser.add_option(
        "-r", "--remove", dest="remove", action="store_true",
        help="Give the user the option to remove duplicate files.")
    parser.add_option(
        "-f", "--force", dest="force", action="store_true",
        help="With \"remove\", force removal of all but the first copy of duplicate content.")
    opts, args = parser.parse_args()
    if len(args) < 1:
        parser.error(
            """Provide at least one directory (or multiple files) to \
scan for duplicates""")

    set_debug(opts.debug)
    dbg("Arguments: %r" % args)
    for base in args:
        if os.path.isfile(base):
            dbg("File: %s" % base)
            hash_file(base)
        else:
            dbg("Basedir: %s" % base)
            walk_dir(base)
    handle_duplicates(opts.remove, opts.force)

    return 0

if __name__ == "__main__":
    main()


