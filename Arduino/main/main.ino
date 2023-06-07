int humid;
int temperature;
int sunlight;
int moisture;
int timeActive = 0;

void setup(){
  //setupServer();
  setupAHT();
  //setupMois();
  setupSunlight();
  //setupLCD();

}

void loop(){
  getHumidTemp();
  //getMoisture();
  getSunlight();
  //serverHost();
  //updateLCD();
  
}
