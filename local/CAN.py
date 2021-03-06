import can
import threading
import writeToCSV as CSV
import binascii
from utils import Reading_CAN

message = Reading_CAN()

#Send messages on the CAN bus.
def send(ID=0, command=0):
    try:
        msg = can.Message(arbitration_id= ID, data = bytearray([command]), is_extended_id=False)
        message.bus.send(msg)
#       print(msg)
    except can.CanError:
        print("Unable to send CAN messages")
    except ValueError:
        print("Command must be in range (0, 256)")

#Read CAN bus, split the data into speed, current and duty cycle and store them in different buffers.
def read():
    while True:
        msg = message.bus.recv(0.0) #set waiting time [s]. If 0.0 non-blocking
        if msg:
            if len(message.data) > 50: # Set maximum buffer size
                message.clear()
            if msg.arbitration_id == 0x0F6:   # This is the ID of the Ardunio
                msg_hex = binascii.hexlify(msg.data).decode('ascii') #convert from bytearray to hex
                data = [int(msg_hex[0:8],16), int(msg_hex[8:12],16),int(msg_hex[12:16],16)]
                message.data.append(data) #Add the last reading to the buffer
                if message.data_queue: #Put the reading in the queue if recording
                    message.data_queue.put(data) 
 
# Set the ID of the message based on the type of command send. 
def command(data):
    for key in data.keys():        
        if key == 'speed':
            ID = 1
            send(ID, int(data[key])) 
        if key == 'current':
            ID = 2
            send(ID, int(data[key])) 
        if key == 'dutyCycle':
            ID = 3
            send(ID, int(data[key]))
        if key == 'LED':
            ID = 4
            send(ID, int(data[key]))

# initialize the CAN interface and start the background thread that listen on the bus.
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
