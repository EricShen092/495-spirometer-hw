/*
 * Simple code to read in analog values from IR sensors
 * 
 */

void setup()                    // run once, when the sketch starts
{
 Serial.begin(9600);            // set the baud rate to 9600, same should be of your Serial Monitor
 pinMode(A5, INPUT);
 pinMode(A4, INPUT);
}

void loop()
{
    Serial.println("Side");
    Serial.println(analogRead(A5));
    Serial.println("Middle");
    Serial.println(analogRead(A4));
    delay(500);                 // 0.5 second delay
}
