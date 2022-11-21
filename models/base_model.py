#!/usr/bin/python3
"""Contains the class BaseModel"""
import uuid
from datetime import datetime


class BaseModel():
    """Defines all common attributes/methods for other subclassess"""
    def __init__(self):
        """Creates a class instance"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def __str__(self):
        """Returns the formatted str representation of an obj"""
        return f"[BaseModel] ({self.id}) {self.__dict__}"

    def save(self):
        """Updates the public instance attribute updated_at"""
        self.updated_at = datetime.now()

    def to_dict(self):
        """Returns a dict containing all keys/values of __dict__ of the
        instance.
        In addition a key __class__ is added with class name as value"""
        obj_dict = self.__dict__
        obj_dict["__class__"] = "BaseModel"
        obj_dict["created_at"] = self.created_at.isoformat()
        obj_dict["updated_at"] = self.updated_at.isoformat()
        
        return obj_dict
