#---------------------------------------------------------------------
# web_sockets  is an extention of the flask application and acts as a
# bridge between the Flask server and the the mosquitto broker.
# Data recieved over websockets can be sent over MQTT and vice versa. 
#---------------------------------------------------------------------

from flask import  Blueprint, render_template
import time
import logging
import threading
import json
from flask_socketio import SocketIO, emit, disconnect
from flask_mqtt import Mqtt
from __main__ import websocketio, app

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
    
# Emit over websocket the sensors data. This function fires every time
# a new message is published on a topic.
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

# When the user clicks the button to start/stop recording, this function sends the message
# to the broker and informs the other clients whether someone is recording or not.
@websocketio.on('record', namespace='/sensors')
def record(data):
    global isRecording
    isRecording = not isRecording
    emit('busy',"",broadcast=True, include_self=False)
    mqtt.publish("record", str(data))

# Recieve the motor commands from the web page and publish them to the broker.
@websocketio.on('motorCommands', namespace="/sensors")
def sendCommands(data):
    mqtt.publish("motorsControl", str(data))

#Record latency    
@websocketio.on('my_ping', namespace='/sensors')
def ping_pong():
    emit('my_pong')

# Count the number of connected client and inform the new client whether
# someone is recording or not.
@websocketio.on('connect', namespace='/sensors')
def connect():
    global connectedWebClients    
    connectedWebClients += 1    
    emit('busy', {'isRecording': isRecording})


@websocketio.on('disconnect', namespace='/sensors')
def test_disconnect():
    global connectedWebClients
    connectedWebClients -= 1