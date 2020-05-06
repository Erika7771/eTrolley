from tinkerforge.ip_connection import IPConnection
from tinkerforge.brick_imu import BrickIMU
from utils import Reading_IMU

r = Reading_IMU()    
ipcon = None

def cb_acceleration(x,y,z):               
    if len(r.buff_vel) > 50 or len(r.buff_acc) > 50:
            r.clear()       
    r.buff_acc.append([x,y,z])
    if r.data_queue_acc:
        r.data_queue_acc.put([x,y,z])
    
    
def cb_angular_velocity(x,y,z):    
    r.buff_vel.append([x,y,z])
    if r.data_queue_vel:
        r.data_queue_vel.put([x,y,z])
           
def IMU_init():
    global ipcon
    
    HOST = "localhost"
    PORT = 4223
    UID = "5VHux5" # Unique ID of IMU Brick
    
    period = 7 #ms
    ipcon = IPConnection() # Create IP connection object
    imu = BrickIMU(UID, ipcon) # Create device object
    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected
    print("Hey, IMU connected!")
    
    imu.register_callback(imu.CALLBACK_ACCELERATION, cb_acceleration)
    imu.register_callback(imu.CALLBACK_ANGULAR_VELOCITY, cb_angular_velocity)
    imu.set_acceleration_period(period) # 0- 2³²-1
    imu.set_angular_velocity_period(period)
    
def get_buffers():
    return r.getBuffers()

def emptyBuffes():
    r.clear()

def record(sensor):
        dataType = 'acc' if sensor=='IMU_acc' else  'vel'
        r.record(sensorName=sensor, dataType=dataType)
    
def record_stop(sensor):
     dataType = 'acc' if sensor=='IMU_acc' else  'vel'
     r.record_stop(dataType=dataType)
    
def disconnect():
    global ipcon
    ipcon.disconnect()