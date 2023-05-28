int humidity;
int temperature;
int sunlight;
int moisture;

void setup(){
  setupServer();
  setupAHT;
}

void loop(){
  getHumidity();
  serverHost();
}
