import logging
import eventlet
import socketio
import json
import writeToCSV as CSV
import time
import threading

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

# logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s',)

s = None

# Create local server instance
sio = socketio.Server()
app = socketio.WSGIApp(sio)

recording = False
connectedClients = 0

@sio.event
def connect(sid, environ):
    global connectedClients
    connectedClients += 1      
    print('connected ', sid)

@sio.event
def disconnect(sid):
    global connectedClients
    connectedClients -= 1
    print('disconnect ', sid)  
    
# Start and stop record of selected sensors    
@sio.on('record',namespace='/sensors')
def record(sid,data):
    action = data[0]
    sensors = data[1]
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
 
@sio.on('motorsControl',namespace='/sensors')
def sendCommands(sid,data):
    CAN.command(data)

def getBuffers(sensorName):
    raw_data = json.dumps(sensorName.get_buffers())
    sensorName.emptyBuffes()
    return raw_data
    
def getBuffer(sensorName):
    raw_data = json.dumps(sensorName.get_buffer())
    sensorName.emptyBuffer()
    return raw_data

# Emit sensors data on corresponding channels each "ms" milliseconds.
# This function acts as a python thread. 
def startStream(ms=100):    
    ms = ms/1000
    while True:
        sio.sleep(ms)
        raw_data = getBuffers(IMU)
        sio.emit('sendIMU_buffer',raw_data, namespace='/sensors')
        
        raw_data = getBuffers(Razor_IMU)
        sio.emit('sendRazorIMU_buffer',raw_data, namespace='/sensors')
        
        raw_data = getBuffer(LoadCell)
        sio.emit('sendLC_buffer',raw_data, namespace='/sensors')
        
        raw_data = getBuffer(CAN)
        sio.emit('sendCAN_buffer',raw_data, namespace='/sensors')

if __name__ == '__main__':
    ''' Sensors initialization '''
    IMU.IMU_init()
    Razor_IMU.init()
    CAN.init()
    LoadCell.init()
    
    #start the background thread
    thread = sio.start_background_task(startStream,ms=100)   
    
    print("starting Local server")
    eventlet.wsgi.server(eventlet.listen(('', 5500)), app)    
        
    print("Something went wrong, local server is no longer running!")
        