import time

# Error-level 'enum' Python style
class ErrorLevel:
	INFO, ERROR, DEBUG = range(3)

# Can easily swap out the implementation of this to use a logger class
def print_msg(msg, lev):
	if lev == ErrorLevel.INFO:
		print "Info: {0}".format(msg)
	elif lev == ErrorLevel.ERROR:
		print "Error: {0}".format(msg)
	elif lev == ErrorLevel.DEBUG:
		print "Debug: {0}".format(msg)

