import csv
import serial
import time
from datetime import datetime

username = input("Enter your name: ")
mov_label = input("Add a label for the movement you will perform: ")
cycles = int(input("Enter the number of cycles: "))
cycle_time = int(input("Enter how many seconds you want each cycle to last: "))
rest_time = int(input("Write how many seconds you should rest between each cycle: "))
t1 = datetime.now().strftime("%Y%m%d-%H%M%S")
csv_file_route = ("C:/Users/Owner/Skill Transfer/EMG Data/Saved data/{0}_{1}_{2}_data.csv".format(t1,username,mov_label))
relaxed_file_route = ("C:/Users/Owner/Skill Transfer/EMG Data/Saved data/{0}_RELAXED_data.csv".format(username))
sensor1_file = []
sensor2_file = []
r_sensor1_file = []
r_sensor2_file = []
r_label = [0]
label = []
xd = ("***************************************")
cycle_number = 1
cycle_range = cycle_time*10
rest_samples = cycle_range*cycles

print("\n{x}\nID: {u}\nMovement: {m}\nCycles: {c}\nDuration of each cycle: {s} seconds\n{x}\n".format(x=xd,u=username,m=mov_label,c=cycles,s=cycle_time))
question = input("Do you want to continue?\nYes = 1 / No = 0\n")
if (question == str(1)):
    arduino = serial.Serial('COM6', baudrate=9600)
    arduino.close()
    time.sleep(1)
    print("\nFirst I need samples of your relaxed muscle.\n")
    time.sleep(2)
    print("Please relax your muscle for 5 seconds.\n")
    time.sleep(1)
    for x in range(5, 0, -1):
        seconds = x % 60
        minutes = int(x / 60) % 60
        print(f"{minutes:02}:{seconds:02}")
        time.sleep(1)
    print("\nThank you.\n")
    time.sleep(1)
    print("Taking samples of your relaxed muscle...\n")
    time.sleep(1)

    arduino.open()
    for x in range(rest_samples):
        r_label_data = 0
        data = arduino.readline().decode().strip('\r\n')

        try:
            r_sensor1_data, r_sensor2_data = data.split(',')
            r_s1_float = float(r_sensor1_data)
            r_s2_float = float(r_sensor2_data)
            r_s1_int = int(r_s1_float)
            r_s2_int = int(r_s2_float)

            print(r_s1_int, r_s2_int) 
            r_label.append(r_label_data)
            r_sensor1_file.append(r_s1_int)
            r_sensor2_file.append(r_s2_int)
        except ValueError:
            print("Error: The data received is not numeric")

    with open(relaxed_file_route, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["s1", "s2", "label"])

        for value1, value2, value3 in zip(r_sensor1_file, r_sensor2_file, r_label):
            writer.writerow([value1, value2, value3])
    print("\nThe data has been successfully saved in", relaxed_file_route)
    arduino.close()
    time.sleep(2)
    print("\nIt's time to take the movement samples")
    time.sleep(2)
    print("\nStarting in 5 seconds...\n")

    for x in range(5, 0, -1):
        seconds = x % 60
        minutes = int(x / 60) % 60
        print(f"{minutes:02}:{seconds:02}")
        time.sleep(1)
    time.sleep(1)
    arduino.open()

    for x in range(int(cycles)):
        print("\nCycle #"+str(cycle_number))
        cycle_number+=1

        for i in range(int(cycle_range)):
            
            label_data = int(mov_label)
            data = arduino.readline().decode().strip('\r\n')
      
            try:
                sensor1_data, sensor2_data = data.split(',')
                s1_float = float(sensor1_data)
                s2_float = float(sensor2_data)
                s1_int = int(s1_float)
                s2_int = int(s2_float)

                print(s1_int, s2_int)
                label.append(label_data)
                sensor1_file.append(s1_int)
                sensor2_file.append(s2_int)
            except ValueError:
                print("Error: The data received is not numeric")

        arduino.close()
        print("")
        if(cycle_number<=int(cycles)):
            time.sleep(1)
            print("Rest time:\n")
            for x in range(rest_time, 0, -1):
                seconds = x % 60
                minutes = int(x / 60) % 60
                print(f"{minutes:02}:{seconds:02}")
                time.sleep(1)
            print("TIME'S UP!")
            time.sleep(1)
            arduino.open()       
        
    with open(csv_file_route, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["s1", "s2", "label"]) 

        for value1, value2, value3 in zip(sensor1_file, sensor2_file, label):
            writer.writerow([value1, value2, value3])
    print("The data has been successfully saved in", csv_file_route)

else:
    print("\nSee you next time\n")