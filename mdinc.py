import re

# TODO: require.

inc_prog = re.compile("(?<=include \').+(?=\')", re.UNICODE)

def mdinc(args):
    """
    All lines in format:
	include 'filename.markdown'
    will be translated into the contents in 'filename.markdown'.
    Recursive translate cannot be supported yet.
    """
    filename = args[0]
    try:
	f = open(filename)
	for line in f:
	    line = line[:-1]
	    res = inc_prog.search(line)
	    if res != None:
		inc_f = open(res.group(0))
		for line in inc_f:
		    print line[:-1]
	    else:
		print line
    except IOError:
	print "Can not access file: %s" % (filename)
