<h1>Arduino datu pārraides projekts</h1>

<p>Tīmekļa lapas kods Arduino datu temperatūras, mitruma un apgaismojuma pārraidīšanai uz Django tīmekļa lapu</p>

<h3>Arduino kods</h3>

<p><pre>#include "DHT.h"
#include <<!-- Tag stopper -->WiFi.h>
#include <<!-- Tag stopper -->HTTPClient.h>

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

// LV: Arduino kontroliera WiFi savienojuma nosaukums un parole
// ENG: Arduino controller WiFi connection name and password
const char* ssid = "PvP";
const char* password = "Silver123";

// LV: Sensora ID Django mājas lapā
// ENG: Sensor ID in Django web page
String ID = "Sensors_nr_1001: Rēzekne";

// LV: Gulēšanas laiks sekundēs
// ENG: Sleeping time in seconds
#define uS_TO_S_FACTOR 1000000
#define TIME_TO_SLEEP  300
RTC_DATA_ATTR int bootCount = 0;

// LV: Pamošanās iemesla izvade
// ENG: Wakeup reason printing
void print_wakeup_reason(){
  esp_sleep_wakeup_cause_t wakeup_reason;

  wakeup_reason = esp_sleep_get_wakeup_cause();

  switch(wakeup_reason)
  {
    case ESP_SLEEP_WAKEUP_EXT0 : Serial.println("Wakeup caused by external signal using RTC_IO"); break;
    case ESP_SLEEP_WAKEUP_EXT1 : Serial.println("Wakeup caused by external signal using RTC_CNTL"); break;
    case ESP_SLEEP_WAKEUP_TIMER : Serial.println("Wakeup caused by timer"); break;
    case ESP_SLEEP_WAKEUP_TOUCHPAD : Serial.println("Wakeup caused by touchpad"); break;
    case ESP_SLEEP_WAKEUP_ULP : Serial.println("Wakeup caused by ULP program"); break;
    default : Serial.printf("Wakeup was not caused by deep sleep: %d\n",wakeup_reason); break;
  }
}

void setup(){
  Serial.begin(115200);
  delay(1000);

  ++bootCount;
  Serial.println("Boot number: " + String(bootCount));

  print_wakeup_reason();

  WiFi.begin(ssid, password);
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
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

  // LV: Ieslēd dziļās gulēšanas režīmu
  // ENG: Turns on deep sleep mode
  esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR);
  Serial.println("Setup ESP32 to sleep for every " + String(TIME_TO_SLEEP) +
  " Seconds");

  Serial.println("Going to sleep now");
  delay(1000);
  Serial.flush(); 
  esp_deep_sleep_start();
  Serial.println("This will never be printed");
}

void loop(){}</pre><p>