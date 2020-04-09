import time
import can

bustype = 'socketcan'
channel = 'can0'
bus = can.interface.Bus(channel=channel, bustype=bustype)
times = 10 #number of messages to send

#send messages on the CAN bus
def send(times):    
    for i in range(times):
        msg = can.Message(arbitration_id=0xAA, data=[ i, 0, 1, 3, 1, 4, 1], is_extended_id=False)
#        msg = can.Message(arbitration_id=0xc0ffee, data=b'message', is_extended_id=False)
        bus.send(msg)
        print(msg)
    time.sleep(1)

#send(times)

def read():
    while True:
        message = bus.recv(0.0) #set waiting time [s]. If 0.0 non-blocking
        if message:
            print(message)

read()