import time
import can
import threading
import writeToCSV as CSV
import binascii
from utils import Reading_CAN

times = 5 #number of messages to send

message = Reading_CAN()

#Send messages on the CAN bus.
def send(times = 5, command = None):
    if command:
        buffer = command
    else:
        buffer = [ 2, 0, 1, 3, 1, 4, 1]
    try:
        for i in range(times):
            msg = can.Message(arbitration_id=0xAA, data = buffer, is_extended_id=False)
    #       msg = can.Message(arbitration_id=0xc0ffee, data=b'message', is_extended_id=False)
            message.bus.send(msg)
    #       print(msg)
    except can.CanError:
         print("Unable to send CAN messages")     

#Read CAN bus, split the data into speed, current and duty cycle and store them in different buffers.
#Each time the Arduino receives a command, it sends it back to the Raspbery.
#To differentiate the messages, the id is checked. 
def read():
    while True:
        msg = message.bus.recv(0.0) #set waiting time [s]. If 0.0 non-blocking
        if msg:
            if len(message.data) > 5:  
                message.clear()
            if msg.arbitration_id == 0x0F6:    
                msg_hex = binascii.hexlify(msg.data).decode('ascii') #convert from bytearray to  hex
                data = [int(msg_hex[0:8],16), int(msg_hex[8:12],16),int(msg_hex[12:16],16)]
                message.data.append(data)
            else:
                data = (msg.data)
                print(f"Received from Arduino: {data}")
            if message.data_queue:
                message.data_queue.put(data)

def command(command):
    message = binascii.a2b_qp(command)
    send(times = 1, command = message)

def init():
    bustype = 'socketcan'
    channel = 'can0'
    message.bus = can.interface.Bus(channel=channel, bustype=bustype,receive_own_messages=False)   
    print("Hey, CAN connected!")
    t_read = threading.Thread(target=read)
    t_read.start()


def get_buffer():
    return message.getBuffer()

def emptyBuffer():
    message.clear()

def record():
    message.record(sensorName = "CAN")
    
def record_stop():
    message.record_stop()

if __name__ == "__main__":
    init()
    command("start")
#     while True:
#           print(get_buffer())
# #         send(times)