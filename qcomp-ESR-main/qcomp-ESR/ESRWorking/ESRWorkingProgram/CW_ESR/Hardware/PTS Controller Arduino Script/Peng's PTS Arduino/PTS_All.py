'''using pts_test.ino!!! path:D:\workspace\ESRWorking\ESRWorkingProgram\CW_ESR\Hardware\PTS Controller Arduino Script\Peng's PTS Arduino'''
import time
import visa
rm=visa.ResourceManager()
arduino=rm.open_resource('COM13')

time.sleep(5)

GHz=1e9
MHz=1e6
kHz=1e3

#print GHz
mode='f'  #s (sinlge sweep) or f (single frequency)

single_freq=str(int(2870*MHz))
#single_output = single_freq.rjust(10,'0')
single_output =0
power = 100

#print single_output

start=1*GHz
stop=2*GHz
steps=100

dwell_time=20 #ms
runs=10

print(arduino.read())
if mode=='s':
    arduino.write(mode+str(start)+'#'+str(stop)+'#'+str(steps)+'#'+str(dwell_time)+'#') #+str(runs))
if mode=='f':
    arduino.write(mode+str(single_output)+'#')#+'#'+str(stop)+'#'+str(steps)+'#'+str(dwell_time)+'#')
if mode =='p':
    arduino.write(mode+str(power)+'#')

print(arduino.read())
arduino.close()