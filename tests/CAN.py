import time
import can
import threading
import writeToCSV as CSV

bus = None
csvfile = None
times = 5 #number of messages to send


#read all the messages on CAN bus
def read():
    global bus
    while True:
        message = bus.recv(0.0) #set waiting time [s]. If 0.0 non-blocking
#         if message:
#             print(message)            


#send messages on the CAN bus
def send(times = 5):
    global bus
    for i in range(times):
        msg = can.Message(arbitration_id=0xAA, data=[ i, 0, 1, 3, 1, 4, 1], is_extended_id=False)
#        msg = can.Message(arbitration_id=0xc0ffee, data=b'message', is_extended_id=False)
        bus.send(msg)
#     print(msg)


def read():
    global bus
    while True:
        message = bus.recv(0.0) #set waiting time [s]. If 0.0 non-blocking
        if csvfile and message:
            print(f"suka: {message}")
            CSV.write_file(csvfile, 'CAN', message.data)        
#         if message:
#             print(message.data)

def init():
    global bus
    bustype = 'socketcan'
    channel = 'can0'
    bus = can.interface.Bus(channel=channel, bustype=bustype,receive_own_messages=False)   
    print("Hey, CAN connected!")
    t_read = threading.Thread(target=read)
    # t_read.daemon = True
    t_read.start()
    t_write = threading.Thread(target=send)
    # t_read.daemon = True
    t_write.start()

 
def record():
    global csvfile    
    csvfile = CSV.create_file('CAN')
        
def record_stop():
    global csvfile
    csvfile = None            

if __name__ == "__main__":
    
    while True:
        send(times)