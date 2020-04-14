#!/usr/bin/env python3

""" IMU 1.2 """

HOST = "localhost"
PORT = 4223
UID = "5VHux5" # Unique ID of IMU Brick

import numpy as np
import os
import json
import time
from tinkerforge.ip_connection import IPConnection
from tinkerforge.brick_imu import BrickIMU

buffer  = np.zeros((1,6))

def IMU_reading():
    global buffer, trigger
    
    path = "../tests"
    file_j = "readings.json"

    ipcon = IPConnection() # Create IP connection object
    imu = BrickIMU(UID, ipcon) # Create device object
    ipcon.connect(HOST, PORT) # Connect to brickd
        # Don't use device before ipcon is connected
    print("Hey, IMU connected!")
    
    temp = np.zeros((1,6))
    
    while True:
        time.sleep(0.1)
        
        if buffer.shape[0] >= 51:
            clear_buffer()
            
        [x,y,z] = imu.get_acceleration()
        a = [x,y,z]
        [ax,ay,az] = imu.get_angular_velocity()
        v = [ax,ay,az]
        a.extend(v)
        a_np = np.array(a).reshape(1,6)
        temp = np.append(buffer,a_np,axis=0)
        buffer = temp
        
        #log data with json
        #data = {'Ax':x, 'Ay':y, 'Az':z, 'Vx':ax, 'Vy':ay, 'Vz':z} 
        #with open(os.path.join(path,file_j), 'a') as f:
            #json.dump(data,f)
        #print(a)
    
    print("Bye bye, IMU disconnected!")    
    ipcon.disconnect()  

def clear_buffer():
    global buffer
    buffer = np.zeros((1,6))

def get_buffer():
    global buffer
    tmp_buffer = np.copy(buffer)
    return tmp_buffer[1:][:]
