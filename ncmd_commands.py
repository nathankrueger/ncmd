#!/usr/bin/python

import re

class NCMD_CMDS:
	QUIT_CMD='quit'
	MOVE_CMD='mv'
	COPY_CMD='cp'
	REMOVE_CMD='rm'

CMD_KEY='cmd'
SRCS_KEY='srcs'
DEST_KEY='dest'
BLOCK_KEY='block'
RESP_KEY='rsp'
STATUS_KEY='status'

SUCCESS_RESP='success'
FAILURE_RESP='fail'

def genStringFromList(input_list):
	return " ".join(input_list)

def genCommand(cmd, source_list, dest, block):
	srcs = genStringFromList(source_list)
	return "{0}:({1}) {2}:({3}) {4}:({5}) {6}:({7})".format(CMD_KEY, cmd, SRCS_KEY, srcs, DEST_KEY, dest, BLOCK_KEY, block)

def genCmdSuccessResp(ncmd):
	return "{0}:(1}) {2}:({3})".format(RESP_KEY, ncmd, STATUS_KEY, SUCCESS_RESP)

def genCmdFailureResp(ncmd):
	return "{0}:(1}) {2}:({3})".format(RESP_KEY, ncmd, STATUS_KEY, FAILURE_RESP)

def isSuccessfulRsp(nrsp):
	return getResponseStatus(nrsp) == SUCCESS_RESP

def isUnsuccessfulRsp(nrsp):
	return getResponseStatus(nrsp) == FAILURE_RESP

def getResponseStatus(nrsp):
	result = ''
	match = re.search(r'{0}:\(.+\) {1}:\((.+)\)'.format(RESP_KEY, STATUS_KEY))
	if match:
		result = match.group(1)
	return result

def isResponse(ncmd, nrsp):
	result = False
	match = re.search(r'{0}:\((.+)\) {1}:\(.+\)'.format(RESP_KEY, STATUS_KEY))
	if match:
		result = (match.group(1) == ncmd)
	return result

def isQuitCmd(cmd):
	return (cmd == NCMD_CMDS.QUIT_CMD)

def isMove(ncmd):
	return getCommandCmd(ncmd) == NCMD_CMDS.MOVE_CMD

def isCopy(ncmd):
	return getCommandCmd(ncmd) == NCMD_CMDS.COPY_CMD

def isRemove(ncmd):
	return getCommandCmd(ncmd) == NCMD_CMDS.REMOVE_CMD

def getQuitSequence():
	return "{0} now".format(NCMD_CMDS.QUIT_CMD)

def isQuitSequence(data):
	return data == getQuitSequence()

def getRecognizedCmds():
	result = []
	result.append(NCMD_CMDS.QUIT_CMD)
	result.append(NCMD_CMDS.MOVE_CMD)
	result.append(NCMD_CMDS.COPY_CMD)
	result.append(NCMD_CMDS.REMOVE_CMD)
	return result

def getCommandCmd(cmd):
	result = ''
	match = re.search(r'{0}:\((\w+)\)'.format(CMD_KEY), cmd)
	if match:
		result = match.group(1)
	return result

def getCommandSrcs(cmd):
	result = []
	match = re.search(r'{0}:\((.+?)\)'.format(SRCS_KEY), cmd)
	if match:
		result_str = match.group(1)
		result = result_str.split(" ")
	return result

def getCommandDest(cmd):
	result = ''
	match = re.search(r'{0}:\((.+?)\)'.format(DEST_KEY), cmd)
	if match:
		result = match.group(1)
	return result

def getCommandBlock(cmd):
	result = ''
	match = re.search(r'{0}:\((.+?)\)'.format(BLOCK_KEY), cmd)
	if match:
		result = match.group(1)
	return result

