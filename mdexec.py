import re
import subprocess

exec_prog = re.compile("Exec:", re.UNICODE)
append_prog = re.compile("(?<=Append_to\s\').+(?=\'\s:)", re.UNICODE)
replace_prog = re.compile("(?<=Replace_in\s\').+(?=\'\s:)", re.UNICODE)
replace_text_prog = re.compile("to\s:", re.UNICODE)
replace_and_prog = re.compile("and\s:", re.UNICODE)
code_prog = re.compile("(?<=    ).+", re.UNICODE)

NORMAL_STATE = 0
EXEC_STATE = 1
APPEND_STATE = 2
REPLACE_PATTERN_STATE = 3
REPLACE_STATE = 4

state = NORMAL_STATE
file_object = None
file_name = None
replace_pattern = None
replace_pattern_prog = None
replace_text = None
text = None

def normal_handle(line):
    global state, file_object, file_name, replace_pattern, replace_text

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

    # Replace found
    res = replace_prog.search(line)
    if res != None:
	state = REPLACE_PATTERN_STATE
	file_name = res.group(0)
	replace_pattern = []
	replace_text = []
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
	    file_object.write(line + '\n')
	except IOError:
	    print "Error happened while trying to append text into file: %s" % (file_name)
    else:
        file_object.close()
	state = NORMAL_STATE
	handlers[state](line)

def replace_handle(line):
    global state, file_name, replace_pattern, replace_pattern_prog, replace_text

    if len(line) == 0: return

    if state == REPLACE_PATTERN_STATE:
	res = replace_text_prog.search(line)
	if res != None:
	    state = REPLACE_STATE
	    pattern = '\n'.join(replace_pattern)
	    replace_pattern_prog = re.compile(pattern, re.UNICODE)
	    return

	res = code_prog.search(line)
	if res != None:
	    line = line[4:]
	    replace_pattern.append(line)
	else:
	    # Not supposed to happen
	    pass
    else:
	res = code_prog.search(line)
	if res != None:
	    line = line[4:]
	    replace_text.append(line)
	else:
	    file_object = open(file_name, "r")
	    text = ''.join(line for line in file_object)
	    file_object.close()
	    text = replace_pattern_prog.sub(''.join(replace_text), text)
	    file_object = open(file_name, "w")
	    file_object.write(text)
	    file_object.close()
	    res = replace_and_prog.search(line)
	    if res != None:
		state = REPLACE_PATTERN_STATE
		replace_pattern = []
		replace_text = []
	    else:
		state = NORMAL_STATE
		handlers[state](line)


handlers = {NORMAL_STATE : normal_handle,
	    EXEC_STATE : exec_handle,
	    APPEND_STATE : append_handle,
	    REPLACE_PATTERN_STATE : replace_handle,
	    REPLACE_STATE : replace_handle}


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
