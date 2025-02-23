"""
Identify files containing duplicate content within a filesystem location.
"""

import os.path
import hashlib
from queue import Queue
from threading import Thread, RLock

# My custom utility module
from dgutil import fs
from dgutil.msg import dbg, err, warn
from dgutil.collection import update_multimap
from dgutil.type import type_check, type_error

from duprem.file import File, FileError


DEFAULT_THREADS = 4

map_lock = RLock()
processed_lock = RLock()

class DupEngine:
    """
    Conduct the duplicate file search and removal.
    """

    def __init__(self, plugins):
        self.plugins = plugins
        self.processed_paths = {}
        self.content_paths = {}
        self.failures = []

        self.queue = Queue()

    def display_paths(self, files):
        """Print a zero-indexed list of paths

        :param files: list of File, print the paths of these in order
        """
        for idx, file in enumerate(files):
            print(f"{idx}: {file.path}")

    def delete_files_except(self, files, keep):
        """Unlink (i.e. delete) the files, except those at the given index(es).

        :param files: list of files to potentially delete
        :param keep: integer or list of integer indexes of files to not delete
        """

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

        for idx, file in enumerate(files):
            if idx not in keep:
                print(f"> Deleting: {file.path}")
                fs.unlink(file.path)
            else:
                print(f">  Keeping: {file.path}")

    def get_description_from_file_group(self, files, warningOnDifferent:str|None=None):
        """
        Get a shared description of files in this set, or warn if they differ

        :param files: list of File, files to get the description from
        :param warningOnDifferent: str|None, warn with this message on mismatch
            occurs, or ignore mismatch on `None`
        :return: description shared by all the files
        :rtype: str|None
        """
        desc = None
        for file in files:
            if desc is None:
                desc = file.description()
            elif desc != file.description():
                if warningOnDifferent is not None:
                    filelist = "\n".join([f"{f.path} ({f.typename()})" for f in files])
                    warn(f"{warningOnDifferent}:\n{filelist}")
                return None
        return desc

    def delete_select_files(self, files, force):
        """Delete files as specified by the user, or automatically"

        :param files: files to potentially delete
        :param force: automatically delete all but the first copy of all duplicates
        :param desc: string description of the type of files being deleted
        :return: whether to continue (i.e., 'q' was not selected)
        """
        if len(files) <= 1:
            return True

        desc = self.get_description_from_file_group(
            files, "Not deleting duplicate content of variable kinds")
        if desc is None: return

        print(f"Duplicate {desc} content:")

        if force:
            # Delete all files except for the first.
            self.delete_files_except(files, 0)

        else:
            # Get input from the user for which file to retain.
            choice = None
            self.display_paths(files)
            print("k: Keep all")
            while True:
                choice = input(f"Retain which {desc}(s) (comma-separated)? ")
                choice = choice.strip()
                if choice == "k":
                    break
                if choice == "q":
                    # Tell the calling function to quit.
                    return False
                try:
                    # Parse a comma-delimited list of numeric choices
                    choices = choice.split(",")
                    keep = []
                    for c in choices:
                        num = int(c.strip())
                        if num < 0 or num >= len(files):
                            raise ValueError
                        keep.append(num)
                    self.delete_files_except(files, keep)
                    break
                except ValueError:
                    # Redo the input
                    pass

        return True

    def delete_duplicates(self, force):
        """For each set of duplicate files, ask the user which to keep.

        :param force: automatically delete all but the first copy of duplicates
        """
        for files in self.content_paths.values():
            keepgoing = self.delete_select_files(files, force)
            if not keepgoing: return

    def display_failures(self):
        """Output paths that failed to be processed."""
        if len(self.failures) > 0:
            print("Failures:")
            for path in self.failures:
                print(f"  {path}")

    def display_duplicates(self):
        """Output sets of paths that contain duplicate content."""

        for files in self.content_paths.values():
            if len(files) > 1:
                desc = self.get_description_from_file_group(files)
                if desc is None: desc = "mixed"
                desc = " " if desc == "" else f" {desc} "
                print(f"Duplicate{desc}content:")
                self.display_paths(files)

    def already_processed(self, path):
        """Note that the filepath has been processed.

        :param path: path to the file or directory
        :return: boolean, whether the path processing is up to date
        """
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
        """Note that the path, with modification time, has been processed.

        :param path: path to the file or directory
        """
        try:
            mtime = fs.get_modify_time(path)
        except OSError:
            mtime = None
        self.processed_paths[path] = mtime

    def clear(self):
        """Reinitialize the program state"""

        self.processed_paths.clear()
        self.content_paths.clear()
        self.failures.clear()

    def process_file(self, filepath):
        """Store the hash the file contents.

        :param filepath: path to the file
        :return: boolean, whether any duplicates were found
        """

        try:
            # Canonicalize the path
            filepath = fs.get_real_path(filepath, strict=True)
        except OSError as ex:
            # Only produce failure output once for this invalid path.
            with processed_lock:
                if not self.already_processed(filepath):
                    err("Unable to open path %s (%s)" % (filepath, str(ex)))
                    self.failures.append(filepath)
                    self.set_processed(filepath)
            return False

        with processed_lock:
            if self.already_processed(filepath):
                return False
            self.set_processed(filepath)

        dbg("Processing %s" % filepath)

        hashfn = hashlib.sha1()

        file = None
        for plugin in self.plugins:
            if plugin.can_handle(filepath):
                file = plugin.load_file(filepath)
                break
        if file is None:
            # No plugin was found, so use the default file handler.
            file = File(filepath)

        foundDuplicate = False
        try:
            filehash = file.hash(hashfn)
            with map_lock:
                foundDuplicate = update_multimap(self.content_paths, filehash, file)
        except FileError as ex:
            err("%s" % str(ex))
            self.failures.append(filepath)

        return foundDuplicate

    def find_duplicates_in_dir(self, basedir, threads=DEFAULT_THREADS):
        """Recursively walk a directory to generate file hashes.

        :param basedir: the top directory
        :return: boolean, whether any duplicates were found
        """

        foundDuplicate = False

        if self.already_processed(basedir):
            return False
        self.set_processed(basedir)

        if threads > 1:
            q = Queue()

            def worker():
                while True:
                    filepath = q.get()
                    foundDup = self.process_file(filepath)
                    nonlocal foundDuplicate
                    if foundDup: foundDuplicate = True
                    q.task_done()

            for threadNum in range(threads):
                t = Thread(
                    name="process_file%d" % threadNum,
                    target=worker,
                    args=[])
                t.daemon = True
                t.start()

            for subdir, dirs, filenames in fs.walk(basedir):
                for filename in filenames:
                    filepath = os.path.join(subdir, filename)
                    q.put(filepath)

            q.join()
        else:
            for subdir, dirs, filenames in fs.walk(basedir):
                for filename in filenames:
                    filepath = os.path.join(subdir, filename)
                    foundDuplicate = self.process_file(filepath) or foundDuplicate

        return foundDuplicate

    def find_duplicates(self, paths, threads=DEFAULT_THREADS):
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
                foundDuplicate = self.find_duplicates_in_dir(path, threads) or foundDuplicate
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

