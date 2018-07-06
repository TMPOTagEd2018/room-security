#include <Wire.h>
#include <math.h>

#include <SparkFunLSM9DS1.h>

LSM9DS1 imu;

#define LSM9DS1_M  0x1E
#define LSM9DS1_AG  0x6B

#define ADDR 0x06
#define DT 100

const int in = 13;

int opened = 0;
int ang = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  delay(2000);
  Serial.println();
  Serial.println("Hello");

  Wire.begin(ADDR);
  Wire.onReceive(recv);
  Wire.onRequest(send);
  
  imu.settings.device.commInterface = IMU_MODE_I2C;
  imu.settings.device.mAddress = LSM9DS1_M;
  imu.settings.device.agAddress = LSM9DS1_AG;

  if (!imu.begin()) {
    Serial.println("GYRO NOT FOUND");
    while(1);
  }
  Serial.println("Gyro found!");

  pinMode(in, INPUT);

  Serial.print("I2c opening on addr: ");
  Serial.println(ADDR);
  Serial.println("Ready ...");

}



void loop() { 
  if(imu.gyroAvailable()){
    imu.readGyro();
  }

  ang = constrain(imu.calcGyro(imu.gy), -127, 127);
  Serial.print("Gyro: ");
  Serial.println(ang);

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
  //Wire.write(0x00 << 1);
  Wire.write(ang);
  //Wire.write(openned);
}

