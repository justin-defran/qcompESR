# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 14:54:21 2015

@author: duttlab6
"""

import numpy as np
import visa
import time

def binary(num, pre='', length=4, spacer=0):
    return '{0}{{:{1}>{2}}}'.format(pre, spacer, length).format(bin(num)[2:])

pin_list=[44,43,41,40,16,15,20,19,18,17,27,26,2,1,29,28,4,3,31,
          30,6,5,33,32,8,7,35,34,10,9,37,36,12,11,39,38,14,13]
          

    
freq=str(2870000000)
a=[]
s=''
for i in list(range(10)):
    digits=binary(int(freq[i]))
    s+=digits
    a.append(digits[0])
    a.append(digits[1])
    a.append(digits[2])
    a.append(digits[3])
b=a[2:]
print(s)
'''
for i in range(38):
    if b[i]=='0':
        print 'Pin',pin_list[i],'HIGH'
    else:
        print 'Pin',pin_list[i],'LOW'
'''
rm=visa.ResourceManager()
print(rm.list_resources())
arduino=rm.open_resource("com13")
print(arduino.read())
print(arduino.query(s+'.'))

#for i in range(2):
    
    

