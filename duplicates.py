#
# Identify files containing duplicate content within a filesystem location.
# Intended for use with media files such as images or audio.
#

import os
import hashlib
from optparse import OptionParser

# My custom utility module
from util.msg import set_debug, dbg, info, warn, err
from util.collections import update_multimap
from util.type import type_check, type_error

from .file import File, ImageFile, ImageError

# Paths that have already been evaluated
processed_paths = {}

content_paths = {}
image_content_paths = {}
failures = []

def display_paths(paths):
    '''Print a zero-indexed list of paths

    :param paths: ordered list of paths
    '''
    for idx, path in enumerate(paths):
        print("%d: %s" % (idx, path))

def delete_files_except(filepaths, keep):
    '''Unlink (i.e. delete) the files, except those at the given index(es).

    :param filepaths: list of files to potentially delete
    :param keep: integer or list of integer indexes of files to not delete
    '''

    # Check and prep arguments
    if type(keep) is int:
        # Make a single-item list to allow consistent processing.
        keep = [keep]
    elif type(keep) is list:
        # Type check
        for idx, item in enumerate(keep):
            type_check(item, int, "keep[%d]" % idx)
    else:
        type_error("keep", str(type(keep)), "<class 'int'> or <class list<class int>>")
        
    for idx, path in enumerate(filepaths):
        if idx not in keep:
            print("> Deleting: %s" % path)
            os.unlink(path)
        else:
            print(">  Keeping: %s" % path)

def delete_select_files(filepaths, force, desc):
    '''Delete files as specified by the user, or automatically"

    :param filepaths: file paths to potentially delete
    :param force: automatically delete all but the first copy of all duplicates
    :param desc: string description of the type of files being deleted
    :return: whether to continue (i.e., 'q' was not selected)
    '''
    if len(filepaths) <= 1:
        return True

    print("Duplicate %s content:" % desc)

    if force:
        # Delete all files except for the first.
        delete_files_except(filepaths, 0)
            
    else:
        # Get input from the user for which file to retain.
        choice = None
        display_paths(filepaths)
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
                    if num < 0 or num >= len(filepaths):
                        raise ValueError
                    keep.append(num)
                dbg("KEEP: %r")
                delete_files_except(filepaths, keep)
                break
            except ValueError as ex:
                dbg("E: %s" % str(ex))
                # Redo the input
                pass

    return True

def delete_duplicates(force):
    '''For each set of duplicate files, ask the user which to keep.

    :param force: automatically delete all but the first copy of all duplicates
    '''
    for filepaths in content_paths.values():
        keepgoing = delete_select_files(filepaths, force, "file")
        if not keepgoing: return

    for imagepaths in image_content_paths.values():
        keepgoing = delete_select_files(imagepaths, force, "image")
        if not keepgoing: return

def display_failures():
    '''Output paths that failed to be processed.'''
    if len(failures) > 0:
        print("Failures:")
        for filepath in failures:
            print("  %s" % filepath)
                    
def display_duplicates():
    '''Output sets of paths that contain duplicate content.'''

    for paths in content_paths.values():
        if len(paths) > 1:
            print("Duplicate content:")
            display_paths(paths)

    for image_paths in image_content_paths.values():
        if len(image_paths) > 1:
            print("Duplicate image content:")
            display_paths(image_paths)

def already_processed(path):
    '''Note that the filepath has been processed.

    :param path: path to the file or directory
    :return: boolean, whether the path processing is up to date
    '''
    if path in processed_paths:
        prev_mtime = processed_paths[path]
        try:
            mtime = os.path.getmtime(path)
            # A 'None' value of 'prev_mtime' means the file was not accessible
            # before, but now it is.
            if prev_mtime is None or mtime > prev_mtime:
                # %%% Remove the file's hash from data structures
                return False
        except OSError as ex:
            # In case of broken symlinks or generally corrupt data.
            if prev_mtime is not None:
                # The file wasn't corrupt before, but now is
                err("Failed to get modification date for path %s" % path)
            else:
                # Normal case in which a corrupt path was previously processed
                pass
        return True
    return False

def set_processed(path):
    '''Note that the path, with modification time, has been processed.

    :param path: path to the file or directory
    '''
    try:
        mtime = os.path.getmtime(path)
    except OSError:
        mtime = None
    processed_paths[path] = mtime

def clear():
    """Reinitialize the program state"""

    processed_paths.clear()
    content_paths.clear()
    image_content_paths.clear()
    failures.clear()

def process_file(filepath):
    '''Store the hash the file contents.

    :param filepath: path to the file
    :return: boolean, whether any duplicates were found
    '''

    try:
        # Canonicalize the path
        filepath = os.path.realpath(filepath, strict=True)
    except OSError as ex:
        # Only produce failure output once for this invalid path.
        if not already_processed(filepath):
            err("Unable to open path %s (%s)" % (filepath, str(ex)))
            failures.append(filepath)
            set_processed(filepath)
        return False

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
        err("%s" % str(ex))
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
            foundDuplicate = find_duplicates_in_dir(path) or foundDuplicate
        elif os.path.issymlink(path):
            # A link that points to neither a file nor a directory.
            err("Unresolved symlink: %s" % path)
            failures.append(filepath)
        else:
            err("File not found: %s" % path)
    return foundDuplicate

def handle_duplicates(delete=False, force=False):
    """Apply actions to the identified duplicate files

    :param delete: prompt to delete duplicates
    :param force: automatically delete all but the first copy of all duplicates
    """
    if delete:
        delete_duplicates(force)
    else:
        display_duplicates()

    display_failures()



