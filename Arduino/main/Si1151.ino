#include "Si115X.h"

Si115X si1151 = Si115X();

/**
 * Setup for configuration
 */
void setupSunlight()
{
    uint8_t conf[4];

    Wire.begin();
    if (!si1151.Begin())
        Serial.println("Si1151 is not ready!");
    else
        Serial.println("Si1151 is ready!");

}


void getSunlight()
{
    sunlight = si1151.ReadHalfWord_VISIBLE();
}
