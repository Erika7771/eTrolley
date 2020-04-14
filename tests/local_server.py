import logging
import socket
import provaIMU as IMU
import numpy as np
import sys
import json

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s',)

s = None

def server():        
    '''Start server '''
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
#     print("prova11")
    while True:
        mssg = c.recv(1024).decode('utf-8')
        if not mssg:
            s.close()
            logging.debug("No more messages")
            break
        print('From online user: ' + mssg)    
        
        raw_data = IMU.get_buffers()
        data_js = json.dumps(raw_data.__dict__)
        IMU.r.clear()
        
        c.send(data_js.encode('utf-8')) #send sensor data 
        print("Done!")

if __name__ == '__main__':
    
    ''' Start IMU reading '''
    IMU.IMU_init()    
    while True:
        try:
            server()
        except KeyboardInterrupt:
             s.close()
             IMU.disconnect()
             sys.exit(0)
        
    print("Something went wrong, local server is no longer running!")
        