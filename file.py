"""
Class implementing duplicate identification for general files.
"""

from dgutil import fs

BUF_SIZE = 65536

class File:
    """A general file

    :param path: the path to the file
    """

    def __init__(self, path):
        self.path = path

    def typename(self):
        return type(self).__name__

    def description(self):
        return ""

    def hash(self, hashfn):
        """Hash the file contents

        :param hashfn: a hash object
        :return: string, the hash value
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
