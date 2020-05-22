from flask import  Blueprint, render_template
import time
import logging
import threading
import json
from flask_socketio import SocketIO, emit, disconnect
from flask_mqtt import Mqtt
from __main__ import websocketio, app

# web_sockets acts as a bridge between the web server and the the mosquitto broker.
# Data recieved over websockets can be sent over MQTT and vice versa. 

# logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s',)

bp = Blueprint('web_sockets', __name__)

####### MQTT settings #######
hostName = "192.168.4.1"

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = hostName
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False

#Connect to mosquitto broker
mqtt = Mqtt(app)

# Subscribe to sensors topics
mqtt.subscribe("record")
mqtt.subscribe("IMU_data")
mqtt.subscribe("RazorIMU_data")
mqtt.subscribe("CAN_data")
mqtt.subscribe("LoadCell_data")
    
# Emit over websocket the sensors data 
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    msg = json.loads(message.payload)
    msg = json.dumps(msg)
    websocketio.emit(message.topic,msg, namespace='/sensors')


####### WEB SOCKETS #######
    
connectedWebClients = 0
isRecording = False

@bp.route('/')
def index():
    """Serve the index HTML"""
    return render_template('EtestSocket.html', async_mode=websocketio.async_mode)

#Define channels to listen on and functions to execute each time a new message arrives.    
@websocketio.on('record', namespace='/sensors')
def record(data):
    global isRecording
    isRecording = not isRecording
    emit('busy',"",broadcast=True, include_self=False)
    mqtt.publish("record", str(data))

# Recieve motor commands from the web page and publish them to the broker.
@websocketio.on('motorCommands', namespace="/sensors")
def sendCommands(data):
    mqtt.publish("motorsControl", str(data))

#Record latency    
@websocketio.on('my_ping', namespace='/sensors')
def ping_pong():
    emit('my_pong')

#Count number of connected client and send the recording status 
@websocketio.on('connect', namespace='/sensors')
def connect():
    global connectedWebClients    
    connectedWebClients += 1    
    emit('busy', {'isRecording': isRecording})


@websocketio.on('disconnect', namespace='/sensors')
def test_disconnect():
    global connectedWebClients
    connectedWebClients -= 1