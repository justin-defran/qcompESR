

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin 13 as an output.
  pinMode(13, OUTPUT);
  Serial.begin(9600);
  digitalWrite(13, LOW);
}

// the loop function runs over and over again forever
void loop() {
  char mark;
  int len;
  len=0;
  if (Serial.available()>0)
    {len=Serial.available();
      while (Serial.available()>0) 
      {mark=Serial.read();
      if (mark=='\r') 
        {digitalWrite(13, HIGH);
        delay(1000);}
      }
     Serial.println("nu");
    }
  
  delay(1000);              // wait for 1 second
}
