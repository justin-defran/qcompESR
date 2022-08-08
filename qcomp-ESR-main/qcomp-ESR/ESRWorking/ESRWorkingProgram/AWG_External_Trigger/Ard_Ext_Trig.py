import ADwin #ADwin python module
import pyvisa as visa #Virt. Instr. Soft. Arch. to control the Arduino
import time
import sys

#initialize the Arduino
rm = visa.ResourceManager()
arduino = rm.open_resource('COM7')
print((arduino.read()))

#initialize the ADwin
try:
    adw = ADwin.ADwin()
    adw.Boot(adw.ADwindir + 'ADwin11.btl')
    count_proc = 'D:\PyCharmProjects\qcomp-qapps\ESRWorking\ESRWorkingProgram\CW_ESR\Hardware\AdWIN\Trigger_Count_test_1.TB1'
    adw.Load_Process(count_proc)
    print("Adwin was successfully initialized")
except ADWin.ADWinError as e:
    sys.stderr.write(e.errorText)

avg = 0
nor = 10 #Number of Readings
noa = 5 #Number of Averages (Runs)
dwell =5  #Dwell time in ms


adw.Set_Par(1, nor)


while avg < noa:
    adw.Start_Process(1) #Start Counter 1 of the ADWin
    # String sent to the Arduino (This string is controlled by the arduino sketch External_Trigger)
    arduino.write('2870000000#2880000000#' + str(nor) + '#' + str(dwell) + '#')
    # arduino.write('287#288#10#')

    t1 = time.perf_counter() #Elapsed time up to this point

    while adw.Process_Status(1) == 1: #While the ADwin is already running, delay the process
        time.sleep(0.0001)

    dataList = adw.GetData_Long(1, 1, nor) # Get the data collected from the ADwin Counter 1
    t2 = time.perf_counter()  # Elapsed time up to this point

    print((len(dataList), ' points done.'))



    print(("It takes: ", t2 - t1, 'for ', nor, " steps"))
    print(list(dataList))

    avg += 1
    print("Average ", avg, " is done")
    #time.sleep(1)

#close ADwin and Arduino
adw.Clear_Process(1)
arduino.close()
rm.close()


