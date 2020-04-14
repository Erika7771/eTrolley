import logging
import eventlet
import socketio
import provaIMU as IMU
import numpy as np
import sys
import json

#logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s',)

s = None

sio = socketio.Server()
app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

@sio.on('my_message',namespace='/sensors')
def my_message(sid,data):
    print("HO RICEVUTO+++++")
    sio.emit('my response',{'dati':'sensore'},namespace='/sensors')
    
@sio.on('getIMU_buffer',namespace='/sensors')
def getIMU_buffer(sid):
    raw_data = json.dumps(IMU.get_buffers().__dict__)
    IMU.r.clear()
    sio.emit('receiveIMU_buffer',raw_data,namespace='/sensors')

if __name__ == '__main__':
    
    ''' Start IMU reading '''
    IMU.IMU_init()
    
    # starting IMU server
    print("starting IMU server")
    eventlet.wsgi.server(eventlet.listen(('', 5500)), app)
        
    print("Something went wrong, local server is no longer running!")
        