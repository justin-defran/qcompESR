'<ADbasic Header, Headerversion 001.001>
' Process_Number                 = 1
' Initial_Processdelay           = 3000
' Eventsource                    = External
' Control_long_Delays_for_Stop   = No
' Priority                       = High
' Version                        = 1
' ADbasic_Version                = 6.3.0
' Optimize                       = Yes
' Optimize_Level                 = 1
' Stacksize                      = 1000
' Info_Last_Save                 = DUTTLAB8  Duttlab8\Duttlab
'<Header End>
#Include ADwinGoldII.inc
Dim i as LONG
Dim j as LONG
DIM Data_1[1000] AS LONG
DIM Data_2[1000] AS LONG
init:
  Cnt_Enable(0)
  Cnt_Mode(1,8)          ' Counter 1 set to increasing
  Cnt_Clear(1)           ' Clear counter 1
  
  i=1


event:
  IF (i > (Par_1+9)) THEN
    END
  ENDIF

  Cnt_Enable(1)          ' enable counter 1
  CPU_Sleep(Par_2*100000)  ' count time 300 ns
  Cnt_Enable(0)          ' disable counter 1
  Cnt_Latch(1)
  Data_1[i] = Cnt_Read_Latch(1)
  CPU_Sleep(2000)         ' reset time 2000 ns
 
  Inc(i)
  Cnt_Clear(1)


finish:
  Cnt_Enable(0)
