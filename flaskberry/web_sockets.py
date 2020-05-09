from flask import  Blueprint, render_template
import socketio
import time
import logging
import threading
import json
from flask_socketio import SocketIO, emit, disconnect
from __main__ import websocketio, app

# web_sockets acts as a bridge between the web server and the local server.
# Data recieved over websockets can be sent over local sockets and vice versa. 

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
    
#The data sent from the local server on the different channels are stored in local variables     
@sio.on('sendIMU_buffer',namespace='/sensors')
def storeData(data):
    global IMU_data
    IMU_data = data
 
@sio.on('sendRazorIMU_buffer',namespace='/sensors')
def storeData(data):
    global RazorIMU_data
    RazorIMU_data = data 

@sio.on('sendLC_buffer',namespace='/sensors')
def storeData(data):
    global LoadCell_data
    LoadCell_data = data
    
@sio.on('sendCAN_buffer',namespace='/sensors')
def storeData(data):
    global CAN_data
    CAN_data = data

####### WEB SOCKETS #######

thread = None
threadLC = None
stop_threads = False
connectedWebClients = 0
isRecording = False

# Each "ms" milliseconds, sendStream emits the sensors data over websockets.
# getStream and getStreamLC act in the same way, but at different frequencies since the load cell
# is slower than the others sensors.

def sendStream(ms=100):
    global stop_threads
    global IMU_data
    global RazorIMU_data
    global CAN_data
    
    print("STREAM PROVA STARTED")
    
    ms = ms/1000
    start = time.time()
    while True:
        websocketio.sleep(ms)
        websocketio.emit('IMU_data',IMU_data,namespace='/sensors')
        websocketio.emit('RazorIMU_data',RazorIMU_data,namespace='/sensors')
        websocketio.emit('CAN_data',CAN_data,namespace='/sensors')        
        websocketio.emit('LoadCell_data',LoadCell_data,namespace='/sensors')
        
        if stop_threads:
                break    


# def getLC(ms=100):
#     global stop_threads
#     global LoadCell_data
#     
#     print("STREAM LC STARTED")
#     
#     ms = ms/1000
#     while True:
#         websocketio.sleep(ms)        
#         sio.emit('getLoadCell_buffer','', namespace='/sensors',callback=LoadCellCallback)
#         websocketio.emit('LoadCell_data',LoadCell_data,namespace='/sensors')
#         
#         if stop_threads:
#             break 
#   
@bp.route('/')
def index():
    """Serve the index HTML"""
    return render_template('EtestSocket.html', async_mode=websocketio.async_mode)


def bridgeWebLocal(channel,msg=""):
    sio.emit(channel,msg,namespace='/sensors')


#Define channels to listen on and functions to execute each time a new message arrives.    
@websocketio.on('record', namespace='/sensors')
def record(data):
    global isRecording
    isRecording = not isRecording
    emit('busy',"",broadcast=True, include_self=False)
    bridgeWebLocal('record',data)    

# Recieve motor commands from the web page and send them to the local server. 
@websocketio.on('motorCommands', namespace="/sensors")
def sendCommands(data):
    bridgeWebLocal('motorsControl',data)

#Record latency    
@websocketio.on('my_ping', namespace='/sensors')
def ping_pong():
    emit('my_pong')

# @websocketio.on('my_event', namespace='/sensors')
# def ping_pong(message):
#     print(message)

#starts the background tasks as soon as someone connects to the web application
@websocketio.on('connect', namespace='/sensors')
def connect():
    global connectedWebClients
    global thread
    global threadLC
    global stop_threads
    
    connectedWebClients += 1    
    stop_threads = False
    
    if thread is None: 
        thread = websocketio.start_background_task(sendStream,ms=100)     
#         threadLC = websocketio.start_background_task(getLC,ms=100)
    emit('busy', {'isRecording': isRecording})
    

@websocketio.on('disconnect', namespace='/sensors')
def test_disconnect():
    global stop_threads    
    global connectedWebClients
    global thread
    global threadLC
    
    connectedWebClients -= 1
    if connectedWebClients < 1:
        stop_threads = True
        thread = None
        threadLC = None
