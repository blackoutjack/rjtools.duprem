#
# Identify files containing duplicate content within a filesystem location.
# Intended for use with media files such as images or audio.
#

import os.path
import hashlib

# My custom utility module
from dgutil import fs
from dgutil.msg import dbg, err
from dgutil.collection import update_multimap
from dgutil.type import type_check, type_error

from duprem.file import File, ImageFile, ImageError


class DupEngine:
    """
    Conduct the duplicate file search and removal.
    """

    def __init__(self):
        self.processed_paths = {}
        self.content_paths = {}
        self.image_content_paths = {}
        self.failures = []

    def display_paths(self, paths):
        '''Print a zero-indexed list of paths

        :param paths: ordered list of paths
        '''
        for idx, path in enumerate(paths):
            print("{idx}: {path}")

    def delete_files_except(self, filepaths, keep):
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
                fs.unlink(path)
            else:
                print(">  Keeping: %s" % path)

    def delete_select_files(self, filepaths, force, desc):
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
            self.delete_files_except(filepaths, 0)

        else:
            # Get input from the user for which file to retain.
            choice = None
            self.display_paths(filepaths)
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
                    #dbg("CHOICES: %r" % choices)
                    keep = []
                    for c in choices:
                        #dbg("C: %r" % c)
                        num = int(c.strip())
                        #dbg("NUM: %d" % num)
                        if num < 0 or num >= len(filepaths):
                            raise ValueError
                        keep.append(num)
                    #dbg("KEEP: %r")
                    self.delete_files_except(filepaths, keep)
                    break
                except ValueError:
                    # Redo the input
                    pass

        return True

    def delete_duplicates(self, force):
        '''For each set of duplicate files, ask the user which to keep.

        :param force: automatically delete all but the first copy of all duplicates
        '''
        for filepaths in self.content_paths.values():
            keepgoing = self.delete_select_files(filepaths, force, "file")
            if not keepgoing: return

        for imagepaths in self.image_content_paths.values():
            keepgoing = self.delete_select_files(imagepaths, force, "image")
            if not keepgoing: return

    def display_failures(self):
        '''Output paths that failed to be processed.'''
        if len(self.failures) > 0:
            print("Failures:")
            for filepath in self.failures:
                print(f"  {filepath}")

    def display_duplicates(self):
        '''Output sets of paths that contain duplicate content.'''

        for paths in self.content_paths.values():
            if len(paths) > 1:
                print("Duplicate content:")
                self.display_paths(paths)

        for image_paths in self.image_content_paths.values():
            if len(image_paths) > 1:
                print("Duplicate image content:")
                self.display_paths(image_paths)

    def already_processed(self, path):
        '''Note that the filepath has been processed.

        :param path: path to the file or directory
        :return: boolean, whether the path processing is up to date
        '''
        if path in self.processed_paths:
            prev_mtime = self.processed_paths[path]
            try:
                mtime = fs.get_modify_time(path)
                # A 'None' value of 'prev_mtime' means the file was not accessible
                # before, but now it is.
                if prev_mtime is None or mtime > prev_mtime:
                    # %%% Remove the file's hash from data structures
                    return False
            except OSError as ex:
                # In case of broken symlinks or generally corrupt data.
                if prev_mtime is not None:
                    # The file wasn't corrupt before, but now is
                    err("Failed to get modification date for path %s: %s" % (path, str(ex)))
                else:
                    # Normal case in which a corrupt path was previously processed
                    pass
            return True
        return False

    def set_processed(self, path):
        '''Note that the path, with modification time, has been processed.

        :param path: path to the file or directory
        '''
        try:
            mtime = fs.get_modify_time(path)
        except OSError:
            mtime = None
        self.processed_paths[path] = mtime

    def clear(self):
        """Reinitialize the program state"""

        self.processed_paths.clear()
        self.content_paths.clear()
        self.image_content_paths.clear()
        self.failures.clear()

    def process_file(self, filepath):
        '''Store the hash the file contents.

        :param filepath: path to the file
        :return: boolean, whether any duplicates were found
        '''

        try:
            # Canonicalize the path
            filepath = fs.get_real_path(filepath, strict=True)
        except OSError as ex:
            # Only produce failure output once for this invalid path.
            if not self.already_processed(filepath):
                err("Unable to open path %s (%s)" % (filepath, str(ex)))
                self.failures.append(filepath)
                self.set_processed(filepath)
            return False

        if self.already_processed(filepath):
            return False

        dbg("Processing %s" % filepath)

        hashfn = hashlib.sha1()

        if ImageFile.is_image(filepath):
            file = ImageFile(filepath)
            multimap = self.image_content_paths
        else:
            file = File(filepath)
            multimap = self.content_paths

        foundDuplicate = False
        try:
            filehash = file.hash(hashfn)
            foundDuplicate = update_multimap(multimap, filehash, filepath)
        except ImageError as ex:
            err("%s" % str(ex))
            self.failures.append(filepath)
        self.set_processed(filepath)

        return foundDuplicate

    def find_duplicates_in_dir(self, basedir):
        """Recursively walk a directory to generate file hashes.

        :param basedir: the top directory
        :return: boolean, whether any duplicates were found
        """
        foundDuplicate = False

        if self.already_processed(basedir):
            return False

        for subdir, dirs, files in fs.walk(basedir):
            for file in files:
                filepath = os.path.join(subdir, file)
                foundDuplicate = self.process_file(filepath) or foundDuplicate

        self.set_processed(basedir)
        return foundDuplicate

    def find_duplicates(self, paths):
        """Recurse directories to look for duplicate file content

        :param paths: directories or files to scan for duplicates
        :return: boolean, whether any duplicates were found
        """
        foundDuplicate = False
        for path in paths:
            if fs.is_file(path):
                dbg("File: %s" % path)
                foundDuplicate = self.process_file(path) or foundDuplicate
            elif fs.is_dir(path):
                dbg("Basedir: %s" % path)
                foundDuplicate = self.find_duplicates_in_dir(path) or foundDuplicate
            elif fs.is_link(path):
                # A link that points to neither a file nor a directory.
                err("Unresolved link: %s" % path)
                self.failures.append(path)
            else:
                err("File not found: %s" % path)
        return foundDuplicate

    def handle_duplicates(self, delete=False, force=False):
        """Apply actions to the identified duplicate files

        :param delete: prompt to delete duplicates
        :param force: automatically delete all but the first copy of all duplicates
        """
        if delete:
            self.delete_duplicates(force)
        else:
            self.display_duplicates()

        self.display_failures()

