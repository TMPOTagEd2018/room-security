#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_MMA8451.h>

#define DT 100

Adafruit_MMA8451 mma = Adafruit_MMA8451();

const int buzzer = 2;
const int in = 13;

bool buzzing = false;
int opened = 0;
int accel = 0;

void setup(void){
  Serial.begin(115200);
  delay(2000);
  Serial.println();
  Serial.println("Starting box node");

  if(!mma.begin()){
    Serial.println("ACCEL NOT FOUND");
    while(1);
  }
  Serial.println("Accel found!");

  mma.setRange(MMA8451_RANGE_2_G);
  
  Serial.print("Range = "); Serial.print(2 << mma.getRange());  
  Serial.println("G");

  pinMode(in, INPUT);
  pinMode(buzzer, OUTPUT);

  Serial.print("I2c opening on addr: ");
  Serial.println(ADDR);
  Serial.println("Ready ...");
}

void loop(){
  sensors_event_t e;
  mma.getEvent(&e);

  accel = sqrt(pow(e.acceleration.x, 2) + pow(e.acceleration.y, 2) + pow(e.acceleration.z, 2)) - 9;
  opened = (digitalRead(in)) ? 1 : 0;

  accel = constrain(accel, -127, 127);

  Serial.print("Acceleration: ");
  Serial.print(accel);
  Serial.print(", ");
  if(byte(accel) > 128){
    Serial.println((byte)accel - 256);
  } else {
    Serial.println(byte(accel));
  }
  Serial.print("Opened: ");
  Serial.println(opened);

  if (Serial.available() > 0) {
    char* rec = Serial.readString();
    
  }

  if(buzzing){
    tone(buzzer, 1000);
  } else {
    noTone(buzzer);
  }
  
  delay(DT);
}
