#include "Si115X.h"
#include <Wire.h>
#include <Arduino.h>
#define SDA 18
#define SCL 19

Si115X si1151 = Si115X();

/**
 * Setup for configuration
 */
void setupSunlight()
{
    Serial.begin(115200);
    uint8_t conf[4];

    Wire.begin(SDA, SCL);
    if (!si1151.Begin())
        Serial.println("Si1151 is not ready!");
    else
        Serial.println("Si1151 is ready!");

}


void getSunlight()
{
    sunlight = si1151.ReadHalfWord_VISIBLE();
    Serial.print("Sunlight: ");
    Serial.println(sunlight);
}
