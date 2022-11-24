#!/usr/bin/python3
""" Defines the entry point to the AirBnB Console project """
import cmd
import sys
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models import storage


class HBNBCommand(cmd.Cmd):
    """ Defines a line-oriented command processor
    (a command-line interface) that extends the cmd module """
    # assign a custom prompt
    prompt = '(hbtn) '

    # initialize object
    def __init__(self):
        """ Initializes class objects """
        # initialize super class (is this necessary)? No!
        cmd.Cmd.__init__(self)
        self.classes = {'BaseModel': self.create_BaseModel,
                        'User': self.create_User,
                        'State': self.create_State,
                        'City': self.create_City,
                        'Place': self.create_Place,
                        'Amenity': self.create_Amenity,
                        'Review': self.create_Review}

    def do_quit(self, line):
        """ exits the program: <quit> call method implementation
        Args:
            line - each command call method (a do_x method)
            takes an argument containing the command to be executed
            and (potentially) the command's args """
        sys.exit(1)  # success

    def help_quit(self):
        """ quit help """
        print('syntax: quit\n--terminates the application')

    def do_EOF(self, line):
        """ exits the program: <Ctrl + D> call method implementation """
        print(),  # to exit properly(with a new line)
        return True  # to the cmdloop's stop flag

    def help_EOF(self):
        print('syntax: Ctrl + D\n--terminates the application')

    # override cmd.emptyline - re-executes last cmd if emptyline
    def emptyline(self):
        pass  # do nothing

    # ========= helper methods ===========

    def create_BaseModel(self, **kwargs):
        """ creates a new BaseModel instance """
        if kwargs:
            return BaseModel(**kwargs)
        else:
            return BaseModel()

    def create_User(self, **kwargs):
        """ creates a new User instance """
        if kwargs:
            return User(**kwargs)
        else:
            return User()

    def create_State(self, **kwargs):
        """ creates a new State instance """
        if kwargs:
            return State(**kwargs)
        else:
            return State()

    def create_City(self, **kwargs):
        """ creates a new City instance """
        if kwargs:
            return City(**kwargs)
        else:
            return City()

    def create_Place(self, **kwargs):
        """ creates a new Place instance """
        if kwargs:
            return Place(**kwargs)
        else:
            return Place()

    def create_Amenity(self, **kwargs):
        """ creates a new Amenity instance """
        if kwargs:
            return Amenity(**kwargs)
        else:
            return Amenity()

    def create_Review(self, **kwargs):
        """ creates a new Review instance """
        if kwargs:
            return Review(**kwargs)
        else:
            return Review()

    @staticmethod
    def get_value(args):
        """ returns a value from args """
        attr_value = args[3]
        if len(args) > 4:
            value = ' '.join(args[3:])
            print(value)
            if value[0] == '"':
                values = value.split('"')
                attr_value = values[1]
        return attr_value

    # ========== end of helper functions ==============

    # ++++ custom console commands ++++ #

    def do_create(self, line):
        """ <create class_name> creates a new instance of BaseModel, saves
        it(to JSON file) & prints the id (instance's) """
        # check that class name is included in command
        if line:
            # check if class is valid
            for class_, method in (self.classes).items():
                if class_ in line:
                    new = method()
                    new.save()
                    print(new.id)
                    break
            else:
                # provided_class doesn't exist
                print("** class doesn't exist **")
        else:
            print('** class name missing **')

    def do_show(self, line):
        """ <show object_id> prints the string representation of
        an instance based on class name and id """
        # check that class name & id are provided along with command
        if line:
            args = line.split()
            # check that class exists
            if args[0] and args[0] not in (self.classes).keys():
                print("** class doesn't exist **")
            else:
                # class exists, check id is provided
                if len(args) > 1:
                    # check that an object with [id] exists
                    # get the string objects
                    objects = storage.all()
                    # search for [this_id] object representation
                    this_key = f'{args[0]}.{args[1]}'
                    for obj, str_rep in objects.items():
                        if obj == this_key:
                            # print this_obj (its str rep)
                            print(str_rep)  # the object
                            break  # from objects looping
                    else:
                        # objects exhausted before [this_obj] is found
                        print("** no instance found **")
                else:
                    # id not provided (arg[1] missing)
                    print("** instance id missing **")
        else:
            # line empty (no args)
            print("** class name missing **")

    def do_destroy(self, line):
        """ <destroy class_name object_id> deletes an instance based on
        the class name and id (& saves the change into the JSON file) """
        # check that class name & id are provided along with command
        if line:
            args = line.split()
            # check that class exists
            if args[0] and args[0] not in (self.classes).keys():
                # if args[0] and args[0] != 'BaseModel':
                print("** class doesn't exist **")
            else:
                # class exists, check id is provided
                if len(args) > 1:
                    # check that an object with [id] exists
                    # get the string objects (as reloaded)
                    objects = storage.all()
                    # search for [this_id] object representation
                    this_key = f'{args[0]}.{args[1]}'
                    for obj, str_rep in objects.items():
                        if obj == this_key:
                            # delete the obj, str_rep pair
                            del (objects[obj])
                            # reserialize objects into file (to reflect change)
                            storage.save()
                            break
                    else:
                        # objects exhausted before [this_obj] is found
                        print("** no instance found **")
                else:
                    # id not provided (arg[1] missing)
                    print("** instance id missing **")
        else:
            # line empty (no args)
            print("** class name missing **")

    def do_all(self, line):
        """ <all> or <all class_name> prints all string representation
        of all instances based or not on the class name """
        # check if class_name is provided (for filter)
        # get all objects and only print out BaseModel instances
        objects = storage.all()
        obj_list = []
        if line:
            # check the classname provided exists
            for cls in (self.classes).keys():
                if line == cls:
                    for obj, val in objects.items():
                        cls_name = (obj.split('.'))[0]
                        # if an object is of given class, print it
                        if cls_name == line:
                            # obj_list.append(str(method(**val)))
                            obj_list.append(str(val))
                    print(obj_list)
                    break
            else:
                # some other class provided
                print("** class doesn't exist **")
        else:
            # print all instances (no filter)
            for obj, val in objects.items():
                obj_list.append(str(val))
            print(obj_list)

    def do_update(self, line):
        """ <update class_name object_id attribute_name attribute_value>
        updates the instance [class_name.object_id]'s attribute
        [attribute_name] to [attribute_value] if [attribute_name]
        already exists. Adds the attribute [name]->[value] pair otherwise
        (& saves the change into the JSON file) """
        # check that class name & id are provided along with command
        if line:
            args = line.split()
            # check that class exists
            if args[0] and args[0] not in (self.classes).keys():
                print("** class doesn't exist **")
            else:
                # class exists, check id is provided
                if len(args) > 1:
                    objects = storage.all()
                    this_key = f'{args[0]}.{args[1]}'
                    for obj, str_rep in objects.items():
                        if obj == this_key:
                            # object exists: update or add attribute
                            if len(args) > 2:
                                # check if attribute already exists
                                for k, val in (str_rep.to_dict()).items():
                                    if k == args[2]:
                                        # attribute already exists
                                        # check if attr_value provided
                                        if len(args) > 3:
                                            # attr_value provided, cast+update
                                            attr_val = self.get_value(args)
                                            attr_val = type(val)(attr_val)
                                            setattr(str_rep, args[2], attr_val)
                                            # reserialize objects into file
                                            str_rep.save()
                                        else:
                                            print("** value missing **")
                                        break  # from for loop
                                else:
                                    # attribute doesn't exist, add it
                                    if len(args) > 3:
                                        # extend object dict_rep
                                        attr_value = self.get_value(args)
                                        setattr(str_rep, args[2], attr_value)
                                        # reserialize __objects into file
                                        str_rep.save()
                                    else:
                                        print("** value missing **")
                            else:
                                # attribute_name missing
                                print("** attribute name missing **")
                            break
                    else:
                        # objects exhausted before [this_obj] is found
                        print("** no instance found **")
                else:
                    # id not provided (arg[1] missing)
                    print("** instance id missing **")
        else:
            # line empty (no args)
            print("** class name missing **")


# run the script if executed as main
if __name__ == '__main__':
    # instantiate class and run infinitely
    HBNBCommand().cmdloop()
