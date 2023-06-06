#include <Adafruit_AHTX0.h>

Adafruit_AHTX0 aht;

void setupAHT() {
  Wire.begin(0,4);
  Serial.begin(115200);
  Serial.println("Adafruit AHT10/AHT20 demo!");
  if (! aht.begin()) {
    Serial.println("Could not find AHT? Check wiring");
    while (1) delay(10);
  }
  Serial.println("AHT10 or AHT20 found");
}

void getHumidTemp() {
  sensors_event_t humidity, temp;
  aht.getEvent(&humidity, &temp);// populate temp and humidity objects with fresh data
  temperature = temp.temperature;
  humid = humidity.relative_humidity;
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println("degrees C" );
  Serial.print("Relative Humidity: ");
  Serial.println(humid);
}
