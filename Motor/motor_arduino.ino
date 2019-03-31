#include <Servo.h> 
String str;
Servo myservo;
Servo myservo2;

void setup() 
{ 


  myservo.attach(9, 500, 2400); // 修正脈衝寬度範圍
  myservo2.attach(10, 500, 2400);
  myservo.write(0); // 一開始先置中90度
  myservo2.write(90);
  Serial.begin(9600);
  delay(3000);
} 

void loop() 
{
  if (Serial.available()){
    str = Serial.readStringUntil('\n');

     if (str == "deg0"){
        myservo.writeMicroseconds(500);
        delay(1500);
      } else if (str == "deg180"){
        myservo.writeMicroseconds(2400);
        delay(1500);
      }  else if (str == "deg50"){
        myservo.writeMicroseconds(1027);
        delay(1500);
      }  else if (str == "deg110"){
        myservo.writeMicroseconds(1661);
        delay(1500);
      }  else if (str == "deg170"){
        myservo.writeMicroseconds(2294);
        delay(1500);
      } else if (str == "deg45"){
        myservo2.writeMicroseconds(975);
        delay(3000);
        myservo2.writeMicroseconds(1450);//90
        delay(300);
      } else if (str == "deg135"){
        myservo2.writeMicroseconds(1925);
        delay(3000);
        myservo2.writeMicroseconds(1450);//90
        delay(300);
      }
      
  }
  /*for(int i = 500; i <= 2399; i+=633){
    myservo.writeMicroseconds(i); // 直接以脈衝寬度控制

    delay(300);
  }
  for(int i = 2399; i >= 500; i-=633){
    myservo.writeMicroseconds(i);

    delay(300);
  }*/
  //exit(1);
}
