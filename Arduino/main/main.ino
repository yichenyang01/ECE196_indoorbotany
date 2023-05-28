int humid;
int temperature;
int sunlight;
int moisture;

void setup(){
  setupServer();
  setupAHT();
  setupMois();
}

void loop(){
  getHumidTemp();
  getMoisture();
  serverHost();
}
