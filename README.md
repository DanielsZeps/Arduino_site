<h1>Arduino datu pārraides projekts</h1>

<p>Tīmekļa lapas kods Arduino datu temperatūras, mitruma un apgaismojuma pārraidīšanai uz Django tīmekļa lapu</p>

<h3>Arduino kods</h3>

<p>
<pre>#include "DHT.h"
#include <WiFi.h>
#include <HTTPClient.h>

// LV: DHT sensora parametri
// ENG: DHT sensr parameters
#define DHTPIN 2
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

// LV: Gaismas rezistora parametri
// ENG: Light resistor parameters
const int ldrPin = 4;
const float GAMMA = 0.7;
const float RL10 = 20;
const int R1 = 10000;

// LV: Gulēšanas laiks sekundēs
// ENG: Sleeping time in seconds
#define uS_TO_S_FACTOR 1000000
#define TIME_TO_SLEEP  300

// LV: Arduino kontroliera WiFi savienojuma nosaukums un parole
// ENG: Arduino controller WiFi connection name and password
const char* ssid = "PvP";
const char* password = "Silver123";

// LV: Sensora ID Django mājas lapā
// ENG: Sensor ID in Django web page
String ID = "Sensors_nr_1001: Rēzekne";

void setup(){
  // LV: Atļautie WiFi savienojuma mēģinājumi
  // ENG: Allowed WiFi connection try ammount
  int wif_connection_tries_left = 20;

  WiFi.begin(ssid, password);
  while(WiFi.status() != WL_CONNECTED && wif_connection_tries_left > 0) {
    delay(500);
    wif_connection_tries_left -= 1;
  }
  if (wif_connection_tries_left > 0) {
    if(WiFi.status()== WL_CONNECTED){
      HTTPClient http;

      pinMode(ldrPin, INPUT);
      dht.begin();
      analogReadResolution(12);  
      analogSetAttenuation(ADC_11db);

      float h = dht.readHumidity();
      float t = dht.readTemperature();
      int analogValue = analogRead(ldrPin);
      float lux = NAN;
      if (analogValue != 0) {
        float voltage = analogValue / 4095.0 * 3.3;
        float resistance = R1 * voltage / (3.3 - voltage); // Corrected formula
        float lux = pow(RL10 * 1e3 * pow(10, GAMMA) / resistance, (1 / GAMMA)) * 3.70233246946;
      }
      String serverPath = "https://daniels0zeps.eu.pythonanywhere.com/sensor/" + ID + "/" + String(lux) + "/" + String(t) + "/" + String(h);

      http.begin(serverPath);
      int httpResponseCode = http.GET();
      
      http.end();
    }
  }

  // LV: Ieslēd dziļās gulēšanas režīmu
  // ENG: Turns on deep sleep mode
  delay(1000);
  Serial.flush(); 
  esp_deep_sleep_start();
}

void loop(){}</pre>
<p>