/*
  LiquidCrystal Library - Serial Input
 
 Demonstrates the use a 16x2 LCD display.  The LiquidCrystal
 library works with all LCD displays that are compatible with the 
 Hitachi HD44780 driver. There are many of them out there, and you
 can usually tell them by the 16-pin interface.
 
 This sketch displays text sent over the serial port 
 (e.g. from the Serial Monitor) on an attached LCD.
 
 The circuit:
 * LCD RS pin to digital pin 12
 * LCD Enable pin to digital pin 11
 * LCD D4 pin to digital pin 5
 * LCD D5 pin to digital pin 4
 * LCD D6 pin to digital pin 3
 * LCD D7 pin to digital pin 2
 * LCD R/W pin to ground
 * 10K resistor:
 * ends to +5V and ground
 * wiper to LCD VO pin (pin 3)
 
 Library originally added 18 Apr 2008
 by David A. Mellis
 library modified 5 Jul 2009
 by Limor Fried (http://www.ladyada.net)
 example added 9 Jul 2009
 by Tom Igoe 
 modified 22 Nov 2010
 by Tom Igoe
 
 This example code is in the public domain.
 
 http://arduino.cc/en/Tutorial/LiquidCrystalSerial
 */

// include the library code:
#include <LiquidCrystal.h>

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(12, 11, 10, 5, 4, 3, 2);
int backLight = 13;

byte degree[8] = {
  0b01000,
  0b10100,
  0b01000,
  0b00000,
  0b00000,
  0b00000,
  0b00000,
  0b00000
};

byte minute[8] = {
  0b01000,
  0b01000,
  0b01000,
  0b00000,
  0b00000,
  0b00000,
  0b00000,
  0b00000
};

byte second[8] = {
  0b01010,
  0b01010,
  0b01010,
  0b00000,
  0b00000,
  0b00000,
  0b00000,
  0b00000
};

int incoming = 0;   // for incoming serial data

void setup() {
  // create a new character
  lcd.createChar(1, degree); 
  lcd.createChar(2, minute); 
  lcd.createChar(3, second); 
  // set up the LCD's number of columns and rows: 
  lcd.begin(16, 2);
  // initialize the serial communications:
  Serial.begin(9600);
  pinMode(backLight, OUTPUT);
  digitalWrite(backLight, HIGH); // turn backlight on. Replace 'HIGH' with 'LOW' to turn it off.
}

void loop()
{
  // when characters arrive over the serial port...
  if (Serial.available()) {
    // wait a bit for the entire message to arrive
    delay(100);
    // clear the screen
    lcd.clear();
    // read all the available characters
    while (Serial.available() > 0) {
      // display each character to the LCD
      incoming = Serial.read();
      switch (incoming) {
      case 34: // "
        lcd.write(3);
        break;
      case 39: // '
        lcd.write(2);
        break;
      case 42: // *
        lcd.write(1);
        break;
      case 17:
        lcd.setCursor(0, 1);
        break;
      case 18:
        lcd.home();
        break;
      case 24:
        lcd.clear();
        break;
      default: 
        lcd.write(char(incoming));
      }
    }
  }
}


