'''
Created on May 9, 2016

@author: Kai Zhang
'''
from Hardware.MCL.NanoDrive import MCL_NanoDrive
import ADwin
import sys,os,time


class ADWIN_MCL():
    '''
    This is for ADWIN_MCL Keeping NV.
    '''


    def __init__(self,*args):
        pass
    
    def initialize(self):
        '''
        Return value is 0 if OK, -1 if not OK

        '''
        self.nd=MCL_NanoDrive()
        self.nd_handle=self.nd.InitHandles().get('L')
        if self.nd_handle==None:
            return -1
        
        self.adw=ADwin.ADwin()
        if self.adw_boot():
            if self.adw_load_process():
                return 0
        
        return -1
    
    def adw_boot(self):
        try:
            btl = self.adw.ADwindir + 'ADwin11.btl'
            self.adw.Boot(btl)
            return True
        except ADwin.ADwinError as e:
            sys.stderr.write(e.errorText)
            return False
            
    def adw_load_process(self):
        try:
            count_proc = os.path.join(os.path.dirname(__file__),'Hardware\\ADWIN\\TrialCounter.TB1') # TrialCounter is configured as process 1
            self.adw.Load_Process(count_proc)
            return True
        except ADwin.ADwinError as e:
            sys.stderr.write(e.errorText)
            return False
        
    def laser_on(self):
        self.nd.SetClock('Aux', 1, self.nd_handle)
        
    def laser_off(self):
        self.nd.SetClock('Aux', 0, self.nd_handle)
        
        
    def cleanup(self):
        
        self.nd.ReleaseAllHandles()
        
        self.adw.Clear_Process(1)
        return 0

'''
def keepNV(adw,nd):
    #counts=
    while True:
'''

if __name__ == '__main__':
    hardware=ADWIN_MCL()
    if hardware.initialize()==0:
        keepNV(hardware.adw,hardware.nd)
        
    keepNV()