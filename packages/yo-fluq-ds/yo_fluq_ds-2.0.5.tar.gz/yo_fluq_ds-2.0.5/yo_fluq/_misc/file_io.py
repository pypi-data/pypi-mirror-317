import pickle
import json
import os
from .obj import Obj

# region extended

import yaml
import jsonpickle

# endregion extended

class FileIO:

    @staticmethod
    def read_bytes(filename):
        with open(filename, 'rb') as file:
            return file.read()

    @staticmethod
    def read_pickle(filename):
        with open(filename, 'rb') as file:
            return pickle.load(file)

    @staticmethod
    def read_json(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            result = json.load(file)
            return result

    @staticmethod
    def read_text(filename, encoding='utf-8'):
        with open(filename, 'r', encoding=encoding) as file:
            return file.read()

    @staticmethod
    def write_pickle(data, filename):
        with open(filename, 'wb') as file:
            pickle.dump(data, file)

    @staticmethod
    def write_json(data, filename):
        with open(filename, 'w') as file:
            json.dump(data, file, indent=1)

    @staticmethod
    def write_text(data, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(data)

    @staticmethod
    def write_bytes(data, filename):
        with open(filename, 'wb') as file:
            file.write(data)


    # region extended
    @staticmethod
    def read_yaml(filename):
        with open(filename, 'r') as file:
            return yaml.load(file)

    @staticmethod
    def read_jsonpickle(filename):
        with open(filename, 'r') as file:
            return jsonpickle.loads(file.read())

    @staticmethod
    def write_yaml(data, filename):
        with open(filename, 'w') as file:
            yaml.dump(data, file)

    @staticmethod
    def write_jsonpickle(data, filename):
        with open(filename, 'w') as file:
            file.write(jsonpickle.dumps(data))

    # endregion extended