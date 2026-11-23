
from tkinter import N

import serial,time,random


def getSample(port):
    #port = port #serial.Serial(port = comPort baudrate = 9600, timeout=0.5)
    result = 0.0
    try:
        weight = port.readline().decode("utf-8")
        pos = weight.find("N")
        if pos > 0 :
            weight = weight[7:12].replace(" ","")
            print(weight) #          146kg N
            if weight != " " and weight != "":
                result = float(weight)
    except Exception as e:
        pass
        #print("at 1128=> ",e)
    return result

port = serial.Serial(port = "COM4", baudrate = 9600, timeout=0.5, write_timeout=3.0)

while True:
    rdn = int(random.random()*200)
    str_rdn = str(rdn).zfill(3)
    print('         '+str_rdn+'kg N\n')
    port.write(('         '+str_rdn+'kg N\n').encode('utf-8'))
    time.sleep(0.5)
    #port.write('         146kg N\n'.encode('utf-8'))
    #port.write('           0kg T\n'.encode('utf-8'))
