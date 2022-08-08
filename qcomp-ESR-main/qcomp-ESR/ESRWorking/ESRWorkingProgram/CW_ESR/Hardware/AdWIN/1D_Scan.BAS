'<ADbasic Header, Headerversion 001.001>
' Process_Number                 = 1
' Initial_Processdelay           = 4000
' Eventsource                    = External
' Control_long_Delays_for_Stop   = No
' Priority                       = High
' Version                        = 1
' ADbasic_Version                = 5.0.8
' Optimize                       = Yes
' Optimize_Level                 = 1
' Info_Last_Save                 = DUTTLAB8  Duttlab8\Kai
'<Header End>
' 1D_Scan.bas
' Configured as Process 2, Priority High, External trigger.


'#Include ADwinGoldII.inc
'DIM Data_1[1500] AS LONG
'DIM index AS LONG
'
'
'init:
'  Cnt_Enable(0)
'  Cnt_Mode(1,8)          ' Counter 1 set to increasing
'  Cnt_Clear(1)           ' Clear counter 1
'  Cnt_Enable(1)          ' enable counter 1
'
'  index=1
'
'
'event:  'starts after trigger positive edge, ends after negative edge(??)
' 
'  Processdelay = 1000 'added by erin
'  
'  IF (index>=1) THEN 
'    Data_1[index]=Cnt_Read(1)
'  ENDIF
'  Cnt_Clear(1)
'  Inc(index)
'  IF (index>par_1) THEN 'replaced w/ test number par_1
'    END
'  ENDIF
'
'
'finish:
'  Cnt_Enable(0)

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
