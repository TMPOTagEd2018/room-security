#include <Wire.h>
#include <math.h>

#include <Adafruit_TSL2561_U.h>
#include <SparkFunLSM9DS1.h>
#include <Adafruit_Sensor.h>

Adafruit_TSL2561_Unified tsl = Adafruit_TSL2561_Unified(TSL2561_ADDR_FLOAT, 12345);

LSM9DS1 imu;

#define LSM9DS1_M  0x1E
#define LSM9DS1_AG  0x6B

#define ADDR 0x06

#define DT 250

int lux = 0;
int ang = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  delay(2000);
  Serial.println();

  Wire.begin(ADDR);
  Wire.onReceive(recv);
  Wire.onRequest(send);

  imu.settings.device.commInterface = IMU_MODE_I2C;
  imu.settings.device.mAddress = LSM9DS1_M;
  imu.settings.device.agAddress = LSM9DS1_AG;
  
  if (! imu.begin()) {
    Serial.println("GYRO NOT FOUND");
    while (1);
  }
  Serial.println("Gyro found!");

   // Make sure Lux is in
  if(!tsl.begin()){
    Serial.println("LUX NOT FOUND");
    while(1);
  }
  Serial.println("Lux found!");

  configLux();


  Serial.print("I2c opening on addr: ");
  Serial.println(ADDR);
  Serial.println("Ready ...");

}

void configLux(void)
{
  /* You can also manually set the gain or enable auto-gain support */
  // tsl.setGain(TSL2561_GAIN_1X);      /* No gain ... use in bright light to avoid sensor saturation */
  // tsl.setGain(TSL2561_GAIN_16X);     /* 16x gain ... use in low light to boost sensitivity */
  tsl.enableAutoRange(true);          /* Auto-gain ... switches automatically between 1x and 16x */
  
  /* Changing the integration time gives you better sensor resolution (402ms = 16-bit data) */
  tsl.setIntegrationTime(TSL2561_INTEGRATIONTIME_13MS);      /* fast but low resolution */
  // tsl.setIntegrationTime(TSL2561_INTEGRATIONTIME_101MS);  /* medium resolution and speed   */
  // tsl.setIntegrationTime(TSL2561_INTEGRATIONTIME_402MS);  /* 16-bit data but slowest conversions */
 
  /* Update these values depending on what you've set above! */  
  Serial.println("------------------------------------");
  Serial.print  ("Gain:         "); Serial.println("Auto");
  Serial.print  ("Timing:       "); Serial.println("13 ms");
  Serial.println("------------------------------------");
}

void loop() { 
  sensors_event_t luxE;
  tsl.getEvent(&luxE);
  lux = constrain(luxE.light, -127, 127);
  Serial.print("Light: ");
  Serial.println(lux);

  if(imu.gyroAvailable()){
    imu.readGyro();
  }

  ang = constrain(imu.calcGyro(imu.gy), -127, 127);
  Serial.print("Gyro: ");
  Serial.println(ang);
  
  delay(DT);
}

void recv(int){
  byte r = Wire.read();
  Serial.println(r);
}

void send(){
  Wire.write(lux);
  Wire.write(ang);
}

