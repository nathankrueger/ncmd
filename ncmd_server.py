#!/usr/bin/python

import socket
import os
import time
import shutil
import sys
import re

# NCMD Libs
import ncmd_print as np
from ncmd_print import ErrorLevel as ErrorLevel
import ncmd_commands as ncmds
import ncmd_fileops as nfops

QUIT_CMD = "quit now"
HOST = ""
PORT = 10123
ROOT_DIR_PATH = "/share/CACHEDEV1_DATA"

def bindServerSocket():
	server_sock = None
	try:
		server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_sock.bind((HOST, PORT))
		np.print_msg("Successfully bound server socket to port:{0}".format(PORT), ErrorLevel.INFO)
	except Exception as err:
		np.print_msg("Failed to bind server socket to port:{0}".format(PORT), ErrorLevel.ERROR)
		server_sock = None

	return server_sock

def acceptConnection(server_sock):
	server_sock.listen(1)
	conn, addr = server_sock.accept()
	return (conn, addr)	

def processData(data):
	quit = False
	np.print_msg("Received command: {0}".format(data), ErrorLevel.INFO)

	dest = ncmds.getCmdDest(data)
	srcs = getCommandSrcs(data)

	if ncmds.isQuitSequence(data):
		quit = True
	elif ncmds.isMove(data):
		for src in srcs:
			if nfops.move(src, dest):
				# Respond Success
			else:
				# Respond failure
		
	elif ncmds.isCopy(data):
		for src in srcs:
			if nfops.copy(src, dest):
				# Respond Success
			else:
				# Respond failure

	elif ncmds.isRemove(data):
		if nfops.remove(dest):
			# Respond Success
		else:
			# Respond failure

	return quit

def main():
	server_sock = bindServerSocket()
	if server_sock:
		while True:
			conn = None
			try:
				conn, addr = acceptConnection(server_sock)
				np.print_msg("Successfully connected to client: {0}:{1}".format(addr[0], PORT), ErrorLevel.INFO)
			except socket.error as msg:
				np.print_msg(msg, ErrorLevel.ERROR)
				server_sock = None
		
			if conn:
				data = conn.recv(1024)
				conn.close()
				if processData(data):
					break
				
	# Keep this at the end for safety!
	if server_sock:
		server_sock.close()

if __name__ == '__main__':
	main()
