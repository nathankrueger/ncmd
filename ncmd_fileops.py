#!/usr/bin/python

import os
import time
import shutil
import sys

# NCMD Libs
import ncmd_print as np
from ncmd_print import ErrorLevel as ErrorLevel

def isFile(path):
	return os.path.isfile(path)

def isDirectory(path):
	return (not os.path.isfile(path) and os.path.exists(path))

def copy(src, dest):
	result = True
	try:
		if isFile(src):
			shutil.copy(src, dest)
		elif isDirectory(src):
			shutil.copytree(src, dest)
		np.print_msg("Copied {0} to {1}...".format(src, dest), ErrorLevel.INFO)
	except Exception as err:
		np.print_msg("Failed to copy {0} to {1}...\n\t{2}".format(src, dest, err), ErrorLevel.ERROR)
		result = False
	
	return result

def move(src, dest):
	result = True
	try:
		shutil.move(src, dest)
		np.print_msg("Moved {0} to {1}...".format(src, dest), ErrorLevel.INFO)
	except Exception as err:
		np.print_msg("Failed to move {0} to {1}...\n\t{2}".format(src, dest, err), ErrorLevel.ERROR)
		result = False

	return result

def remove(target):
	result = True
	try:
		if isFile(target):
			os.remove(target)
		elif isDirectory(target):
			shutil.rmtree(target)
		np.print_msg("Removed {0}...".format(target), ErrorLevel.INFO)
	except Exception as err:
		np.print_msg("Failed to remove {0}...\n\t{2}".format(target, err), ErrorLevel.ERROR)
		result = False

	return result

