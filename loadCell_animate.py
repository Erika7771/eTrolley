#!/usr/bin/python3
from hx711 import HX711
import RPi.GPIO as GPIO
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import logging

GPIO.setwarnings(False)
# logging.basicConfig(level=logging.DEBUG)

#Set VDD pin to 3.3V 
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, True)

hx711 = HX711(dout_pin=5, pd_sck_pin=6, channel='A', gain=128)
hx711.reset()

x_len = 200
y_range = [-100000, 100000]
x = np.arange(x_len)

read = np.zeros((1,x_len))

fig = plt.figure()

ax1 = fig.add_subplot(1,1,1)
line, = ax1.plot(x,read[0])
plt.title('Load Cell ')
plt.xlabel('Samples')
plt.ylabel('Values')

ax1.set_ylim(y_range)

def animate(i,read):
    measures = hx711.get_raw_data(times=2)
    meas = np.array(measures)
    temp = np.append(read[0],meas-2*63227)
    read[0] = temp[-x_len:]

    
    line.set_ydata(read[0])
        
    return line,

ani = animation.FuncAnimation(fig, animate,fargs=(read,), interval=30, blit=True)

plt.show() 

