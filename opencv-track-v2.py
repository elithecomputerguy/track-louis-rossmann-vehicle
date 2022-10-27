from __future__ import print_function
from tkinter import CENTER
import cv2 as cv
import argparse

import RPi.GPIO as GPIO
import time

h = 0
w = 0
center = (0,0) 
x_axis_check = 0

def detectAndDisplay(frame):
    global x_axis_check
    global h
    global w

    global center

    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)
    #-- Detect faces
    faces = face_cascade.detectMultiScale(frame_gray, minSize=(100,100))
    for (x,y,w,h) in faces:
        center = (x + w//2, y + h//2)
        frame = cv.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)
        faceROI = frame_gray[y:y+h,x:x+w]

        font = cv.FONT_HERSHEY_SIMPLEX
        cv.putText(frame, str(center) + str(h), (50, 50), font, 1, (0, 255, 255), 2, cv.LINE_4)

    cv.imshow('Capture - Face detection', frame)

parser = argparse.ArgumentParser(description='Code for Cascade Classifier tutorial.')
parser.add_argument('--face_cascade', help='Path to face cascade.', default='data/louis-cascade/cascade.xml')
parser.add_argument('--camera', help='Camera divide number.', type=int, default=0)
args = parser.parse_args()
face_cascade_name = args.face_cascade
face_cascade = cv.CascadeClassifier()

#-- 1. Load the cascades
if not face_cascade.load(cv.samples.findFile(face_cascade_name)):
    print('--(!)Error loading face cascade')
    exit(0)
camera_device = args.camera
#-- 2. Read the video stream
cap = cv.VideoCapture(camera_device)
if not cap.isOpened:
    print('--(!)Error opening video capture')
    exit(0)
while True:
    ret, frame = cap.read()
    if frame is None:
        print('--(!) No captured frame -- Break!')
        break

    detectAndDisplay(frame)
    
    x_axis = 0

    if x_axis_check != center[0]:
        x_axis = center[0]
        x_axis_check = x_axis
    
    print(h)
    print(w)
    print (str(center))
    print (center[0])
    print (x_axis)
    print (x_axis_check)
    print("****")

    if x_axis > 400 :
        f = open("speed.txt", "w")
        f.write("slow")
        f.close()
        f = open("command.txt", "w")
        f.write("right")
        f.close()    
        x_axis = 0        
        time.sleep(.1)

    elif x_axis < 250 and x_axis != 0:
        f = open("speed.txt", "w")
        f.write("slow")
        f.close()
        f = open("command.txt", "w")
        f.write("left")
        f.close()      
        x_axis = 0        
        time.sleep(.1) 

    elif (h) < 130 and h != 0:
        f = open("speed.txt", "w")
        f.write("slow")
        f.close()
        f = open("command.txt", "w")
        f.write("forward")
        f.close()
        h = 0            
        time.sleep(.1) 

    else:
        f = open("speed.txt", "w")
        f.write("stop")
        f.close()

    if cv.waitKey(10) == 27:
        break