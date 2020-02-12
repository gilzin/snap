#!/usr/bin/python
import sys
import logging
import struct
from time import sleep as CD
import snap7.client as c
from snap7.util import *
from snap7.snap7types import *

logger = logging.getLogger(__name__)


BLOCK = 0x82 # !!! DEPENDS ON THE LOGIC!! most common block id is 0x84 (it's the data block)

def ReadMemory(plc,byte,bit,datatype):
	result = plc.read_area(BLOCK,1,byte,datatype) #
	if datatype == S7WLBit:
		return get_bool(result,0,bit)
	elif datatype == S7WLByte or datatype == S7WLWord:
		return get_int(result,0)
	elif datatype == S7WLReal:
		return get_real(result,0)
	elif datatype == S7WLDWord:
		return get_dword(result,0)
	else:
		return None

def WriteMemory(plc,byte,bit,datatype,value):
	result = plc.read_area(BLOCK,1,byte,datatype)
        if datatype == S7WLBit:
                set_bool(result,0,bit,value)
        elif datatype == S7WLByte or datatype == S7WLWord:
                set_int(result,0,value)
        elif datatype == S7WLReal:
                set_real(result,0,value)
        elif datatype == S7WLDWord:
                set_dword(result,0,value)
	plc.write_area(BLOCK,1,byte,result)

def ReadOutputs():
	buffer = "["
	for i in range(8):
		if ReadMemory(plc,0,i,S7WLBit) == True:
			buffer+="1"
		else:
			buffer+="0"
		buffer+=","
	return buffer[:-1]+"]"

if __name__=="__main__":
	plc = c.Client()
	print  "Client Made"
	plc.connect(sys.argv[1],0,0)
	if plc.get_connected() == True:
		print ReadOutputs()
	else:
		print "Something Wrong"
