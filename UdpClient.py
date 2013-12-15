import socket
import sys
import json

HOST, PORT = "192.168.1.200", 9999

cmd = {"Address":1,
       "cmd":"GetFunction"}

data = json.dumps(cmd,indent = "  ")
    
# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# As you can see, there is no connect() call; UDP has no connections.
# Instead, data is directly sent to the recipient via sendto().
sock.sendto(bytes(data, "utf-8"), (HOST, PORT))
received = str(sock.recv(1024), "utf-8")

print("Sent:     {}".format(data))
print("Received: {}".format(received))
