#!/usr/bin/python

import socket
import os
import time
import shutil
import sys

# NCMD Libs
import ncmd_print as np
from ncmd_print import ErrorLevel as ErrorLevel

HOST="192.168.1.189"
PORT=10123

def main():
	client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		client_sock.connect((HOST, PORT))
	except socket.error as msg:
		np.print_msg(msg, ErrorLevel.ERROR)
		client_sock = None

	if client_sock:
		np.print_msg("Successfully connected to host: {0}:{1}".format(HOST, PORT), ErrorLevel.INFO)
		client_sock.sendall(sys.argv[1])

	# Keep this at the end for safety!
	if client_sock:
		client_sock.close()

if __name__ == '__main__':
	main()
