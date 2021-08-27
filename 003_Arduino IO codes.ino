// For normal white/dark assay

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(12, OUTPUT);  // For white LED
  pinMode(4, OUTPUT);  // For Valve1
  pinMode(5, OUTPUT);  // For Valve2
  pinMode(7, OUTPUT);  // For Triggering SD9
  pinMode(8, OUTPUT);  // For Vibration Motor
  
  Serial.write('5');
}
  int x;
  int var;
  

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() > 0) {
    x = Serial.parseInt();
    
    switch (x) {
      default:
        digitalWrite(12, HIGH);
        digitalWrite(4, LOW);
        digitalWrite(5, LOW);
        digitalWrite(7, LOW);
        digitalWrite(8, LOW);
        Serial.write('5');
        break;
      case 3:  // For Light Off Phase
        digitalWrite(12, LOW);
        Serial.write('5');
        break;
      case 4:  // For Light On Phase
        digitalWrite(12, HIGH);
        Serial.write('5');
        break;
      case 5:  // For Turning Off Everything Except the light
        digitalWrite(4, LOW);
        digitalWrite(5, LOW);
        digitalWrite(7, LOW);
        Serial.write('5');
        break;
      case 11:  // For Turn on Valve1
        digitalWrite(4, HIGH);
        Serial.write('5');
        break;
      case 12:  // For Turn off Valve1
        digitalWrite(4, LOW);
        Serial.write('5');
        break;
      case 13:  // For Turn on Valve2
        digitalWrite(5, HIGH);
        Serial.write('5');
        break;
      case 14:  // For Turn off Valve2
        digitalWrite(5, LOW);
        Serial.write('5');
        break;
      case 15:  // For Turn on Vibration/SD9
        var = 0;
        digitalWrite(4, HIGH); // Turn on the Relay for SD9
        while (var < 1800) {
          // do something repetitive 1800 times
          var++;        
          digitalWrite(7, HIGH); // Trigger SD9
          delay(500);
          digitalWrite(7, LOW); // Reset SD9
          delay(500);
        }
        digitalWrite(4, LOW); // Turn off the Relay for SD9
        Serial.write('5');
        break;
      case 16:  // For Turning off Vibration/SD9
        digitalWrite(7, LOW); // Reset SD9
        digitalWrite(4, LOW); // Turn off the Relay for SD9
        Serial.write('5');
        break;
      case 17:  // For Turning on Vibration Motor
        digitalWrite(8, HIGH); // Trigger SD9
        delay(100);
        digitalWrite(8, LOW); // Reset SD9
        Serial.write('5');
        break;
    }
  }
}
