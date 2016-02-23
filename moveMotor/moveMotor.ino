// Run a A4998 Stepstick from an Arduino

int x; 
char inByte;
#define BAUD (9600)


void setup() 
{
  Serial.begin(BAUD);
  pinMode(6,OUTPUT); // Enable
  pinMode(5,OUTPUT); // Step
  pinMode(4,OUTPUT); // Dir
  digitalWrite(6,LOW); // Set Enable low

  pinMode(13, OUTPUT);

  // Set initial state
  digitalWrite(6, HIGH);  // stay still
}

void loop() 
{
  if (Serial.available() > 0){
    inByte = Serial.read();
    switch (inByte) {
      case 'A': // start
        digitalWrite(6, LOW); 
        break;
      case 'B': // stop
        digitalWrite(6, HIGH);
        break;
      case 'C': // reverse
        if (digitalRead(4) == HIGH){
          digitalWrite(4, LOW);
        }
        else
          digitalWrite(4, HIGH);
        break;
      default:
        digitalWrite(6, HIGH); // stop
    }   
  }
  
  digitalWrite(5,HIGH); // Output high
  delay(1); // Wait
  digitalWrite(5,LOW); // Output low
  delay(1); // Wait
}
