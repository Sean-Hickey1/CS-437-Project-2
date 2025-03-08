import socket
import picar_4wd as fc
import time

HOST = "172.20.10.10" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)
CAR_SPEED = 30

import psutil

def get_cpu_temperature():
    try:
        # Read from the system file
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = int(f.read()) / 1000  # Convert from millidegree
        return temp
    except FileNotFoundError:
        # Alternative method using vcgencmd
        temp_str = os.popen("vcgencmd measure_temp").readline()
        temp = float(temp_str.replace("temp=", "").replace("'C\n", ""))
        return temp
        
        
        
def get_pi_uptime():
	with open("/proc/uptime", "r") as f:
		uptime_seconds = float(f.readline().split()[0])
		return time.strftime("%H:%M:%S", time.gmtime(uptime_seconds))


global STATE, TEMP, UPTIME

STATE = "   "
TEMP = get_cpu_temperature()
UPTIME = get_pi_uptime()

def analyzeStroke(keyVal):
    global TEMP, UPTIME, STATE
    
    if (keyVal == b"87"):           # w
        # forward
        print("Moving forward")
        fc.forward(CAR_SPEED)
        STATE = "MOVING"
    elif (keyVal == b"83"):         # s
        # backward
        print("Moving backward")
        fc.backward(CAR_SPEED)
        STATE = "MOVING"
    elif (keyVal == b"65"):         # a
        # left
        print("Moving left")
        fc.turn_left(CAR_SPEED)
        STATE = "TURNING"
    elif (keyVal == b"68"):         # d
        # right
        print("Moving right")
        fc.turn_right(CAR_SPEED)
        STATE = "TURNING"
    elif (keyVal == b"32"):         # spacebar
        # stop
        print("Car stop")
        fc.stop()
        STATE = "STOPPED"
    
    elif (keyVal == b"114"):        # r
        # refresh / update battery and temperature 
        TEMP = get_cpu_temperature()
        UPTIME = get_pi_uptime()
    

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Server")
    s.bind((HOST, PORT))
    print("Bind")
    s.listen()

    try:
        #client, clientInfo = s.accept() # for allowing more than one message for the client
        while 1:
            client, clientInfo = s.accept() 
            print("server recv from: ", clientInfo)
            data = client.recv(1024)      # receive 1024 Bytes of message in binary format
            print(data) 
            analyzeStroke(data)
            print("Analyzed")
            
            
            if data == b"114":
                print("Into the thick of it")
                info_data = f"{TEMP},{UPTIME},{STATE}"
                print(info_data)     
                client.sendall(info_data.encode()) # Echo back to client
            elif data != b"":
                print(data)
                client.sendall(data)
            
    except: 
        print("Closing socket")
        client.close()  
        s.close()   

