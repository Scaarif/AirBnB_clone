# AirBnB Clone - The Console
Description:
	The project implements the first feature/part in a four feature/part project
	This part, the console, does the following:
		> create your data model
		> manage (create, update, destroy, etc) objects via a console / command interpreter
		> store and persist objects to a file (JSON file)
	Simply put, this first part is to manipulate a powerful storage system. This storage engine will give us an abstraction
	between “My object” and “How they are stored and persisted”. This means: from your console code (the
	command interpreter itself) and from the front-end and RestAPI you will build later, you won’t have to pay
	attention (take care) of how your objects are stored.
	This abstraction will also allow you to change the type of storage easily without updating all of your codebase.
	The console will be a tool to validate this storage engine

How to Use:
	The module <console.py> at the root of the project defines the entry point to the project.
		Do: ./console.py (This initiates/runs the console)
	Console Usage: (hbtn) <--- type command here ---> 
			e.g.  help (for implemented commands) or help command (to get some information on <command>)
	Example console usage: (hbtn) help quit
				syntax: quit                                                                                                                                                    --terminates the application
