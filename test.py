#!/usr/bin/python3
from models import storage
from models.base_model import BaseModel

print("Creating a new object")
my_obj = BaseModel()

print("Saving my model")
my_obj.save()
