import socket
import time
import os
import json

path = "../"
file_j = "tests/readingsClient.json"

def client():
    host = socket.gethostname()  # get local machine name
    port = 8080  # Make sure it's within the > 1024 $$ <65535 range

    s = socket.socket()
    s.connect((host, port))

#     message = input('-> ')
    message = "Hey, manda i nuovi dati"
    while message != 'q':
        s.send(message.encode('utf-8'))
        data = s.recv(1024).decode('utf-8')  # read max 1024 bytes
        print("data type: " +str(type(data)))
        print('Received from server: \n' +str(data))        
        time.sleep(1)
#         message = input('==> ')
    s.close()

if __name__ == '__main__':
    client()
