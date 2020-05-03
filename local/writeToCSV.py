import os
import glob
import csv
import time
import os.path
from pathlib import Path
from datetime import datetime
import numpy as np

my_path = Path(__file__).resolve().parents[1]

def create_file(sensor):
    global my_path
    
    path = str(my_path) + f"/flaskberry/static/recordings/{sensor}/"
    list_of_files = glob.glob(f'{path}*')
    for file in list_of_files:
        os.remove(file)
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")    
    
    file_name = (path + timestamp + "_" + sensor   + ".csv")
    csvfile = file_name
    
    with open(csvfile, "a") as output:
        writer = csv.writer(output, delimiter=",", lineterminator = '\n')
        
        if sensor == "IMU_acc":  
            writer.writerow(['timestamp','IMU_acc_x','IMU_acc_y','IMU_acc_z'])
        elif sensor == "Razor_acc":
            writer.writerow(['timestamp','Razor_acc_x','Razor_acc_y','Razor_acc_z'])
        elif sensor == "IMU_vel":
            writer.writerow(['timestamp','IMU_vel_x','IMU_vel_y','IMU_vel_z'])
        elif sensor == "Razor_vel":   
            writer.writerow(['timestamp','Razor_vel_x','Razor_vel_y','Razor_vel_z'])
        elif sensor == "CAN":
            writer.writerow(['timestamp','speed','current','duty_cycle'])  
        else:
            writer.writerow(['timestamp','LC_data'])  
    
    return csvfile

def write_file(csvfile, sensor, data_queue, STOP_TOKEN):
    with open(csvfile, "a")as output:
        writer = csv.writer(output, delimiter=",", lineterminator = '\n')
        start_time = datetime.now()
        while True:
            line = data_queue.get()
            if line == STOP_TOKEN:
                return            
            writer.writerow([datetime.now()-start_time]+list(line))
                                            
            
def unifile(sensors):
    global my_path
    
    if "all" in sensors:
        sensors.remove("all")        
    
    files = []
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    
    list_of_files = glob.glob(f'{my_path}/flaskberry/static/recordings/*.csv')
    for file in list_of_files:
        os.remove(file)
    
    finalUniFile = str(my_path) + f"/flaskberry/static/recordings/"+ timestamp + ".csv"
    newData = np.array([])
    maxLength = 0
    idLongest = None
    
    for sensor in sensors:        
        path = str(my_path) + f"/flaskberry/static/recordings/{sensor}/"
        list_of_files = glob.glob(f'{path}*.csv')
        if len(list_of_files)<1:
            return None
        latest_file = max(list_of_files, key=os.path.getctime)
        files.append(latest_file)
        with open(latest_file) as latest_file:
            fileObject = csv.reader(latest_file,delimiter=',')
            row_count = 0
            timeCol = []
            for row in fileObject:
                row_count += 1
                timeCol.append(row[0])
            
            if row_count > maxLength:
                newData = np.array([timeCol]).T
                maxLength = row_count
                    
    for file in files:
        oldData = []
        with open(file) as file:  
            reader = csv.reader(file,delimiter=',')
            for row in reader:
                oldData.append(row[1:])
             
        oldData = np.array(oldData)
        header = np.array(oldData[0,:])
        stretchedData = [stretchList(oldData[1:,j],maxLength-1) for j in range(len(oldData[0]))]
        stretchedData = np.array(stretchedData).T
        completeArray = np.append([header],stretchedData, axis=0)

        if newData.size > 0:
            newData = np.concatenate((newData,completeArray), axis=1)
        else:
            newData = completeArray
        
    with open(finalUniFile, "w") as output:
        writer = csv.writer(output, delimiter=",", lineterminator = '\n')    
        for row in newData:
            writer.writerow(row)
            
def stretchList(arr, finalLength, fill_char=''):
    newList = [fill_char] * finalLength
    startingLength = len(arr)
    d = finalLength - startingLength

    if d <= 0:
        return arr

    triggerStep = finalLength/(d+1)
    trigger = triggerStep

    oldEl = 0
    for i in range(0, finalLength):
        if i+1 > trigger:
            trigger += triggerStep
        else:
            newList[i] = arr[oldEl]
            oldEl += 1
            
    newList[-1] = arr[-1]

    return newList
            
if __name__ == "__main__":
    sensors = ["IMU_acc", "IMU_vel","Razor_acc", "Razor_vel", "Load_Cell"]
    unifile(sensors)
    print("Do something")