import threading
import time
import pickle
import logging
import socket
import IMU_loop as IMU
import numpy as np
import signal
import sys

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s',)

s = None

def signal_handler(signal, frame):
    global s
    logging.debug("closing socket server")
    s.close()
    sys.exit(0)

def server():
    global s
    logging.debug('SERVER starting')
    host = socket.gethostname()   # get local socket address
    port = 8080  # Make sure it's within the > 1024 $$ <65535 range
    addr = str(host) + ":" + str(port) 

    s = socket.socket() #BSD socket,  type=SOCK_STREAM, AF_INET address family
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))    
    
    s.listen(1) #nb of connection requests
    c, adress = s.accept()
    print("Connection from: " + str(addr))
    while True:
        mssg = c.recv(1024).decode('utf-8')
        if not mssg:
            s.close()
            logging.debug("No more messages")
            break
#         e.set()
        print('From online user: ' + mssg)    
        
        raw_data = IMU.get_buffer()        
        data = raw_data.dumps()        
        IMU.buffer = np.zeros((1,6))
#         print("Sending data: " + str(data))
        c.send(data) #send sensor data
        print("Done!")
#         e.clear()      
    

   


def funzione1(e):
    logging.debug('funzione 1 starting')
    server()
    #e.set()
    #logging.debug('Event is set')

def funzione2(e):
    logging.debug('funzione 2 starting')
    while not e.isSet():
        #event_is_set = e.wait(t)
        time.sleep(1)
        IMU.IMU_reading()
#         print("IMU.buffer: " + str(IMU.buffer))
        print("ciao da 2 ")

if __name__ == '__main__':   

    signal.signal(signal.SIGINT, signal_handler)
    e = threading.Event()
    
    t1 = threading.Thread(name='blocking', target=funzione1, args=(e,))
    t1.start()

    t2 = threading.Thread(name='non-blocking', target=funzione2, args=(e,))
    t2.start()
    #event_is_set = e.wait()
    #logging.debug('event set: %s', event_is_set)