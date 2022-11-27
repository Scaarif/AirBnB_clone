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
    prompt = '(hbnb) '

    # initialize object
    def __init__(self):
        """ Initializes class objects """
        # initialize super class (is this necessary)? No!
        cmd.Cmd.__init__(self)
        self.classes = ['BaseModel',
                        'User',
                        'State',
                        'City',
                        'Place',
                        'Amenity',
                        'Review']

    def do_quit(self, line):
        """ Quit command to exit the program """
        sys.exit()  # success

    def do_EOF(self, line):
        """ <Ctrl + D> to exit the program """
        print(),  # to exit properly(with a new line)
        return True  # to the cmdloop's stop flag

    # override cmd.emptyline - re-executes last cmd if emptyline
    def emptyline(self):
        pass  # do nothing

    # override cmd.precmd - re-write line if in the form <class>.cmd
    def precmd(self, line):
        # for cls in self.classes:
        if '.' in line:
            # if line.startswith(cls):
            cmd_strs = line.split('.')
            # check if command has args as in show(id)
            args = cmd_strs[1].split('(')
            command = args[0]
            cls = cmd_strs[0]
            # print('command: ', command)
            # print('args: ', args)
            if len(args[1]):
                if len(args[1].split(',')) == 1:
                    # the likes of User.show("id")
                    args = (args[1].strip(')')).strip('"')
                    # print('single arg args')
                else:
                    # the likes of User.update("id", "att", "attr_val")
                    args = args[1].strip(')')
                    # print('multiple args args')
                    if '{' in args:
                        # print('possible dict')
                        pass
                    # format multi_args eg into id att "attr_val"
                    multi_args = []
                    for idx, arg in enumerate(args.split(',')):
                        if (idx < 2) or len((arg.strip(' ')).split(' ')) == 1:
                            multi_args.append((arg.strip(' ')).strip('"'))
                        else:
                            multi_args.append(arg)  # as quoted stringi
                    # print(multi_args)
                    args = ' '.join(multi_args)
                # print('actual args: ', args)
                cmd_strs = []
                cmd_strs.append(args)
                cmd_strs.append(cls)
                cmd_strs.append(command)
            else:
                cmd_strs[1] = cmd_strs[1].strip('()')
            line = ' '.join(reversed(cmd_strs))
            # print(line)
        return cmd.Cmd.precmd(self, line)

    # ========= helper methods ===========

    @staticmethod
    def get_value(args):
        """ returns a value from args """
        attr_value = args[3]
        if len(args) > 4:
            value = ' '.join(args[3:])
            # print(value)
            if value[0] == '"':
                values = value.split('"')
                attr_value = values[1]
        else:
            attr_value = attr_value.strip('"')
        return attr_value

    def get_class_objects(self, line, objects):
        """ returns a list of the objects in <line> class """
        obj_list = []
        for cls in self.classes:
            if line == cls:
                for obj, val in objects.items():
                    cls_name = (obj.split('.'))[0]
                    # if an object is of given class, print it
                    if cls_name == line:
                        obj_list.append(str(val))
                return obj_list
        else:
            # some other class provided
            print("** class doesn't exist **")
            return (-1)

    @staticmethod
    def handle_attributes_dict(attrs):
        """ rebuilds arguments from a dictionary """
        # attrs is a str of attr_names and corresponding values
        attrs = attrs.strip('}')
        # print(attrs)
        list_ = attrs.split()
        # print(list_)
        # rebuild args to order expected
        values = []
        attr_dict = {}
        for idx, attr in enumerate(list_):
            if ':' in attr:
                # print('attr_name: ', attr)
                if idx != 0:
                    # assign prev attr_name, its value
                    attr_dict[name.strip("'")] = ' '.join(values)
                    # empty values to hold next attr's values
                    values = []
                name = attr.strip('"":')
            else:
                values.append(attr.strip('" ""'))
        # add last name: values pair
        attr_dict[name.strip("'")] = ' '.join(values)
        # print(attr_dict)
        return attr_dict

    # ========== end of helper functions ==============

    # ++++ custom console commands ++++ #

    def do_create(self, line):
        """ Create command to create a new instance """
        # check that class name is included in command
        if line:
            # check if class is valid
            for class_ in self.classes:
                if class_ in line:
                    # new = method()
                    new = eval(class_)()
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
            if args[0] and args[0] not in self.classes:
                print("** class doesn't exist **")
            else:
                # class exists, check id is provided
                if len(args) > 1:
                    # check that an object with [id] exists
                    # get the string objects
                    objects = storage.all()
                    # search for [this_id] object representation
                    args[1] = args[1].strip('"')
                    this_key = f"{args[0]}.{args[1]}"
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
            if args[0] and args[0] not in self.classes:
                # if args[0] and args[0] != 'BaseModel':
                print("** class doesn't exist **")
            else:
                # class exists, check id is provided
                if len(args) > 1:
                    # check that an object with [id] exists
                    # get the string objects (as reloaded)
                    objects = storage.all()
                    # search for [this_id] object representation
                    args[1] = args[1].strip('"')
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
        if line:
            # check the classname provided exists
            objs = self.get_class_objects(line, objects)
            if objs == -1:
                pass  # class doesn't exist
            else:
                print(objs)
        else:
            # print all instances (no filter)
            obj_list = []
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
            dict_args = {}
            if '{' in line:
                # pass to the function, the dictionary part
                dict_args = self.handle_attributes_dict((line.split('{'))[1])
            # check that class exists
            if args[0] and args[0] not in self.classes:
                print("** class doesn't exist **")
            else:
                # class exists, check id is provided
                if len(args) > 1:
                    objects = storage.all()
                    args[1] = args[1].strip('"')
                    this_key = f'{args[0]}.{args[1]}'
                    for obj, str_rep in objects.items():
                        if obj == this_key:
                            # object exists: update or add attribute
                            # check if a dictionary of attributes' provided
                            if dict_args:
                                # print("dictionary case")
                                for k, v in dict_args.items():
                                    self.update_attribute(args, str_rep, k, v)
                            else:
                                # print("normal case")
                                # just a single attribute-value pair to update
                                self.update_attribute(args, str_rep)
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

    def do_count(self, line):
        """ returns the number of objects in a given class """
        if not line:
            print("** class name missing **")
        else:
            # get objects in the class
            objects = storage.all()
            objs = self.get_class_objects(line, objects)
            # print count if class exists
            if objs != -1:
                print("{}".format(len(objs) if len(objs) else 0))

    def update_attribute(self, args, str_rep, *attr_args):
        """ performs the update process on the basis of how many attributes
        should be updated (how many times the updating happens per
        cmdloop) """
        # if attr_args is defined, comes in order(attr_name, attr_value)
        if attr_args:
            args[2], args[3] = attr_args[0], attr_args[1]
        # make update (either way)
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
                    # print("entirely new attribute")
                    if len(args) > 3:
                        # extend object dict_rep
                        attr_value = self.get_value(args)
                        if attr_value.isnumeric():
                            attr_value = int(attr_value)
                        elif attr_value[0].isnumeric() and '.' in attr_value:
                            attr_value = float(attr_value)
                        setattr(str_rep, args[2], attr_value)
                        # reserialize __objects into file
                        str_rep.save()
                    else:
                        print("** value missing **")
                    break
        else:
            # attribute_name missing
            print("** attribute name missing **")


# run the script if executed as main
if __name__ == '__main__':
    HBNBCommand().cmdloop()
