'<ADbasic Header, Headerversion 001.001>
' Process_Number                 = 1
' Initial_Processdelay           = 4000
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
' 1D_Scan.bas
' Configured as Process 1, Priority High, External trigger.


#Include ADwinGoldII.inc
DIM Data_1[1000] AS LONG
DIM i AS LONG



init:
  Cnt_Enable(0)
  Cnt_Mode(1,8)          ' Counter 1 set to increasing
  Cnt_Clear(1)           ' Clear counter 1
  Cnt_Enable(1)          ' enable counter 1

  i=0



event:
  
  IF (i > Par_1) THEN
    END
  ENDIF
  
  Data_1[i] = Cnt_Read(1)
  
  
  Inc(i)
  Cnt_Clear(1)
  
finish:
  Cnt_Clear(1)
  Cnt_Enable(0)
