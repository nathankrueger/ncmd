#!/usr/bin/python

import socket
import os
import time
import shutil
import sys
import argparse

# NCMD Libs
import ncmd_print as np
from ncmd_print import ErrorLevel as ErrorLevel
import ncmd_commands as ncmds

recognized_cmds = ncmd.getRecognizedCmds()

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

	if not cmd in recognized_cmds:
		np.print_msg("Unrecognized command: {0}".format(args.cmd), ErrorLevel.ERROR)
		sys.exit()
	
	if ncmds.isQuitCmd(args.cmd):
		ncmd = ncmds.getQuitSequence()
	else:
		ncmd = ncmds.genCommand(args.cmd, args.src, args.dest, blocking)

	np.print_msg("Command to send: {0}".format(ncmd, ErrorLevel.DEBUG)

	if args.port:
		PORT = args.port

	if args.host:
		HOST = args.host

	client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		client_sock.connect((HOST, PORT))
	except socket.error as msg:
		np.print_msg(msg, ErrorLevel.ERROR)
		client_sock = None

	if client_sock:
		np.print_msg("Successfully connected to host: {0}:{1}".format(HOST, PORT), ErrorLevel.INFO)
		client_sock.sendall(ncmd)

	# Keep this at the end for safety!
	if client_sock:
		client_sock.close()

if __name__ == '__main__':
	main()
