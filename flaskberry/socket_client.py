import json
import socketio
import time
import numpy as np
import signal
import sys

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

@sio.event
def disconnect():
    print('disconnected from server')
    
@sio.on('my response')
def my_response(data):
    print('grazie per i dati ', data)

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
    
def getStream(ms=100):
    ms = ms/1000
    while True:
        print("mi daresti i dati pf?")
        sio.emit('my_message', {'dammi i dati': 'pf'},namespace='/sensors')
        sio.sleep(ms)
 
if __name__ == "__main__":
    try:
        sio.connect('http://localhost:5500',namespaces=['/sensors'])
        getStream(2000)
    except KeyboardInterrupt:
        sys.exit(0)
