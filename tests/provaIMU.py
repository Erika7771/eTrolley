#!/usr/bin/env python3

""" IMU 1.2 """

HOST = "localhost"
PORT = 4223
UID = "5VHux5" # Unique ID of IMU Brick

import time
from tinkerforge.ip_connection import IPConnection
from tinkerforge.brick_imu import BrickIMU

class Reading:    
    def __init__(self):
        self.buff_acc = []
        self.buff_vel = [] 
    
    def clear(self):
        self.buff_acc.clear()
        self.buff_vel.clear()        

r = Reading()
ipcon = None

def cb_acceleration(x,y,z):    
    if len(r.buff_vel) > 50 or len(r.buff_acc) > 50:
            r.clear()       
    r.buff_acc.append([x,y,z])
    
def cb_angular_velocity(x,y,z):   
    r.buff_vel.append([x,y,z])
    
def IMU_init():
    global ipcon
    period = 10 #ms
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
    return r
    
def disconnect():
    global ipcon
    ipcon.disconnect()