#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import socketserver
from Command import CmdGetFunction
from ModbusMaster import ModbusMaster

mm = ModbusMaster(port = "/dev/ttyUSB0",timeout = 0.2,baudrate = 9600)

def process_request(data):
    req = json.loads(data.decode())

    if "Address" not in req or "cmd" not in req:
        return b"Error"

    slave = req["Address"]

    if "GetFunction" == req["cmd"]:
        cmd = CmdGetFunction(slave)
    else:
        return b"Error"

    rsp = mm.execute_cmd(cmd)
    if None == rsp:
        return b"Error"

    return json.dumps(rsp)

class MyUDPHandler(socketserver.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]

        rsp = process_request(data)

        socket.sendto(rsp, self.client_address)

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    server = socketserver.UDPServer((HOST, PORT), MyUDPHandler)
    server.serve_forever()

