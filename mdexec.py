import re
import subprocess

# TODO: Append to, Replace in.

exec_prog = re.compile("Exec:", re.UNICODE)
append_prog = re.compile("(?<=Append_to\s\').+(?=\'\s:)", re.UNICODE)
code_prog = re.compile("(?<=    )\w+", re.UNICODE)

NORMAL_STATE = 0
EXEC_STATE = 1
APPEND_STATE = 2

state = NORMAL_STATE
file_object = None
file_name = None

def normal_handle(line):
    global state, file_object, file_name

    if len(line) == 0: return
    # print line

    # Exec found
    res = exec_prog.search(line)
    if res != None:
	state = EXEC_STATE
	return

    # Append_to found
    res = append_prog.search(line)
    if res != None:
	state = APPEND_STATE
	file_name = res.group(0)
	try:
	    file_object = open(file_name, "a")
	    file_object.write("")
	except IOError:
	    print "Can not access file %s" % (file_name)
	return


def exec_handle(line):
    global state

    if len(line) == 0: return
    res = code_prog.search(line)
    if res != None:
	# print line
	subprocess.call(line, shell=True)
    else:
	state = NORMAL_STATE
	handlers[state](line)


def append_handle(line):
    global state, file_object, file_name

    if len(line) == 0: return
    res = code_prog.search(line)
    if res != None:
	line = line[4:]
	# print line
	try:
	    file_object.write(line)
	except IOError:
	    print "Error happened while trying to append text into file: %s" % (file_name)
    else:
        file_object.close()
	state = NORMAL_STATE
	handlers[state](line)


handlers = {NORMAL_STATE : normal_handle,
	    EXEC_STATE : exec_handle,
	    APPEND_STATE : append_handle}


def mdexec(args):
    """
    All lines in format:
	Exec:
	    some commands
    will trigger the execution of 'some commands' in the shell.
    """
    global state, file_object, file_name
    state = NORMAL_STATE
    file_object = None
    file_name = None

    filename = args[0]
    try:
	f = open(filename)
	for line in f:
	    handlers[state](line[:-1])
    except IOError:
	print "Can't access file: %s." % (filename)
