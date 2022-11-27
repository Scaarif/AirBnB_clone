#!/usr/bin/python3
""" Defines tests for the HBNBCommand class as defined in the console
module """
from console import HBNBCommand
import unittest


class TestHBNBCommand(unittest.TestCase):
    """ Defines tests for HBNBCommand attributes and methods """
    def setUp(self):
        """ set up class instances for use in tests """
        self.command = HBNBCommand()

    # test that the class inherits from cmd.Cmd
    # test that the custom promt is (hbtn)
    # test that quit and EOF are imlemented and work
    # test that do_commands have docstrings (return a str) on <help command>
    # test that emptyline + ENTER does not execute anything
    # test that the do_ methods have been implemented:
    # create -> creates a new instance of <class>
    # show -> prints the str rep of an object <id> of class <class>
    # destroy -> deletes an instance (so show returns no instance found after)
    # all -> displays (str reps of) all objects currently in created
    # (loads from file.json)
    # update -> updates (attribute's value) if in existence /adds a new
    # attribute (name & value) to an object
    # test that error handling is correctly implemented for the different
    # methods including:
    # value type, class or id missing, unimplemented classes, etc
    # =================== WRITE THE TESTS PER METHOD (i.e. a class per method)
