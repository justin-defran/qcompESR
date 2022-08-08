char freq[45];
int test;
void setup()
{
  int i,ard,str;
  for (i=2;i<12;i++)
  {
  pinMode(i,OUTPUT);
  }
   for (i=22;i<50;i++)
  {
  pinMode(i,OUTPUT);
  }
 Serial.begin(9600);
 for (ard=2;ard<12;ard++)
    {
      digitalWrite(ard,HIGH);
     }
     for (ard=22;ard<50;ard++)
      {
        digitalWrite(ard,HIGH);
      }
      for (str=1;str<39;str++)
      {
       freq[str]='0';
      }
      
  
}

void loop()
{
 char mark;
 int str,ard;
 if (Serial.available()>0)
 {
  mark=Serial.read();
  if (mark=='*')
  {
   while (Serial.available()>0) {mark=Serial.read();}
   Serial.println("PTS3200 Arduino 1.");
  }
  else if (mark=='c')
  {
   while (Serial.available()>0) {mark=Serial.read();}
   for (str=1;str<39;str++)  {Serial.print(freq[str]);}
   Serial.println();
  }
  else if (mark=='F')
  {
   str=0;
   while (Serial.available()>0)
   {
    str++;
    freq[str]=Serial.read();
    if (str<11)
    {
     if (freq[str]=='1') {digitalWrite(str+1,LOW);}
        else  {digitalWrite(str+1,HIGH);}
    }
     else
     {
       if (freq[str]=='1') {digitalWrite(str+11,LOW);}
        else  {digitalWrite(str+11,HIGH);}
     }
   }
   Serial.print("The length of input string is: ");
   Serial.println(str);
  }
  else {Serial.println("Wrong input,please try again.");}
 }
 
     
 
delay(1000);

}
