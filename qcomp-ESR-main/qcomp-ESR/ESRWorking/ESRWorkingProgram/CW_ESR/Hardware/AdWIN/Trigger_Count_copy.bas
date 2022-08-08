'<ADbasic Header, Headerversion 001.001>
' Process_Number                 = 2
' Initial_Processdelay           = 4000
' Eventsource                    = External
' Control_long_Delays_for_Stop   = No
' Priority                       = High
' Version                        = 1
' ADbasic_Version                = 5.0.8
' Optimize                       = No
' Info_Last_Save                 = DUTTLAB8  Duttlab8\Kai
'<Header End>
' 1D_Scan.bas
' Configured as Process 2, Priority High, External trigger.


#Include ADwinGoldII.inc
DIM year, mon, day, h,m,s As Long
DIM Data_1[1000] AS LONG
DIM index AS LONG


init:
  Cnt_Enable(0)
  Cnt_Clear(15)
  Cnt_Mode(1,8)
  Cnt_Mode(2,0)
  Cnt_Mode(3,0)
  Cnt_Mode(4,0)          ' Counter 1 set to increasing
  ' Cnt_Enable(1)          ' enable counter 1
  'Cnt_Clear(1)           ' Clear counter 1
  Cnt_Enable(15)
  index=1
  Processdelay=30000
  Par_10=300000000/Processdelay


event:

    
  'IF (index>0) THEN
  Data_1[index]=Cnt_Read(1)
  Cnt_Clear(1)
  'ENDIF

  'IF (index>10) THEN
  '  END
  'ENDIF

  'Cnt_Clear(1)
  'Inc(index)
  index = index+1
finish:
  Cnt_Enable(0)
