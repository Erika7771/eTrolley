#----------------------------------------------------------------------------------
# Example of how to connect to the mosquitto broker without running the Flask server.
#----------------------------------------------------------------------------------
import paho.mqtt.client as mqtt
import os
import json

hostName = "192.168.4.1"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"({os.path.basename(__file__)}) Connection successfully established")      
    else:
        print(f"(Error value: {rc}). Connection refused")
    return    

# When a new message is published on a subscribed topic, on_message is executed
# unless another function is defined for that specific topic.
def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode('utf-8')))
    print("message topic=",message.topic)
    print("message qos=",message.qos)

# Set as callback function for the topic "IMU_data". It is executed instead of
# on_message
def on_IMU_data(client, userdata, message):
    #Convert string message to dictionary 
    IMU_data =json.loads(message.payload)
    print(type(IMU_data))
    

if __name__ == "__main__":
    try:
        print(f"({os.path.basename(__file__)}) Connecting to mosquitto broker...")
        mqttClient = mqtt.Client("mqttClient")        
        mqttClient.connect(hostName, 1883)
        mqttClient.on_connect = on_connect
        
    except ConnectionRefusedError:
        print(f"({os.path.basename(__file__)}) Connection refused")
    
    #Subscribe to sensors topics
    mqttClient.subscribe("IMU_data")
    mqttClient.subscribe("RazorIMU_data")
    mqttClient.subscribe("CAN_data")
    mqttClient.subscribe("LoadCell_data") 
     
    # Set callback functions
    mqttClient.on_message = on_message    
    mqttClient.message_callback_add("IMU_data", on_IMU_data)
    
    #Keep the connection alive forever.
    mqttClient.loop_forever()
    
    #to stop the forever loop
#     mqttClient.disconnect()