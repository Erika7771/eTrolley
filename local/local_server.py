import logging
import eventlet
import socketio
import json
import writeToCSV as CSV

#sensors
import IMU 
import Razor_IMU
import CAN

#My load cell has a broken wire, set the variable to False to read the true data
ignoreLoadCell = True 

if ignoreLoadCell:
    import LoadCellSimulate as LoadCell
else:
    import LoadCell
    

# logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s',)

s = None

sio = socketio.Server()
app = socketio.WSGIApp(sio)

recording = False

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)  
    
@sio.on('getIMU_buffer',namespace='/sensors')
def getIMU_buffer(sid,data):    
    raw_data = json.dumps(IMU.get_buffers())
    IMU.emptyBuffes()
    return raw_data

@sio.on('getRazorIMU_buffer',namespace='/sensors')
def getIMU_buffer(sid,data):
    raw_data = json.dumps(Razor_IMU.get_buffers())
    Razor_IMU.emptyBuffes()
    return raw_data

@sio.on('getLoadCell_buffer',namespace='/sensors')
def getLoadCell_buffer(sid,data):
    raw_data = json.dumps(LoadCell.get_buffer())   
    LoadCell.emptyBuffer()
    return raw_data

@sio.on('getCAN_buffer',namespace='/sensors')
def getCAN_buffer(sid,data):
    raw_data = json.dumps(CAN.get_buffer())   
    CAN.emptyBuffer()
    return raw_data
    
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
        
            

if __name__ == '__main__':
    
    ''' Sensors initialization '''
    IMU.IMU_init()
    Razor_IMU.init()
    CAN.init()
    LoadCell.init()
    
    print("starting Local server")
    eventlet.wsgi.server(eventlet.listen(('', 5500)), app)
        
    print("Something went wrong, local server is no longer running!")
        