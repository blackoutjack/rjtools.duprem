"""
Class implementing duplicate identification for general files.
"""

from rjtools.util import fs

BUF_SIZE = 65536

def can_handle(filepath:str):
    """
    Whether this file can be processed by this File class

    Plugin modules should implement this module-global function and return True
    to indicate that this plugin is able to determine whether its content
    duplicates that of other files.

    :param filepath: str, path to the file
    :return: whether this module can determine if this file duplicates others
    :rtype: bool
    """
    return True

def load_file(filepath:str):
    """
    Create a File object as defined by this module.

    Plugin modules should implement this module-global function as a factory.

    :param filepath: str, path to the file to be evaluated
    :return: newly created File object
    :rtype: File or subclass
    """
    return File(filepath)

class File:
    """A general file

    :param path: the path to the file
    """

    def __init__(self, path):
        self.path = path

    def typename(self):
        """The name of this file class"""
        return type(self).__name__

    def description(self):
        """Tag to report in the cmd output"""
        return ""

    def hash(self, hashfn):
        """
        Hash the file contents

        Uses a file api wrapper to redirect to in-memory fs for unit testing
        Feel free to use `open` if not testing with included system.

        :param hashfn: a hash object
        :return: the hash value
        :rtype: str
        """

        with fs.binary_open(self.path) as fl:
            self.hash_file_bytes(fl, hashfn)
            return hashfn.hexdigest()

    def hash_file_bytes(self, fl, hashfn):
        while True:
            data = fl.read(BUF_SIZE)
            if not data:
                break
            hashfn.update(data)

class FileError(Exception):
    """An error processing a file"""

    def __init__(self, msg):
        super().__init__(msg)
