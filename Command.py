#!/usr/bin/python3
# -*- coding: utf-8 -*-

import struct
from crc import gen_crc

class Command:
    def __init__(self,slave):
        self.slave = slave
        self.fcode = 1
        self.regaddr = 1
        self.regnum = 1

        self.response = None
        self.func = []

    def pack(self):
        return None

    def parse(self,rsp = b''):
        return "ERROR"
    
class CmdGetFunction(Command):
    FUNCTION_BRIGHTNESS_LIGHT = 1
    
    def __init__(self,*argl,**args):
        Command.__init__(self,*argl,**args)

        self.fcode   = 3;
        self.regaddr = 1
        self.regnum  = 1
        
    def pack(self):
        # 子设备号
        msg  = struct.pack("B",self.slave)
        msg += struct.pack("B",self.fcode)
        msg += struct.pack("BB",(self.regaddr >> 8) & 0xFF,self.regaddr & 0xFF)
        msg += struct.pack("BB",(self.regnum >> 8) & 0xFF,self.regnum & 0xFF)

        crc_code = gen_crc(msg)

        msg += struct.pack("BB",(crc_code >> 8) & 0xFF, crc_code & 0xFF)

        return msg

    def parse(self,rsp = b''):
        if self.slave != rsp[0]:
            return None

        crc_code = gen_crc(rsp[:-2])
        if (crc_code >> 8) & 0xFF != rsp[-2] or crc_code & 0xFF != rsp[-1]:
            return {"Address":self.slave,"State":"ERROR"}

        if self.fcode != rsp[1]:
            return {"Address":self.slave,"State":"ERROR"}

        # 返回成功
        if self.fcode == rsp[1]:
            if 2 != rsp[2]:
                return {"Address":self.slave,"State":"ERROR"}
            
            self.response = "SUCCESS"
            val = (rsp[3] << 8) + rsp[4]

            if 0 != val & CmdGetFunction.FUNCTION_BRIGHTNESS_LIGHT:
                self.func.append("BrightnessLight")

        return {"Address":self.slave,
                "State":"Success",
                "Function":self.func}
            
                        
if __name__ == '__main__':
    cmd = CmdGetFunction(slave = 1)

    msg = cmd.pack()
    print(msg)
    
