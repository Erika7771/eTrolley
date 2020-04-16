""" SparkFun Razor 9 Dof"""

from FaBo9AXISMPU9250Python import FaBo9Axis_MPU9250 
from datetime import datetime
import threading, time
import sys
import numpy as np

class Reading:    
    def __init__(self):
        self.buff_acc = []
        self.buff_vel = [] 
    
    def clear(self):
        self.buff_acc.clear()
        self.buff_vel.clear()        

r = Reading()
Razor_IMU = FaBo9Axis_MPU9250.MPU9250()



def read():  
  while True: # ~2ms per loop
    if len(r.buff_vel) > 50 or len(r.buff_acc) > 50:
        r.clear()
    data_acc = Razor_IMU.readAccel()       
    data_vel = Razor_IMU.readGyro()
    r.buff_acc.append(list(data_acc.values()))
    r.buff_vel.append(list(data_vel.values()))
    time.sleep(0.008)     
      
def get_buffers():
    return r

# Start background process 
t_read = threading.Thread(target=read)
# t_read.daemon = True
t_read.start()

# 
# def Razor_IMU_init():
    

# sif __name__ == "__main__":
# try:        
#     
#     #Razor_IMU_init()       
#     while True:
#         data = get_buffers()
#         print(f"size of buff_vel: {len(data.buff_vel)}")
#         print(" ay = " , ( accel['y'] ))
#         print(" az = " , ( accel['z'] ))

        
#         print(" gx = " , ( gyro['x'] ))
#         print(" gy = " , ( gyro['y'] ))
#         print(" gz = " , ( gyro['z'] ))

#         mag = mpu9250.readMagnet()
#         print(" mx = " , ( mag['x'] ))
#         print(" my = " , ( mag['y'] ))
#         print(" mz = " , ( mag['z'] ))
#         print("Hola")

#         time.sleep(1)

# except KeyboardInterrupt:
#     sys.exit()
