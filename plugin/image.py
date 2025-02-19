import io

from PIL import Image, UnidentifiedImageError
from dgutil import fs

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
        fl = fs.binary_open(self.path)
        return Image.open(fl)

    def description(self):
        return "image"

    def hash(self, hashfn):
        """Hash the image data

        :param hashfn: a hash object
        :return: string, the hash value
        """

        try:
            with self.open() as img, io.BytesIO() as bmpbytes:
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

