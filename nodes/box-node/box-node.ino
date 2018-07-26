#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_MMA8451.h>

#define DT 100
#define ADDR 0x06

Adafruit_MMA8451 mma = Adafruit_MMA8451();

const int buzzer = 2;
const int in = 13;

bool buzzing = false;
int opened = 0;
int accel = 0;

void recv(int /*unused*/){
  byte r = Wire.read();
  if(r==1){
    buzzing = true;
    Serial.println("BUZZING");
  }else if (r==254){
    buzzing = false;
  }
  Serial.write(r);
}

void setup(void){
  Serial.begin(115200);
  delay(2000);
  Serial.println();
  Serial.println("- Starting box node. ");

  Wire.begin(ADDR);
  Wire.onReceive(recv);

  if(!mma.begin()){
    Serial.println("- Accelerometer not found. ");
    while(1);
  }

  Serial.println("- Accelerometer found.");

  mma.setRange(MMA8451_RANGE_2_G);
  
  Serial.print("- Range = "); 
  Serial.print(2 << mma.getRange());  
  Serial.println("G");

  pinMode(in, INPUT);
  pinMode(buzzer, OUTPUT);

  Serial.print("- I2C opening on addr: ");
  Serial.println(ADDR);
  Serial.println("- Ready ...");
}

void loop(){
  sensors_event_t e;
  mma.getEvent(&e);

  Serial.print("accel:");
  Serial.println(sqrt(sq(e.acceleration.x) + sq(e.acceleration.y)));

  Serial.print("contact:");
  Serial.println((digitalRead(in)) ? 1 : 0);

  if (Serial.available() > 0) {
   String rec = Serial.readString();
   if(rec == "server/alarm:1") {
    buzzing = true;
   } else if(rec == "server/alarm:0") {
    buzzing = false;
   }
  }

  if(buzzing){
    tone(buzzer, 1000);
  } else {
    noTone(buzzer);
  }
  
  delay(DT);
}


