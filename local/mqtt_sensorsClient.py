#----------------------------------------------------------------------------------
#MQTT client that manages the sensors and the motors.
#----------------------------------------------------------------------------------

import paho.mqtt.client as mqtt
import json
import writeToCSV as CSV
import time
import threading
import os.path
# Sensors
import IMU 
import Razor_IMU
import CAN

# My load cell has a broken wire, set the variable to False to read the true data
ignoreLoadCell = True 
if ignoreLoadCell:
    import LoadCellSimulate as LoadCell
else:
    import LoadCell    
    
    
hostName = "192.168.4.1"
recording = False

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode('utf-8')))
    print("message topic=",message.topic)
    print("message qos=",message.qos)

def getBuffers(sensorName):
    raw_data = json.dumps(sensorName.get_buffers())
    sensorName.emptyBuffes()
    return raw_data
    
def getBuffer(sensorName):
    raw_data = json.dumps(sensorName.get_buffer())
    sensorName.emptyBuffer()
    return raw_data

#Send commands to the motors over CAN bus
def sendCommands(message):
    msg = message.payload.decode('utf-8').replace("'", '"')
    msg = json.loads(msg)
    CAN.command(msg)

# Start and stop record of selected sensors    
def record(message):
    msg =  message.payload.decode()
    lst = msg.replace("[", "").replace("]", "").replace("'", "")
    lst = lst.split(', ')
    
    action = lst[0]
    sensors = lst[1:]
    
    if action == "start":
        if 'IMU_acc' in sensors:
            IMU.record('IMU_acc')
        if 'IMU_vel' in sensors:
            IMU.record('IMU_vel')
        if 'Razor_acc' in sensors:
            Razor_IMU.record('Razor_acc')
        if 'Razor_vel' in sensors:
            Razor_IMU.record('Razor_vel')
        if 'Load_Cell' in sensors:
            LoadCell.record()
        if 'CAN' in sensors:
            CAN.record()              
    elif action == "stop":
        if 'IMU_acc' in sensors:            
            IMU.record_stop('IMU_acc')
        if 'IMU_vel' in sensors:
            IMU.record_stop('IMU_vel')
        if 'Razor_acc' in sensors:
            Razor_IMU.record_stop('Razor_acc')
        if 'Razor_vel' in sensors:
            Razor_IMU.record_stop('Razor_vel')
        if 'Load_Cell' in sensors:
            LoadCell.record_stop()        
        if 'CAN' in sensors:
            CAN.record_stop()
        CSV.unifile(sensors)

def publish_data():
    while True:
        raw_data = getBuffers(IMU)
        msg = {'topic':'IMU_data', 'payload':raw_data}
        mqttClient.publish(msg['topic'], msg['payload'])
        raw_data = getBuffers(Razor_IMU)
        msg = {'topic':'RazorIMU_data', 'payload':raw_data}
        mqttClient.publish(msg['topic'], msg['payload'])
        raw_data = getBuffer(LoadCell)
        msg= {'topic':'LoadCell_data', 'payload':raw_data}
        mqttClient.publish(msg['topic'], msg['payload'])
        raw_data = getBuffer(CAN)
        msg = {'topic':'CAN_data', 'payload':raw_data}
        mqttClient.publish(msg['topic'], msg['payload'])
        time.sleep(0.1)

def on_record(client, userdata, message):
    record(message)

def on_motorsControl(client, userdata, message):
    sendCommands(message)
    
#chek if the connection to the broker completed successfully
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"({os.path.basename(__file__)}) Connection successfully established")      
    else:
        print(f"(Error value: {rc}). Connection refused")
    return    

# Start the sensors, connect to the broker, start background thread to publish the data and
# susbribe to the channels used to manage the recordings and the motors. 
if __name__ == '__main__':
    
    #Sensors initialization
    IMU.IMU_init()
    Razor_IMU.init()
    CAN.init()
    LoadCell.init()
    
    # Connect to mosquitto broker
    try:
        print(f"({os.path.basename(__file__)}) Connecting to mosquitto broker...")
        mqttClient = mqtt.Client("mqtt_sensors")        
        mqttClient.connect(hostName, 1883)
        mqttClient.on_connect = on_connect
        
    except ConnectionRefusedError:
        print(f"({os.path.basename(__file__)}) Connection refused")
    
    # message_callback_add(Topic, Function) executes Function when a new message is published
    # on Topic. on_message is called whenever a new message is published on the subscribed channels
    # for which no other callback function is defined.   
    mqttClient.on_message = on_message    
    mqttClient.message_callback_add("record", on_record)
    mqttClient.message_callback_add("motorsControl", on_motorsControl)
    
    # Start thread to constantly publish sensors data 
    thread = threading.Thread(target = publish_data, daemon=True)
    thread.start()
    
    # Subscribe to the topics used to manage the user inputs.
    mqttClient.subscribe("record")
    mqttClient.subscribe("motorsControl")
    
    #Keep the connection alive forever. Blocking
    mqttClient.loop_forever()
    
    #to stop the forever loop
#     mqttClient.disconnect()
    
