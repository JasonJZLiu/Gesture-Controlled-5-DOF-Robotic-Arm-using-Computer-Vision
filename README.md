# Gesture-Controlled 5-DOF Robotic Arm using Computer Vision
This is the code for my "Gesture Controlled 5 DOF Robotic Arm using Computer Vision" project. I created a gesture-controlled, 3D-printable, 5-degrees-of-freedom, desktop-sized robotic arm. The robotic arm is actuated using three standard servos and two micro servos. The arm is able to mimic human arm movements, which are detected using the Python OpenCV library. The PWM signals of the servos are processed in Python and sent to an Arduino Uno via serial.

## How to use this program:
To use this software package, upload the Arduino code to an Arduino first. The user would also have to wear the a green, a red, and a yellow colour block on his/her wrist, elbow, and tricep respectively. I made those three colour blocks using LEGO and velcro tape. 


The user can then tune the upper and lower bound of each of the three HSV colour masks by running HSV.py three times. When running HSV.py for one particular colour, the user can adjust the upper and lower bound HSV values (six values per colour) until only that colour block shows up. Note down those six values and change them accordingly in the main Python file (Line 15 - Line 23). Make sure to run the HSV.py file three times to determine the lower and upper bounds for all three colours.


Finally, run the main Python file, titled "Gesture_Controlled_Robotic_Arm_Python_Code.py". Ensure that the Arduino is plugged in so that the Python program can send the PWM signals to the Arduino.

## More Information Regarding this Project:
The following is a demo video of this project:
https://www.youtube.com/watch?v=PDEdxRVkMdo

If you want to check out the full description of the project, including the downloadable STL files and a part list, check out the following link:
https://grabcad.com/library/5-dof-robotic-arm-6
