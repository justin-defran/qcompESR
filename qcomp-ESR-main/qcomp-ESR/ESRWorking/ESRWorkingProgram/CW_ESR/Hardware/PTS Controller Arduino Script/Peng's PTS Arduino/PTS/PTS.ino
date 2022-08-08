int incomingByte = 0;
String inData;
String output;
String a=", ";
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
      Serial.println("System initialization is complete.");
     
}

void loop() {
    while (Serial.available() > 0)
    {
        char recieved = Serial.read();
        inData += recieved; 
        
        // Process message when new line character is recieved
        if (recieved == '.')
        {
            Serial.println("Arduino Received: ");
            Serial.println(inData);
            int i;
            for (i=0;i<38;i++)
            {if (inData[i+2]=='0'){digitalWrite(pin[i],HIGH);}
            else{digitalWrite(pin[i],LOW);
                 output += pin[i]+a;}
            }
        Serial.println("Pins set LOW: " + output);    
            

            inData = ""; // Clear recieved buffer
        }
    }
}

