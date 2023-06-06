int soilPin = 32;//Declare a variable for the soil moisture sensor 
int soilPower = 23;//Variable for Soil moisture Power

void setupMois() 
{
 // pinMode(soilPin, LOW);
  //pinMode(soilPower, OUTPUT);
  //digitalWrite(soilPower, LOW); //Set to LOW so no power is flowing through the sensor
  Serial.begin(115200);
  pinMode(soilPin, INPUT);
}

void getMoisture() 
{
  //digitalWrite(soilPower, HIGH);
  moisture = analogRead(soilPin);
  Serial.print("Moisture: ");
  Serial.println(moisture);
  //digitalWrite(soilPower, LOW);
}
