import json
import socket
import time
import numpy as np
import signal
import sys
#     
# def signal_handler(signal, frame):
#     sys.exit(0)
host = socket.gethostname()  # get local machine name
port = 8080  # Make sure it's within the > 1024 $$ <65535 range

   
    
def getData():
    
    s = socket.socket()
    s.connect((host, port)) 
#     global s
    message = "Hey, manda i nuovi dati"
    s.send(message.encode('utf-8'))
    data = s.recv(4096).decode('utf-8') # read max 2048 bytes .
    data_js= json.loads(data) 
#     print(f'Received from server json:{data_js}\n')
    print(type(data_js))    
    return data_js

def closeSocket():
    s.close()
 
if __name__ == "__main__":
#signal.signal(signal.SIGINT, signal_handler)
    while True:
        try:
            getData()
            time.sleep(1)
            
        except KeyboardInterrupt:
            sys.exit(0)