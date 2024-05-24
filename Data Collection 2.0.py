import csv
import serial
import time
from datetime import datetime
import os
import threading

def get_user_input():
    username = input("Enter your name: ")
    return username

def initialize_file_routes(username):
    directory = f"C:/Users/Owner/Skill Transfer/EMG Data/{username}_Movements"
    if not os.path.exists(directory):
        os.makedirs(directory)
    t1 = datetime.now().strftime("%Y%m%d-%H%M%S")
    relaxed_file_route = f"{directory}/{username}_RELAXED_{t1}.csv"
    movement_file_route = f"{directory}/{username}_MOVEMENT_{t1}.csv"
    return relaxed_file_route, movement_file_route

def countdown(seconds):
    for x in range(seconds, 0, -1):
        print(f"{x // 60:02}:{x % 60:02}")
        time.sleep(1)

def collect_relaxed_data(arduino, file_path):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["s1", "s2", "label"])
        print("\nCollecting 100 samples of your relaxed muscle...")
        for _ in range(100):
            data = arduino.readline().decode().strip()
            try:
                s1, s2 = map(float, data.split(','))
                writer.writerow([int(s1), int(s2), 0])
                print(f"Data: [{int(s1)}, {int(s2)}]")
            except ValueError:
                print("Error: The data received is not numeric")

def collect_movement_data(arduino, file_path):
    global stop_collecting
    stop_collecting = False
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["s1", "s2", "label"])
        print("Collecting movement data...")
        while not stop_collecting:
            data = arduino.readline().decode().strip()
            if data:
                try:
                    s1, s2 = map(float, data.split(','))
                    writer.writerow([int(s1), int(s2), 1])
                    print(f"Data: [{int(s1)}, {int(s2)}]")
                except ValueError:
                    print("Error: The data received is not numeric")

def stop_data_collection():
    global stop_collecting
    input()
    stop_collecting = True

def main():
    username = get_user_input()
    relaxed_file_route, movement_file_route = initialize_file_routes(username)
    
    arduino = serial.Serial('COM6', baudrate=9600, timeout=1)
    arduino.close()
    time.sleep(1)
    
    print("\nFirst I need samples of your relaxed muscle.\n")
    time.sleep(2)
    print("Please relax your muscle for 5 seconds.\n")
    time.sleep(1)
    countdown(5)
    arduino.open()
    time.sleep(1)
    collect_relaxed_data(arduino, relaxed_file_route)
    arduino.close()
    print("\nReady to record movement. Press Enter to start...")
    print("Once sampling has started, press Enter again to stop.")
    input()
    arduino.open()
    stop_thread = threading.Thread(target=stop_data_collection)
    stop_thread.start()
    collect_movement_data(arduino, movement_file_route)
    stop_thread.join()

    arduino.close()
    print("\nData collection complete.")
    print(f"All files have been saved in the directory: {os.path.dirname(relaxed_file_route)}\n")

if __name__ == "__main__":
    main()
