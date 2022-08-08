'''
Created on Jul 3, 2015

@author: Kai Zhang
'''
# modified on Oct. 14, 2019 by Gurudev Dutt
# major issues are updating to Python 3, Qt5 and fixing module imports
from PyQt5 import QtCore
import multiprocessing, time, sys, numpy  # ,visa
import pyvisa as visa
#import visa # visa is the name of the python3 package
import os

# from .SynthUSBII.Wrapper import SynthUSB
from .SynthUSBII.Wrapper import SynthUSB
from .AmpNV.Wrapper import AmpNV
from .SynthHD.Wrapper import SynthHD
import ADwin # ADwin package is available on PyPi, used pip to install

class ScanThread(QtCore.QThread):
    stopped = QtCore.pyqtSignal(str)
    status = QtCore.pyqtSignal(str)
    data = QtCore.pyqtSignal(numpy.ndarray)

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.sweeping = False

    def run(self):
        self.sweeping = True
        self.stopping = False
        self.proc = ScanProcess3()
        self.p_conn, c_conn = multiprocessing.Pipe()
        self.proc.get_conn(c_conn)
        self.proc.parameters = self.para
        self.proc.start()

        while self.sweeping:
            self.p_conn.poll(None)
            reply = self.p_conn.recv()
            # print reply
            if reply == 'Abort!' or reply == 'Process Ends.':
                self.sweeping = False
                self.stopped.emit(reply)
                break

            elif self.stopping:
                self.p_conn.send('s')
            elif type(reply) is str:
                self.status.emit(reply)
                self.p_conn.send('r')
            elif type(reply) is numpy.ndarray:
                # print str(0)
                self.data.emit(reply)
                self.p_conn.send('r')

    def stop(self):
        self.stopping = True


class ScanProcess(multiprocessing.Process):
    '''
    Using SynthUSBII
    '''

    def get_conn(self, conn):
        self.conn = conn
        self.scanning = False

    def run(self):

        self.scanning = True
        self.initialize()

        avg = 0
        delay = 0.2
        f_end = 0
        while avg <= self.parameters['NOA']:  # and self.scanning:
            self.conn.poll(None)
            r = self.conn.recv()
            if r == 's':
                self.scanning = False
                break
            if avg > 0:
                if f_end == self.parameters['START'] * 1000:
                    f_end = self.parameters['STOP'] * 1000 + (self.parameters['STOP'] - self.parameters['START']) / \
                            self.parameters['NOS']
                percentage = (self.parameters['STOP'] * 1000 - f_end) / (
                            self.parameters['STOP'] * 1000 - self.parameters['START'] * 1000)
                total_time = self.parameters['DWELL'] * self.parameters['NOS'] / 1000.0  # in seconds
                delay += percentage * total_time
            print((delay), end=' ')
            print((self.syn.get_status()['FREQ']), end=' ')
            self.syn.startSweep()

            time.sleep(delay)
            self.adw.Start_Process(1)

            while self.adw.Process_Status(1) == 1:
                time.sleep(0.001)
            f_end = self.syn.get_status()['FREQ']
            print(f_end)
            dataList = self.adw.GetData_Long(1, 1, self.parameters['NOS'])

            if avg == 0:
                self.conn.send('cal')
            if avg > 0:
                self.conn.send(numpy.asarray(dataList, dtype=int))
            avg += 1

        self.cleanup()
        self.scanning = False

    def initialize(self):

        self.conn.send('init')

        self.adw = ADwin.ADwin()
        try:
            self.adw.Boot(self.adw.ADwindir + 'ADwin11.btl')
            count_proc = os.path.join(os.path.dirname(__file__), 'AdWIN',
                                      '1D_Scan.TB1')  # TrialCounter is configured as process 1
            self.adw.Load_Process(count_proc)
            self.adw.Set_Par(1, self.parameters['NOS'])
            self.adw.Set_Processdelay(1, int(self.parameters['DWELL'] * 300000))
        except ADwin.ADwinError as e:
            sys.stderr.write(e.errorText)
            self.conn.poll(None)
            self.conn.recv()
            self.conn.send('Abort!')
            self.scanning = False
            return

        print(('adwin ready'), end=' ')

        self.amp = AmpNV()
        if self.amp.current_status['SWITCH'] == 0:
            self.amp.set(0)
            self.amp.switch(True)
            self.amp.get_status()
        if not self.amp.current_status['TEST_A']:
            sys.stderr.write('AmpNV Alarm: test PA bias alarm!')
            self.conn.poll(None)
            self.conn.recv()
            self.conn.send('Abort!')
            self.scanning = False
            return
        if not self.amp.current_status['TEST_T']:
            sys.stderr.write('AmpNV Alarm: test PA bias trigger!')
            self.conn.poll(None)
            self.conn.recv()
            self.conn.send('Abort!')
            self.scanning = False
            return
        self.amp.set(self.parameters['AMPPOW'])

        print(('amp ready'), end=' ')

        self.syn = SynthUSB()

        if not self.syn.current_status['LOCKED']:
            sys.stderr.write('SynthUSB Alarm: not locked!')
            self.conn.poll(None)
            self.conn.recv()
            self.conn.send('Abort!')
            self.scanning = False
            return
        step = (self.parameters['STOP'] - self.parameters['START']) / self.parameters['NOS']
        self.syn.setSweep(self.parameters['START'] * 1000, (self.parameters['STOP']) * 1000, step * 1000,
                          self.parameters['DWELL'])
        self.syn.setFreq(self.parameters['START'] * 1000)
        self.syn.setPower(self.parameters['SYNPOW'])

        print('synth ready')

        self.conn.poll(None)
        self.conn.recv()
        self.conn.send('success')

    def cleanup(self):
        self.adw.Clear_Process(1)
        self.syn.cleanup()
        self.amp.cleanup()
        if self.scanning:
            self.conn.poll(None)
            self.conn.recv()
        self.conn.send('Process Ends.')


