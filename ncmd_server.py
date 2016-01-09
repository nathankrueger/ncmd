#!/usr/bin/python

import socket
import os
import time
import shutil
import sys
import re
import datetime
import argparse

# NCMD Libs
import ncmd_print as np
from ncmd_print import MessageLevel as MessageLevel
import ncmd_commands as ncmds
import ncmd_fileops as nfops

MAX_TRANSFER_BYTES=2048
QUIT_CMD = "quit now"
HOST = ""
PORT = 10123
ROOT_DIR_PATH = "/share/CACHEDEV1_DATA"

# Set up the server socket
def bindServerSocket(port):
	server_sock = None
	try:
		server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server_sock.bind((HOST, port))
		np.print_msg("Successfully bound server socket to port:{0}".format(PORT), MessageLevel.INFO)
	except Exception as err:
		np.print_msg("Failed to bind server socket to port:{0}".format(PORT), MessageLevel.ERROR)
		server_sock = None

	return server_sock

# Accept incoming socket connections
def acceptConnection(server_sock):
	server_sock.listen(1)
	conn, addr = server_sock.accept()
	return (conn, addr)

# Validate a path against the server mount
def validatePath(path, server_mnt):
	result = False
	# Paths beginning with the server mount are considered 'valid'
	if path.find(server_mnt) == 0:
		result = True

	return result

# Validate source / destination paths
def validatePaths(paths, server_mnt):
	result = True
	for path in paths:
		if not validatePath(path, server_mnt):
			result = False
			break
	
	return result

# Deal with generating the appropriate response for a command
def processResponse(ncmd, success):
	nresp = ''
	if ncmds.getCommandBlock(ncmd):
		if success:
			nresp = ncmds.genCmdSuccessResp(ncmd)
		else:
			nresp = ncmds.genCmdFailureResp(ncmd)
	else:
		pass # No response for non-blocking
	
	return nresp

# Handle the current command string -- the actual file operations occur here
def processCmd(ncmd, args):
	quit = False
	cmd_success = True
	np.print_msg("Received command: {0}".format(ncmd), MessageLevel.INFO)

	dest = ncmds.getCommandDest(ncmd)
	srcs = ncmds.getCommandSrcs(ncmd)
	
	if ncmds.isQuitSequence(ncmd):
		quit = True

	else:
		if args.validate_server_mount:
			srcs_valid = validatePaths(srcs, args.validate_server_mount)
			dest_valid = validatePath(dest, args.validate_server_mount)
			cmd_success = srcs_valid and dest_valid
	
		# Only try and conduct file operations when validation is disabled,
		# or if validation is enabled, and it passes.
		if cmd_success:	
			if ncmds.isMove(ncmd):
				for src in srcs:
					if not nfops.move(src, dest):
						cmd_success = False
	
			elif ncmds.isCopy(ncmd):
				for src in srcs:
					if not nfops.copy(src, dest):
						cmd_success = False
	
			elif ncmds.isRemove(ncmd):
				# The naming here isn't ideal, but this code gets the job done!
				for src in srcs:
					if not nfops.remove(src):
						cmd_success = False
	
				if not nfops.remove(dest):
					cmd_success = False

	return quit, cmd_success

# Deal with the current connection, getting, sending, and closing
def processConnection(conn, args):
	ncmd = conn.recv(ncmds.MAX_CMD_SIZE)
	quit, cmd_success = processCmd(ncmd, args)

	resp = processResponse(ncmd, cmd_success)
	if len(resp) > 0:
		try:
			conn.send(resp)
		except Exception as err:
			np.print_msg(msg, MessageLevel.ERROR)

	conn.close()
	return quit

def getArgs():
	parser = argparse.ArgumentParser(description='Copy, move, remove quickly on a remotely mounted folder.')
	parser.add_argument('--port', type=int, help='Specify a custom port.')
	parser.add_argument('--validate_server_mount', type=str, help='Specify a mount on the server to validate incoming paths against.')

	return parser.parse_args()

def main():
	# Get the port
	args = getArgs()
	server_port = PORT
	if args.port:
		server_port = args.port

	# Bind the sever socket
	server_sock = bindServerSocket(server_port)
	if server_sock:
		while True:
			conn = None
			try:
				conn, addr = acceptConnection(server_sock)
				np.print_msg("Successfully connected to client: {0}:{1}".format(addr[0], PORT), MessageLevel.INFO)
			except socket.error as msg:
				np.print_msg(msg, MessageLevel.ERROR)
				conn = None
		
			if conn:
				quit = processConnection(conn, args)
				if quit:
					np.print_msg("Server shutdown requested @ {0}...".format(datetime.datetime.now()), MessageLevel.INFO)
					break
				
	# Keep this at the end for safety!
	if server_sock:
		server_sock.close()

if __name__ == '__main__':
	main()

