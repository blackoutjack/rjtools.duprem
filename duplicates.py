#
# Identify files containing duplicate content within a filesystem location.
# Intended for use with media files such as images or audio.
#

import sys
import os
import hashlib
from optparse import OptionParser

# My custom utility module
from util.msg import set_debug, dbg, info, warn, err
from util.collections import update_multimap

from .file import File, ImageFile, ImageError

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

# Create a hash of the contents of a general file.
def process_file(filepath):
    if already_processed(filepath):
        return False

    dbg("Processing %s" % filepath)

    hashfn = hashlib.sha1()

    if ImageFile.is_image(filepath):
        file = ImageFile(filepath)
        multimap = image_content_paths
    else:
        file = File(filepath)
        multimap = content_paths

    foundDuplicate = False
    try:
        filehash = file.hash(hashfn)
        foundDuplicate = update_multimap(multimap, filehash, filepath)
    except ImageError as ex:
        warn("%s" % str(ex))
        failures.append(filepath)
    set_processed(filepath)

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



