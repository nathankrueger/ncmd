#!/usr/bin/python

import socket
import os
import time
import shutil
import sys

# NCMD Libs
import ncmd_print as np
from ncmd_print import ErrorLevel as ErrorLevel

HOST=""
PORT=10123

def main():
	server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	conn = None
	addr = None

	try:
		server_sock.bind((HOST, PORT))
		server_sock.listen(1)
		conn, addr = server_socket.appect()
		np.print_msg("Successfully connected to client: {0}:{1}".format(addr, PORT), ErrorLevel.INFO)

	except socket.error as msg:
		np.print_msg(msg, ErrorLevel.ERROR)
		server_sock = None

	if server_sock:
		data = conn.recv(1024)
		print data

	# Keep this at the end for safety!
	if server_sock:
		server_sock.close()
	
	if conn:
		conn.close()

if __name__ == '__main__':
	main()
