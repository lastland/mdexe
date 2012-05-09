#/usr/bin/python
import sys
from mdinc import *
from mdexec import *
from mdhelp import *

usage_str = """\
    Usage: mdexe <command> [<args>]
    You can use "mdexe help" to see available commands.\
"""

commands = {"exec" : mdexec, "trans" : mdinc, "help" : mdhelp}

if __name__ == "__main__":
    if len(sys.argv) > 1:
	command = sys.argv[1]
    else:
	command = "help"
    command_args = sys.argv[2:]
    if command in commands:
	commands[command](command_args)
    else:
	print "Unknown command: %s." % (command)
	print usage_str
