#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_MMA8451.h>

#define ADDR 0x06
#define DT 250

Adafruit_MMA8451 mma = Adafruit_MMA8451();

const int buzzer = 2;
const int in = 13;

int buzzing = -1;
int opened = 0;
int accel = 0;

void setup(void){
  Serial.begin(115200);
  delay(2000);
  Serial.println();
  Serial.println("Starting box node");

  Wire.begin(ADDR);
  Wire.onReceive(recv);
  Wire.onRequest(send);

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

  if(buzzing == 1){
    tone(buzzer, 1000);
  } else {
    noTone(buzzer);
  }
  
  delay(DT);
}

void recv(int){
  byte r = Wire.read();
  if(r == 1){
    buzzing = 1;
    Serial.println("BUZZING");
  } 
  if(r == 0){
    if(buzzing == 1){ Serial.println("STOPPED BUZZING"); }
    buzzing = false;
  }
}

void send(){
  Wire.write(opened);
  Wire.write(accel);
}

