'<ADbasic Header, Headerversion 001.001>
' Process_Number                 = 1
' Initial_Processdelay           = 150000
' Eventsource                    = Timer
' Control_long_Delays_for_Stop   = No
' Priority                       = High
' Version                        = 1
' ADbasic_Version                = 5.0.8
' Optimize                       = Yes
' Optimize_Level                 = 1
' Info_Last_Save                 = DUTTLAB8-PC  Duttlab8-PC\Duttlab8
'<Header End>


#Include ADwinGoldII.inc
DIM Data_1[1000] AS LONG
DIM i AS LONG


init:
  Cnt_Enable(0)
  Cnt_Clear(1)           ' Clear counter 1
  Cnt_Mode(1,8)          ' Counter input external
  Cnt_Enable(1)         ' enable counter 1
  i=1               ' step 1



event:
  Data_1[i] = Cnt_Read(1)
  Cnt_Clear(1)
  Inc(i)
  IF (i>par_1) THEN
    END
  ENDIF





finish:
  Cnt_Enable(0)
