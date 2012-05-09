help_str = """\
    Usage: mdexe <command> [<args>]

    Available commands:
	trans   translate markdown document with "include" and "require" into normal markdown.
	exec    execute the markdown document.\
"""

def mdhelp(args):
    """
    Print the available commands.
    """
    print help_str
