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
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from __main__ import websocketio, app


bp = Blueprint('web_sockets', __name__)

def webBridge(channel,data,namespace):
    print("bridge")
    websocketio.emit(channel,data,namespace=namespace)

####### LOCAL SOCKETS #######

sio = socketio.Client()
sio.connect('http://localhost:5500',namespaces=['/sensors'])

@sio.event
def connect():
    print('connection established')

@sio.event
def disconnect():
    print('disconnected from server')
    
@sio.on('my response')
def my_response(sid,data):
    print('grazie per i dati ', data)
    
@sio.on("receiveIMU_buffer",namespace='/sensors')
def receiveIMU_buffer(data):
    print("RECEIVED DATA")
    webBridge('IMU_data',data,'/sensors')
    



####### WEB SOCKETS #######

thread = None
thread_lock = Lock()

connectedWebClients = 0

def getStream(ms=100):
    
    print("STREAM STARTED")
    
    ms = ms/1000
    while True:
        websocketio.sleep(ms)
        sio.emit('getIMU_buffer', namespace='/sensors')


@bp.route('/')
def index():
    """Serve the index HTML"""
    #return render_template('index.html')
    return render_template('EtestSocket.html', async_mode=websocketio.async_mode)


@websocketio.on('my_broadcast_event', namespace='/sensors')
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@websocketio.on('disconnect_request', namespace='/sensors')
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session['receive_count'] = session.get('receive_count', 0) + 1
    # for this emit we use a callback function
    # when the callback function is invoked we know that the message has been
    # received and it is safe to disconnect
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']},
         callback=can_disconnect)

@websocketio.on('my_ping', namespace='/sensors')
def ping_pong():
    emit('my_pong')

@websocketio.on('my_event', namespace='/sensors')
def ping_pong(message):
    print(message)
    
@websocketio.on('connect', namespace='/sensors')
def connect():
    
    global connectedWebClients
    connectedWebClients += 1
    
    global thread
    with thread_lock:
        if thread is None:
            thread = websocketio.start_background_task(getStream,ms=2000)
    emit('my_response', {'data': 'connected from chart eheh'})    


@websocketio.on('disconnect', namespace='/sensors')
def test_disconnect():
    print('Client disconnected', request.sid)
