import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from tinkerforge.ip_connection import IPConnection
from tinkerforge.brick_imu import BrickIMU
import FaBo9Axis_MPU9250

#Live plots of Tinkerforge and Sparkfun IMU readings using matplotlib

#Tinkerforge IMU initialization 
HOST = "localhost"
PORT = 4223
UID = "5VHux5" # Unique ID of IMU Brick

ipcon = IPConnection() # Create IP connection object
imu = BrickIMU(UID, ipcon) # Create device object
ipcon.connect(HOST, PORT) # Connect to brickd

# Sparkfun IMU initialization
mpu9250 = FaBo9Axis_MPU9250.MPU9250()

x_len = 200
y_range_IMU = [-1500, 1500]
y_range_SF = [-250, 250]
x = np.arange(x_len)

#IMU readings
acc = np.zeros((3,x_len),dtype = int)
vel = np.zeros((3,x_len),dtype = int)

#SparkFun readins
gyro = np.zeros((3,x_len))
accel = np.zeros((3,x_len))


#Figure for IMU
fig = plt.figure()

ax1 = fig.add_subplot(2,1,1)
line1x,line1y,line1z, = ax1.plot(x, acc[0], x, acc[1], x, acc[2])
plt.title('IMU 1.2 ')
plt.xlabel('Samples')
plt.ylabel('Acceleration')
plt.legend(['acc_x','acc_y','acc_z'])

ax2 = fig.add_subplot(2,1,2)
line2x,line2y,line2z,  = ax2.plot(x, vel[0], x, vel[1], x, vel[2])
plt.xlabel('Samples')
plt.ylabel('Angular velocity')
plt.legend(['vel_x','vel_y','vel_z'])

#Figure for SparkFun
fig2 = plt.figure()

ax3 = fig2.add_subplot(2,1,1)
l1x,l1y,l1z, = ax3.plot(x, accel[0], x, accel[1], x, accel[2])
plt.title('SparkFun')
plt.xlabel('Samples')
plt.ylabel('Acceleration')
plt.legend(['acc_x','acc_y','acc_z'])

ax4 = fig2.add_subplot(2,1,2)
l2x,l2y,l2z,  = ax4.plot(x, gyro[0], x, gyro[1], x, gyro[2])
plt.xlabel('Samples')
plt.ylabel('Angular velocity')
plt.legend(['vel_x','vel_y','vel_z'])

line = [line1x,line1y,line1z,line2x,line2y,line2z,l1x,l1y,l1z,l2x,l2y,l2z,]

for ax in [ax1, ax2, ax3]:
    ax.set_ylim(y_range_IMU)
    
for ax in [ax4]:   
    ax.set_ylim(y_range_SF)
    
def animate(i,acc,vel, accel, gyro):
    [x,y,z] = imu.get_acceleration()
    [xv,yv,zv] = imu.get_angular_velocity()
    ac = mpu9250.readAccel()
    gy = mpu9250.readGyro()
    np_data = np.array(list(ac.values()))
    np_gyro = np.array(list(gy.values()))
    a = np.array([x,y,z])
    v = np.array([xv,yv,zv])
    
    for j in range(0,3):
        temp1 = np.append(acc[j],a[j])
        acc[j] = temp1[-x_len:]
        
        temp2 = np.append(vel[j],v[j])
        vel[j] = temp2[-x_len:]
        
        temp3 = np.append(accel[j],1000*np_data[j])
        accel[j] = temp3[-x_len:]
        temp4 = np.append(gyro[j],np_gyro[j])
        gyro[j] = temp4[-x_len:]
        
        line[j].set_ydata(acc[j])
        line[j+3].set_ydata(vel[j])
        line[j+6].set_ydata(accel[j])
        line[j+9].set_ydata(gyro[j])
        
    return l1x,l1y,l1z,l2x,l2y,l2z,line1x,line1y,line1z,line2x,line2y,line2z,

ani = animation.FuncAnimation(fig, animate,fargs=(acc,vel,accel,gyro, ), interval=40, blit=True)

plt.show() 

# ipcon.disconnect() 