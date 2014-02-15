#include <Servo.h> 
#include <LiquidCrystal.h>

#define CMD_DELIM '_'

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
Servo servoArm;
int bufSize = 16;
boolean idle = true;

void setup() 
{ 
  Serial.begin(9600);
  lcd.begin(16, 2);
  servoArm.attach(9);  // attaches the servo on pin 9 to the servo object 
  lcd.print("   Ready and");
  lcd.setCursor(0,1);
  lcd.print("    waiting!");
} 
 
int extractInt(char buf[], int lsb, int msb)
{
  int tr = 0;
  int pow = 1;
  int i = lsb;
  for(i; i >= msb; i--)
  {
    tr += pow * (buf[i] - 48);
    pow = pow * 10;
  }
  return tr;
}
 
void loop() 
{
  if(Serial.available())
  {
    idle=false;
    char buf [bufSize];
    int bytesRead = Serial.readBytesUntil(CMD_DELIM, buf, bufSize);
    
    if(buf[0] == 71 and buf[1] == 84)
    {
       lcd.clear();
       lcd.print("Moving Servo To:");
       lcd.setCursor(0,1);
       int moveTo = extractInt(buf, 4, 2);
       lcd.print(String(moveTo));
       servoArm.write(moveTo);
    }
    else
    {
       lcd.clear();
       lcd.print("Bad Command:");
       lcd.setCursor(0,1);
       int i;
       for(i=0; i<bufSize; i++);
       {
         lcd.print(char(buf[i]));
       }
    }
    delay(1000);
  }
  else
  {
    if(idle == false)
    {
      lcd.clear();
      lcd.print("Idle. Continuing");
      lcd.setCursor(0,1);
      lcd.print("happily...!");
      idle=true;
    }
  }
} 
