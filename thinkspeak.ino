#include <SoftwareSerial.h>
#define RX 10
#define TX 11
String AP = "DESKTOP-spiro";       // CHANGE ME
String PASS = "testings"; // CHANGE ME
String HOST = "35.1.5.132";
String PORT = "8080";
int countTrueCommand;
int countTimeCommand; 
boolean found = false; 
int valSensor = 1;
SoftwareSerial esp8266(RX,TX); 
 
  
void setup() {
  Serial.begin(9600);
  esp8266.begin(115200);
  pinMode(A5, INPUT);
  pinMode(A4, INPUT);
  sendCommand("AT",5,"OK");
  sendCommand("AT+RST",5,"OK");
  sendCommand("AT+CWMODE=1",5,"OK");
  sendCommand("AT+CWJAP=\""+ AP +"\",\""+ PASS +"\"",20,"OK");
  sendCommand("AT+CIPMUX=1",5,"OK");
  sendCommand("AT+CIPSTART=0,\"UDP\",\""+ HOST +"\","+ PORT,15,"OK");
}
void loop() {
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
 //sendCommand("AT+CIPCLOSE=0",5,"OK");
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
