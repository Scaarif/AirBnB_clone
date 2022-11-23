#!/usr/bin/python3
"""
File storage module
"""
import json
from models.base_model import BaseModel


class FileStorage:
    """
    Serializes instances to a JSON file and deserializes JSON file to instances
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        Returns the dict __objects
        """
        return self.__objects

    def new(self, obj):
        """
        Sets in __objects the obj with key <obj class name>.id

        Args:
            obj(object): Newly created objected to be added to __objects dict

        """
        key = f"BaseModel.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """
        Serializes __objects to the JSON file (path: __file_path)
        """
        with open(self.__file_path, "w") as fd:
            dict_store = {}
            for k, v in self.__objects.items():
                dict_store[k] = v.to_dict()
            json.dump(dict_store, fd, indent=4)

    def reload(self):
        """
        Deserializes the JSON file to __objects only if the JSON file
        `__file_path` exists; otherwise do nothing.
        If the file doesn't exist, no exception should be raised
        """
        try:
            with open(self.__file_path) as fd:
                for obj in json.load(fd).values():
                    self.new(BaseModel(**obj))

        except Exception:
            return
