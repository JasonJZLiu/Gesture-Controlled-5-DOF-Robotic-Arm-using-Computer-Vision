#include <Servo.h>
Servo Base;
Servo Arm1;
Servo Arm2;
Servo Wrist;
Servo Tilt;
Servo Claw;

/*----------------The following values are the initial servo values----------------*/
int base_angle = 90;
int arm1_angle = 72;
int arm2_angle = 74;
int wrist_angle;
int tilt_angle = 60;
int claw_angle;
/*---------------------------------------------------------------------------------*/

int incoming[3];

void setup() {
  Base.attach(3);
  Arm1.attach(5);
  Arm2.attach(6);
  Wrist.attach(9);
  Tilt.attach(10);
  Claw.attach(11);
  
  Base.write(base_angle);
  Arm1.write(arm1_angle);
  Arm2.write(arm2_angle);
  Tilt.write(tilt_angle);
  
  Serial.begin(9600);

}

void loop() {
  while(Serial.available() >= 3){
    for (int i = 0; i < 3; i++){
      incoming[i] = Serial.read();
    }

    arm1_angle = incoming[0];
    arm2_angle = incoming[1];
    tilt_angle = incoming[2];
    Arm1.write(arm1_angle);
    Arm2.write(arm2_angle);
    Tilt.write(tilt_angle);
  }
}
