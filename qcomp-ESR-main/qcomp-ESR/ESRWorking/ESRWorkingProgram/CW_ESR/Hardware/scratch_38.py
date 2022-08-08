import ADwin
import os

adw = ADwin.ADwin()

adw.Boot(adw.ADwindir + 'ADwin11.btl')

count_proc = os.path.join(os.path.dirname(__file__),'AdWIN','1D_Scan.TB1')
adw.Load_Process(count_proc)