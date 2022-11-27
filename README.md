# AirBnB Clone - The Console
# Description:
The project implements the first feature/part in a four feature/part project
This part, the console, does the following -
1.create your data model
2.manage, create, update, destroy, etc objects via console/
command interpreter
3.store and persist objects to a file i.e. a JSON file
Simply put, this first part is to manipulate a powerful
storage system. This storage engine will give us an
abstraction between “My object” and
“How they are stored and persisted”. This means,
that from your console code, the
command interpreter itself and from the front-end
and RestAPI you will build later, you won’t have to pay
attention, take care, of how your objects are stored.
This abstraction will also allow you to change the type
of storage easily without updating all of your codebase.
The console will be a tool to validate this storage engine

How to Use
The module, console.py, at the root of the project
defines the entry point to the project.
Do ./console.py -> This initiates the console
Console Usage: $ command
e.g.  help -> for implemented commands or help command ->
to get some information on < --command-- >
Example console usage: $ help quit
Quit command to exit the program
