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

recognized_cmds = ncmds.getRecognizedCmds()

def getArgs():
	parser = argparse.ArgumentParser(description='Copy, move, remove quickly on a remotely mounted folder.')
	parser.add_argument('cmd', metavar='CMD', type=str, help='Command to run (cp, mv, rm)')
	parser.add_argument('src', metavar='SRC', nargs='*', type=str, help='Source path')
	parser.add_argument('dest', metavar='DEST', type=str, help='Destination path')
	parser.add_argument('--port', type=int, help='Specify a custom port.')
	parser.add_argument('--host', type=str, help='Specify a custom hostname where the ncmd server is running.')
	parser.add_argument('--non_blocking', action='store_true', help='Don\'t block on command completion.')
	return parser.parse_args()

def main():
	args = getArgs()
	HOST="192.168.1.189"
	PORT=10123
	blocking = '1'
	if args.non_blocking:
		blocking = '0'

	if not args.cmd in recognized_cmds:
		np.print_msg("Unrecognized command: {0}".format(args.cmd), MessageLevel.ERROR)
		sys.exit()
	
	quit = ncmds.isQuitCmd(args.cmd)
	if quit:
		ncmd = ncmds.getQuitSequence()
	else:
		ncmd = ncmds.genCommand(args.cmd, args.src, args.dest, blocking)

	np.print_msg("Command to send: {0}".format(ncmd), MessageLevel.DEBUG)

	if args.port:
		PORT = args.port

	if args.host:
		HOST = args.host

	client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		client_sock.connect((HOST, PORT))
	except socket.error as msg:
		np.print_msg(msg, MessageLevel.ERROR)
		client_sock = None

	if client_sock:
		np.print_msg("Successfully connected to host: {0}:{1}".format(HOST, PORT), MessageLevel.INFO)
		client_sock.sendall(ncmd)
		if not args.non_blocking and not quit:
			nrsp = client_sock.recv(ncmds.MAX_CMD_SIZE)
			if ncmds.isResponse(ncmd, nrsp):
				if ncmds.isSuccessfulRsp(nrsp):
					np.print_msg("Command: {0} completed successfully.".format(ncmd), MessageLevel.INFO)
				elif ncmds.isFailureRsp(nrsp):
					np.print_msg("Command: {0} completed unsuccessfully.".format(ncmd), MessageLevel.ERROR)
			else:
				np.print_msg("Something odd recieved... not a recognized response: {0}".format(nrsp), MessageLevel.ERROR)

	# Keep this at the end for safety!
	if client_sock:
		client_sock.close()

if __name__ == '__main__':
	main()
