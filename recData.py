
import socket
import time
import json
from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
import atexit


def turnOffMotors():
	mh.getMotor(1).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(2).run(Raspi_MotorHAT.RELEASE)
	print("Motors Off")



atexit.register(turnOffMotors)


mh = Raspi_MotorHAT(addr=0x6f)
lm = mh.getMotor(1)
rm = mh.getMotor(2)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 5555))

while True:
    data, server = server_socket.recvfrom(1024)
    data = json.loads(data)
    print(data)
    print(data["left"])
    
    lm.setSpeed(int(data["left"]))
    rm.setSpeed(int(data["right"]))
    lm.run(Raspi_MotorHAT.FORWARD)
    rm.run(Raspi_MotorHAT.FORWARD)
    time.sleep(0.1)
    