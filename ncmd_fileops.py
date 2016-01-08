#!/usr/bin/python

import os
import time
import shutil
import sys

# NCMD Libs
import ncmd_print as np
from ncmd_print import MessageLevel as MessageLevel

def isFile(path):
	return os.path.isfile(path)

def isDirectory(path):
	return (not os.path.isfile(path) and os.path.exists(path))

def copy(src, dest):
	result = True
	try:
		if isFile(src):
			shutil.copy(src, dest)
			np.print_msg("Copied file {0} to {1}".format(src, dest), MessageLevel.INFO)
		elif isDirectory(src):
			shutil.copytree(src, dest)
			np.print_msg("Copied folder {0} to {1}".format(src, dest), MessageLevel.INFO)
		else:
			np.print_msg("Failed to remove {0} ...\n\tNot a recognized file or folder.".format(src), MessageLevel.ERROR)
			result = False
	except Exception as err:
		np.print_msg("Failed to copy {0} to {1} ...\n\t{2}".format(src, dest, err), MessageLevel.ERROR)
		result = False
	
	return result

def move(src, dest):
	result = True
	try:
		shutil.move(src, dest)
		np.print_msg("Moved {0} to {1}".format(src, dest), MessageLevel.INFO)
	except Exception as err:
		np.print_msg("Failed to move {0} to {1} ...\n\t{2}".format(src, dest, err), MessageLevel.ERROR)
		result = False

	return result

def remove(target):
	result = True
	try:
		if isFile(target):
			os.remove(target)
			np.print_msg("Removed file {0}".format(target), MessageLevel.INFO)
		elif isDirectory(target):
			shutil.rmtree(target)
			np.print_msg("Removed folder {0}".format(target), MessageLevel.INFO)
		else:
			np.print_msg("Failed to remove {0} ...\n\tNot a recognized file or folder.".format(target), MessageLevel.ERROR)
			result = False
	except Exception as err:
		np.print_msg("Failed to remove {0} ...\n\t{2}".format(target, err), MessageLevel.ERROR)
		result = False

	return result

def convertPath(src_mnt, target_mnt, path):
	result = ""
	if path.find(src_mnt) == 0:
		result = target_mnt
		result += path[len(src_mnt):]
	
	return result

