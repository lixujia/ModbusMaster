#!/usr/bin/python3

from serial import Serial
from Command import Command

def print_bytes(s):
    for c in s:
        print("{:02X}".format(c),end = ' ')
    print(" ")

class ModbusMaster(Serial):
    def __init__(self,*args,**argv):
        Serial.__init__(self,*args,**argv)

        while True:
            if b'' == self.read():
                break
            
    def execute_cmd(self,cmd):
        req = cmd.pack()

        self.write(req)
        print("Write Len: {}".format(len(req)))
        print_bytes(req)

        rsp = b''
        while True:
            r = self.read()
            if b'' == r:
                break

            rsp += r

        return cmd.parse(rsp)
        
        
