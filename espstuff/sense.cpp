#include <OneWire.h>
#include <DallasTemperature.h>

const int oneWireBus=4;
OneWire oneWire(oneWireBus);

DallasTemperature sensors(&oneWire);

int _moisture, sensor_analog;

const int sensor_pin = 34;

void setup()
{
  Serial.begin(115200);
  sensors.begin();
}

void loop(){
  sensors.requestTemperatures();
  float temperatureC = sensors.getTempCByIndex(0);
  sensor_analog = analogRead(sensor_pin);
  _moisture = (100-(sensor_analog/4095.00)*100);
  Serial.print(temperatureC);
  Serial.print(",");
  Serial.println(_moisture);
  delay(1000);
}