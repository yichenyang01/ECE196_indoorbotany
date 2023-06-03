int humid;
int temperature;
int sunlight;
int moisture;

void setup(){
  setupServer();
  
  setupAHT();
  setupMois();
  setupSunlight();
  
  setupLCD();
}

void loop(){
  getHumidTemp();
  getMoisture();
  getSunlight();
  serverHost();
  updateLCD();
}
