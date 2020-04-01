import threading
import time
import json
import logging
import socket
import IMU_loop as IMU
import numpy as np

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s',)

def server():
    logging.debug('SERVER starting')
    host = socket.gethostname()   # get local machine name
    port = 8080  # Make sure it's within the > 1024 $$ <65535 range
    addr = str(host) + ":" + str(port)

    s = socket.socket()
    s.bind((host, port))

    s.listen(1)
    c, adress = s.accept()
    print("Connection from: " + str(addr))
    while True:
        mssg = c.recv(1024).decode('utf-8')
        if not mssg:
            break
#         e.set()
        print('From online user: ' + mssg)    
        
        raw_data = IMU.get_buffer()
        
        data = json.dumps(raw_data.tolist())
        
        IMU.buffer = np.zeros((1,6))
#         print("Sending data: " + str(data))
        c.send(str(data).encode("utf-8")) #send sensor data
        print("Done!")
#         e.clear()
    c.close()



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
    
    e = threading.Event()
    t1 = threading.Thread(name='blocking', 
                      target=funzione1,
                      args=(e,))
    t1.start()

    t2 = threading.Thread(name='non-blocking', 
                      target=funzione2, 
                      args=(e,))
    t2.start()
    
    #event_is_set = e.wait()
    #logging.debug('event set: %s', event_is_set)