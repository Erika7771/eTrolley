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

#listen on sensors channels and store readings in local variables 
@sio.on('sendIMU_buffer',namespace='/sensors')
def readData(data):
    global IMU_data
    IMU_data = data
#     print(f"data from sendIMU_buffer:  {data}")
    
@sio.on('sendRazorIMU_buffer',namespace='/sensors')
def readData(data):
    global RazorIMU_data
    RazorIMU_data = data
#     print(f"data from sendRazorIMU_buffer:  {data}")    
    
@sio.on('sendLC_buffer',namespace='/sensors')
def readData(data):
    global LoadCell_data
    LoadCell_data = data
#     print(f"data from sendLC_buffer:  {data}")

@sio.on('sendCAN_buffer',namespace='/sensors')
def readData(data):
    global CAN_data
    CAN_data = data
#     print(f"data from sendCAN_buffer:  {data}")
    
    
# send commands to the motors
def sendMotorsCommand(command):   #command: bytes, buffer or ASCII string 
    sio.emit('motorsControl',command,namespace='/sensors')   

if __name__ == "__main__":
    connectToServer()
     
    while True:
        sendMotorsCommand("start")
#         print(LoadCell_data)
        time.sleep(1)