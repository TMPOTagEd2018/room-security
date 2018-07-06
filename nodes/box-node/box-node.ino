#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_MMA8451.h>

#define ADDR 0x06
#define DT 100

Adafruit_MMA8451 mma = Adafruit_MMA8451();

const int in = 13;
int opened = 0;
int accel = 0;

void setup(void){
  Serial.begin(115200);
  delay(2000);
  Serial.println();
  Serial.println("Starting box nodes");

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

  Serial.print("I2c opening on addr: ");
  Serial.println(ADDR);
  Serial.println("Ready ...");
}

void loop(){
  sensors_event_t e;
  mma.getEvent(&e);

  accel = sqrt(pow(e.acceleration.x, 2) + pow(e.acceleration.y, 2) + pow(e.acceleration.z, 2)) - 9;
  Serial.print("Acceleration: ");
  Serial.println(accel);

  opened = (digitalRead(in)) ? 1 : 0;
  Serial.print("Opened: ");
  Serial.println(opened);
  delay(DT);
}

void recv(int){
  byte r = Wire.read();
  Serial.println(r);
}

void send(){
  Wire.write(accel);
}

