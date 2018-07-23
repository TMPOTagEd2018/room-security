#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_MMA8451.h>

#define ADDR 0x06
#define DT 100

Adafruit_MMA8451 mma = Adafruit_MMA8451();

const int in = 13;

int opened = 0;
int accel = 0;

void setup(void)
{
  Serial.begin(115200);
  delay(2000);
  Serial.println();
  Serial.println("- Starting door node.");

  Wire.begin(ADDR);
  Wire.onRequest(send);

  if (!mma.begin())
  {
    Serial.println("- Accelerometer not found.");
    while (1)
      ;
  }
  Serial.println("- Accelerometer found.");

  mma.setRange(MMA8451_RANGE_2_G);

  Serial.print("- Range = ");
  Serial.print(2 << mma.getRange());
  Serial.println("G");

  pinMode(in, INPUT);

  Serial.print("- I2C opening on addr: ");
  Serial.println(ADDR);
  Serial.println("- Ready.");
}

void loop()
{
  sensors_event_t e;
  mma.getEvent(&e);

  accel = pow(, 10);
  opened = (digitalRead(in)) ? 1 : 0;

  Serial.print("accel:");
  Serial.println(e.acceleration.z);

  Serial.print("contact:");
  Serial.println(opened);

  delay(DT);
}

void send()
{
  Wire.write(opened);
  Wire.write(accel);
}