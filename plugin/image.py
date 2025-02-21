import io
from typing import override

from PIL import Image, UnidentifiedImageError
from rjtools.util import fs

from duprem.file import File, FileError

def can_handle(filepath):
    try:
        img = ImageFile(filepath)
        imgfile = img.open()
        imgfile.close()
    except UnidentifiedImageError:
        return False
    return True

def load_file(filepath):
    return ImageFile(filepath)

class ImageError(FileError):
    pass

class ImageFile(File):
    def __init__(self, path):
        super().__init__(path)

    def open(self):
        """
        Open the image file

        :param filepath: path to the image file
        :raises: UnidentifiedImageError if the file is not a valid image
        :return: image data
        """
        # Using file api wrapper to redirect to in-memory fs for unit testing
        fl = fs.binary_open(self.path)
        return Image.open(fl)

    @override
    def description(self):
        return "image"

    @override
    def hash(self, hashfn):
        """Hash the image data

        :param hashfn: a hash object
        :return: the hash value
        :rtype: str
        """
        try:
            with self.open() as img, io.BytesIO() as bmpbytes:
                # Canonicalize by extracting bitmap data
                # Raises OSError on failure
                img.save(bmpbytes, format='BMP')
                bmpbytes.seek(0)
                self.hash_file_bytes(bmpbytes, hashfn)
        except UnidentifiedImageError as ex:
            raise ImageError("Unable to open %s at %s: %s"
                    % (self.typename(), self.path, str(ex)))
        except OSError as ex:
            raise ImageError("Failure to extract %s data (%s): %s"
                    % (img.format, str(ex), self.path))
        return hashfn.hexdigest()

