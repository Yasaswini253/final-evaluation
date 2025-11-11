#include "DHT.h"

#define DHTPIN 4       // GPIO pin where DHT11 is connected
#define DHTTYPE DHT11  // Sensor type: DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
  delay(2000);  // Give time for sensor to stabilize
  Serial.println("DHT11 Sensor Initialized");
}

void loop() {
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();  // Celsius by default

  // Check if readings are valid
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT11 sensor!");
  } else {
    // Send data in comma-separated format for Python
    Serial.print(temperature, 1);
    Serial.print(",");
    Serial.println(humidity, 1);
  }

  delay(2000);  // Wait 2 seconds before next reading
}
