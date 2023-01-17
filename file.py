#
# Classes encapsulating identification of different kinds of files.
#

import io
from PIL import Image, UnidentifiedImageError

from util import fs

BUF_SIZE = 65536

class File:
    """A general file

    :param path: the path to the file
    """

    def __init__(self, path):
        self.path = path

    def typename(self):
        return type(self).__name__

    def hash(self, hashfn):
        """Hash the file contents

        :param hashfn: a hash object 
        :return: string, the hash value
        """

        # Using 'with' autocloses 'fl' when exiting the block.
        with fs.binary_open(self.path) as fl:
            self.hash_file_bytes(fl, hashfn)
            return hashfn.hexdigest()

    def hash_file_bytes(self, fl, hashfn):
        while True:
            # Buffer the file to limit memory use.
            data = fl.read(BUF_SIZE)
            if not data:
                break
            hashfn.update(data)

class ImageError(Exception):
    pass

class ImageFile(File):

    @staticmethod
    def open_image(filepath):
        fl = fs.binary_open(filepath)
        return Image.open(fl)

    @staticmethod
    def is_image(filepath):
        try:
            img = ImageFile.open_image(filepath)
            img.close()
        except UnidentifiedImageError:
            return False
        return True

    def hash(self, hashfn):
        """Hash the image data

        :param hashfn: a hash object 
        :return: string, the hash value
        """

        try:
            # Using 'with' autocloses 'img' when exiting the block.
            # Raises UnidentifiedImageError on failure to open.
            with ImageFile.open_image(self.path) as img, io.BytesIO() as bmpbytes:
                # Canonicalize by extracting bitmap data
                # Raises OSError on failure
                img.save(bmpbytes, format='BMP')
                bmpbytes.seek(0)
                self.hash_file_bytes(bmpbytes, hashfn)
        except UnidentifiedImageError as ex:
            raise ImageError("Unable to open %s (%s): %s"
                    % (self.typename(), str(ex), self.path))
        except OSError as ex:
            raise ImageError("Failure to extract %s data (%s): %s"
                    % (img.format, str(ex), self.path))
        return hashfn.hexdigest()

class AudioFile(File):

    @staticmethod
    def is_audio(filepath):
        _, ext = os.path.splitext(filepath)
        return ext.lower() in [".mp3", ".flac", ".wav"]


