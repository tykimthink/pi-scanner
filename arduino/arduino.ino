#include <Servo.h> 
#include <LiquidCrystal.h>

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
Servo servoArm;
 
void setup() 
{ 
  lcd.begin(16, 2);
  servoArm.attach(9);  // attaches the servo on pin 9 to the servo object 
  lcd.print("Ready and");
  lcd.setCursor(0,1);
  lcd.print("waiting!");
} 
 
 
void loop() 
{
  int pos = 0; 
  for(pos = 0; pos < 180; pos += 1) 
  {                                 
    servoArm.write(pos);            
    delay(15);                      
  } 
  for(pos = 180; pos>=1; pos-=1)    
  {                                
    servoArm.write(pos);            
    delay(15);                      
  } 
} 
