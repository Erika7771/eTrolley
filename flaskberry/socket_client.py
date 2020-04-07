import socket
import time
import numpy as np

host = socket.gethostname()  # get local machine name
port = 8080  # Make sure it's within the > 1024 $$ <65535 range

s = socket.socket()
s.connect((host, port))
    
def getData():
    message = "Hey, manda i nuovi dati"
    s.send(message.encode('utf-8'))
    data = s.recv(4096)  # read max 2048 bytes
    print('Received from server: \n')
    return np.loads(data)

def closeSocket():
    s.close()