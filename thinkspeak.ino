#include <SoftwareSerial.h>
#include <avr/sleep.h>
#define RX 10
#define TX 11
String AP = "DESKTOP-spiro";       // CHANGE ME
String PASS = "testings"; // CHANGE ME
String HOST = "35.3.85.203";
String PORT = "8080";
int countTrueCommand;
int countTimeCommand; 
boolean found = false; 
int valSensor = 1;
boolean buttonPressed = false;
SoftwareSerial esp8266(RX,TX); 
 
  
void setup() {
  Serial.begin(9600);
  esp8266.begin(115200);
  pinMode(A5, INPUT);
  pinMode(A4, INPUT);
  pinMode(2, INPUT_PULLUP);
  pinMode(13, OUTPUT);
  attachInterrupt(0, buttonISR, RISING);
  digitalWrite(2, LOW);
  boot();
}

void boot() {
  sendCommand("AT",5,"OK");
  sendCommand("AT+RST",5,"OK");
  sendCommand("AT",5,"OK");
  sendCommand("AT+CWMODE=1",5,"OK");
  sendCommand("AT+CWJAP=\""+ AP +"\",\""+ PASS +"\"",20,"OK");
  sendCommand("AT+CIPMUX=1",5,"OK");
  sendCommand("AT+CIPSTART=0,\"UDP\",\""+ HOST +"\","+ PORT,15,"OK");
}

void loop() {
  if (buttonPressed) {
    delay(10);     // debounce button press
    while (digitalRead(2)) {}    // wait for it to be released
    delay(10);     // debounce button release
    digitalWrite(13, LOW);    // turn off LED

    Serial.println("Going to sleep...");
    Serial.flush();
    gotoSleep();    // function to put the processor to sleep; a button press will wake it up

    delay(10);     // debounce button press
    while (!digitalRead(2)) {}    // wait for it to be released
    delay(10);     // debounce button release
    buttonPressed = false;
    Serial.println("Awake!");
    Serial.flush();
    boot();
  }

  
 int sensor_volume = analogRead(A5);
 int sensor_flow = analogRead(A4);
 Serial.print("\n AAAAAAAAAAA " + String(sensor_volume));
 Serial.print("\n BBBBBBBBBBB " + String(sensor_flow));
 String getData = "POST /api/v1/reading "+String(sensor_volume)+","+String(sensor_flow)+"\n";
 sendCommand("AT+CIPSEND=0," +String(getData.length()+4),4,">");
 esp8266.println(getData);
 Serial.print(getData);
 delay(50);
 countTrueCommand++;
}

void buttonISR() { buttonPressed = true; }

void gotoSleep()
{
  set_sleep_mode (SLEEP_MODE_PWR_DOWN);
  noInterrupts();           // timed sequence follows
  sleep_enable();

  // turn off brown-out enable in software
  MCUCR = bit (BODS) | bit (BODSE);  // turn on brown-out enable select
  MCUCR = bit (BODS);        // this must be done within 4 clock cycles of above
  
  ADCSRA = 0;
  interrupts();             // guarantees next instruction executed
  
  
  sleep_cpu();              // nighty-night!
  sleep_disable();          // awake again -- cancel sleep as a precaution
}

void sendCommand(String command, int maxTime, char readReplay[]) {
  Serial.print(countTrueCommand);
  Serial.print(". at command => ");
  Serial.print(command);
  Serial.print(" ");
  while(countTimeCommand < (maxTime*1))
  {
    esp8266.println(command);//at+cipsend
    if(esp8266.find(readReplay))//ok
    {
      found = true;
      break;
    }
  
    countTimeCommand++;
  }
  
  if(found == true)
  {
    Serial.println("OYI");
    countTrueCommand++;
    countTimeCommand = 0;
  }
  
  if(found == false)
  {
    Serial.println("Fail");
    countTrueCommand = 0;
    countTimeCommand = 0;
  }
  
  found = false;
 }
