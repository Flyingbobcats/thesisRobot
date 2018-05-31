#
# Send pwm commands to differential drive robot
#


import socket
import time
import json

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

addr = '127.0.0.1'

cmd = {}
while True:
    
    for i in range(100,255):
        cmd["left"] = i
        cmd["right"] = i
        message = json.dumps(cmd)
        client_socket.sendto(message,(addr,5555))
        print("forward")
        time.sleep(0.1)


