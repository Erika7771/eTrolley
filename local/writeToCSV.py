#----------------------------------------------------------------------------------
# Create and write the csv files with the recordings
#----------------------------------------------------------------------------------
import os
import glob
import csv
import time
import os.path
from pathlib import Path
from datetime import datetime
import numpy as np 

my_path = Path(__file__).resolve().parents[1]

# Create a new csv file for the sensor and write the heading row.
def create_file(sensor):
    global my_path
    
    # Only the last record is kept, empty the sensor directory before creating
    # a new file.
    path = str(my_path) + f"/flaskberry/static/recordings/{sensor}/"
    list_of_files = glob.glob(f'{path}*')
    for file in list_of_files:
        os.remove(file)
    
    # Create the file name with the format "date_time_sensorName.csv"
    timestamp = time.strftime("%Y%m%d_%H%M%S")        
    file_name = (path + timestamp + "_" + sensor   + ".csv")
    csvfile = file_name
    
    # Write the heading row depending on the sensor
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

# This function is executed as a parallel process (see utils.py). It writes the values
# of the queue in the csv file.
def write_file(csvfile, sensor, data_queue, STOP_TOKEN):
    with open(csvfile, "a")as output:        
        writer = csv.writer(output, delimiter=",", lineterminator = '\n')
        start_time = datetime.now()
        while True:
            line = data_queue.get()
            if line == STOP_TOKEN:
                return
            writer.writerow([datetime.now()-start_time]+list(line))
                                            
 # Merge the files of all the recorded sensors into a new one.
 # Since each sensor has its own reading frequency, the values of the lowest ones are
 # evenly spread out to match the timestamps of the fasted sensor and some values are
 # copied to fill the spaces. See the report for more details. 
def unifile(sensors):
    global my_path
    
    if "all" in sensors:
        sensors.remove("all")        
    
    files = []
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    
    # Remove the old csv file before creating a new one
    list_of_files = glob.glob(f'{my_path}/flaskberry/static/recordings/*.csv')
    for file in list_of_files:
        os.remove(file)
    
    # Create the file name with the format "date_time.csv"
    finalUniFile = str(my_path) + f"/flaskberry/static/recordings/"+ timestamp + ".csv"
    newData = np.array([]) #Store the timestamps of the fastest sensor that will be used to create the file. 
    maxLength = 0
    idLongest = None
    
    # Save in "files" a list with the names of the files to combine.
    for sensor in sensors:        
        path = str(my_path) + f"/flaskberry/static/recordings/{sensor}/"
        list_of_files = glob.glob(f'{path}*.csv')
        if len(list_of_files)<1:
            return None
        latest_file = max(list_of_files, key=os.path.getctime)
        files.append(latest_file)
        
        # Open the sensor file, count the number of rows and remove the time offset. 
        with open(latest_file) as latest_file:
            fileObject = csv.reader(latest_file,delimiter=',')
            row_count = 0
            timeCol = []
            #Remove the timestamp offset and create a new time vector
            for row in fileObject:
                row_count += 1
                if row_count == 2: # Save the 1st timestamp as offset
                    offset_dateTime = datetime.strptime(row[0],"%H:%M:%S.%f")
                if not row_count == 1: # Remove the offset from all the timestamps
                    row_dateTime = datetime.strptime(row[0],"%H:%M:%S.%f")
                    timeCol.append(row_dateTime-offset_dateTime)
                else: # Keep the heading element as it is
                     timeCol.append(row[0])
            if row_count > maxLength: # Check for the longest time vector and save it 
                newData = np.array([timeCol]).T
                maxLength = row_count
    
    # Open each file again and extract all the columns but the timestamps. If necessary, 
    # stretch the vectors before adding them to the new file.
    for file in files:
        oldData = []
        with open(file) as file:  
            reader = csv.reader(file,delimiter=',')
            for row in reader:
                oldData.append(row[1:])
             
        oldData = np.array(oldData)
        header = np.array(oldData[0,:])
        # Add values to each column of the sensors with less measurements
        stretchedData = [stretchList(oldData[1:,j],maxLength-1) for j in range(len(oldData[0]))]
        stretchedData = np.array(stretchedData).T
        completeArray = np.append([header],stretchedData, axis=0)
        
        # Add to the timestamps array the readings of all the sensors.
        if newData.size > 0:
            newData = np.concatenate((newData,completeArray), axis=1)
        else:
            newData = completeArray
        
    # Open the csv file and copy the array with the sensors data     
    with open(finalUniFile, "w") as output:
        writer = csv.writer(output, delimiter=",", lineterminator = '\n')    
        for row in newData:
            writer.writerow(row)
   
#strech list of readings. Copy the last value to fill the spaces.
def stretchList(arr, finalLength, fill_char=''):
    newList = [fill_char] * finalLength
    startingLength = len(arr)
    d = finalLength - startingLength # How many values must be added to the original vector

    if d <= 0:
        return arr
    
    triggerStep = finalLength/(d+1)
    trigger = triggerStep
    oldEl = 0
    
    #Create a new vector with the final lenght. At each iteration the value of the old vector is copied in the new one
    # and every triggerStep this value is copied in the next cell too.
    for i in range(0, finalLength):
        if i+1 > trigger:
            trigger += triggerStep
            newList[i] = arr[oldEl-1]
        else:
            newList[i] = arr[oldEl]
            oldEl += 1
    #keep the last value in the same position        
    newList[-1] = arr[-1]

    return newList