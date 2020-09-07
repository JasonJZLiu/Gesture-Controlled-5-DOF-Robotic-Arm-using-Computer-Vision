from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse, cv2, imutils, time, serial, struct, math

def theta(v, w): 
	return np.arccos(v.dot(w)/(np.linalg.norm(v)*np.linalg.norm(w)))



arm2_angle = 74 
arm1_angle = 72

# Define the lower and upper bounds of the green, red, and yellow filters
greenLower = (38, 95, 72)
greenUpper = (96, 255, 145)

redLower = (0,122,119)
redUpper = (255,255,255)

yellowLower = (15, 115, 72)
yellowUpper = (27, 174, 255)



vs = VideoStream(src=0).start()
# Allow the camera to load
time.sleep(2.0)

#Initilize communication with Arduino
arduino = serial.Serial('COM3', 9600) #Comment this line out to test out the program without an Arduino connected


Horizontal_Vector = np.array([-10,0])
Arm2_Vector = np.array([0,0.1])
Arm1_Vector = np.array([0,0.1])




while True:
	frame = vs.read()

	#Define the size of the frame, blur it
	frame = imutils.resize(frame, width=800)
	#Blur the frame
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	#Convert to HSV Colour Space
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

	#Construct masks for the three colours, then perform a series of dilations and erosions to remove small areas left in the mask
	green_mask = cv2.inRange(hsv, greenLower, greenUpper)
	green_mask = cv2.erode(green_mask, None, iterations=2)
	green_mask = cv2.dilate(green_mask, None, iterations=2)

	red_mask = cv2.inRange(hsv, redLower, redUpper)
	red_mask = cv2.erode(red_mask, None, iterations=2)
	red_mask = cv2.dilate(red_mask, None, iterations=2)

	yellow_mask = cv2.inRange(hsv, yellowLower, yellowUpper)
	yellow_mask = cv2.erode(yellow_mask, None, iterations=2)
	yellow_mask = cv2.dilate(yellow_mask, None, iterations=2)


    #Find contours in the mask and define each of the colour's centers
	green_cnts = cv2.findContours(green_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	green_cnts = imutils.grab_contours(green_cnts)
	green_center = None

	red_cnts = cv2.findContours(red_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	red_cnts = imutils.grab_contours(red_cnts)
	red_center = None

	yellow_cnts = cv2.findContours(yellow_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	yellow_cnts = imutils.grab_contours(yellow_cnts)
	yellow_center = None


	#Proceed only if at least one contour was found
	if len(green_cnts) > 0:
		#Find the largest contour in the mask, then compute its minimum enclosing circle and centroid
		c = max(green_cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		green_center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		#Only assign and draw a center if its radius meets a certain size
		if radius > 10:
			cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
			cv2.circle(frame, green_center, 5, (0, 0, 255), -1)
			#print('The green center is ', green_center)

	if len(red_cnts) > 0:
		c = max(red_cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		red_center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		if radius > 10:
			cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
			cv2.circle(frame, red_center, 5, (0, 0, 255), -1)
			#print('The red center is ', red_center)


	if len(yellow_cnts) > 0:
		c = max(yellow_cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		yellow_center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		if radius > 10:
			cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
			cv2.circle(frame, yellow_center, 5, (0, 0, 255), -1)
			#print('The red center is ', red_center)

	#Only draw and compute the vector if both centers are present
	if (red_center and yellow_center):
		Arm1_Vector = np.array([red_center[0]-yellow_center[0], red_center[1]-yellow_center[1]])

		#Only proceed if the length of the vector falls in a certain range
		if (np.linalg.norm(Arm1_Vector) > 80 and np.linalg.norm(Arm1_Vector)< 300 ):
			cv2.line(frame, red_center, yellow_center, (0, 255, 0), thickness=3, lineType=8)
			arm1_angle = theta(Arm1_Vector,Horizontal_Vector)
			arm1_angle = round(180 * arm1_angle / np.pi)

			if (Arm1_Vector[1]<0):
				arm1_angle = arm1_angle * -1

			arm1_angle = arm1_angle - 18
			if(arm1_angle < 0):
				arm1_angle = 160
			elif (arm1_angle >160):
				arm1_angle = 160
			elif (arm1_angle < 50):
				arm1_angle = 50


	#Only draw and compute the vector if both centers are present
	if (green_center and red_center):
		Arm2_Vector = np.array([red_center[0]-green_center[0], red_center[1]-green_center[1]])

		if (np.linalg.norm(Arm2_Vector) > 100 and np.linalg.norm(Arm1_Vector)< 230):
			cv2.line(frame, green_center, red_center, (0, 255, 0), thickness=3, lineType=8)
			arm2_angle = theta(Arm2_Vector,Arm1_Vector)
			arm2_angle = round(180 * arm2_angle / np.pi)
			
			arm2_angle = arm2_angle - 16 
			if (arm2_angle >154):
				arm2_angle = 154
			elif (arm2_angle < 10):
				arm2_angle = 10


	#Only send the computed angle data if they exist
	if(math.isnan(arm2_angle)==False and math.isnan(arm1_angle)==False):
		#Computes the manipulator angle based on the two previous arm angles so that the manipulator always stays horizontal
		alpha = arm2_angle + 16
		beta = 180 - (arm1_angle + 18)
		tilt_angle = -1*(180 - alpha - beta) + 60
		if (tilt_angle<0):
			tilt_angle = 0
		print("Arm1 Angle is: {}  |  Arm2 Angle is: {}  |  Tilt Angle is: {}".format(int(arm1_angle), int(arm2_angle),int(tilt_angle)))

		#Send the three data to the Arduino
		arduino.write(struct.pack('>BBB',int(arm1_angle),int(arm2_angle), int(tilt_angle))) #Comment this line out to test out the program without an Arduino connected


	#Show the frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	#Press 'q' to stop the loop
	if key == ord("q"):
		break

	
#Stop the camera video stream
vs.stop()
cv2.destroyAllWindows()

