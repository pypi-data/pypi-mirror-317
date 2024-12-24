import pickle
import json
import os
from .obj import Obj

# region yo_fluq_ds

import yaml
import jsonpickle

# endregion yo_fluq_ds

class FileIO:

    @staticmethod
    def read_pickle(filename):
        with open(filename,'rb') as file:
            return pickle.load(file)

    @staticmethod
    def write_pickle(data, filename):
        with open(filename,'wb') as file:
            pickle.dump(data,file)

    @staticmethod
    def read_json(filename, as_obj = False):
        with open(filename,'r') as file:
            result = json.load(file)
            if as_obj:
                return Obj.create(result)
            else:
                return result

    @staticmethod
    def write_json(data, filename):
        with open(filename,'w') as file:
            json.dump(data,file,indent=1)


    @staticmethod
    def read_text(filename):
        with open(filename,'r', encoding='utf-8') as file:
            return file.read()


    @staticmethod
    def write_text(data, filename):
        with open(filename,'w', encoding='utf-8') as file:
            file.write(data)


    # region yo_fluq_ds
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

    # endregion yo_fluq_ds