#
# Classes encapsulating identification of different kinds of files.
#

import io
from PIL import Image, UnidentifiedImageError

BUF_SIZE = 65536

class File:
    def __init__(self, path):
        self.path = path

    def typename(self):
        return type(self).__name__

    def hash(self, hashfn):
        """Hash the file contents

        :param hashfn: a hash object 
        :return: string, the hash value
        """

        with open(self.path, 'rb') as f:
            self.hash_file_bytes(f, hashfn)
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
    def is_image(filepath):
        try:
            img = Image.open(filepath)
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
            # Raises UnidentifiedImageError on failure to open.
            with Image.open(self.path) as img:
                try:
                    imagebytes = io.BytesIO()
                    # Canonicalize by extracting bitmap data
                    # Raises OSError on failure
                    img.save(imagebytes, format='BMP')
                    imagebytes.seek(0)
                    self.hash_file_bytes(imagebytes, hashfn)
                except OSError as ex:
                    raise ImageError("Failure to extract %s data (%s): %s"
                            % (img.format, str(ex), self.path))
        except UnidentifiedImageError as ex:
            raise ImageError("Unable to open %s (%s): %s"
                    % (self.typename(), str(ex), self.path))
        return hashfn.hexdigest()

