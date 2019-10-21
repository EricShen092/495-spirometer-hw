
#include <SoftwareSerial.h>

SoftwareSerial BTserial(10, 11); // RX | TX
void setup() {
  BTserial.begin(9600); 
}

void loop() {

  BTserial.print("Side: ");
  BTserial.print(analogRead(A5));
  BTserial.print("\n");
  BTserial.print("Middle: ");
  BTserial.print(analogRead(A4));
  BTserial.print("\n");
  BTserial.print("\n");
  
  
  //message to the receiving device
  //One second delay
  delay(1000);

}
