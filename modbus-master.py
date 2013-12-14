#!/usr/bin/python3

import serial
from register import Register
from ModbusModule import modbus_pack_read
from ModbusModule import modbus_pack_write

def print_bytes(s):
    for c in s:
        print("{:02X}".format(c),end = ' ')
    print(" ")

if __name__ == "__main__":
    ser = serial.Serial(port = '/dev/ttyUSB0',timeout = 0.2,baudrate = 9600,parity = serial.PARITY_NONE)

    while True:
        if b'' == ser.read():
            break

    reg = Register(Register.REGISTER_TYPE_HOLD,1)
    msg = modbus_pack_read(1,reg,3)

    ser.write(msg)
    print("Write Len: {}".format(len(msg)))
    print_bytes(msg)

    rsp = b''
    while True:
        r = ser.read()
        if b'' == r:
            print("Read Len: {}".format(len(rsp)))
            print_bytes(rsp)
            break
        
        rsp += r

    reg = Register(Register.REGISTER_TYPE_HOLD,2)
    msg = modbus_pack_write(1,reg,[0xFFFF,0x0080])
    ser.write(msg)
    print("Write Len: {}".format(len(msg)))
    print_bytes(msg)

    rsp = b''
    while True:
        r = ser.read()
        if b'' == r:
            print("Read Len: {}".format(len(rsp)))
            print_bytes(rsp)
            break
        
        rsp += r

    reg = Register(Register.REGISTER_TYPE_HOLD,1)
    msg = modbus_pack_read(1,reg,3)

    ser.write(msg)
    print("Write Len: {}".format(len(msg)))
    print_bytes(msg)

    rsp = b''
    while True:
        r = ser.read()
        if b'' == r:
            print("Read Len: {}".format(len(rsp)))
            print_bytes(rsp)
            break
        
        rsp += r

    exit(0)

    brightness = 0;
    while True:
        brightness &= 0x1FFFF

        if brightness > 0x10000:
            msg = modbus_pack_write(1,reg,(brightness - 0x10000) & 0xFFFF)
        else:
            msg = modbus_pack_write(1,reg,(0x10000 - brightness) & 0xFFFF)

        ser.write(msg)
        print("Write Len: {}".format(len(msg)))
        print_bytes(msg)
    
        rsp = b''
        while True:
            r = ser.read()
            if b'' == r:
                print("Read Len: {}".format(len(rsp)))
                print_bytes(rsp)
                break
            
            rsp += r

        brightness += 5000
