char freq[45];
int pin[38]={3,2,7,6,5,4,11,10,9,8,25,24,23,22,29,28,27,26,33,32,31,30,37,36,35,34,41,40,39,38,45,44,43,42,49,48,47,46};
void setup() {
  // put your setup code here, to run once:
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
   for (str=0;str<38;str++)  {Serial.print(freq[str]);}
   Serial.println();
  }
  else if (mark=='F')
  {
   str=0;
   while (Serial.available()>0)
   {
    
    freq[str]=Serial.read();
    if (freq[str]=='1') {digitalWrite(pin[str],LOW);}
        else  {digitalWrite(pin[str],HIGH);}
    str++;
   }
   Serial.print("The length of input string is: ");
   Serial.println(str);
  }
  else {Serial.println("Wrong input,please try again.");}
 }
 
     
 
delay(1000);

}
