
from duprem.file import File, FileError

import os

def can_handle(filepath):
    _, ext = os.path.splitext(filepath)
    return ext.lower() in [".mp3", ".flac", ".wav"]

def load_file(filepath):
    return AudioFile(filepath)

class AudioError(FileError):
    pass

class AudioFile(File):
    def __init__(self, path):
        super().__init__(path)
        
