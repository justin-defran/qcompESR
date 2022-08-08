__author__ = 'duttlab6'
import matplotlib.pylab as plt
import numpy as np
import visa
import os
import sys,traceback
import numpy
import time

start=2.0
stop=3.0
runs=1
steps=500
rate=50 #Hz

for j in range(1):
    save_num=str(j+3)
    a=[]
    b=0
    rm = visa.ResourceManager()
    arduino=rm.open_resource("com12",baud_rate=9600)
    del arduino.timeout
    print arduino.read()
    for i in range(runs):
        result = arduino.query(str(steps))

    arduino.close()
    time.sleep(0.1)









