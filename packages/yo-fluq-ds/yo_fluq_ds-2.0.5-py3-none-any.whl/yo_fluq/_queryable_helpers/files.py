from typing import *
from .._misc import KeyValuePair
from pathlib import Path
import gzip, pickle
import os
import zipfile



def text_file(filename, **kwargs):
    with open(filename, 'r', **kwargs) as file:
        for line in file:
            if line.endswith('\n'):
                line = line[:-1]
            yield line

def zip_text_file(filename, encoding):
    with gzip.open(filename, 'rb') as f:
        for line in f:
            if line.endswith(b'\n'):
                line = line[:-1]
            yield line.decode(encoding)


def pickle_file(filename, file_obj_factory):
    with file_obj_factory(filename) as file:
        while file.read(1):
            file.seek(-1, 1)
            length = file.read(4)
            length = int.from_bytes(length, 'big')
            dump = file.read(length)
            obj = pickle.loads(dump)
            yield obj

def zip_folder(filename,parser):
    with zipfile.ZipFile(filename, 'r') as zfile:
        for name in zfile.namelist():
            yield KeyValuePair(name, parser(zfile.read(name)))




def folder(location: Union[Path, str], pattern: Optional[str] = None):
    if isinstance(location,str):
        location = Path(location)
    elif isinstance(location,Path):
        pass
    else:
        raise ValueError('Location should be either str or Path, but was {0}, {1}'.format(type(location),location))

    if not os.path.isdir(location):
        raise ValueError('{0} is not a directory'.format(location))

    return location.glob(pattern)



