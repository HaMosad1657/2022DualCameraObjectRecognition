import numpy as np
import cv2
import time
import argparse
import logging
from networktables import NetworkTables
# import required libraries

logging.basicConfig(level=logging.DEBUG)
ip = "10.16.57.2"
NetworkTables.initialize(server=ip)
sd = NetworkTables.getTable("SmartDashboard")
# setup and connect to networktables

ap = argparse.ArgumentParser()
ap.add_argument("-minHue", "--minHue", type=int, default=0,help="min hue in hsv")
ap.add_argument("-maxHue", "--maxHue", type=int, default=10,help="max hue in hsv")
args = vars(ap.parse_args())
# get the hue values from the terminal

lowerHsv = (args["minHue"], 100, 100)
upperHsv = (args["maxHue"], 255, 255)
#  setup our hsv ranges and put the hue values in them

cap0 = cv2.VideoCapture(0)
cap0.set(cv2.CAP_PROP_FRAME_WIDTH, 112)
cap0.set(cv2.CAP_PROP_FRAME_HEIGHT, 63)
# setup camera 0 and resize

cap2 = cv2.VideoCapture(2)
cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 112)
cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 63)
# setup camera 2 and resize (we use 0 and 2 because 1 is allways the PiCamera in a rapberry pi, and we use usb cameras)

time.sleep(2.0)
# let the cameras warm up

while True:
	ret0, frame0 = cap0.read()
	ret2, frame2 = cap2.read()
	# get frames
	
	hsv = cv2.cvtColor(frame0, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, lowerHsv, upperHsv)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0]
	if len(cnts) > 0:
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		if radius > 4:
			sd.putNumber("XvalueCam0", x)
			print(x)
	else:
		print(0)
		sd.putNumber("XvalueCam0", 0.0)
	# camera 0 object recognition
	
	hsv2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
	mask2 = cv2.inRange(hsv2, lowerHsv, upperHsv)
	mask2 = cv2.erode(mask2, None, iterations=2)
	mask2 = cv2.dilate(mask2, None, iterations=2)
	cnts2 = cv2.findContours(mask2.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	cnts2 = cnts2[0]
	if len(cnts2) > 0:
		c2 = max(cnts2, key=cv2.contourArea)
		((x2, y2), radius2) = cv2.minEnclosingCircle(c2)
		M2 = cv2.moments(c2)
		center2 = (int(M2["m10"] / M2["m00"]), int(M2["m01"] / M2["m00"]))
		if radius2 > 4:
			sd.putNumber("XvalueCam2", x2)
			print(x2)
	else:
		print(0)
		sd.putNumber("XvalueCam2", 0.0)
	# camera 0 object recognition
	
	cv2.imshow('Cam 0', frame0)
	cv2.imshow('Cam 2', frame2)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
cap0.release()
cap2.release()
cv2.destroyAllWindows()