from flask import (
    Blueprint, render_template, session, copy_current_request_context, request
)
import socketio
import time
import logging
import pickle
import threading
import json
from threading import Lock
from flask_socketio import SocketIO, emit, disconnect
from __main__ import websocketio, app

# web_sockets acts as a bridge between the web server and the local server.
# Data recieved over websocket can be sent over local sockets and vice versa. 

#logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s',)

bp = Blueprint('web_sockets', __name__)

IMU_data = None
RazorIMU_data = None
LoadCell_data = None
CAN_data = None
####### LOCAL SOCKETS #######

#Connect to the local server as client
sio = socketio.Client() 

def connectToServer():
    try:
        sio.connect('http://localhost:5500',namespaces=['/sensors'])    
    except socketio.exceptions.ConnectionError:
        print("Flask: waiting for local server...")
        time.sleep(1)
        connectToServer()

connectToServer()

@sio.event
def connect():
    print('Connection established')

@sio.event
def disconnect():
    print('Disconnected from server')    


####### WEB SOCKETS #######

thread = None
thread_LC = None
thread_lock = Lock()

connectedWebClients = 0
    
#callback functions: they recieve the sensors readings and store them.    
def IMUCallback(data):
    global IMU_data
    IMU_data = data

def RazorIMUCallback(data):
    global RazorIMU_data
    RazorIMU_data = data
    
def LoadCellCallback(data):
    global LoadCell_data
    LoadCell_data = data
        
def CANCallback(data):
    global CAN_data
    CAN_data = data        

# Each "ms" milliseconds, this function sends a request to the local server on different channels.
# The readings returned from the server are then given as arguments to the callback functions.
# Finally, these readings are sent to the web application over websockets.
# getStream and getStreamLC act in the same way, but at different frequencies since the load cell
# is slower than the others sensors.
def getStream(ms=100):
    
    global IMU_data
    global RazorIMU_data
    global CAN_data
    
    print("STREAM STARTED")
    
    ms = ms/1000
    while True:
        websocketio.sleep(ms)
        sio.emit('getIMU_buffer','', namespace='/sensors',callback=IMUCallback)
        websocketio.emit('IMU_data',IMU_data,namespace='/sensors')
        
        sio.emit('getRazorIMU_buffer','', namespace='/sensors',callback=RazorIMUCallback)
        websocketio.emit('RazorIMU_data',RazorIMU_data,namespace='/sensors')
        
        sio.emit('getCAN_buffer','', namespace='/sensors',callback=CANCallback)
        websocketio.emit('CAN_data',CAN_data,namespace='/sensors')   
      

def getLC(ms=100):
    
    global LoadCell_data
    
    print("STREAM LC STARTED")
    
    ms = ms/1000
    while True:
        websocketio.sleep(ms)        
        sio.emit('getLoadCell_buffer','', namespace='/sensors',callback=LoadCellCallback)
        websocketio.emit('LoadCell_data',LoadCell_data,namespace='/sensors')
        
@bp.route('/')
def index():
    """Serve the index HTML"""
    return render_template('EtestSocket.html', async_mode=websocketio.async_mode)

def bridgeWebLocal(channel,msg):
    sio.emit(channel,msg,namespace='/sensors')

isRecording = False

#Define channels to listen on and functions to execute each time a new message arrives.
@websocketio.on('record', namespace='/sensors',)
def record(data):
    global isRecording
    isRecording = not isRecording
    emit('busy',"",broadcast=True, include_self=False)
    bridgeWebLocal('record',data)    
    
#Record latency    
@websocketio.on('my_ping', namespace='/sensors')
def ping_pong():
    emit('my_pong')

@websocketio.on('my_event', namespace='/sensors')
def ping_pong(message):
    print(message)

#starts the background tasks as soon as someone connects to the web application
@websocketio.on('connect', namespace='/sensors')
def connect():
    global connectedWebClients
    connectedWebClients += 1    
    
    global thread
    global threadLC
    global thread_lock
    
    with thread_lock:
        if thread is None:
            thread = websocketio.start_background_task(getStream,ms=100)            
            threadLC = websocketio.start_background_task(getLC,ms=100) 
    emit('busy', {'isRecording': isRecording})
    

@websocketio.on('disconnect', namespace='/sensors')
def test_disconnect():
    global connectedWebClients
    connectedWebClients -= 1
