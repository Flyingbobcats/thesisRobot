import sys
import json
import time
import socket
import socketserver
from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
import atexit

# Initialize Motors
mh = Raspi_MotorHAT(addr=0x6f)

def turnOffMotors():
	mh.getMotor(1).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(2).run(Raspi_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

lm = mh.getMotor(1)
rm = mh.getMotor(2)

class ControlPayload(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)
HOST, PORT = "192.168.0.198", 9999


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        # self.data = self.request.recv(1024).strip()
        # print "{} wrote:".format(self.client_address[0])
        # print self.data
        # just send back the same data, but upper-cased
        # self.request.sendall(self.data.upper())
        # try:

        while(True):
            received = self.request.recv(128)
            # print(received)
            try:
                newdata = ControlPayload(received)

                print("L:\t" + str(newdata.LEFT) + " \tR:\t" + str(newdata.RIGHT) + " \tT:\t" + str(newdata.TimeSec))
		#print(type(newdata.LEFT))

                # SET NEW PWM VALUES TO ROBOT HERE

		lm.setSpeed(int(newdata.LEFT))
		rm.setSpeed(int(newdata.RIGHT))

		lm.run(Raspi_MotorHAT.FORWARD)
		rm.run(Raspi_MotorHAT.FORWARD)

            except:
                print("socket error")
		turnOffMotors()
                return
#THIS IS THE PI
print("Server")
server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
# Activate the server; this will keep running until you
# interrupt the program with Ctrl-C
server.serve_forever()
