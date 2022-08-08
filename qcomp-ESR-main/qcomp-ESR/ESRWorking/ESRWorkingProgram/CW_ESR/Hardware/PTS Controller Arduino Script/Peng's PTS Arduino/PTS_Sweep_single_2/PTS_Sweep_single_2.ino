String incomingByte; // for incoming serial data
String a;
String digit;
String b;
String output;
String d=", ";
int pin[38]={3,2,7,6,5,4,11,10,9,8,25,24,23,22,29,28,27,26,33,32,31,30,37,36,35,34,41,40,39,38,45,44,43,42,49,48,47,46};
float A=2000000000;
float B=3000000000;
int s;
int m=0;
int n=5;
String freq;
int ard;
int str;
String steps;
void setup() {
        Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
        int i,ard,str;
  for (i=2;i<12;i++)
  {
  pinMode(i,OUTPUT);
  }
   for (i=22;i<50;i++)
  {
  pinMode(i,OUTPUT);
  }
  pinMode(14,OUTPUT);
 Serial.begin(9600);
 for (ard=2;ard<12;ard++)
    {
      digitalWrite(ard,HIGH);
     }
     for (ard=22;ard<50;ard++)
      {
        digitalWrite(ard,HIGH);
      }
      digitalWrite(14,LOW);
      Serial.println("Initialized");
     
        
        
}

void loop() {

        // send data only when you receive data:
        
        if (Serial.available() > 0) {
                // read the incoming byte:
                int k;int p;
                steps=Serial.readString();
                s=steps.toInt();
                
                for (k=0;k<s+1;k++){
                     freq=String(k*(B-A)/s+A);
                     incomingByte = freq;
                     a="";b="";output="";
                     int i;
                     for (i=0;i<10;i++){
                          digit = String(incomingByte[i]);
                          //Serial.println(digit);
                          a=String(digit.toInt(),BIN);
                          if (a.length()==3){
                              a=String(0,BIN)+a;}
                          if (a.length()==2){
                              a=String(0,BIN)+String(0,BIN)+a;}
                          if (a.length()==1){
                              a=String(0,BIN)+String(0,BIN)+String(0,BIN)+a;}
                           b+=a;
                          }
                     for (i=0;i<38;i++){
                          if (b[i+2]=='0'){digitalWrite(pin[i],HIGH);}
                          else{digitalWrite(pin[i],LOW); output += pin[i]+d;}
                         }    
                     digitalWrite(14,HIGH);
                     delay(0.1);
                     digitalWrite(14,LOW);
                     delay(20);
                     }
               for (ard=2;ard<12;ard++)
                   {digitalWrite(ard,HIGH);}
               for (ard=22;ard<50;ard++)
                   {digitalWrite(ard,HIGH);} 
               Serial.println("0");
            }
        }

