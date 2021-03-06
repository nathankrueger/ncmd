#!/usr/bin/python

import socket
import os
import time
import shutil
import sys
import argparse

# NCMD Libs
import ncmd_print as np
from ncmd_print import MessageLevel as MessageLevel
import ncmd_commands as ncmds
import ncmd_fileops

recognized_cmds = ncmds.getRecognizedCmds()
LAST_MNT_FILENAME=".lastmnt"

def getLastClientMnt():
	result = ''
	fileContents = getLastMntFileContents()
	try:
		result = fileContents.split('\n')[0]
	except:
		result = ''
	return result

def getLastServerMnt():
	result = ''
	fileContents = getLastMntFileContents()
	try:
		result = fileContents.split('\n')[1]
	except:
		result = ''
	return result

def getLastMntFileContents():
	result = ''
	try:
		if os.path.isfile(LAST_MNT_FILENAME):
			f = open(LAST_MNT_FILENAME, 'r')
			result = f.read()
			f.close()
	except Exception as err:
		np.print_msg("An error occured retrieving the previous mount file: {0}".format(err), MessageLevel.ERROR)
		result = ''

	return result

def writeLastMntFile(client_mount_path, server_mount_path):
	try:
		f = open(LAST_MNT_FILENAME, 'w')
		f.write(client_mount_path)
		f.write(server_mount_path)
		f.close()
	except Exception as err:
		np.print_msg("An error occured writing the previous mount file: {0}".format(err), MessageLevel.ERROR)
		result = ''
		
def getClientMount(client_arg):
	result = client_arg
	if not result:
		result = getLastClientMnt()
	return result

def getServerMount(client_arg):
	result = client_arg
	if not result:
		result = getLastServerMnt()
	return result

def getArgs():
	parser = argparse.ArgumentParser(description='Copy, move, remove quickly on a remotely mounted folder.')
	parser.add_argument('cmd', metavar='CMD', type=str, help='Command to run (cp, mv, rm)')
	parser.add_argument('src', metavar='SRC', nargs='*', type=str, help='Source path')
	parser.add_argument('dest', metavar='DEST', type=str, help='Destination path')
	parser.add_argument('--port', type=int, help='Specify a custom port.')
	parser.add_argument('--host', type=str, help='Specify a custom hostname where the ncmd server is running.')
	parser.add_argument('--non_blocking', action='store_true', help='Don\'t block on command completion.')
	parser.add_argument('--client_mount', type=str, help='Specify a mount for the client.')
	parser.add_argument('--server_mount', type=str, help='Specify a mount for the server.')

	return parser.parse_args()

def main():
	args = getArgs()
	HOST="192.168.1.189"
	PORT=10123
	blocking = '1'
	if args.non_blocking:
		blocking = '0'

	# Parse the command.
	if not args.cmd in recognized_cmds:
		np.print_msg("Unrecognized command: {0}".format(args.cmd), MessageLevel.ERROR)
		sys.exit()
	
	client_mnt = getClientMount(args.client_mount)
	server_mnt = getServerMount(args.server_mount)
	
	# Some debug messages to help the user figure out what their mounts are if not explicitly set.
	np.print_msg("Using client mount: {0}".format(client_mnt), MessageLevel.DEBUG)
	np.print_msg("Using server mount: {0}".format(server_mnt), MessageLevel.DEBUG)

	# Convert the client path to a server path, if possible
	sources = []
	destination = ''
	if (client_mnt and server_mnt):
		# Add sources we can parse -- in the future maybe we should error out and warn the user if we can't
		for src in args.src:
			converted_source = ncmd_fileops.convertPath(client_mnt, server_mnt, src)
			if converted_source:
				sources.append(converted_source)
	
		destination = ncmd_fileops.convertPath(client_mnt, server_mnt, args.dest)

	else:
		sources = args.src
		destination = args.dest
		
	quit = ncmds.isQuitCmd(args.cmd)
	if quit:
		ncmd = ncmds.getQuitSequence()
	else:
		ncmd = ncmds.genCommand(args.cmd, sources, destination, blocking)

	np.print_msg("Command to send: {0}".format(ncmd), MessageLevel.DEBUG)

	if args.port:
		PORT = args.port

	if args.host:
		HOST = args.host

	client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Try the connection.
	try:
		client_sock.connect((HOST, PORT))
	except socket.error as msg:
		np.print_msg(msg, MessageLevel.ERROR)
		client_sock = None

	if client_sock:
		np.print_msg("Successfully connected to host: {0}:{1}".format(HOST, PORT), MessageLevel.INFO)
		client_sock.sendall(ncmd)

		# Close the connection on the client when quitting to allow socket reuse!
		if quit:
			client_sock.close()
			client_sock = None

		# We only expect responses for blocking commands, and expect none for the quit cmd.
		if not args.non_blocking and not quit:
			nrsp = client_sock.recv(ncmds.MAX_CMD_SIZE)

			# If the recieved response is legit.
			if ncmds.isResponse(ncmd, nrsp):
				if ncmds.isSuccessfulRsp(nrsp):
					np.print_msg("Command: {0} completed successfully.".format(ncmd), MessageLevel.INFO)
				elif ncmds.isFailureRsp(nrsp):
					np.print_msg("Command: {0} completed unsuccessfully.".format(ncmd), MessageLevel.ERROR)
			else:
				np.print_msg("Something odd recieved, not a recognized response: {0}".format(nrsp), MessageLevel.ERROR)

	# Keep this at the end for safety!
	if client_sock:
		client_sock.close()

	# Maybe a more sophisticated decesion here later -- like if the mount paths exist.
	writeLastMntFile(client_mnt, server_mnt)

if __name__ == '__main__':
	main()
