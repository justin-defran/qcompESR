'''
Created on Dec 23, 2016

@author: Kai
'''

import visa,sys,time

class SynthHD(object):
    '''
    '''
    
    def __init__(self,debug=False):
        self.debug=debug
        rm = visa.ResourceManager()
        visas=rm.list_resources()
        if self.debug:
            print(visas)
        if 'COM3' in visas:
            try:
                ins = rm.open_resource('COM3',open_timeout=1)
                ins.write_termination=None
                ins.read_termination='\n'
                info = []
                ins.write('?')
                for i in range(56):
                    info.append(ins.read().replace('\r', '').replace('\n',''))
                if self.debug:
                    for each in info:
                        pass
                        print(each)
                if info[52]=='-) Serial Number  324':
                    self.ins=ins
            except visa.VisaIOError:
                pass
        else:
            for each_visa in visas:
                try:
                    ins = rm.open_resource(each_visa,open_timeout=1)
                    ins.write_termination=None
                    ins.read_termination='\n'
                    info = []
                    ins.write('?')
                    for i in range(56):
                        info.append(ins.read().replace('\r', '').replace('\n',''))
                    if self.debug:
                        for each in info:
                            pass
                            #print each
                    if info[52]=='-) Serial Number  324':
                        self.ins=ins
                except visa.VisaIOError:
                    pass
            
        self.current_status={}
        try:
            self.get_status(info)
        except:
            pass
        
    def get_status(self,*args):
        if len(args)==0:
            print('none')
            self.ins.write('?')
            info=[]
            for i in range(55):
                info.append(self.ins.read().replace('\r', '').replace('\n',''))
        else:
            
            info=args[0]

        a,b=info[1].replace('f) RF Frequency Now (MHz)  ','').split(', ')
        self.current_status['A_FREQ']=float(a)
        self.current_status['B_FREQ']=float(b)
        
        a,b=info[2].replace('W) RF Power (dBm)  ','').split(', ')
        self.current_status['A_LEVEL']=float(a)
        self.current_status['B_LEVEL']=float(b)
        
        a,b=info[5].replace('a) VGA DAC Setting (0=mim, 45000=max) ','').split(', ')
        self.current_status['A_LEVEL_RAW']=int(a)
        self.current_status['B_LEVEL_RAW']=int(b)
        
        a,b=info[8].replace('r) PA On(1) or Off(0) ','').split(', ')
        self.current_status['A_POWER_ON']=a=='1'
        self.current_status['B_POWER_ON']=b=='1'
    
    
    def sendCom(self,s):
        self.ins.write(s)
        
    def querySingle(self,s):
        if '?' in s:
            self.ins.write(s)
            reply=self.ins.read().replace('\r', '').replace('\n','')
            print(reply,len(reply))
            
    def setSingleSwitch(self,channel,switch):
        if channel==0 or channel==1:
            c='C'+str(channel)
        try:
            if switch:
                self.sendCom(c+'E1r1')
            else:
                self.sendCom(c+'E0r0')
        except:
            pass
            
    def setSingleFreq(self,channel,freq):
        if channel==0 or channel==1:
            c='C'+str(channel)
        try:
            freq_float=float(freq)
            f='f'+str(freq_float)
        except:
            pass
        try:
            self.ins.write(c+f)
        except:
            pass
        
    def setSingleLevel_dBm(self,channel,dbm_level):
        if channel==0 or channel==1:
            c='C'+str(channel)
        try:
            level_float=float(dbm_level)
            a='W'+str(level_float)
        except:
            pass
        try:
            self.ins.write(c+a)
        except:
            pass
        
    def setSweep_pixelTrig(self,startFreq,stopFreq,stepFreq,level):
        try:
            c='C0' # channel 1
            level_float=float(level)
            a='['+str(level_float)+']'+str(level_float)
            f=float(startFreq)
            f1='l'+str(f)
            f=float(stopFreq)
            f2='u'+str(f)
            f=float(stepFreq)
            f3='s'+str(f)
            trig='w2'
        except:
            return
        try:
            self.ins.write(c+a+f1+f2+f3+trig)
        except:
            pass
        
    def setSweep_noTrig(self,startFreq,stopFreq,stepFreq,level,timeStep):
        try:
            c='C0' # channel 1
            level_float=float(level)
            a='['+str(level_float)+']'+str(level_float)
            f=float(startFreq)
            f1='l'+str(f)
            f=float(stopFreq)
            f2='u'+str(f)
            f=float(stepFreq)
            f3='s'+str(f)
            f=float(timeStep)
            f4='t'+str(f)
            trig='w0'
        except:
            return
        try:
            self.ins.write(c+a+f1+f2+f3+f4+trig)
        except:
            pass
        
    def setSweep_lineTrig(self,startFreq,stopFreq,stepFreq,level,timeStep):
        try:
            c='C0' # channel 1
            level_float=float(level)
            a='['+str(level_float)+']'+str(level_float)
            f=float(startFreq)
            f1='l'+str(f)
            f=float(stopFreq)
            f2='u'+str(f)
            f=float(stepFreq)
            f3='s'+str(f)
            f=float(timeStep)
            f4='t'+str(f)
            trig='w1'
        except:
            return
        try:
            self.ins.write(c+a+f1+f2+f3+f4+trig)
        except:
            pass
        
    def startSweep(self):
        try:
            self.ins.write('C0r1g1')
        except:
            pass
            
    def stopSweep(self):
        try:
            self.ins.write('g0C0r0')
        except:
            pass
            
            





if __name__ == '__main__':
    syn=SynthHD(True)
    syn.setSingleFreq(0, 1000)
    syn.setSingleSwitch(0, False)
    time.sleep(1)
    syn.setSweep_lineTrig(800, 1300, 25, -5,100)
    time.sleep(1)
    syn.startSweep()

    
