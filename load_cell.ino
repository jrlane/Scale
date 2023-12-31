#include "HX711.h"

// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = 2;
const int LOADCELL_SCK_PIN = 3;

float calibration_factor = 3920;

HX711 scale;

void setup() {
  Serial.begin(57600);
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale.set_scale(calibration_factor);
  delay(1000);
  scale.tare();
}

void loop() {

  if (scale.wait_ready_retry(10)) {
    //long reading = scale.read();
    //Serial.print("HX711 reading: ");
    //Serial.println(reading);
  //Serial.print("Reading: ");
  Serial.print(scale.get_units(), 1);
  //Serial.print(" lbs");
  //Serial.print(" calibration_factor: ");
  //Serial.print(calibration_factor);
  Serial.println();
  } else {
    //Serial.println("HX711 not found.");
  }

  delay(100);
  
}