class ScanProcess2(multiprocessing.Process):
    '''
    use synthHD
    '''

    def get_conn(self, conn):
        self.conn = conn
        self.scanning = False

    def run(self):
        self.scanning = True
        self.initialize()

        avg = 0
        delay = 0.2
        f_end = 0
        while avg <= self.parameters['NOA'] and self.scanning:
            self.conn.poll(None)
            r = self.conn.recv()
            if r == 's':
                self.scanning = False
                break
            if avg > 0:
                if f_end == self.parameters['START'] * 1000:
                    f_end = self.parameters['STOP'] * 1000 + (self.parameters['STOP'] - self.parameters['START']) / \
                            self.parameters['NOS']
                percentage = (self.parameters['STOP'] * 1000 - f_end) / (
                            self.parameters['STOP'] * 1000 - self.parameters['START'] * 1000)
                total_time = self.parameters['DWELL'] * self.parameters['NOS'] / 1000.0  # in seconds
                delay += percentage * total_time
            print((delay), end=' ')
            print((self.syn.get_status()['FREQ']), end=' ')
            self.syn.startSweep()

            time.sleep(delay)
            self.adw.Start_Process(1)

            while self.adw.Process_Status(1) == 1:
                time.sleep(0.001)
            f_end = self.syn.get_status()['FREQ']
            print(f_end)
            dataList = self.adw.GetData_Long(1, 1, self.parameters['NOS'])

            if avg == 0:
                self.conn.send('cal')
            if avg > 0:
                self.conn.send(numpy.asarray(dataList, dtype=int))
            avg += 1

        self.cleanup()
        self.scanning = False

    def initialize(self):

        self.conn.send('init')

        self.adw = ADwin.ADwin()
        try:
            self.adw.Boot(self.adw.ADwindir + 'ADwin11.btl')
            count_proc = os.path.join(os.path.dirname(__file__), 'AdWIN',
                                      'PeriodicCounter.TB1')  # TrialCounter is configured as process 1
            self.adw.Load_Process(count_proc)
            self.adw.Set_Par(1, self.parameters['NOS'])
            self.adw.Set_Processdelay(1, int(self.parameters['DWELL'] * 300000))
        except ADwin.ADwinError as e:
            sys.stderr.write(e.errorText)
            self.conn.poll(None)
            self.conn.recv()
            self.conn.send('Abort!')
            self.scanning = False
            return

        print(('adwin ready'), end=' ')

        # self.amp=AmpNV()
        # if self.amp.current_status['SWITCH']==0:
        #     self.amp.set(0)
        #     self.amp.switch(True)
        #     self.amp.get_status()
        # if not self.amp.current_status['TEST_A']:
        #     sys.stderr.write('AmpNV Alarm: test PA bias alarm!')
        #     self.conn.poll(None)
        #     self.conn.recv()
        #     self.conn.send('Abort!')
        #     self.scanning=False
        #     return
        # if not self.amp.current_status['TEST_T']:
        #     sys.stderr.write('AmpNV Alarm: test PA bias trigger!')
        #     self.conn.poll(None)
        #     self.conn.recv()
        #     self.conn.send('Abort!')
        #     self.scanning=False
        #     return
        # self.amp.set(self.parameters['AMPPOW'])
        #
        # print('amp ready'),

        self.syn = SynthHD()
        if not self.syn.current_status['LOCKED']:
            sys.stderr.write('SynthUSB Alarm: not locked!')
            self.conn.poll(None)
            self.conn.recv()
            self.conn.send('Abort!')
            self.scanning = False
            return
        if self.syn.current_station['LOCKED']:
            self.conn.poll()
            self.conn.recv()
            self.scanning = True

        step = (self.parameters['STOP'] - self.parameters['START']) / self.parameters['NOS']
        self.syn.setSweep(self.parameters['START'] * 1000, (self.parameters['STOP'] + 100 * step) * 1000, step * 1000,
                          self.parameters['DWELL'])
        self.syn.setFreq(self.parameters['START'] * 1000)
        self.syn.setPower(self.parameters['SYNPOW'])

        print('synth ready')

        self.conn.poll(None)
        self.conn.recv()
        self.conn.send('success')

    def cleanup(self):
        self.adw.Clear_Process(1)
        self.syn.cleanup()
        self.amp.cleanup()
        if self.scanning:
            self.conn.poll(None)
            self.conn.recv()
        self.conn.send('Process Ends.')


