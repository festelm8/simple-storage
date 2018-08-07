"""
Simple file storage based on file hashes.

Structure of storage:
<root_dir>/<hash[:2]/hash[2:4]/hash[4:].ext>
"""
import os
import hashlib
from pathlib import Path


def make_path(root_dir:str, md5hash:str, ext:str):
    root = Path(root_dir)
    return (root_dir /
            md5hash[:2] /
            md5hash[2:4] /
            (md5hash[4:] + ext))


class TooBigFileException(Exception):
    pass


class File():
    """
    File class dummy.

    Any your orm class could be here.
    Or you can just mix in this class into your model.
    """
    filename = None
    ext = None
    size = None
    md5hash = None


class FileStorage():

    def __init__(self, root_dir:str='.',
                 max_filesize=2010000):
        """
        Max filesize (in bytes) approx 2Mb.
        """
        self.root_dir = Path(root_dir)
        try:
            self.root_dir.mkdir(parents=True)
        except FileExistsError:
            #print('Directory exists')
            pass
        self.max_filesize = max_filesize

    def get_file_path(self, md5hash:str):
        dir_with_file = (self.root_dir /
                         md5hash[:2] / md5hash[2:4])
        if not dir_with_file.is_dir():
            raise FileNotFoundError(
                'No file whith this hash {}.'
                .format(md5hash))

        filename = md5hash[4:]
        path_to_file = [fil for fil in dir_with_file.iterdir()
                        if fil.name.startswith(filename)]
        if not path_to_file:
            return None
        path_to_file = path_to_file[0]
        return str(path_to_file)

    def store_file(self, ext:str,
                   binary:bytes):
        if len(binary) > self.max_filesize:
            raise TooBigFileException()
        md5hash = hashlib.md5(binary).hexdigest()
        path_to_file = make_path(self.root_dir,
                                 md5hash,
                                 ext)
        path_to_file = Path(path_to_file)
        if path_to_file.is_file():
            return md5hash
        if not path_to_file.parent.is_dir():
            path_to_file.parent.mkdir(parents=True)
        with path_to_file.open('wb') as target_file:
            target_file.write(binary)
            target_file.flush()
        return md5hash
