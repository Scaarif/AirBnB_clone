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
        self.classes = ['BaseModel',
                        'User',
                        'State',
                        'City',
                        'Place',
                        'Amenity',
                        'Review']

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

    # override default behavior if dict value
    def postcmd(self, stop, line):
        if stop:
            return True
        elif '{' in line:
            # print('postcmd: ', line)
            pass

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

    # ========== end of helper functions ==============

    # ++++ custom console commands ++++ #

    def do_create(self, line):
        """ <create class_name> creates a new instance of BaseModel, saves
        it(to JSON file) & prints the id (instance's) """
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
            # check for possible dictionary of values============
            if '{' in line:
                # print('dict_of attributes: ', (line.split())[2:])
                pass
            # ================================end_of_dict_handling=======
            args = line.split()
            # print('line split: ', args)
            # check that class exists
            if args[0] and args[0] not in self.classes:
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


# run the script if executed as main
if __name__ == '__main__':
    # instantiate class and run infinitely
    HBNBCommand().cmdloop()