class ScanProcess3(multiprocessing.Process): #Arduino and Adwin
    '''
    Using PTS and Arduino MUX controller
    '''

    def get_conn(self, conn): #Connection to the Main App
        self.conn = conn
        self.scanning = False

    def run(self): #Counting Process
        #Initinalizing the Arduino
        rm = visa.ResourceManager()
        arduino = rm.open_resource('com3')
        print((arduino.read()))

        GHz = 1e9
        MHz = 1e6
        kHz = 1e3

        mode = 's'  # s (sinlge sweep) or f (single frequency)

        self.scanning = True
        self.initialize()

        avg = 0 #Counter for averages
        #Defining the parameters
        start = self.parameters['START'] * GHz
        stop = self.parameters['STOP'] * GHz
        steps = self.parameters['NOS']
        dwell_time = self.parameters['DWELL']  # ms

        time.sleep(0.2)

        while avg < self.parameters['NOA'] and self.scanning:
            self.conn.poll(None)
            r = self.conn.recv()
            if r == 's':
                self.scanning = False
                break

            self.adw.Start_Process(1) #Initialize the Adwin
            #String sent to the Arduino
            arduino.write(mode + str(start) + '#' + str(stop) + '#' + str(steps) + '#' + str(dwell_time) + '#')

            t1 = time.perf_counter() #Elapsed time at this point
            while self.adw.Process_Status(1) == 1:
                time.sleep(0.001)   #Delay the code while the Adwin is running
            #getting the data list
            dataList = self.adw.GetData_Long(1, 1, self.parameters['NOS'])  # len(self.yArr)+19 in confocal

            print((len(dataList), ' points done.'))
            t2 = time.perf_counter() #Elapsed time at this point
            print(("It takes: ", t2 - t1, 'for ', self.parameters['NOS'], " steps"))
            print(list(dataList))

            if avg == 0:
                self.conn.send('cal')
            if avg > 0: #When the process is done, send the data list to the app
                self.conn.send(numpy.asarray(dataList, dtype=int))

            avg += 1 #Increase the counter
            print("Average ", avg, " is done")

        self.cleanup() #Close all connections
        self.scanning = False

    def initialize(self):

        self.conn.send('init')
        #Initializing the Adwin
        self.adw = ADwin.ADwin()
        try:
            self.adw.Boot(self.adw.ADwindir + 'ADwin11.btl')
            count_proc = os.path.join(os.path.dirname(__file__), 'AdWIN', 'Trigger_Count_test_1.TB1')
            # '1D_Scan.TB2')   # TrialCounter is configured as process 1
            # count_proc = os.path.join(os.path.dirname(__file__), 'AdWIN', 'CW_ESR_TrigCounter.TB1')
            print(os.path.dirname(__file__))
            self.adw.Load_Process(count_proc)
            self.adw.Set_Par(1, self.parameters['NOS'])
            # self.adw.Set_Par(2, int(self.parameters['DWELL']))
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # self.adw.Set_Processdelay(1, int(self.parameters['DWELL']*300000)) #functional only when set as "internal" in ADbasic.
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        except ADwin.ADwinError as e:
            sys.stderr.write(e.errorText)
            self.conn.poll(None)
            self.conn.recv()
            self.conn.send('Abort!')
            self.scanning = False
            return

        print('adwin ready', end=' ')
        '''
        self.amp = AmpNV()
        if self.amp.current_status['SWITCH'] == 0:
            self.amp.set(0)
            self.amp.switch(True)
            self.amp.get_status()
        if not self.amp.current_status['TEST_A']:
            sys.stderr.write('AmpNV Alarm: test PA bias alarm!')
            self.conn.poll(None)
            self.conn.recv()
            self.conn.send('Abort!')
            self.scanning = False
            return
        if not self.amp.current_status['TEST_T']:
            sys.stderr.write('AmpNV Alarm: test PA bias trigger!')
            self.conn.poll(None)
            self.conn.recv()
            self.conn.send('Abort!')
            self.scanning = False
            return
        self.amp.set(self.parameters['AMPPOW'])

        print 'amp ready',
        '''

        self.conn.poll(None)
        self.conn.recv()
        self.conn.send('success')

    def cleanup(self):
        self.adw.Clear_Process(1)
        # self.syn.cleanup()
        # self.amp.cleanup()
        if self.scanning:
            self.conn.poll(None)
            self.conn.recv()
        self.conn.send('Process Ends.')