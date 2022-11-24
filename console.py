#!/usr/bin/python3
"""
Entry point of the command interpreter
"""
import re
import cmd
import sys
import models
import argparse
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


CLASSES = [
    "BaseModel",
    "User",
    "State",
    "City",
    "Amenity",
    "Place",
    "Review"
]

parser = argparse.ArgumentParser()
args = str(parser.parse_args())


def parser(args):
    """Parses arguments parsed to our HBNBCommands
    Returns an array of strings
    """
    return re.findall(r"(\b[^\s]+\b)", args)


class HBNBCommand(cmd.Cmd):
    """Command interpreter for AirBnB project"""
    prompt = "(hbnb) "
    storage = models.storage

    def do_EOF(self, line):
        """Implements EOF for the command interpreter
        """
        print("")
        return True

    def do_quit(self, line):
        """Quit command to exit the program
        """
        sys.exit()

    def emptyline(self):
        """Ensures that empty line + <ENTER> shouldn't execute anything
        """
        pass

    def do_create(self, args):
        """Creates a new instance of a class
        Saves it to the JSON file and prints the id
        """
        argv = parser(args)
        if len(argv) == 0:
            print("** class name missing **")
        elif argv[0] not in CLASSES:
            print("** class doesn't exist **")
        else:
            model = eval(argv[0])()
            print(model.id)
            model.save()

    def do_show(self, args):
        """Prints str repr of an instance based on the class name and id
        """
        argv = parser(args)
        if len(argv) == 0:
            print("** class name is missing **")
        elif argv[0] not in CLASSES:
            print("** class doesn't exist **")
        elif len(argv) == 1:
            print("** instance id missing **")
        else:
            all_dict = self.storage.all()
            key = f"{argv[0]}.{argv[1]}"
            if all_dict.get(key):
                print(str(all_dict[key]))
            else:
                print("** no instance found **")

    def do_destroy(self, args):
        """Deletes an instance based on the class name & id and save the change
        """
        argv = parser(args)
        if len(argv) == 0:
            print("** class name missing **")
        elif argv[0] not in CLASSES:
            print("** class doesn't exist **")
        elif len(argv) == 1:
            print("** instance id missing **")
        else:
            all_dict = self.storage.all()
            key = f"{argv[0]}.{argv[1]}"
            if all_dict.get(key):
                del all_dict[key]
                self.storage.save()
            else:
                print("** no instance found **")

    def do_all(self, args):
        """Prints all str representation of all instances
        """

        argv = parser(args)

        all_dicts = self.storage.all()
        all_objects = []
        class_objects = []
        for k, v in all_dicts.items():
            all_objects.append(str(v))
            if len(argv) != 0:
                if argv[0] == v.__class__.__name__:
                    class_objects.append(str(v))
        if len(argv) == 0:
            print(all_objects)
        elif argv[0] in CLASSES:
            print(class_objects)
        else:
            print("** class doesn't exist **")

    def do_update(self, args):
        """Updates an instance based on the class and id by adding attribute
        """
        argv = parser(args)

        if len(argv) == 0:
            print("** class name missing **")
        elif argv[0] not in CLASSES:
            print("** class doesn't exist **")
        elif len(argv) == 1:
            print("** instance id missing **")
        elif len(argv) == 2:
            all_dict = self.storage.all()
            key = f"{argv[0]}.{argv[1]}"
            if all_dict.get(key) is None:
                print("** no instance found **")
            else:
                print("** attribute name missing **")
        elif len(argv) == 3:
            print("** value missing **")
        else:
            all_dict = self.storage.all()
            key = f"{argv[0]}.{argv[1]}"
            obj = all_dict.get(key)
            if argv[2] in type(obj).__dict__:
                attr_type = type(obj.__class__.__dict__[argv[2]])
                setattr(obj, argv[2], attr_type(argv[3]))
            else:
                setattr(obj, argv[2], argv[3])
            self.storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
