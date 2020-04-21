import os
import csv
import time
import os.path
from pathlib import Path

def create_file(sensor):
    
    my_path = Path(__file__).resolve().parents[1]
    path = str(my_path) + f"/flaskberry/static/recordings/{sensor}/"
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    
    file_name = (path + timestamp + "_" + sensor   + ".csv")
    csvfile = file_name
    
    with open(csvfile, "a") as output:
        writer = csv.writer(output, delimiter=",", lineterminator = '\n')
        
        if sensor == "IMU_acc" or sensor == "Razor_acc":   
            writer.writerow(['acc_x','acc_y','acc_z'])            
        elif sensor == "IMU_vel" or sensor == "Razor_vel":   
            writer.writerow(['vel_x','vel_y','vel_z'])
        else:
            writer.writerow(['data'])  
    
    return csvfile

def write_file(csvfile, sensor, data):    

    with open(csvfile, "a")as output:
        writer = csv.writer(output, delimiter=",", lineterminator = '\n')
        if sensor != 'Load_Cell':
            writer.writerow(data)
        else:
            writer.writerows(data)

if __name__ == "__main__":
    print("bella")