import time

# Error-level 'enum' Python style
class MessageLevel:
	INFO, ERROR, DEBUG = range(3)

# Can easily swap out the implementation of this to use a logger class
def print_msg(msg, lev):
	if lev == MessageLevel.INFO:
		print "Info: {0}".format(msg)
	elif lev == MessageLevel.ERROR:
		print "Error: {0}".format(msg)
	elif lev == MessageLevel.DEBUG:
		print "Debug: {0}".format(msg)

