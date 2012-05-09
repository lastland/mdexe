import re
import subprocess

# TODO: Append to, Replace in.

exec_prog = re.compile("Exec:", re.UNICODE)
code_prog = re.compile("(?<=    )\w+", re.UNICODE)

NORMAL_STATE = 0
EXEC_STATE = 1

state = NORMAL_STATE

def normal_handle(line):
    global state

    print line

    res = exec_prog.search(line)
    if res != None:
	state = EXEC_STATE


def exec_handle(line):
    global state

    res = code_prog.search(line)
    if res != None:
	print line
	subprocess.call(line, shell=True)
    else:
	state = NORMAL_STATE
	handlers[state](line)

handlers = {NORMAL_STATE : normal_handle,
	    EXEC_STATE : exec_handle}


def mdexec(args):
    """
    All lines in format:
	Exec:
	    some commands
    will trigger the execution of 'some commands' in the shell.
    """
    global state
    state = NORMAL_STATE

    filename = args[0]
    try:
	f = open(filename)
	for line in f:
	    handlers[state](line)
    except IOError:
	print "Can't access file: %s." % (filename)
