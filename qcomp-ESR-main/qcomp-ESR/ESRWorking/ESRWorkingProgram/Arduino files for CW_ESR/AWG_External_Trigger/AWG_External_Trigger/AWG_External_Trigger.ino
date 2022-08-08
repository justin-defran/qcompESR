String Start;
String Stop;
String Steps;

float A;
float B;
int s;

String incomingByte; // for incoming serial data
String a;
String b;
String d=", ";
String digit;
int pin[38]={3,2,7,6,5,4,11,10,9,8,25,24,23,22,29,28,27,26,33,32,31,30,37,36,35,34,41,40,39,38,45,44,43,42,49,48,47,46};
int PWMpin = 12;
float freq;
int count = 0;

void setup() {
    Serial.begin(9600); //begin serial comm.
    pinMode(13, OUTPUT); //setting output pin which goes to the adwin counting trigger
    attachInterrupt(2,single_sweep,RISING); //setting the AWGtrigger
    Serial.println("Initialized");
}

void loop() {
  while(Serial.available()>0){ //reading the serial data from python
    Start=Serial.readStringUntil('#');
    Stop=Serial.readStringUntil('#');
    Steps=Serial.readStringUntil('#');
  }
}

void single_sweep(){

static int current_iter = 0; //defining a static variable to memorize the the previous frequency in each trigger

    A=Start.toFloat(); 
    B=Stop.toFloat();
    s=Steps.toInt();

 if(A>0 && freq <= B ) {
    float step_freq;
    step_freq = (B - A)/(s-1);
    int i;
    freq = A + current_iter * step_freq; //adjusting the frequency
    current_iter += 1;
    incomingByte = String(freq);
         a=""; b="";
         
    if (freq <= B){
      // Serial.println(freq);
         for (i=0;i<10;i++){ //this part converts the frequency into a BCD
              digit = String(incomingByte[i]);
              //Serial.println(digit);
              a=String(digit.toInt(),BIN);
              if (a.length()==3){
                  a=String(0,BIN)+a;}
              if (a.length()==2){
                  a=String(0,BIN)+String(0,BIN)+a;}
              if (a.length()==  1){
                  a=String(0,BIN)+String(0,BIN)+String(0,BIN)+a;}
               b+=a;
              }

         for (i=0;i<38;i++){ //this part sets the pin states according to the given frequency
              if (b[i+2]=='0'){digitalWrite(pin[i],HIGH);}
              else{digitalWrite(pin[i],LOW);}
             }
        
         digitalWrite(13,HIGH); //pulse sent to adwin to start counting
         delayMicroseconds(10);
         digitalWrite(13,LOW);
         delayMicroseconds(10);
         
    }
   
   else { //stop the process when the frequency limit is reached
    freq = B+step_freq;
    // Serial.println("Exceeded stop frequency!");
   }
  }
}



