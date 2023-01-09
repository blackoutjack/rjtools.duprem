#
# Identify files containing duplicate content within a filesystem location.
# Intended for use with media files such as images or audio.
#

import sys
import os
import io
import hashlib
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

# Paths that have already been evaluated
processed_paths = {}

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
    foundDuplicate = False
    if key not in hashmap:
        hashmap[key] = []
    values = hashmap[key]
    foundDuplicate = len(values) > 0
    values.append(value)
    return foundDuplicate

def already_processed(path):
    if path in processed_paths:
        filetime = os.path.getmtime(path)
        if filetime > processed_paths[path]:
            # %%% Remove the file's hash from data structures
            return False
        return True
    return False

def set_processed(path):
    processed_paths[path] = os.path.getmtime(path)

def clear():
    processed_paths.clear()
    content_paths.clear()
    image_content_paths.clear()
    failures.clear()

def hash_file_bytes(fl, hashfn):
    while True:
        data = fl.read(BUF_SIZE)
        if not data:
            break
        hashfn.update(data)

# Create a hash of the contents of a general file.
def process_file(filepath):
    foundDuplicate = False
    hashfn = hashlib.sha1()

    if already_processed(filepath):
        return False
    
    _, ext = os.path.splitext(filepath)
    ext = ext.lower()
    if ext == ".jpg" or ext == ".jpeg":
        foundDuplicate = hash_jpeg(hashfn, filepath)
    else:
        # Read the file and pass to the hash function.
        # Buffer the file to limit memory use.
        with open(filepath, 'rb') as f:
            hash_file_bytes(f, hashfn)
            foundDuplicate = update_hashmap(
                    content_paths,
                    hashfn.hexdigest(),
                    filepath
                )
    set_processed(filepath)
    return foundDuplicate

def hash_jpeg(hashfn, filepath):
    """Create a hash of the image data in a JPEG.

    Don't include EXIF headers and canonicalize by converting to BMP data.
    Assumes the file extension was checked already.
    :param hashfn: a hash object 
    :param filepath: the file to hash
    :return: boolean, whether any duplicates were found
    """

    # Use pillow module to convert to BMP.
    foundDuplicate = False
    try:
        with Image.open(filepath) as jpg:
            imagebytes = io.BytesIO()
            try:
                jpg.save(imagebytes, format='BMP')
                imagebytes.seek(0)
                hash_file_bytes(imagebytes, hashfn)
                foundDuplicate = update_hashmap(
                        image_content_paths,
                        hashfn.hexdigest(),
                        filepath
                    )
            except OSError as ex:
                warn("Failure to convert JPEG to BMP (%s): %s" % (str(ex), filepath))
                failures.append(filepath)
    except UnidentifiedImageError as ex:
        warn("Unable to open JPEG (%s): %s" % (str(ex), filepath))
        failures.append(filepath)
    return foundDuplicate    

def find_duplicates_in_dir(basedir):
    """Recursively walk a directory to generate file hashes.

    :param basedir: the top directory
    :return: boolean, whether any duplicates were found
    """
    foundDuplicate = False

    if already_processed(basedir):
        return False

    for subdir, dirs, files in os.walk(basedir):
        for file in files:
            filepath = os.path.join(subdir, file)
            foundDuplicate = process_file(filepath) or foundDuplicate

    set_processed(basedir)
    return foundDuplicate

def find_duplicates(paths):
    """Recurse directories to look for duplicate file content
    
    :param paths: directories or files to scan for duplicates
    :return: boolean, whether any duplicates were found
    """
    foundDuplicate = False
    for path in paths:
        if os.path.isfile(path):
            dbg("File: %s" % path)
            foundDuplicate = process_file(path) or foundDuplicate
        elif os.path.isdir(path):
            dbg("Basedir: %s" % path)
            find_duplicates_in_dir(path)
            foundDuplicate = process_file(path) or foundDuplicate
        elif os.path.issymlink(path):
            # A link that points to neither a file nor a directory.
            warn("Unresolved symlink: %s" % path)
            failures.append(filepath)
        else:
            err("File not found: %s" % path)
    return foundDuplicate

def handle_duplicates(remove=False, force=False):
    """Apply actions to the identified duplicate files

    :param remove: prompt to remove duplicates
    :param force: automatically remove all but the first copy of all duplicates
    """
    if remove:
        remove_duplicates(force)
    else:
        display_duplicates()

    display_failures()



