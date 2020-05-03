import socketio
import time

#Connect to Local server to retrieve data and send commands without using the web application

sio = socketio.Client()
LocalHost = "192.168.1.11:5500"

def connectToServer():
    try:
        sio.connect("http://" +LocalHost ,namespaces=['/sensors'])    
    except socketio.exceptions.ConnectionError:
        print("waiting for local server...")
        time.sleep(1)
        connectToServer()

@sio.event
def connect():
    print('Connection established')
    
@sio.event
def disconnect():
    print('Disconnected from server')
   
IMU_data = None
RazorIMU_data = None
LoadCell_data = None
CAN_data = None

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
# the values returned from the server are then given as arguments to the callback functions.
# getStream and getStreamLC act in the same way, but at different frequencies since the load cell
# is slower than the others sensors.
def getStream(ms=100):
    
    global IMU_data
    global RazorIMU_data
    global CAN_data
    
    print("STREAM STARTED")
    
    ms = ms/1000
    while True:
        sio.sleep(ms)
        sio.emit('getIMU_buffer','', namespace='/sensors',callback=IMUCallback)        
        sio.emit('getRazorIMU_buffer','', namespace='/sensors',callback=RazorIMUCallback)         
        sio.emit('getCAN_buffer','', namespace='/sensors',callback=CANCallback)

def getStreamLC(ms=1000):
    
    global LoadCell_data
    
    print("STREAM LC STARTED")
    
    ms = ms/1000
    while True:
        sio.sleep(ms)        
        sio.emit('getLoadCell_buffer','', namespace='/sensors',callback=LoadCellCallback)

    
if __name__ == "__main__":
    connectToServer()
    sio.start_background_task(getStream, ms=100)
    sio.start_background_task(getStreamLC, ms=1000)
     
    while True:
        print(LoadCell_data)
        time.sleep(1)