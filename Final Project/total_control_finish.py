# !/usr/bin/env python3
# -*-coding: utf-8 -*-
import time
# import RPi.GPIO as GPIO
import socket
import urllib.request
import urllib.parse
import urllib.error
import json
from datetime import datetime

Save_Data_path = "C:\\Users\\cheny\\Desktop\\python env\\data.txt"
Recv_Data_path = "C:\\Users\\cheny\\Desktop\\python env\\rev.txt"


def motor():
    # GPIO.setmode(GPIO.BOARD)
    # MotorPin=12
    # GPIO.setup(MotorPin,GPIO.OUT)
    # pwm_motor = GPIO.PWM(MotorPin, 50)

    # pwm_motor.start(7.5)

    # for a in range(4):
    #     pwm_motor.ChangeDutyCycle(4)
    #     time.sleep(0.1)
        
    # for d in range(3):
    #     pwm_motor.ChangeDutyCycle(11)
    #     time.sleep(0.07)
        
    # GPIO.cleanup()
    print("Enter Motor")
    motor_data2_txt()



def UDP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    PORT = 9930
    network = ''

    s.bind((network, PORT))
    print('Listening for broadcast at ', s.getsockname())
           
    while True:
        data, address = s.recvfrom(65535)
        data = data.decode('utf-8')
        print(data)

        if data == "feed":
            motor()
            


    
    
def motor_data2_txt():
    
    with open(Save_Data_path, 'a')as save_f:
        strr = "---- Feed Dog\n"
        save_f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + strr)
        
    Num_save_f = open(Save_Data_path)
    Save_lines = len(Num_save_f.readlines())
    print(Save_lines)

    if (Save_lines % 10 == 0):
        print("enter")
        Read_save_f = open(Save_Data_path,'r')
        recv_f = open(Recv_Data_path,'w')
        save_data_lines_str = Read_save_f.readlines()
        print(save_data_lines_str)
        for line in save_data_lines_str:
            sned2cloud_str = line

            data = { 'date': sned2cloud_str}
        
            url = 'https://mighty-sierra-05175.herokuapp.com/api/iot-feeder'

            req = urllib.request.Request(url)

            req.add_header('Content-Type','application/json;charset = utf-8')

            jsondata = json.dumps(data)

            jsondataasbytes = jsondata.encode("utf-8")

            req.add_header('Content-Length',len(jsondataasbytes))

            response = urllib.request.urlopen(req,jsondataasbytes).read()
            
            print(response)

        recv_f.close()
        Read_save_f.close()
        print("Send Data to Database")


    
    


if __name__=='__main__':
  UDP()  
