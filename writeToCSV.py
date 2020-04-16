#!/usr/bin/env python3

""" IMU 1.2 """

HOST = "localhost"
PORT = 4223
UID = "5VHux5" # Unique ID of IMU Brick

from tinkerforge.ip_connection import IPConnection
from tinkerforge.brick_imu import BrickIMU
#import time
import os
import csv
#import numpy as np
#import matplotlib.pyplot as plt

def save_file(file_name):
    size = input('Insert number of measurements to take: ')

    while not size.isdigit():
        print("Expected a number! ")
        size = input("Try again: ")
       
    size = int(size)   
    count = 0

    #create a new file
    file_name = (file_name or "Accelerometer.csv")
  
    if os.path.exists(file_name):
        os.remove(file_name)
        
#     csvfile = "Accelerometer.csv"
    csvfile = file_name
    with open(file_name, "a")as output:
        writer = csv.writer(output, delimiter=",", lineterminator = '\n')
        writer.writerow(['step','acc_x','acc_y','acc_z', 'vel_x','vel_y', 'vel_z'])

    while count < size:

        data = [count]
        [x,y,z] = imu.get_acceleration
        a = [x,y,z]
        [ax,ay,az] = imu.get_angular_velocity()
        v = [ax,ay,az]
        a.extend(v)
        data.extend(a)
        
        with open(csvfile, "a")as output:
            writer = csv.writer(output, delimiter=",", lineterminator = '\n')
            writer.writerow(data)
             
        count +=1
    print("done!")     
    

ipcon = IPConnection() # Create IP connection object
imu = BrickIMU(UID, ipcon) # Create device object
ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected 

save_file(file_name = input("Write the name of the file (default: Accelerometer.csv): "))

ipcon.disconnect()  
   

""" Data plot """
# step = np.linspace(1,size,size,dtype = np.int32)
# plt.plot(step,acc_arr[:,0],label='x acceleration')
# plt.plot(step,acc_arr[:,1],label='y acceleration')
# plt.plot(step,acc_arr[:,2],label='z acceleration')
# plt.legend(loc='best')
# plt.show()

