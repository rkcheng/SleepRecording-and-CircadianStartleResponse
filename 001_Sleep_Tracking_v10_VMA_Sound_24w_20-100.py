import sys
import traceback
import serial
sys.path.append("C:\\opencv\\build\\python\\2.7")
import copy
from PIL import ImageGrab
import numpy as np
import cv2
import math
import time
from time import strftime
import os
from numpy import array
import xlwt
import xlrd
from Test2_24 import Excel_Save
from pygame import mixer # Load the required library
import pygame

connected = False
# For RueyToshiba
#ser = serial.Serial("COM15", 9600, writeTimeout = 0)
# For Dell Desktop
ser = serial.Serial("COM4", 9600, writeTimeout = 0)

while not connected:
    serin = ser.read()
    connected = True

def nothing(x):
    pass

# Change parameters here =========================================
Cycles = 300 # define how many light/dark cycles for this experiment. The experiment starts with darkness
CycleDuration = 900 # This time in seconds multiplied by 2 equals the time each video/Excel file is saved.
framerate = 5.3 # define frames per second (fps)
SearchSize= 10 # in pixels
LightOffTime = '220000' # in HHMMSS format
tempQQ = 0  # Minute offset for testing sound
LightOnTime = '080000' # in HHMMSS format
ComputerName = 'Administrator' # Options RueyToshiba or user
#ComputerName = 'RueyToshiba' # Options RueyToshiba or user
# ================================================================

pygame.mixer.init()
#effect = pygame.mixer.Sound('C:\Users\' + ComputerName + user\LabRawData\Excel\Sounds\Frequency_30Hz_SineWave.wav')
effect = pygame.mixer.Sound('D:\LabRawData\Excel\Sounds\Frequency_30Hz_SineWave.wav')


def savescreen():
    print('This is the exit strategy')
    tt961 = strftime("%m",) + strftime("%d",) + '_' + strftime("%H",) + strftime("%M",) + strftime("%S",)
    print tt961ab
    ImageGrab.grab().save("D:\\LabRawData\\Excel\\Screen_" + tt961 + "_AbortView_Line115.jpg", "JPEG")
import atexit
atexit.register(savescreen)


RGB = 0 # 1 stands for color video and 0 stands for B/W video
total = int(Cycles * CycleDuration * 2 * framerate) + 6000;  # Total secods for this experiment. # Needs to multiply frame rate later

stamp = np.zeros((100,200,3))
#stamp = np.zeros((10,20,3))

#print ("7")
ser.write("4")
while ser.read() != '5':
    ser.read
    print ('Waiting')

#print ("8")

HowMany = raw_input("Enter How Many Tanks to Track (Including the IR LED Box): ")
GroupName = raw_input("Enter Group Name: ")
cv2.namedWindow('frame')

# Capture image wirh specified size and frame rate
cap = cv2.VideoCapture(0)

# For the fourcc to work, add C:\opencv\build\x86\vc10\bin to System PATH
cap.set(6 ,cv2.cv.CV_FOURCC('M', 'J', 'P', 'G') );
fourcc = cv2.cv.CV_FOURCC('M','J','P','G')

#cap.set(6 ,cv2.cv.CV_FOURCC('D', 'I', 'V', 'X') );
#fourcc = cv2.cv.CV_FOURCC('D','I','V','X')

cap.set(3, 1096) # change Width  800x600 for small monitor;1280x1024 for HD monitor
cap.set(4, 1096) # change Height
#cap.set(5, 100) # change Frame rate
#cap.set(14,120) # Gain

# Create trackbar in the 'frame'
#cv2.createTrackbar('Brightness','control',0,255,nothing)
#cv2.setTrackbarPos('Brightness','control', 50)
#cv2.createTrackbar('Contrast','control',0,255,nothing)
#cv2.setTrackbarPos('Contrast','control', 25)
#cv2.createTrackbar('Saturation','control',0,128,nothing)
#cv2.setTrackbarPpos('Saturation','control', 30)
#cv2.createTrackbar('Exposure','control',0,1,nothing)
#cv2.setTrackbarPos('Exposure','control', 0)

# Setup SimpleBlobDetector parameters
params = cv2.SimpleBlobDetector_Params()
params.minDistBetweenBlobs = 50;
# Change parameters here =========================================
params.minArea = 2;  # for 7dpf ABWT, 3 is recommended, 1 for blue light; 6 for HD
params.maxArea = 200;
if RGB == 1:
    params.minThreshold = 40;  # For Color
else:
    params.minThreshold = 12;  # For B/W
# ================================================================

params.filterByCircularity = False;
params.filterByConvexity = False;
params.filterByInertia = False;
params.filterByColor = False;
params.filterByArea = True;
detector = cv2.SimpleBlobDetector(params)
# ============================================
# Blob detection
detector = cv2.SimpleBlobDetector(params)

ii = 0
i = 0
tt4=''
tt40=''
tt41=''
tt91=[]
tt91=list(xrange(Cycles*2+1))  # List for light status change
tt92 = 1
tt93 = 0
tt99 = 0
tt96 = 0 # this is the count for the number of files saved in the folder
tt961 = '' # this is the time string for saving files
tt961aa = '' # No Webcam Time
tt961ab = '0' # Error Location
tt962 = 0 # for saving video files
tt963 = 0 # for quit and save
tt964 = 0 # togle for experiment
tt965 = 0 # togle for displaying Light Status
tt9651 = 0 # toggle for vibration
tt9652 = 0 # toggle for light
tt9653 = 0 # toggle for vibration
if LightOffTime > LightOnTime:
    tt966 = 1 # togle for displaying Light Status (overnight)
    tt965 = 0 #  111111
else:
    tt966 = 0 # (same day)
    tt965 = 1
CurrentTime = 0 # for current time

tt6=list(xrange(total))
Font = cv2.FONT_HERSHEY_SIMPLEX
dummy= 0
preset=0

data01=[];
data01Stamp=[];
oldL01=0
oldX01=0
oldY01=0
small01=0
tt801=''

data02=[];
data02Stamp=[];
oldL02=0
oldX02=0
oldY02=0
small02=0
tt802=''

data03=[];
data03Stamp=[];
oldL03=0
oldX03=0
oldY03=0
small03=0
tt803=''

data04=[];
data04Stamp=[];
oldL04=0
oldX04=0
oldY04=0
small04=0
tt804=''

data05=[];
data05Stamp=[];
oldL05=0
oldX05=0
oldY05=0
small05=0
tt805=''

data06=[];
data06Stamp=[];
oldL06=0
oldX06=0
oldY06=0
small06=0
tt806=''

data07=[];
data07Stamp=[];
oldL07=0
oldX07=0
oldY07=0
small07=0
tt807=''

data08=[];
data08Stamp=[];
oldL08=0
oldX08=0
oldY08=0
small08=0
tt808=''

data09=[];
data09Stamp=[];
oldL09=0
oldX09=0
oldY09=0
small09=0
tt809=''

data10=[];
data10Stamp=[];
oldL10=0
oldX10=0
oldY10=0
small10=0
tt810=''

data11=[];
data11Stamp=[];
oldL11=0
oldX11=0
oldY11=0
small11=0
tt811=''

data12=[];
data12Stamp=[];
oldL12=0
oldX12=0
oldY12=0
small12=0
tt812=''

data13=[];
data13Stamp=[];
oldL13=0
oldX13=0
oldY13=0
small13=0
tt813=''

data14=[];
data14Stamp=[];
oldL14=0
oldX14=0
oldY14=0
small14=0
tt814=''

data15=[];
data15Stamp=[];
oldL15=0
oldX15=0
oldY15=0
small15=0
tt815=''

data16=[];
data16Stamp=[];
oldL16=0
oldX16=0
oldY16=0
smalll6=0
tt816=''

data17=[];
data17Stamp=[];
oldL17=0
oldX17=0
oldY17=0
smalll7=0
tt817=''

data18=[];
data18Stamp=[];
oldL18=0
oldX18=0
oldY18=0
smalll8=0
tt818=''

data19=[];
data19Stamp=[];
oldL19=0
oldX19=0
oldY19=0
smalll9=0
tt819=''

data20=[];
data20Stamp=[];
oldL20=0
oldX20=0
oldY20=0
small20=0
tt820=''

data21=[];
data21Stamp=[];
oldL21=0
oldX21=0
oldY21=0
small21=0
tt821=''

data22=[];
data22Stamp=[];
oldL22=0
oldX22=0
oldY22=0
small22=0
tt822=''

data23=[];
data23Stamp=[];
oldL23=0
oldX23=0
oldY23=0
small23=0
tt823=''

data24=[];
data24Stamp=[];
oldL24=0
oldX24=0
oldY24=0
small24=0
tt824=''

data25=[];
data25Stamp=[];
oldL25=0
oldX25=0
oldY25=0
small25=0
tt825=''



save1=0
setupbox = 0

#tt801 = "C:\Users\RueyToshiba\Desktop\Webcam\\" + GroupName
#tt802 = "C:\Users\RueyToshiba\Desktop\Webcam\\" + GroupName
#tt803 = "C:\Users\RueyToshiba\Desktop\Webcam\\" + GroupName
#tt804 = "C:\Users\RueyToshiba\Desktop\Webcam\\" + GroupName
#tt805 = "C:\Users\RueyToshiba\Desktop\Webcam\\" + GroupName
#tt806 = "C:\Users\RueyToshiba\Desktop\Webcam\\" + GroupName
#tt807 = "C:\Users\RueyToshiba\Desktop\Webcam\\" + GroupName
#tt808 = "C:\Users\RueyToshiba\Desktop\Webcam\\" + GroupName
#tt809 = "C:\Users\RueyToshiba\Desktop\Webcam\\" + GroupName
#tt810 = "C:\Users\RueyToshiba\Desktop\Webcam\\" + GroupName
#tt811 = "C:\Users\RueyToshiba\Desktop\Webcam\\" + GroupName
#tt812 = "C:\Users\RueyToshiba\Desktop\Webcam\\" + GroupName
#tt813 = "C:\Users\RueyToshiba\Desktop\Webcam\\" + GroupName
#tt814 = "C:\Users\RueyToshiba\Desktop\Webcam\\" + GroupName
#tt815 = "C:\Users\RueyToshiba\Desktop\Webcam\\" + GroupName
#tt816 = "C:\Users\RueyToshiba\Desktop\Webcam\\" + GroupName
#tt817 = "C:\Users\RueyToshiba\Desktop\Webcam\\" + GroupName
#tt818 = "C:\Users\RueyToshiba\Desktop\Webcam\\" + GroupName
#tt819 = "C:\Users\RueyToshiba\Desktop\Webcam\\" + GroupName
#tt820 = "C:\Users\RueyToshiba\Desktop\Webcam\\" + GroupName
#tt821 = "C:\Users\RueyToshiba\Desktop\Webcam\\" + GroupName
#tt822 = "C:\Users\RueyToshiba\Desktop\Webcam\\" + GroupName
#tt823 = "C:\Users\RueyToshiba\Desktop\Webcam\\" + GroupName
#tt824 = "C:\Users\RueyToshiba\Desktop\Webcam\\" + GroupName
#tt825 = "C:\Users\RueyToshiba\Desktop\Webcam\\" + GroupName

tt801 = "D:\\LabRawData\\Webcam\\" + GroupName
tt802 = "D:\\LabRawData\\Webcam\\" + GroupName
tt803 = "D:\\LabRawData\\Webcam\\" + GroupName
tt825 = "D:\\LabRawData\\Webcam\\" + GroupName


#  Below is the mouse evemt
boxes=[]
boxes1=[]
VibrationStatus = 0
drawing = False
mode = 0
fourcc = cv2.cv.CV_FOURCC('M','J','P','G')

def set_up_ROIs(event,x,y,flags,param):
    if len(boxes1) <= 4:
        global boxnumber, drawing, img, gray2, gray3, arr, arr1, dummy, mode
        boxnumner = 0
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            sbox = [x, y]
            boxes1.append(sbox)
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing == True:
                if len(boxes1) == 1:
                    arr = array(gray2)
                    cv2.rectangle(arr,(boxes1[-1][0],boxes1[-1][-1]),(x, y),(0,0,255),1)
                    cv2.imshow('frame',arr)
                elif len(boxes1) == 3:
                    arr1 = array(gray3)
                    cv2.rectangle(arr1,(boxes1[-1][0],boxes1[-1][-1]),(x, y),(0,0,255),1)
                    cv2.imshow('frame',arr1)
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = not drawing
            ebox = [x, y]
            boxes1.append(ebox)
            if len(boxes1) == 4:
                cv2.rectangle(gray3,(boxes1[-2][-2],boxes1[-2][-1]),(boxes1[-1][-2],boxes1[-1][-1]), (0,0,255),1)
                cv2.imshow('frame',gray3)
                sbox = [boxes1[-2][-2],boxes1[-2][-1]]
                boxes.append(sbox)
                boxes.append(ebox)
                mode = 1
                dummy = 1
                i=0
            elif len(boxes1) == 2:
                if not os.path.exists(tt801):
                    os.makedirs(tt801)
                tempXa = boxes1[-1][-2]-boxes1[-2][-2]
                tempYa = boxes1[-1][-1]-boxes1[-2][-1]
                tempXb = tempXa - (tempXa % 4)
                tempYb = tempYa - (tempYa % 6)
                tempXc = tempXb / 4
                tempYc = tempYb / 6
                tempZ=0
                for bby in range(6):
                    for bbx in range(4):
                        tempZ = tempZ + 1
                        sbox = [boxes1[-2][-2] + bbx * tempXc,boxes1[-2][-1] + bby * tempYc]
                        boxes.append(sbox)
                        ebox = [boxes1[-2][-2] + (bbx+1) * tempXc-1,boxes1[-2][-1] + (bby+1) * tempYc-1]
                        boxes.append(ebox)
                        if tempZ % 2 == 0:
                            cv2.rectangle(gray3,(boxes[-2][-2],boxes[-2][-1]),(boxes[-1][-2],boxes[-1][-1]), (0,0,255),1)
                        elif tempZ % 2 == 1:
                            cv2.rectangle(gray3,(boxes[-2][-2],boxes[-2][-1]),(boxes[-1][-2],boxes[-1][-1]), (0,255,0),1)
                        cv2.imshow('frame',gray3)
# ====================================================

tt = time.time()
tt1 = str(tt).find('.',1,len(str(tt)))
tt2 = str(tt)[tt1-8:tt1]
tt5 = str(tt)[tt1+1:len(str(tt))]
tt40 = tt2 + tt5.ljust(2,'0')


while(tt964 == 0):
    CurrentTime = strftime("%H",) + strftime("%M",) + strftime("%S",)
    if tt966 == 0:
        if (int(CurrentTime) >= int(LightOffTime) and int(CurrentTime) < int(LightOnTime)):
            if tt965 == 0:
                print ('Light is Off at 111-' + CurrentTime + ' ================')
                ser.write("3")
                while ser.read() != '5':
                    ser.read
                    print ('Waiting')
                tt965 = 1
        elif (int(CurrentTime) > int(LightOffTime) and int(CurrentTime) >= int(LightOnTime)):
            if tt965 == 1:
                print ('Light is On at ' + CurrentTime + ' === Light On After Light Off ===')
                ser.write("4") 
                while ser.read() != '5':
                    ser.read
                    print ('Waiting')
                tt965 = 0
        else:
            if tt965 == 1:
                print ('Light is On at ' + CurrentTime + ' === Experiment Starts ===')
                ser.write("4") 
                while ser.read() != '5':
                    ser.read
                    print ('Waiting')
                tt965 = 0
    else:
        if (int(CurrentTime) >= int(LightOffTime) and int(CurrentTime) > int(LightOnTime)):
            if tt965 == 0:
                print ('Light is Off at 222-' + CurrentTime)
                ser.write("3")
                while ser.read() != '5':
                    ser.read
                    print ('Waiting')
                tt965 = 1
        elif (int(CurrentTime) >= int(LightOnTime)):
            if tt965 == 1:  # Changed it from 1 to 0
                tt961a = strftime("%d",)
                if int(tt961a) > 0 : # This is where you determin on which date you would like to turn on the light in the morning at 8am.
                    ser.write("4")
                    print ('Light is On at ' + CurrentTime + ' === Light On After Light Off ===')
                else:
                    #print ('Light is NOT On at ' + CurrentTime)
                    ser.write("3")
                while ser.read() != '5':
                    ser.read
                    print ('Waiting')
                tt965 = 0
            else:
                tt961a = strftime("%d",)
                tt224 = strftime("%H",)
                tt225 = strftime("%M",)
                # 160928_subhom_sleep_G03
                if int(tt961a) == 41:  # Define on which date to do the 6 cycles of visuomotor assay
                    if int(tt224) > 15: # starts the first cycle after 4pm
                        if int(tt224) < 23:
                            if int(tt225) >= 20: # Ignore this
                                if int(tt224) < 22:
                                    if int(tt225) < 30:  # Light off at 30' in the hour
                                        if tt9652 == 0:
                                            ser.write("7")
                                            while ser.read() != '5':
                                                ser.read
                                                print ('Waiting')
                                            tt9652 = 1
                                    else:
                                        if tt9652 == 1:
                                            #print ('UV is Off at ' + CurrentTime)
                                            print ('Light is Off at ' + CurrentTime)
                                            ser.write("3")
                                            while ser.read() != '5':
                                                ser.read
                                                print ('Waiting')
                                            tt9652 = 2
                            else: # light on at 00
                                if int(tt224) < 23:
                                    if tt9652 == 2:
                                        print ('Light is On at ' + CurrentTime)
                                        ser.write("4")
                                        while ser.read() != '5':
                                            ser.read
                                            print ('Waiting')
                                        tt9652 = 0
        elif int(CurrentTime) < LightOnTime:
            if tt965 == 0:
                print ('Light is still Off at ' + CurrentTime)
                tt961a = strftime("%d",)
                ser.write("3")
                while ser.read() != '5':
                    ser.read
                    print ('Waiting')
                tt965 = 1
        if tt965 == 1:
            tt224 = strftime("%H", )
            tt225 = strftime("%M", )
            tt226 = strftime("%S", )
            if (int(tt224) > 0 and int(tt224) <=6):
                if int(tt224) % 2 == 0:  # Even Hour
                    if int(tt225) == 0:
                        if int(tt226) == 0:
                            if VibrationStatus == 0:
                                effect.set_volume(0.2)
                                effect.play(maxtime=200)
                                print '222 at ' + CurrentTime
                                VibrationStatus = 1
                                tt9653 = 1
                        if int(tt226) == 1:
                            if VibrationStatus == 1:
                                effect.stop
                                tt9653 = 0
                                VibrationStatus = 0
                    if int(tt225) == 1:
                        if int(tt226) == 0:
                            if VibrationStatus == 0:
                                effect.set_volume(0.3)
                                effect.play(maxtime=200)
                                print '223 at ' + CurrentTime
                                VibrationStatus = 1
                                tt9653 = 1
                        if int(tt226) == 1:
                            if VibrationStatus == 1:
                                effect.stop
                                tt9653 = 0
                                VibrationStatus = 0
                    if int(tt225) == 2:
                        if int(tt226) == 0:
                            if VibrationStatus == 0:
                                effect.set_volume(0.4)
                                effect.play(maxtime=200)
                                print '224 at ' + CurrentTime
                                VibrationStatus = 1
                                tt9653 = 1
                        if int(tt226) == 1:
                            if VibrationStatus == 1:
                                effect.stop
                                tt9653 = 0
                                VibrationStatus = 0
                    if int(tt225) == 3:
                        if int(tt226) == 0:
                            if VibrationStatus == 0:
                                effect.set_volume(0.5)
                                effect.play(maxtime=200)
                                print '225 at ' + CurrentTime
                                VibrationStatus = 1
                                tt9653 = 1
                        if int(tt226) == 1:
                            if VibrationStatus == 1:
                                effect.stop
                                tt9653 = 0
                                VibrationStatus = 0
                    if int(tt225) == 4:
                        if int(tt226) == 0:
                            if VibrationStatus == 0:
                                effect.set_volume(0.6)
                                effect.play(maxtime=200)
                                print '226 at ' + CurrentTime
                                VibrationStatus = 1
                                tt9653 = 1
                        if int(tt226) == 1:
                            if VibrationStatus == 1:
                                effect.stop
                                tt9653 = 0
                                VibrationStatus = 0
                    if int(tt225) == 5:
                        if int(tt226) == 0:
                            if VibrationStatus == 0:
                                effect.set_volume(0.7)
                                effect.play(maxtime=200)
                                print '227 at ' + CurrentTime
                                VibrationStatus = 1
                                tt9653 = 1
                        if int(tt226) == 1:
                            if VibrationStatus == 1:
                                effect.stop
                                tt9653 = 0
                                VibrationStatus = 0
                    if int(tt225) == 6:
                        if int(tt226) == 0:
                            if VibrationStatus == 0:
                                effect.set_volume(0.8)
                                effect.play(maxtime=200)
                                print '228 at ' + CurrentTime
                                VibrationStatus = 1
                                tt9653 = 1
                        if int(tt226) == 1:
                            if VibrationStatus == 1:
                                effect.stop
                                tt9653 = 0
                                VibrationStatus = 0
                    if int(tt225) == 7:
                        if int(tt226) == 0:
                            if VibrationStatus == 0:
                                effect.set_volume(0.9)
                                effect.play(maxtime=200)
                                print '229 at ' + CurrentTime
                                VibrationStatus = 1
                                tt9653 = 1
                        if int(tt226) == 1:
                            if VibrationStatus == 1:
                                effect.stop
                                tt9653 = 0
                                VibrationStatus = 0
                    if int(tt225) == 8:
                        if int(tt226) == 0:
                            if VibrationStatus == 0:
                                effect.set_volume(1.0)
                                effect.play(maxtime=200)
                                print '230 at ' + CurrentTime
                                VibrationStatus = 1
                                tt9653 = 1
                        if int(tt226) == 1:
                            if VibrationStatus == 1:
                                effect.stop
                                tt9653 = 0
                                VibrationStatus = 0
                    if int(tt225) == 9:
                        if int(tt226) == 0:
                            if VibrationStatus == 0:
                                effect.set_volume(1.0)
                                effect.play(maxtime=200)
                                print '230 at ' + CurrentTime
                                VibrationStatus = 1
                                tt9653 = 1
                        if int(tt226) == 1:
                            if VibrationStatus == 1:
                                effect.stop
                                tt9653 = 0
                                VibrationStatus = 0
                    if int(tt225) == 10:
                        if int(tt226) == 0:
                            if VibrationStatus == 0:
                                effect.set_volume(0.9)
                                effect.play(maxtime=200)
                                print '229 at ' + CurrentTime
                                VibrationStatus = 1
                                tt9653 = 1
                        if int(tt226) == 1:
                            if VibrationStatus == 1:
                                effect.stop
                                tt9653 = 0
                                VibrationStatus = 0
                    if int(tt225) == 11:
                        if int(tt226) == 0:
                            if VibrationStatus == 0:
                                effect.set_volume(0.8)
                                effect.play(maxtime=200)
                                print '228 at ' + CurrentTime
                                VibrationStatus = 1
                                tt9653 = 1
                        if int(tt226) == 1:
                            if VibrationStatus == 1:
                                effect.stop
                                tt9653 = 0
                                VibrationStatus = 0
                    if int(tt225) == 12:
                        if int(tt226) == 0:
                            if VibrationStatus == 0:
                                effect.set_volume(0.7)
                                effect.play(maxtime=200)
                                print '227 at ' + CurrentTime
                                VibrationStatus = 1
                                tt9653 = 1
                        if int(tt226) == 1:
                            if VibrationStatus == 1:
                                effect.stop
                                tt9653 = 0
                                VibrationStatus = 0
                    if int(tt225) == 13:
                        if int(tt226) == 0:
                            if VibrationStatus == 0:
                                effect.set_volume(0.6)
                                effect.play(maxtime=200)
                                print '226 at ' + CurrentTime
                                VibrationStatus = 1
                                tt9653 = 1
                        if int(tt226) == 1:
                            if VibrationStatus == 1:
                                effect.stop
                                tt9653 = 0
                                VibrationStatus = 0
                    if int(tt225) == 14:
                        if int(tt226) == 0:
                            if VibrationStatus == 0:
                                effect.set_volume(0.5)
                                effect.play(maxtime=200)
                                print '225 at ' + CurrentTime
                                VibrationStatus = 1
                                tt9653 = 1
                        if int(tt226) == 1:
                            if VibrationStatus == 1:
                                effect.stop
                                tt9653 = 0
                                VibrationStatus = 0
                    if int(tt225) == 15:
                        if int(tt226) == 0:
                            if VibrationStatus == 0:
                                effect.set_volume(0.4)
                                effect.play(maxtime=200)
                                print '224 at ' + CurrentTime
                                VibrationStatus = 1
                                tt9653 = 1
                        if int(tt226) == 1:
                            if VibrationStatus == 1:
                                effect.stop
                                tt9653 = 0
                                VibrationStatus = 0
                    if int(tt225) == 16:
                        if int(tt226) == 0:
                            if VibrationStatus == 0:
                                effect.set_volume(0.3)
                                effect.play(maxtime=200)
                                print '223 at ' + CurrentTime
                                VibrationStatus = 1
                                tt9653 = 1
                        if int(tt226) == 1:
                            if VibrationStatus == 1:
                                effect.stop
                                tt9653 = 0
                                VibrationStatus = 0
                    if int(tt225) == 17:
                        if int(tt226) == 0:
                            if VibrationStatus == 0:
                                effect.set_volume(0.2)
                                effect.play(maxtime=200)
                                print '222 at ' + CurrentTime
                                VibrationStatus = 1
                                tt9653 = 1
                        if int(tt226) == 1:
                            if VibrationStatus == 1:
                                effect.stop
                                tt9653 = 0
                                VibrationStatus = 0
                else:  # Odd hour
                    if int(tt225) == 0+tempQQ:
                        if int(tt226) == 0:
                            if VibrationStatus == 0:
                                effect.set_volume(1.0)
                                effect.play(maxtime=200)
                                print '230 at ' + CurrentTime
                                VibrationStatus = 1
                                tt9653 = 1
                        if int(tt226) == 1:
                            if VibrationStatus == 1:
                                effect.stop
                                tt9653 = 0
                                VibrationStatus = 0
                    if int(tt225) == 1+tempQQ:
                        if int(tt226) == 0:
                            if VibrationStatus == 0:
                                effect.set_volume(0.9)
                                effect.play(maxtime=200)
                                print '229 at ' + CurrentTime
                                VibrationStatus = 1
                                tt9653 = 1
                        if int(tt226) == 1:
                            if VibrationStatus == 1:
                                effect.stop
                                tt9653 = 0
                                VibrationStatus = 0
                    if int(tt225) == 2+tempQQ:
                        if int(tt226) == 0:
                            if VibrationStatus == 0:
                                effect.set_volume(0.8)
                                effect.play(maxtime=200)
                                print '228 at ' + CurrentTime
                                VibrationStatus = 1
                                tt9653 = 1
                        if int(tt226) == 1:
                            if VibrationStatus == 1:
                                effect.stop
                                tt9653 = 0
                                VibrationStatus = 0
                    if int(tt225) == 3+tempQQ:
                        if int(tt226) == 0:
                            if VibrationStatus == 0:
                                effect.set_volume(0.7)
                                effect.play(maxtime=200)
                                print '227 at ' + CurrentTime
                                VibrationStatus = 1
                                tt9653 = 1
                        if int(tt226) == 1:
                            if VibrationStatus == 1:
                                effect.stop
                                tt9653 = 0
                                VibrationStatus = 0
                    if int(tt225) == 4+tempQQ:
                        if int(tt226) == 0:
                            if VibrationStatus == 0:
                                effect.set_volume(0.6)
                                effect.play(maxtime=200)
                                print '226 at ' + CurrentTime
                                VibrationStatus = 1
                                tt9653 = 1
                        if int(tt226) == 1:
                            if VibrationStatus == 1:
                                effect.stop
                                tt9653 = 0
                                VibrationStatus = 0
                    if int(tt225) == 5+tempQQ:
                        if int(tt226) == 0:
                            if VibrationStatus == 0:
                                effect.set_volume(0.5)
                                effect.play(maxtime=200)
                                print '225 at ' + CurrentTime
                                VibrationStatus = 1
                                tt9653 = 1
                        if int(tt226) == 1:
                            if VibrationStatus == 1:
                                effect.stop
                                tt9653 = 0
                                VibrationStatus = 0
                    if int(tt225) == 6+tempQQ:
                        if int(tt226) == 0:
                            if VibrationStatus == 0:
                                effect.set_volume(0.4)
                                effect.play(maxtime=200)
                                print '224 at ' + CurrentTime
                                VibrationStatus = 1
                                tt9653 = 1
                        if int(tt226) == 1:
                            if VibrationStatus == 1:
                                effect.stop
                                tt9653 = 0
                                VibrationStatus = 0
                    if int(tt225) == 7+tempQQ:
                        if int(tt226) == 0:
                            if VibrationStatus == 0:
                                effect.set_volume(0.3)
                                effect.play(maxtime=200)
                                print '223 at ' + CurrentTime
                                VibrationStatus = 1
                                tt9653 = 1
                        if int(tt226) == 1:
                            if VibrationStatus == 1:
                                effect.stop
                                tt9653 = 0
                                VibrationStatus = 0
                    if int(tt225) == 8+tempQQ:
                        if int(tt226) == 0:
                            if VibrationStatus == 0:
                                effect.set_volume(0.2)
                                effect.play(maxtime=200)
                                print '222 at ' + CurrentTime
                                VibrationStatus = 1
                                tt9653 = 1
                        if int(tt226) == 1:
                            if VibrationStatus == 1:
                                effect.stop
                                tt9653 = 0
                                VibrationStatus = 0
                    if int(tt225) == 9+tempQQ:
                        if int(tt226) == 0:
                            if VibrationStatus == 0:
                                effect.set_volume(0.2)
                                effect.play(maxtime=200)
                                print '222 at ' + CurrentTime
                                VibrationStatus = 1
                                tt9653 = 1
                        if int(tt226) == 1:
                            if VibrationStatus == 1:
                                effect.stop
                                tt9653 = 0
                                VibrationStatus = 0
                    if int(tt225) == 10+tempQQ:
                        if int(tt226) == 0:
                            if VibrationStatus == 0:
                                effect.set_volume(0.3)
                                effect.play(maxtime=200)
                                print '223 at ' + CurrentTime
                                VibrationStatus = 1
                                tt9653 = 1
                        if int(tt226) == 1:
                            if VibrationStatus == 1:
                                effect.stop
                                tt9653 = 0
                                VibrationStatus = 0
                    if int(tt225) == 11+tempQQ:
                        if int(tt226) == 0:
                            if VibrationStatus == 0:
                                effect.set_volume(0.4)
                                effect.play(maxtime=200)
                                print '224 at ' + CurrentTime
                                VibrationStatus = 1
                                tt9653 = 1
                        if int(tt226) == 1:
                            if VibrationStatus == 1:
                                effect.stop
                                tt9653 = 0
                                VibrationStatus = 0
                    if int(tt225) == 12+tempQQ:
                        if int(tt226) == 0:
                            if VibrationStatus == 0:
                                effect.set_volume(0.5)
                                effect.play(maxtime=200)
                                print '225 at ' + CurrentTime
                                VibrationStatus = 1
                                tt9653 = 1
                        if int(tt226) == 1:
                            if VibrationStatus == 1:
                                effect.stop
                                tt9653 = 0
                                VibrationStatus = 0
                    if int(tt225) == 13+tempQQ:
                        if int(tt226) == 0:
                            if VibrationStatus == 0:
                                effect.set_volume(0.6)
                                effect.play(maxtime=200)
                                print '226 at ' + CurrentTime
                                VibrationStatus = 1
                                tt9653 = 1
                        if int(tt226) == 1:
                            if VibrationStatus == 1:
                                effect.stop
                                tt9653 = 0
                                VibrationStatus = 0
                    if int(tt225) == 14+tempQQ:
                        if int(tt226) == 0:
                            if VibrationStatus == 0:
                                effect.set_volume(0.7)
                                effect.play(maxtime=200)
                                print '227 at ' + CurrentTime
                                VibrationStatus = 1
                                tt9653 = 1
                        if int(tt226) == 1:
                            if VibrationStatus == 1:
                                effect.stop
                                tt9653 = 0
                                VibrationStatus = 0
                    if int(tt225) == 15+tempQQ:
                        if int(tt226) == 0:
                            if VibrationStatus == 0:
                                effect.set_volume(0.8)
                                effect.play(maxtime=200)
                                print '228 at ' + CurrentTime
                                VibrationStatus = 1
                                tt9653 = 1
                        if int(tt226) == 1:
                            if VibrationStatus == 1:
                                effect.stop
                                tt9653 = 0
                                VibrationStatus = 0
                    if int(tt225) == 16+tempQQ:
                        if int(tt226) == 0:
                            if VibrationStatus == 0:
                                effect.set_volume(0.9)
                                effect.play(maxtime=200)
                                print '229 at ' + CurrentTime
                                VibrationStatus = 1
                                tt9653 = 1
                        if int(tt226) == 1:
                            if VibrationStatus == 1:
                                effect.stop
                                tt9653 = 0
                                VibrationStatus = 0
                    if int(tt225) == 17+tempQQ:
                        if int(tt226) == 0:
                            if VibrationStatus == 0:
                                effect.set_volume(1.0)
                                effect.play(maxtime=200)
                                print '230 at ' + CurrentTime
                                VibrationStatus = 1
                                tt9653 = 1
                        if int(tt226) == 1:
                            if VibrationStatus == 1:
                                effect.stop
                                tt9653 = 0
                                VibrationStatus = 0


                        # Capture frame-by-frame
    ret, frame = cap.read()
    
    # codes for the control panel
    try:
        gray2 = frame [:]
        if mode == 0:
            gray3 = copy.copy(frame)
        else:
            pass
            #gray4 = copy.deepcopy(frame)
        if dummy == 1:
            if setupbox == 0:
                setupbox = 1
                if RGB == 1:
                    #Below is for RGB
                    Tank01= cv2.VideoWriter(tt801 + '\\Tank01_RGB.avi',fourcc, 10.0, (boxes[1][0]-boxes[0][0],boxes[1][1]-boxes[0][1]))
                    Tank02= cv2.VideoWriter(tt802 + '\\Tank02_RGB.avi',fourcc, 10.0, (boxes[3][0]-boxes[2][0],boxes[3][1]-boxes[2][1]))
                    Tank03= cv2.VideoWriter(tt803 + '\\Tank03_RGB.avi',fourcc, 10.0, (boxes[5][0]-boxes[4][0],boxes[5][1]-boxes[4][1]))
                else:
                    #Below is for B/W
                    tt961 = strftime("%m",) + strftime("%d",) + '_' + strftime("%H",) + strftime("%M",) + strftime("%S",)
                    if int(HowMany) == 25:
                        tt962 = tt96 + 1
                        if (boxes[15][0]-boxes[0][0]) % 2 == 0:
                            if (boxes[15][1]-boxes[0][1]) % 2 == 0:
                                Tank0108= cv2.VideoWriter(tt801 + '\\Tank0108_BW_' + tt961 + '_' + ('%04d' % tt962) + '.avi',fourcc, int(framerate), ((boxes[15][0]-boxes[0][0])/2,(boxes[15][1]-boxes[0][1])/2),0)
                            else:
                                Tank0108= cv2.VideoWriter(tt801 + '\\Tank0108_BW_' + tt961 + '_' + ('%04d' % tt962) + '.avi',fourcc, int(framerate), ((boxes[15][0]-boxes[0][0])/2,((boxes[15][1]-boxes[0][1])/2)+1),0)
                        else:
                            if (boxes[15][1]-boxes[0][1]) % 2 == 0:
                                Tank0108= cv2.VideoWriter(tt801 + '\\Tank0108_BW_' + tt961 + '_' + ('%04d' % tt962) + '.avi',fourcc, int(framerate), (((boxes[15][0]-boxes[0][0])/2)+1,(boxes[15][1]-boxes[0][1])/2),0)
                            else:
                                Tank0108= cv2.VideoWriter(tt801 + '\\Tank0108_BW_' + tt961 + '_' + ('%04d' % tt962) + '.avi',fourcc, int(framerate), (((boxes[15][0]-boxes[0][0])/2)+1,((boxes[15][1]-boxes[0][1])/2)+1),0)

                        if (boxes[31][0]-boxes[16][0]) % 2 == 0:
                            if (boxes[31][1]-boxes[16][1]) % 2 == 0:
                                Tank0916= cv2.VideoWriter(tt802 + '\\Tank0916_BW_' + tt961 + '_' + ('%04d' % tt962) + '.avi',fourcc, int(framerate), ((boxes[31][0]-boxes[16][0])/2,(boxes[31][1]-boxes[16][1])/2),0)
                            else:
                                Tank0916= cv2.VideoWriter(tt802 + '\\Tank0916_BW_' + tt961 + '_' + ('%04d' % tt962) + '.avi',fourcc, int(framerate), ((boxes[31][0]-boxes[16][0])/2,((boxes[31][1]-boxes[16][1])/2)+1),0)
                        else:
                            if (boxes[31][1]-boxes[16][1]) % 2 == 0:
                                Tank0916= cv2.VideoWriter(tt802 + '\\Tank0916_BW_' + tt961 + '_' + ('%04d' % tt962) + '.avi',fourcc, int(framerate), (((boxes[31][0]-boxes[16][0])/2)+1,(boxes[31][1]-boxes[16][1])/2),0)
                            else:
                                Tank0916= cv2.VideoWriter(tt802 + '\\Tank0916_BW_' + tt961 + '_' + ('%04d' % tt962) + '.avi',fourcc, int(framerate), (((boxes[31][0]-boxes[16][0])/2)+1,((boxes[31][1]-boxes[16][1])/2)+1),0)

                        if (boxes[47][0]-boxes[32][0]) % 2 == 0:
                            if (boxes[47][1]-boxes[32][1]) % 2 == 0:
                                Tank1724= cv2.VideoWriter(tt803 + '\\Tank1724_BW_' + tt961 + '_' + ('%04d' % tt962) + '.avi',fourcc, int(framerate), ((boxes[47][0]-boxes[32][0])/2,(boxes[47][1]-boxes[32][1])/2),0)
                            else:
                                Tank1724= cv2.VideoWriter(tt803 + '\\Tank1724_BW_' + tt961 + '_' + ('%04d' % tt962) + '.avi',fourcc, int(framerate), ((boxes[47][0]-boxes[32][0])/2,((boxes[47][1]-boxes[32][1])/2)+1),0)
                        else:
                            if (boxes[47][1]-boxes[32][1]) % 2 == 0:
                                Tank1724= cv2.VideoWriter(tt803 + '\\Tank1724_BW_' + tt961 + '_' + ('%04d' % tt962) + '.avi',fourcc, int(framerate), (((boxes[47][0]-boxes[32][0])/2)+1,(boxes[47][1]-boxes[32][1])/2),0)
                            else:
                                Tank1724= cv2.VideoWriter(tt803 + '\\Tank1724_BW_' + tt961 + '_' + ('%04d' % tt962) + '.avi',fourcc, int(framerate), (((boxes[47][0]-boxes[32][0])/2)+1,((boxes[47][1]-boxes[32][1])/2)+1),0)


                        Tank25= cv2.VideoWriter(tt825 + '\\Tank25_BW_' + tt961 + '_' + ('%04d' % tt962) + '.avi',fourcc, int(framerate), (boxes[49][0]-boxes[48][0],boxes[49][1]-boxes[48][1]),0)

        if mode == 1:
            tt = time.time()
            tt1 = str(tt).find('.',1,len(str(tt)))
            tt2 = str(tt)[tt1-8:tt1]
            tt5 = str(tt)[tt1+1:len(str(tt))]
            tt4 = tt2 + tt5.ljust(2,'0')
            tt4 = str((int(tt4) - int(tt40))).rjust(8,'0')
            if tt91[1]==1:
                ser.write("4")  # Sets every ports low except the background infrared
                tt91[0]=int(tt4)
                for oo in range(Cycles):
                    tt91[(oo)*2+1] = int(tt4) + CycleDuration * 100 * ((oo)*2+1)
                    tt91[(oo)*2+2] = int(tt4) + CycleDuration * 100 * ((oo)*2+2)
            else:
                if int(tt4) - tt91[tt92] > 0 :
                    if tt92 % 2 == 1:
                        #ser.write("4")  
                        #print ('Output 8 is LOW for turnning on the white light')
                        tt92 = tt92 + 1
                        #tt93 = 1
                    else:
                        #ser.write("3")  
                        #print ('Output 8 is High for turnning off the whilte light')
                        if tt92 < Cycles * 2:
                            tt92 = tt92 + 1
                            if tt92 >= 2:
                                tt98 = int(HowMany)
                                tt96 = tt96 + 1
                                tt961 = strftime("%m",) + strftime("%d",) + '_' + strftime("%H",) + strftime("%M",) + strftime("%S",)
                                print ('Files_' + ('%04d' % tt96) + ' were saved at ' + tt961)
                                if int(HowMany) == 25:
                                    tt99 = Excel_Save(tt92, tt96, tt961, tt98, HowMany, GroupName, boxes, data01, data01Stamp, data02, data02Stamp, data03, data03Stamp, data04, data04Stamp, data05, data05Stamp, data06, data06Stamp, data07, data07Stamp, data08, data08Stamp, data09, data09Stamp, data10, data10Stamp,data11, data11Stamp, data12, data12Stamp, data13, data13Stamp, data14, data14Stamp, data15, data15Stamp, data16, data16Stamp, data17, data17Stamp, data18, data18Stamp, data19, data19Stamp, data20, data20Stamp, data21, data21Stamp, data22, data22Stamp, data23, data23Stamp, data24, data24Stamp, Tank0108, Tank0916, Tank1724, Tank25)
                                    tt962 = tt96 + 1
                                    if (boxes[15][0]-boxes[0][0]) % 2 == 0:
                                        if (boxes[15][1]-boxes[0][1]) % 2 == 0:
                                            Tank0108= cv2.VideoWriter(tt801 + '\\Tank0108_BW_' + tt961 + '_' + ('%04d' % tt962) + '.avi',fourcc, int(framerate), ((boxes[15][0]-boxes[0][0])/2,(boxes[15][1]-boxes[0][1])/2),0)
                                        else:
                                            Tank0108= cv2.VideoWriter(tt801 + '\\Tank0108_BW_' + tt961 + '_' + ('%04d' % tt962) + '.avi',fourcc, int(framerate), ((boxes[15][0]-boxes[0][0])/2,((boxes[15][1]-boxes[0][1])/2)+1),0)
                                    else:
                                        if (boxes[15][1]-boxes[0][1]) % 2 == 0:
                                            Tank0108= cv2.VideoWriter(tt801 + '\\Tank0108_BW_' + tt961 + '_' + ('%04d' % tt962) + '.avi',fourcc, int(framerate), (((boxes[15][0]-boxes[0][0])/2)+1,(boxes[15][1]-boxes[0][1])/2),0)
                                        else:
                                            Tank0108= cv2.VideoWriter(tt801 + '\\Tank0108_BW_' + tt961 + '_' + ('%04d' % tt962) + '.avi',fourcc, int(framerate), (((boxes[15][0]-boxes[0][0])/2)+1,((boxes[15][1]-boxes[0][1])/2)+1),0)

                                    if (boxes[31][0]-boxes[16][0]) % 2 == 0:
                                        if (boxes[31][1]-boxes[16][1]) % 2 == 0:
                                            Tank0916= cv2.VideoWriter(tt802 + '\\Tank0916_BW_' + tt961 + '_' + ('%04d' % tt962) + '.avi',fourcc, int(framerate), ((boxes[31][0]-boxes[16][0])/2,(boxes[31][1]-boxes[16][1])/2),0)
                                        else:
                                            Tank0916= cv2.VideoWriter(tt802 + '\\Tank0916_BW_' + tt961 + '_' + ('%04d' % tt962) + '.avi',fourcc, int(framerate), ((boxes[31][0]-boxes[16][0])/2,((boxes[31][1]-boxes[16][1])/2)+1),0)
                                    else:
                                        if (boxes[31][1]-boxes[16][1]) % 2 == 0:
                                            Tank0916= cv2.VideoWriter(tt802 + '\\Tank0916_BW_' + tt961 + '_' + ('%04d' % tt962) + '.avi',fourcc, int(framerate), (((boxes[31][0]-boxes[16][0])/2)+1,(boxes[31][1]-boxes[16][1])/2),0)
                                        else:
                                            Tank0916= cv2.VideoWriter(tt802 + '\\Tank0916_BW_' + tt961 + '_' + ('%04d' % tt962) + '.avi',fourcc, int(framerate), (((boxes[31][0]-boxes[16][0])/2)+1,((boxes[31][1]-boxes[16][1])/2)+1),0)

                                    if (boxes[47][0]-boxes[32][0]) % 2 == 0:
                                        if (boxes[47][1]-boxes[32][1]) % 2 == 0:
                                            Tank1724= cv2.VideoWriter(tt803 + '\\Tank1724_BW_' + tt961 + '_' + ('%04d' % tt962) + '.avi',fourcc, int(framerate), ((boxes[47][0]-boxes[32][0])/2,(boxes[47][1]-boxes[32][1])/2),0)
                                        else:
                                            Tank1724= cv2.VideoWriter(tt803 + '\\Tank1724_BW_' + tt961 + '_' + ('%04d' % tt962) + '.avi',fourcc, int(framerate), ((boxes[47][0]-boxes[32][0])/2,((boxes[47][1]-boxes[32][1])/2)+1),0)
                                    else:
                                        if (boxes[47][1]-boxes[32][1]) % 2 == 0:
                                            Tank1724= cv2.VideoWriter(tt803 + '\\Tank1724_BW_' + tt961 + '_' + ('%04d' % tt962) + '.avi',fourcc, int(framerate), (((boxes[47][0]-boxes[32][0])/2)+1,(boxes[47][1]-boxes[32][1])/2),0)
                                        else:
                                            Tank1724= cv2.VideoWriter(tt803 + '\\Tank1724_BW_' + tt961 + '_' + ('%04d' % tt962) + '.avi',fourcc, int(framerate), (((boxes[47][0]-boxes[32][0])/2)+1,((boxes[47][1]-boxes[32][1])/2)+1),0)


                                    Tank25= cv2.VideoWriter(tt825 + '\\Tank25_BW_' + tt961 + '_' + ('%04d' % tt962) + '.avi',fourcc, int(framerate), (boxes[49][0]-boxes[48][0],boxes[49][1]-boxes[48][1]),0)

                                    data01=[];
                                    data01Stamp=[];
                                    data02=[];
                                    data02Stamp=[];
                                    data03=[];
                                    data03Stamp=[];
                                    data04=[];
                                    data04Stamp=[];
                                    data05=[];
                                    data05Stamp=[];
                                    data06=[];
                                    data06Stamp=[];
                                    data07=[];
                                    data07Stamp=[];
                                    data08=[];
                                    data08Stamp=[];
                                    data09=[];
                                    data09Stamp=[];
                                    data10=[];
                                    data10Stamp=[];
                                    data11=[];
                                    data11Stamp=[];
                                    data12=[];
                                    data12Stamp=[];
                                    data13=[];
                                    data13Stamp=[];
                                    data14=[];
                                    data14Stamp=[];
                                    data15=[];
                                    data15Stamp=[];
                                    data16=[];
                                    data16Stamp=[];
                                    data17 = [];
                                    data17Stamp = [];
                                    data18 = [];
                                    data18Stamp = [];
                                    data19 = [];
                                    data19Stamp = [];
                                    data20 = [];
                                    data20Stamp = [];
                                    data21 = [];
                                    data21Stamp = [];
                                    data22 = [];
                                    data22Stamp = [];
                                    data23 = [];
                                    data23Stamp = [];
                                    data24 = [];
                                    data24Stamp = [];

                        elif tt92 == Cycles * 2:
                            # ser.write("6")  # Sets every ports low except the background infrared
                            tt964 = 1
                else:
                    # print int(tt4) - tt91[tt92]
                    tt4 = tt4
            if int(HowMany) > 1:
                cv2.rectangle(gray2,(boxes[0][0],boxes[0][1]),(boxes[1][0],boxes[1][1]), (0,255,0),1)
                cv2.rectangle(gray2,(boxes[2][0],boxes[2][1]),(boxes[3][0],boxes[3][1]), (0,0,255),1)
                if int(HowMany) > 2:
                    cv2.rectangle(gray2,(boxes[4][0],boxes[4][1]),(boxes[5][0],boxes[5][1]), (0,255,0),1)
                    if int(HowMany) > 3:
                        cv2.rectangle(gray2,(boxes[6][0],boxes[6][1]),(boxes[7][0],boxes[7][1]), (0,0,255),1)
                        if int(HowMany) > 4:
                            cv2.rectangle(gray2,(boxes[8][0],boxes[8][1]),(boxes[9][0],boxes[9][1]), (0,255,0),1)
                            if int(HowMany) > 5:
                                cv2.rectangle(gray2,(boxes[10][0],boxes[10][1]),(boxes[11][0],boxes[11][1]), (0,0,255),1)
                                if int(HowMany) > 6:
                                    cv2.rectangle(gray2,(boxes[12][0],boxes[12][1]),(boxes[13][0],boxes[13][1]), (0,255,0),1)
                                    if int(HowMany) > 7:
                                        cv2.rectangle(gray2,(boxes[14][0],boxes[14][1]),(boxes[15][0],boxes[15][1]), (0,0,255),1)
                                        if int(HowMany) > 8:
                                            cv2.rectangle(gray2,(boxes[16][0],boxes[16][1]),(boxes[17][0],boxes[17][1]), (0,255,0),1)
                                            if int(HowMany) > 9:
                                                cv2.rectangle(gray2,(boxes[18][0],boxes[18][1]),(boxes[19][0],boxes[19][1]), (0,0,255),1)
                                                if int(HowMany) > 10:
                                                    cv2.rectangle(gray2,(boxes[20][0],boxes[20][1]),(boxes[21][0],boxes[21][1]), (0,255,0),1)
                                                    if int(HowMany) > 11:
                                                        cv2.rectangle(gray2,(boxes[22][0],boxes[22][1]),(boxes[23][0],boxes[23][1]), (0,0,255),1)
                                                        if int(HowMany) > 12:
                                                            cv2.rectangle(gray2,(boxes[24][0],boxes[24][1]),(boxes[25][0],boxes[25][1]), (0,255,0),1)
                                                            if int(HowMany) > 13:
                                                                cv2.rectangle(gray2,(boxes[26][0],boxes[26][1]),(boxes[27][0],boxes[27][1]), (0,0,255),1)
                                                                if int(HowMany) > 14:
                                                                    cv2.rectangle(gray2,(boxes[28][0],boxes[28][1]),(boxes[29][0],boxes[29][1]), (0,255,0),1)
                                                                    if int(HowMany) > 15:
                                                                        cv2.rectangle(gray2,(boxes[30][0],boxes[30][1]),(boxes[31][0],boxes[31][1]), (0,0,255),1)
                                                                        if int(HowMany) > 16:
                                                                            cv2.rectangle(gray2,(boxes[32][0],boxes[32][1]),(boxes[33][0],boxes[33][1]), (0,255,0),1)
                                                                            if int(HowMany) > 17:
                                                                                cv2.rectangle(gray2,(boxes[34][0],boxes[34][1]),(boxes[35][0],boxes[35][1]), (0,255,0),1)
                                                                                if int(HowMany) > 18:
                                                                                    cv2.rectangle(gray2,(boxes[36][0],boxes[36][1]),(boxes[37][0],boxes[37][1]), (0,255,0),1)
                                                                                    if int(HowMany) > 19:
                                                                                        cv2.rectangle(gray2,(boxes[38][0],boxes[38][1]),(boxes[39][0],boxes[39][1]), (0,255,0),1)
                                                                                        if int(HowMany) > 20:
                                                                                            cv2.rectangle(gray2,(boxes[40][0],boxes[40][1]),(boxes[41][0],boxes[41][1]), (0,255,0),1)
                                                                                            if int(HowMany) > 21:
                                                                                                cv2.rectangle(gray2,(boxes[42][0],boxes[42][1]),(boxes[43][0],boxes[43][1]), (0,255,0),1)
                                                                                                if int(HowMany) > 22:
                                                                                                    cv2.rectangle(gray2,(boxes[44][0],boxes[44][1]),(boxes[45][0],boxes[45][1]), (0,255,0),1)
                                                                                                    if int(HowMany) > 23:
                                                                                                        cv2.rectangle(gray2,(boxes[46][0],boxes[46][1]),(boxes[47][0],boxes[47][1]), (0,255,0),1)
                                                                                                        if int(HowMany) > 24:
                                                                                                            cv2.rectangle(gray2,(boxes[48][0],boxes[48][1]),(boxes[49][0],boxes[49][1]), (0,255,0),1)

            # Below is for Tank 1 tracking =======================================================
            if HowMany > 1:
                tt961ab = '1' # tracking
                if oldL01 == 1:
                    img1 = cv2.subtract(gray3[oldY01-SearchSize:oldY01+SearchSize,oldX01-SearchSize:oldX01+SearchSize],gray2[oldY01-SearchSize:oldY01+SearchSize,oldX01-SearchSize:oldX01+SearchSize]) # local view
                    keypoints = detector.detect(img1)
                    if len(keypoints) > 0:
                        oldX01 = oldX01 - (SearchSize - int(keypoints[0].pt[0]) + boxes[0][0]) + boxes[0][0]
                        oldY01 = oldY01 - (SearchSize - int(keypoints[0].pt[1]) + boxes[0][1]) + boxes[0][1]
                        cv2.circle(gray2, (oldX01, oldY01), 5, (0,0,255),0)
                        #cv2.imshow('frame',gray2)
                        small01=1
                    else:
                        cv2.subtract(gray3[oldY01-SearchSize*2:oldY01+SearchSize*2,oldX01-SearchSize*2:oldX01+SearchSize*2],gray2[oldY01-SearchSize*2:oldY01+SearchSize*2,oldX01-SearchSize*2:oldX01+SearchSize*2]) # extended local view
                        keypoints = detector.detect(img1)
                        if len(keypoints) > 0:
                            oldX01 = int(keypoints[0].pt[0]) + boxes[0][0]
                            oldY01 = int(keypoints[0].pt[1]) + boxes[0][1]
                            cv2.circle(gray2, (oldX01, oldY01), 5, (0,0,255),0)
                            #cv2.imshow('frame',gray2)
                            small01=1
                        else:
                            small01=0
                else:
                    img1 = cv2.subtract(gray3[boxes[0][1]:boxes[1][1],boxes[0][0]:boxes[1][0]],gray2[boxes[0][1]:boxes[1][1],boxes[0][0]:boxes[1][0]]) # global view
                    keypoints = detector.detect(img1)
                    if len(keypoints) > 0:
                        oldX01 = int(keypoints[0].pt[0]) + boxes[0][0]
                        oldY01 = int(keypoints[0].pt[1]) + boxes[0][1]
                        cv2.circle(gray2, (oldX01, oldY01), 5, (0,0,255),0)
                        #cv2.imshow('frame',gray2)
                        small01=1
                    else:
                        small01=0


                if len(keypoints)>0:
                    if small01 < 1:
                        oldL01=1
                        data01.append([oldX01, oldY01])
                    else:
                        data01.append([oldX01, oldY01])
                else:
                    data01.append([0,0])
                    oldL01 = 0

            # ===========================================================================================

            # Below is for Tank 2 tracking =======================================================
            if int(HowMany) > 2:
            
                if oldL02 == 1:
                    img1 = cv2.subtract(gray3[oldY02-SearchSize:oldY02+SearchSize,oldX02-SearchSize:oldX02+SearchSize],gray2[oldY02-SearchSize:oldY02+SearchSize,oldX02-SearchSize:oldX02+SearchSize]) # local view
                    keypoints = detector.detect(img1)
                    if len(keypoints) > 0:
                        oldX02 = oldX02 - (SearchSize - int(keypoints[0].pt[0]) + boxes[2][0]) + boxes[2][0]
                        oldY02 = oldY02 - (SearchSize - int(keypoints[0].pt[1]) + boxes[2][1]) + boxes[2][1]
                        cv2.circle(gray2, (oldX02, oldY02), 5, (0,0,255),0)
                        #cv2.imshow('frame',gray2)
                        small02=1
                    else:
                        img1 = cv2.subtract(gray3[oldY02-SearchSize*2:oldY02+SearchSize*2,oldX02-SearchSize*2:oldX02+SearchSize*2],gray2[oldY02-SearchSize*2:oldY02+SearchSize*2,oldX02-SearchSize*2:oldX02+SearchSize*2]) # Extended local view
                        keypoints = detector.detect(img1)
                        if len(keypoints) > 0:
                            oldX02 = int(keypoints[0].pt[0]) + boxes[2][0]
                            oldY02 = int(keypoints[0].pt[1]) + boxes[2][1]
                            cv2.circle(gray2, (oldX02, oldY02), 5, (0,0,255),0)
                            #cv2.imshow('frame',gray2)
                            small02=1
                        else:
                            small02=0
                else:
                    img1 = cv2.subtract(gray3[boxes[2][1]:boxes[3][1],boxes[2][0]:boxes[3][0]],gray2[boxes[2][1]:boxes[3][1],boxes[2][0]:boxes[3][0]]) # global view
                    keypoints = detector.detect(img1)
                    if len(keypoints)>0:
                        oldX02 = int(keypoints[0].pt[0]) + boxes[2][0]
                        oldY02 = int(keypoints[0].pt[1]) + boxes[2][1]
                        cv2.circle(gray2, (oldX02, oldY02), 5, (0,0,255),0)
                        #cv2.imshow('frame',gray2)
                        small02=1
                    else:
                        small02=0

                if len(keypoints)>0:
                    if small02 < 1:
                        oldL02=1
                        data02.append([oldX02, oldY02])
                    else:
                        data02.append([oldX02, oldY02])
                else:
                    data02.append([0,0])
                    oldL02 = 0
            # =========================================================
            # Below is for Tank 3 tracking =======================================================
            if int(HowMany) > 3:
            
                if oldL03 == 1:
                    img1 = cv2.subtract(gray3[oldY03-SearchSize:oldY03+SearchSize,oldX03-SearchSize:oldX03+SearchSize],gray2[oldY03-SearchSize:oldY03+SearchSize,oldX03-SearchSize:oldX03+SearchSize]) # local view
                    keypoints = detector.detect(img1)
                    if len(keypoints) > 0:
                        oldX03 = oldX03 - (SearchSize - int(keypoints[0].pt[0]) + boxes[4][0]) + boxes[4][0]
                        oldY03 = oldY03 - (SearchSize - int(keypoints[0].pt[1]) + boxes[4][1]) + boxes[4][1]
                        cv2.circle(gray2, (oldX03, oldY3), 5, (0,0,255),0)
                        #cv2.imshow('frame',gray2)
                        small03=1
                    else:
                        img1 = cv2.subtract(gray3[oldY03-SearchSize*2:oldY03+SearchSize*2,oldX03-SearchSize*2:oldX03+SearchSize*2],gray2[oldY03-SearchSize*2:oldY03+SearchSize*2,oldX03-SearchSize*2:oldX03+SearchSize*2]) # Extended local view
                        keypoints = detector.detect(img1)
                        if len(keypoints) > 0:
                            oldX03 = int(keypoints[0].pt[0]) + boxes[4][0]
                            oldY03 = int(keypoints[0].pt[1]) + boxes[4][1]
                            cv2.circle(gray2, (oldX03, oldY03), 5, (0,0,255),0)
                            #cv2.imshow('frame',gray2)
                            small03=1
                        else:
                            small03=0
                else:
                    img1 = cv2.subtract(gray3[boxes[4][1]:boxes[5][1],boxes[4][0]:boxes[5][0]],gray2[boxes[4][1]:boxes[5][1],boxes[4][0]:boxes[5][0]]) # global view
                    keypoints = detector.detect(img1)
                    if len(keypoints)>0:
                        oldX03 = int(keypoints[0].pt[0]) + boxes[4][0]
                        oldY03 = int(keypoints[0].pt[1]) + boxes[4][1]
                        cv2.circle(gray2, (oldX03, oldY03), 5, (0,0,255),0)
                        #cv2.imshow('frame',gray2)
                        small03=1
                    else:
                        small03=0
    
                if len(keypoints)>0:
                    if small03 < 1:
                        oldL03=1
                        data03.append([oldX03, oldY03])
                    else:
                        data03.append([oldX03, oldY03])
                else:
                    data03.append([0,0])
                    oldL03 = 0
            # ================================================        
            # Below is for Tank 4 tracking =======================================================
            if int(HowMany) > 4:
            
                if oldL04 == 1:
                    img1 = cv2.subtract(gray3[oldY04-SearchSize:oldY04+SearchSize,oldX04-SearchSize:oldX04+SearchSize],gray2[oldY04-SearchSize:oldY04+SearchSize,oldX04-SearchSize:oldX04+SearchSize]) # local view
                    keypoints = detector.detect(img1)
                    if len(keypoints) > 0:
                        oldX04 = oldX04 - (SearchSize - int(keypoints[0].pt[0]) + boxes[6][0]) + boxes[6][0]
                        oldY04 = oldY04 - (SearchSize - int(keypoints[0].pt[1]) + boxes[6][1]) + boxes[6][1]
                        cv2.circle(gray2, (oldX04, oldY04), 5, (0,0,255),0)
                        #cv2.imshow('frame',gray2)
                        small04=1
                    else:
                        img1 = cv2.subtract(gray3[oldY04-SearchSize*2:oldY04+SearchSize*2,oldX04-SearchSize*2:oldX04+SearchSize*2],gray2[oldY04-SearchSize*2:oldY04+SearchSize*2,oldX04-SearchSize*2:oldX04+SearchSize*2]) # local view
                        keypoints = detector.detect(img1)
                        if len(keypoints) > 0:
                            oldX04 = int(keypoints[0].pt[0]) + boxes[6][0]
                            oldY04 = int(keypoints[0].pt[1]) + boxes[6][1]
                            cv2.circle(gray2, (oldX04, oldY04), 5, (0,0,255),0)
                            #cv2.imshow('frame',gray2)
                            small04=1
                        else:
                            small04=0

                else:
                    img1 = cv2.subtract(gray3[boxes[6][1]:boxes[7][1],boxes[6][0]:boxes[7][0]],gray2[boxes[6][1]:boxes[7][1],boxes[6][0]:boxes[7][0]]) # global view
                    keypoints = detector.detect(img1)
                    if len(keypoints)>0:
                        oldX04 = int(keypoints[0].pt[0]) + boxes[6][0]
                        oldY04 = int(keypoints[0].pt[1]) + boxes[6][1]
                        cv2.circle(gray2, (oldX04, oldY04), 5, (0,0,255),0)
                        #cv2.imshow('frame',gray2)
                        small04=1
                    else:
                        small04=0
                        cv2.imshow('frame',gray2)
                if len(keypoints)>0:
                    if small04 < 1:
                        oldL04=1
                        data04.append([oldX04, oldY04])
                    else:
                        data04.append([oldX04, oldY04])
                else:
                    data04.append([0,0])
                    oldL04 = 0
            # ================================================        
            # Below is for Tank 5 tracking =======================================================
            if int(HowMany) > 5:
            
                if oldL05 == 1:
                    img1 = cv2.subtract(gray3[oldY05-SearchSize:oldY05+SearchSize,oldX05-SearchSize:oldX05+SearchSize],gray2[oldY05-SearchSize:oldY05+SearchSize,oldX05-SearchSize:oldX05+SearchSize]) # local view
                    keypoints = detector.detect(img1)
                    if len(keypoints) > 0:
                        oldX05 = oldX05 - (SearchSize - int(keypoints[0].pt[0]) + boxes[8][0]) + boxes[8][0]
                        oldY05 = oldY05 - (SearchSize - int(keypoints[0].pt[1]) + boxes[8][1]) + boxes[8][1]
                        cv2.circle(gray2, (oldX05, oldY05), 5, (0,0,255),0)
                        #cv2.imshow('frame',gray2)
                        small05=1
                    else:
                        img1 = cv2.subtract(gray3[oldY05-SearchSize*2:oldY05+SearchSize*2,oldX05-SearchSize*2:oldX05+SearchSize*2],gray2[oldY05-SearchSize*2:oldY05+SearchSize*2,oldX05-SearchSize*2:oldX05+SearchSize*2]) # Extended local view
                        keypoints = detector.detect(img1)
                        if len(keypoints) > 0:
                            oldX05 = int(keypoints[0].pt[0]) + boxes[8][0]
                            oldY05 = int(keypoints[0].pt[1]) + boxes[8][1]
                            cv2.circle(gray2, (oldX05, oldY05), 5, (0,0,255),0)
                            #cv2.imshow('frame',gray2)
                            small05=1
                        else:
                            small05=0
                else:
                    img1 = cv2.subtract(gray3[boxes[8][1]:boxes[9][1],boxes[8][0]:boxes[9][0]],gray2[boxes[8][1]:boxes[9][1],boxes[8][0]:boxes[9][0]]) # global view
                    keypoints = detector.detect(img1)
                    if len(keypoints)>0:
                        oldX05 = int(keypoints[0].pt[0]) + boxes[8][0]
                        oldY05 = int(keypoints[0].pt[1]) + boxes[8][1]
                        cv2.circle(gray2, (oldX05, oldY05), 5, (0,0,255),0)
                        #cv2.imshow('frame',gray2)
                        small05=1
                    else:
                        small05=0

                if len(keypoints)>0:
                    if small05 < 1:
                        oldL05=1
                        data05.append([oldX05, oldY05])
                    else:
                        data05.append([oldX05, oldY05])
                else:
                    data05.append([0,0])
                    oldL05 = 0
            # ================================================        
            # Below is for Tank 6 tracking =======================================================
            if int(HowMany) > 6:
            
                if oldL06 == 1:
                    img1 = cv2.subtract(gray3[oldY06-SearchSize:oldY06+SearchSize,oldX06-SearchSize:oldX06+SearchSize],gray2[oldY06-SearchSize:oldY06+SearchSize,oldX06-SearchSize:oldX06+SearchSize]) # local view
                    keypoints = detector.detect(img1)
                    if len(keypoints) > 0:
                        oldX06 = oldX06 - (SearchSize - int(keypoints[0].pt[0]) + boxes[10][0]) + boxes[10][0]
                        oldY06 = oldY06 - (SearchSize - int(keypoints[0].pt[1]) + boxes[10][1]) + boxes[10][1]
                        cv2.circle(gray2, (oldX06, oldY06), 5, (0,0,255),0)
                        #cv2.imshow('frame',gray2)
                        small06=1
                    else:
                        img1 = cv2.subtract(gray3[oldY06-SearchSize*2:oldY06+SearchSize*2,oldX06-SearchSize*2:oldX06+SearchSize*2],gray2[oldY06-SearchSize*2:oldY06+SearchSize*2,oldX06-SearchSize*2:oldX06+SearchSize*2]) # Extended local view
                        keypoints = detector.detect(img1)
                        if len(keypoints) > 0:
                            oldX06 = int(keypoints[0].pt[0]) + boxes[10][0]
                            oldY06 = int(keypoints[0].pt[1]) + boxes[10][1]
                            cv2.circle(gray2, (oldX06, oldY06), 5, (0,0,255),0)
                            #cv2.imshow('frame',gray2)
                            small06=1
                        else:
                            small06=0
                else:
                    img1 = cv2.subtract(gray3[boxes[10][1]:boxes[11][1],boxes[10][0]:boxes[11][0]],gray2[boxes[10][1]:boxes[11][1],boxes[10][0]:boxes[11][0]]) # global view
                    keypoints = detector.detect(img1)
                    if len(keypoints)>0:
                        oldX06 = int(keypoints[0].pt[0]) + boxes[10][0]
                        oldY06 = int(keypoints[0].pt[1]) + boxes[10][1]
                        cv2.circle(gray2, (oldX06, oldY06), 5, (0,0,255),0)
                        #cv2.imshow('frame',gray2)
                        small06=1
                    else:
                        small06=0

                if len(keypoints)>0:
                    if small06 < 1:
                        oldL06=1
                        data06.append([oldX06, oldY06])
                    else:
                        data06.append([oldX06, oldY06])
                else:
                    data06.append([0,0])
                    oldL06 = 0
            # ================================================        
            # Below is for Tank 7 tracking =======================================================
            if int(HowMany) > 7:
            
                if oldL07 == 1:
                    img1 = cv2.subtract(gray3[oldY07-SearchSize:oldY07+SearchSize,oldX07-SearchSize:oldX07+SearchSize],gray2[oldY07-SearchSize:oldY07+SearchSize,oldX07-SearchSize:oldX07+SearchSize]) # local view
                    keypoints = detector.detect(img1)
                    if len(keypoints) > 0:
                        oldX07 = oldX07 - (SearchSize - int(keypoints[0].pt[0]) + boxes[12][0]) + boxes[12][0]
                        oldY07 = oldY07 - (SearchSize - int(keypoints[0].pt[1]) + boxes[12][1]) + boxes[12][1]
                        cv2.circle(gray2, (oldX07, oldY07), 5, (0,0,255),0)
                        #cv2.imshow('frame',gray2)
                        small07=1
                    else:
                        img1 = cv2.subtract(gray3[oldY07-SearchSize*2:oldY07+SearchSize*2,oldX07-SearchSize*2:oldX07+SearchSize*2],gray2[oldY07-SearchSize*2:oldY07+SearchSize*2,oldX07-SearchSize*2:oldX07+SearchSize*2]) # Extended local view
                        keypoints = detector.detect(img1)
                        if len(keypoints) > 0:
                            oldX07 = int(keypoints[0].pt[0]) + boxes[12][0]
                            oldY07 = int(keypoints[0].pt[1]) + boxes[12][1]
                            cv2.circle(gray2, (oldX07, oldY07), 5, (0,0,255),0)
                            #cv2.imshow('frame',gray2)
                            small07=1
                        else:
                            small07=0
                else:
                    img1 = cv2.subtract(gray3[boxes[12][1]:boxes[13][1],boxes[12][0]:boxes[13][0]],gray2[boxes[12][1]:boxes[13][1],boxes[12][0]:boxes[13][0]]) # global view
                    keypoints = detector.detect(img1)
                    if len(keypoints)>0:
                        oldX07 = int(keypoints[0].pt[0]) + boxes[12][0]
                        oldY07 = int(keypoints[0].pt[1]) + boxes[12][1]
                        cv2.circle(gray2, (oldX07, oldY07), 5, (0,0,255),0)
                        #cv2.imshow('frame',gray2)
                        small07=1
                    else:
                        small07=0

                if len(keypoints)>0:
                    if small07 < 1:
                        oldL07=1
                        data07.append([oldX07, oldY07])
                    else:
                        data07.append([oldX07, oldY07])
                else:
                    data07.append([0,0])
                    oldL07 = 0
            # ================================================        
            # Below is for Tank 8 tracking =======================================================
            if int(HowMany) > 8:
            
                if oldL08 == 1:
                    img1 = cv2.subtract(gray3[oldY08-SearchSize:oldY08+SearchSize,oldX08-SearchSize:oldX08+SearchSize],gray2[oldY08-SearchSize:oldY08+SearchSize,oldX08-SearchSize:oldX08+SearchSize]) # local view
                    keypoints = detector.detect(img1)
                    if len(keypoints) > 0:
                        oldX08 = oldX08 - (SearchSize - int(keypoints[0].pt[0]) + boxes[14][0]) + boxes[14][0]
                        oldY08 = oldY08 - (SearchSize - int(keypoints[0].pt[1]) + boxes[14][1]) + boxes[14][1]
                        cv2.circle(gray2, (oldX08, oldY08), 5, (0,0,255),0)
                        #cv2.imshow('frame',gray2)
                        small08=1
                    else:
                        img1 = cv2.subtract(gray3[oldY08-SearchSize*2:oldY08+SearchSize*2,oldX08-SearchSize*2:oldX08+SearchSize*2],gray2[oldY08-SearchSize*2:oldY08+SearchSize*2,oldX08-SearchSize*2:oldX08+SearchSize*2]) # Extended local view
                        keypoints = detector.detect(img1)
                        if len(keypoints) > 0:
                            oldX08 = int(keypoints[0].pt[0]) + boxes[14][0]
                            oldY08 = int(keypoints[0].pt[1]) + boxes[14][1]
                            cv2.circle(gray2, (oldX08, oldY08), 5, (0,0,255),0)
                            #cv2.imshow('frame',gray2)
                            small08=1
                        else:
                            small08=0
                else:
                    img1 = cv2.subtract(gray3[boxes[14][1]:boxes[15][1],boxes[14][0]:boxes[15][0]],gray2[boxes[14][1]:boxes[15][1],boxes[14][0]:boxes[15][0]]) # global view
                    keypoints = detector.detect(img1)
                    if len(keypoints)>0:
                        oldX08 = int(keypoints[0].pt[0]) + boxes[14][0]
                        oldY08 = int(keypoints[0].pt[1]) + boxes[14][1]
                        cv2.circle(gray2, (oldX08, oldY08), 5, (0,0,255),0)
                        #cv2.imshow('frame',gray2)
                        small08=1
                    else:
                        small08=0

                if len(keypoints)>0:
                    if small08 < 1:
                        oldL08=1
                        data08.append([oldX08, oldY08])
                    else:
                        data08.append([oldX08, oldY08])
                else:
                    data08.append([0,0])
                    oldL08 = 0
            # ================================================        
            # Below is for Tank 9 tracking =======================================================
            if int(HowMany) > 9:
                
                if oldL09 == 1:
                    img1 = cv2.subtract(gray3[oldY09-SearchSize:oldY09+SearchSize,oldX09-SearchSize:oldX09+SearchSize],gray2[oldY09-SearchSize:oldY09+SearchSize,oldX09-SearchSize:oldX09+SearchSize]) # local view
                    keypoints = detector.detect(img1)
                    if len(keypoints) > 0:
                        oldX09 = oldX09 - (SearchSize - int(keypoints[0].pt[0]) + boxes[16][0]) + boxes[16][0]
                        oldY09 = oldY09 - (SearchSize - int(keypoints[0].pt[1]) + boxes[16][1]) + boxes[16][1]
                        cv2.circle(gray2, (oldX09, oldY09), 5, (0,0,255),0)
                        #cv2.imshow('frame',gray2)
                        small09=1
                    else:
                        img1 = cv2.subtract(gray3[oldY09-SearchSize*2:oldY09+SearchSize*2,oldX09-SearchSize*2:oldX09+SearchSize*2],gray2[oldY09-SearchSize*2:oldY09+SearchSize*2,oldX09-SearchSize*2:oldX09+SearchSize*2]) # Extended local view
                        keypoints = detector.detect(img1)
                        if len(keypoints) > 0:
                            oldX09 = int(keypoints[0].pt[0]) + boxes[16][0]
                            oldY09 = int(keypoints[0].pt[1]) + boxes[16][1]
                            cv2.circle(gray2, (oldX09, oldY09), 5, (0,0,255),0)
                            #cv2.imshow('frame',gray2)
                            small09=1
                        else:
                            small09=0
                else:
                    img1 = cv2.subtract(gray3[boxes[16][1]:boxes[17][1],boxes[16][0]:boxes[17][0]],gray2[boxes[16][1]:boxes[17][1],boxes[16][0]:boxes[17][0]]) # global view
                    keypoints = detector.detect(img1)
                    if len(keypoints)>0:
                        oldX09 = int(keypoints[0].pt[0]) + boxes[16][0]
                        oldY09 = int(keypoints[0].pt[1]) + boxes[16][1]
                        cv2.circle(gray2, (oldX09, oldY09), 5, (0,0,255),0)
                        #cv2.imshow('frame',gray2)
                        small09=1
                    else:
                        small09=0

                if len(keypoints)>0:
                    if small09 < 1:
                        oldL09=1
                        data09.append([oldX09, oldY09])
                    else:
                        data09.append([oldX09, oldY09])
                else:
                    data09.append([0,0])
                    oldL09 = 0
            # ================================================        

            # Below is for Tank 10 tracking =======================================================
            if int(HowMany) > 10:
            
                if oldL10 == 1:
                    img1 = cv2.subtract(gray3[oldY10-SearchSize:oldY10+SearchSize,oldX10-SearchSize:oldX10+SearchSize],gray2[oldY10-SearchSize:oldY10+SearchSize,oldX10-SearchSize:oldX10+SearchSize]) # local view
                    keypoints = detector.detect(img1)
                    if len(keypoints) > 0:
                        oldX10 = oldX10 - (SearchSize - int(keypoints[0].pt[0]) + boxes[18][0]) + boxes[18][0]
                        oldY10 = oldY10 - (SearchSize - int(keypoints[0].pt[1]) + boxes[18][1]) + boxes[18][1]
                        cv2.circle(gray2, (oldX10, oldY10), 5, (0,0,255),0)
                        #cv2.imshow('frame',gray2)
                        small10=1
                    else:
                        img1 = cv2.subtract(gray3[oldY10-SearchSize*2:oldY10+SearchSize*2,oldX10-SearchSize*2:oldX10+SearchSize*2],gray2[oldY10-SearchSize*2:oldY10+SearchSize*2,oldX10-SearchSize*2:oldX10+SearchSize*2]) # Extended local view
                        keypoints = detector.detect(img1)
                        if len(keypoints) > 0:
                            oldX10 = int(keypoints[0].pt[0]) + boxes[18][0]
                            oldY10 = int(keypoints[0].pt[1]) + boxes[18][1]
                            cv2.circle(gray2, (oldX10, oldY10), 5, (0,0,255),0)
                            #cv2.imshow('frame',gray2)
                            small10=1
                        else:
                            small10=0
                else:
                    img1 = cv2.subtract(gray3[boxes[18][1]:boxes[19][1],boxes[18][0]:boxes[19][0]],gray2[boxes[18][1]:boxes[19][1],boxes[18][0]:boxes[19][0]]) # global view
                    keypoints = detector.detect(img1)
                    if len(keypoints)>0:
                        oldX10 = int(keypoints[0].pt[0]) + boxes[18][0]
                        oldY10 = int(keypoints[0].pt[1]) + boxes[18][1]
                        cv2.circle(gray2, (oldX10, oldY10), 5, (0,0,255),0)
                        #cv2.imshow('frame',gray2)
                        small10=1
                    else:
                        small10=0

                if len(keypoints)>0:
                    if small10 < 1:
                        oldL10=1
                        data10.append([oldX10, oldY10])
                    else:
                        data10.append([oldX10, oldY10])
                else:
                    data10.append([0,0])
                    oldL10 = 0
            # ================================================        

            # Below is for Tank 11 tracking =======================================================
            if int(HowMany) > 11:
                
                if oldL11 == 1:
                    img1 = cv2.subtract(gray3[oldY11-SearchSize:oldY11+SearchSize,oldX11-SearchSize:oldX11+SearchSize],gray2[oldY11-SearchSize:oldY11+SearchSize,oldX11-SearchSize:oldX11+SearchSize]) # local view
                    keypoints = detector.detect(img1)
                    if len(keypoints) > 0:
                        oldX11 = oldX11 - (SearchSize - int(keypoints[0].pt[0]) + boxes[20][0]) + boxes[20][0]
                        oldY11 = oldY11 - (SearchSize - int(keypoints[0].pt[1]) + boxes[20][1]) + boxes[20][1]
                        cv2.circle(gray2, (oldX11, oldY11), 5, (0,0,255),0)
                        #cv2.imshow('frame',gray2)
                        small11=1
                    else:
                        img1 = cv2.subtract(gray3[oldY11-SearchSize*2:oldY11+SearchSize*2,oldX11-SearchSize*2:oldX11+SearchSize*2],gray2[oldY11-SearchSize*2:oldY11+SearchSize*2,oldX11-SearchSize*2:oldX11+SearchSize*2]) # Extended local view
                        keypoints = detector.detect(img1)
                        if len(keypoints) > 0:
                            oldX11 = int(keypoints[0].pt[0]) + boxes[20][0]
                            oldY11 = int(keypoints[0].pt[1]) + boxes[20][1]
                            cv2.circle(gray2, (oldX11, oldY11), 5, (0,0,255),0)
                            #cv2.imshow('frame',gray2)
                            small11=1
                        else:
                            small11=0
                else:
                    img1 = cv2.subtract(gray3[boxes[20][1]:boxes[21][1],boxes[20][0]:boxes[21][0]],gray2[boxes[20][1]:boxes[21][1],boxes[20][0]:boxes[21][0]]) # global view
                    keypoints = detector.detect(img1)
                    if len(keypoints)>0:
                        oldX11 = int(keypoints[0].pt[0]) + boxes[20][0]
                        oldY11 = int(keypoints[0].pt[1]) + boxes[20][1]
                        cv2.circle(gray2, (oldX11, oldY11), 5, (0,0,255),0)
                        #cv2.imshow('frame',gray2)
                        small11=1
                    else:
                        small11=0

                if len(keypoints)>0:
                    if small11 < 1:
                        oldL11=1
                        data11.append([oldX11, oldY11])
                    else:
                        data11.append([oldX11, oldY11])
                else:
                    data11.append([0,0])
                    oldL11 = 0
            # ================================================
        
            # Below is for Tank 12 tracking =======================================================
            if int(HowMany) > 12:
                
                if oldL12 == 1:
                    img1 = cv2.subtract(gray3[oldY12-SearchSize:oldY12+SearchSize,oldX12-SearchSize:oldX12+SearchSize],gray2[oldY12-SearchSize:oldY12+SearchSize,oldX12-SearchSize:oldX12+SearchSize]) # local view
                    keypoints = detector.detect(img1)
                    if len(keypoints) > 0:
                        oldX12 = oldX12 - (SearchSize - int(keypoints[0].pt[0]) + boxes[22][0]) + boxes[22][0]
                        oldY12 = oldY12 - (SearchSize - int(keypoints[0].pt[1]) + boxes[22][1]) + boxes[22][1]
                        cv2.circle(gray2, (oldX12, oldY12), 5, (0,0,255),0)
                        #cv2.imshow('frame',gray2)
                        small12=1
                    else:
                        img1 = cv2.subtract(gray3[oldY12-SearchSize*2:oldY12+SearchSize*2,oldX12-SearchSize*2:oldX12+SearchSize*2],gray2[oldY12-SearchSize*2:oldY12+SearchSize*2,oldX12-SearchSize*2:oldX12+SearchSize*2]) # Extended local view
                        keypoints = detector.detect(img1)
                        if len(keypoints) > 0:
                            oldX12 = int(keypoints[0].pt[0]) + boxes[22][0]
                            oldY12 = int(keypoints[0].pt[1]) + boxes[22][1]
                            cv2.circle(gray2, (oldX12, oldY12), 5, (0,0,255),0)
                            #cv2.imshow('frame',gray2)
                            small12=1
                        else:
                            small12=0
                else:
                    img1 = cv2.subtract(gray3[boxes[22][1]:boxes[23][1],boxes[22][0]:boxes[23][0]],gray2[boxes[22][1]:boxes[23][1],boxes[22][0]:boxes[23][0]]) # global view
                    keypoints = detector.detect(img1)
                    if len(keypoints)>0:
                        oldX12 = int(keypoints[0].pt[0]) + boxes[22][0]
                        oldY12 = int(keypoints[0].pt[1]) + boxes[22][1]
                        cv2.circle(gray2, (oldX12, oldY12), 5, (0,0,255),0)
                        #cv2.imshow('frame',gray2)
                        small12=1
                    else:
                        small12=0

                if len(keypoints)>0:
                    if small12 < 1:
                        oldL12=1
                        data12.append([oldX12, oldY12])
                    else:
                        data12.append([oldX12, oldY12])
                else:
                    data12.append([0,0])
                    oldL12 = 0
            # ================================================
        
            # Below is for Tank 13 tracking =======================================================
            if int(HowMany) > 13:
                
                if oldL13 == 1:
                    img1 = cv2.subtract(gray3[oldY13-SearchSize:oldY13+SearchSize,oldX13-SearchSize:oldX13+SearchSize],gray2[oldY13-SearchSize:oldY13+SearchSize,oldX13-SearchSize:oldX13+SearchSize]) # local view
                    keypoints = detector.detect(img1)
                    if len(keypoints) > 0:
                        oldX13 = oldX13 - (SearchSize - int(keypoints[0].pt[0]) + boxes[24][0]) + boxes[24][0]
                        oldY13 = oldY13 - (SearchSize - int(keypoints[0].pt[1]) + boxes[24][1]) + boxes[24][1]
                        cv2.circle(gray2, (oldX13, oldY13), 5, (0,0,255),0)
                        #cv2.imshow('frame',gray2)
                        small13=1
                    else:
                        img1 = cv2.subtract(gray3[oldY13-SearchSize*2:oldY13+SearchSize*2,oldX13-SearchSize*2:oldX13+SearchSize*2],gray2[oldY13-SearchSize*2:oldY13+SearchSize*2,oldX13-SearchSize*2:oldX13+SearchSize*2]) # Extended local view
                        keypoints = detector.detect(img1)
                        if len(keypoints) > 0:
                            oldX13 = int(keypoints[0].pt[0]) + boxes[24][0]
                            oldY13 = int(keypoints[0].pt[1]) + boxes[24][1]
                            cv2.circle(gray2, (oldX13, oldY13), 5, (0,0,255),0)
                            #cv2.imshow('frame',gray2)
                            small13=1
                        else:
                            small13=0
                else:
                    img1 = cv2.subtract(gray3[boxes[24][1]:boxes[25][1],boxes[24][0]:boxes[25][0]],gray2[boxes[24][1]:boxes[25][1],boxes[24][0]:boxes[25][0]]) # global view
                    keypoints = detector.detect(img1)
                    if len(keypoints)>0:
                        oldX13 = int(keypoints[0].pt[0]) + boxes[24][0]
                        oldY13 = int(keypoints[0].pt[1]) + boxes[24][1]
                        cv2.circle(gray2, (oldX13, oldY13), 5, (0,0,255),0)
                        #cv2.imshow('frame',gray2)
                        small13=1
                    else:
                        small13=0

                if len(keypoints)>0:
                    if small13 < 1:
                        oldL13=1
                        data13.append([oldX13, oldY13])
                    else:
                        data13.append([oldX13, oldY13])
                else:
                    data13.append([0,0])
                    oldL13 = 0
            # ================================================
 
            # Below is for Tank 14 tracking =======================================================
            if int(HowMany) > 14:
            
                if oldL14 == 1:
                    img1 = cv2.subtract(gray3[oldY14-SearchSize:oldY14+SearchSize,oldX14-SearchSize:oldX14+SearchSize],gray2[oldY14-SearchSize:oldY14+SearchSize,oldX14-SearchSize:oldX14+SearchSize]) # local view
                    keypoints = detector.detect(img1)
                    if len(keypoints) > 0:
                        oldX14 = oldX14 - (SearchSize - int(keypoints[0].pt[0]) + boxes[26][0]) + boxes[26][0]
                        oldY14 = oldY14 - (SearchSize - int(keypoints[0].pt[1]) + boxes[26][1]) + boxes[26][1]
                        cv2.circle(gray2, (oldX14, oldY14), 5, (0,0,255),0)
                        #cv2.imshow('frame',gray2)
                        small14=1
                    else:
                        img1 = cv2.subtract(gray3[oldY14-SearchSize*2:oldY14+SearchSize*2,oldX14-SearchSize*2:oldX14+SearchSize*2],gray2[oldY14-SearchSize*2:oldY14+SearchSize*2,oldX14-SearchSize*2:oldX14+SearchSize*2]) # Extended local view
                        keypoints = detector.detect(img1)
                        if len(keypoints) > 0:
                            oldX14 = int(keypoints[0].pt[0]) + boxes[26][0]
                            oldY14 = int(keypoints[0].pt[1]) + boxes[26][1]
                            cv2.circle(gray2, (oldX14, oldY14), 5, (0,0,255),0)
                            #cv2.imshow('frame',gray2)
                            small14=1
                        else:
                            small14=0
                else:
                    img1 = cv2.subtract(gray3[boxes[26][1]:boxes[27][1],boxes[26][0]:boxes[27][0]],gray2[boxes[26][1]:boxes[27][1],boxes[26][0]:boxes[27][0]]) # global view
                    keypoints = detector.detect(img1)
                    if len(keypoints)>0:
                        oldX14 = int(keypoints[0].pt[0]) + boxes[26][0]
                        oldY14 = int(keypoints[0].pt[1]) + boxes[26][1]
                        cv2.circle(gray2, (oldX14, oldY14), 5, (0,0,255),0)
                        #cv2.imshow('frame',gray2)
                        small14=1
                    else:
                        small14=0

                if len(keypoints)>0:
                    if small14 < 1:
                        oldL14=1
                        data14.append([oldX14, oldY14])
                    else:
                        data14.append([oldX14, oldY14])
                else:
                    data14.append([0,0])
                    oldL14 = 0
            # ================================================

            # Below is for Tank 15 tracking =======================================================
            if int(HowMany) > 15:
            
                if oldL15 == 1:
                    img1 = cv2.subtract(gray3[oldY15-SearchSize:oldY15+SearchSize,oldX15-SearchSize:oldX15+SearchSize],gray2[oldY15-SearchSize:oldY15+SearchSize,oldX15-SearchSize:oldX15+SearchSize]) # local view
                    keypoints = detector.detect(img1)
                    if len(keypoints) > 0:
                        oldX15 = oldX15 - (SearchSize - int(keypoints[0].pt[0]) + boxes[28][0]) + boxes[28][0]
                        oldY15 = oldY15 - (SearchSize - int(keypoints[0].pt[1]) + boxes[28][1]) + boxes[28][1]
                        cv2.circle(gray2, (oldX15, oldY15), 5, (0,0,255),0)
                        #cv2.imshow('frame',gray2)
                        small15=1
                    else:
                        img1 = cv2.subtract(gray3[oldY15-SearchSize*2:oldY15+SearchSize*2,oldX15-SearchSize*2:oldX15+SearchSize*2],gray2[oldY15-SearchSize*2:oldY15+SearchSize*2,oldX15-SearchSize*2:oldX15+SearchSize*2]) # Extended local view
                        keypoints = detector.detect(img1)
                        if len(keypoints) > 0:
                            oldX15 = int(keypoints[0].pt[0]) + boxes[28][0]
                            oldY15 = int(keypoints[0].pt[1]) + boxes[28][1]
                            cv2.circle(gray2, (oldX15, oldY15), 5, (0,0,255),0)
                            #cv2.imshow('frame',gray2)
                            small15=1
                        else:
                            small15=0
                else:
                    img1 = cv2.subtract(gray3[boxes[28][1]:boxes[29][1],boxes[28][0]:boxes[29][0]],gray2[boxes[28][1]:boxes[29][1],boxes[28][0]:boxes[29][0]]) # global view
                    keypoints = detector.detect(img1)
                    if len(keypoints)>0:
                        oldX15 = int(keypoints[0].pt[0]) + boxes[28][0]
                        oldY15 = int(keypoints[0].pt[1]) + boxes[28][1]
                        cv2.circle(gray2, (oldX15, oldY15), 5, (0,0,255),0)
                        #cv2.imshow('frame',gray2)
                        small15=1
                    else:
                        small15=0
    
                if len(keypoints)>0:
                    if small15 < 1:
                        oldL15=1
                        data15.append([oldX15, oldY15])
                    else:
                        data15.append([oldX15, oldY15])
                else:
                    data15.append([0,0])
                    oldL15 = 0
            # ================================================
        
            # Below is for Tank 16 tracking =======================================================
            if int(HowMany) > 16:
            
                if oldL16 == 1:
                    img1 = cv2.subtract(gray3[oldY16-SearchSize:oldY16+SearchSize,oldX16-SearchSize:oldX16+SearchSize],gray2[oldY16-SearchSize:oldY16+SearchSize,oldX16-SearchSize:oldX16+SearchSize]) # local view
                    keypoints = detector.detect(img1)
                    if len(keypoints) > 0:
                        oldX16 = oldX16 - (SearchSize - int(keypoints[0].pt[0]) + boxes[30][0]) + boxes[30][0]
                        oldY16 = oldY16 - (SearchSize - int(keypoints[0].pt[1]) + boxes[30][1]) + boxes[30][1]
                        cv2.circle(gray2, (oldX16, oldY16), 5, (0,0,255),0)
                        #cv2.imshow('frame',gray2)
                        small16=1
                    else:
                        img1 = cv2.subtract(gray3[oldY16-SearchSize*2:oldY16+SearchSize*2,oldX16-SearchSize*2:oldX16+SearchSize*2],gray2[oldY16-SearchSize*2:oldY16+SearchSize*2,oldX16-SearchSize*2:oldX16+SearchSize*2]) # Extended local view
                        keypoints = detector.detect(img1)
                        if len(keypoints) > 0:
                            oldX16 = int(keypoints[0].pt[0]) + boxes[30][0]
                            oldY16 = int(keypoints[0].pt[1]) + boxes[30][1]
                            cv2.circle(gray2, (oldX16, oldY16), 5, (0,0,255),0)
                            #cv2.imshow('frame',gray2)
                            small16=1
                        else:
                            small16=0
                else:
                    img1 = cv2.subtract(gray3[boxes[30][1]:boxes[31][1],boxes[30][0]:boxes[31][0]],gray2[boxes[30][1]:boxes[31][1],boxes[30][0]:boxes[31][0]]) # global view
                    keypoints = detector.detect(img1)
                    if len(keypoints)>0:
                        oldX16 = int(keypoints[0].pt[0]) + boxes[30][0]
                        oldY16 = int(keypoints[0].pt[1]) + boxes[30][1]
                        cv2.circle(gray2, (oldX16, oldY16), 5, (0,0,255),0)
                        #cv2.imshow('frame',gray2)
                        small16=1
                    else:
                        small16=0
    
                if len(keypoints)>0:
                    if small16 < 1:
                        oldL16=1
                        data16.append([oldX16, oldY16])
                    else:
                        data16.append([oldX16, oldY16])
                else:
                    data16.append([0,0])
                    oldL16 = 0
            # ================================================

            # Below is for Tank 17 tracking =======================================================
            if int(HowMany) > 17:

                if oldL17 == 1:
                    img1 = cv2.subtract(
                        gray3[oldY17 - SearchSize:oldY17 + SearchSize, oldX17 - SearchSize:oldX17 + SearchSize],
                        gray2[oldY17 - SearchSize:oldY17 + SearchSize,
                        oldX17 - SearchSize:oldX17 + SearchSize])  # local view
                    keypoints = detector.detect(img1)
                    if len(keypoints) > 0:
                        oldX17 = oldX17 - (SearchSize - int(keypoints[0].pt[0]) + boxes[32][0]) + boxes[32][0]
                        oldY17 = oldY17 - (SearchSize - int(keypoints[0].pt[1]) + boxes[32][1]) + boxes[32][1]
                        cv2.circle(gray2, (oldX17, oldY17), 5, (0, 0, 255), 0)
                        # cv2.imshow('frame',gray2)
                        small17 = 1
                    else:
                        img1 = cv2.subtract(gray3[oldY17 - SearchSize * 2:oldY17 + SearchSize * 2,
                                            oldX17 - SearchSize * 2:oldX17 + SearchSize * 2],
                                            gray2[oldY17 - SearchSize * 2:oldY17 + SearchSize * 2,
                                            oldX17 - SearchSize * 2:oldX17 + SearchSize * 2])  # Extended local view
                        keypoints = detector.detect(img1)
                        if len(keypoints) > 0:
                            oldX17 = int(keypoints[0].pt[0]) + boxes[32][0]
                            oldY17 = int(keypoints[0].pt[1]) + boxes[32][1]
                            cv2.circle(gray2, (oldX17, oldY17), 5, (0, 0, 255), 0)
                            # cv2.imshow('frame',gray2)
                            small17 = 1
                        else:
                            small17 = 0
                else:
                    img1 = cv2.subtract(gray3[boxes[32][1]:boxes[33][1], boxes[32][0]:boxes[33][0]],
                                        gray2[boxes[32][1]:boxes[33][1], boxes[32][0]:boxes[33][0]])  # global view
                    keypoints = detector.detect(img1)
                    if len(keypoints) > 0:
                        oldX17 = int(keypoints[0].pt[0]) + boxes[32][0]
                        oldY17 = int(keypoints[0].pt[1]) + boxes[32][1]
                        cv2.circle(gray2, (oldX17, oldY17), 5, (0, 0, 255), 0)
                        # cv2.imshow('frame',gray2)
                        small17 = 1
                    else:
                        small17 = 0

                if len(keypoints) > 0:
                    if small17 < 1:
                        oldL17 = 1
                        data17.append([oldX17, oldY17])
                    else:
                        data17.append([oldX17, oldY17])
                else:
                    data17.append([0, 0])
                    oldL17 = 0
            # ================================================

            # Below is for Tank 18 tracking =======================================================
            if int(HowMany) > 18:

                if oldL18 == 1:
                    img1 = cv2.subtract(
                        gray3[oldY18 - SearchSize:oldY18 + SearchSize, oldX18 - SearchSize:oldX18 + SearchSize],
                        gray2[oldY18 - SearchSize:oldY18 + SearchSize,
                        oldX18 - SearchSize:oldX18 + SearchSize])  # local view
                    keypoints = detector.detect(img1)
                    if len(keypoints) > 0:
                        oldX18 = oldX18 - (SearchSize - int(keypoints[0].pt[0]) + boxes[34][0]) + boxes[34][0]
                        oldY18 = oldY18 - (SearchSize - int(keypoints[0].pt[1]) + boxes[34][1]) + boxes[34][1]
                        cv2.circle(gray2, (oldX18, oldY18), 5, (0, 0, 255), 0)
                        # cv2.imshow('frame',gray2)
                        small18 = 1
                    else:
                        img1 = cv2.subtract(gray3[oldY18 - SearchSize * 2:oldY18 + SearchSize * 2,
                                            oldX18 - SearchSize * 2:oldX18 + SearchSize * 2],
                                            gray2[oldY18 - SearchSize * 2:oldY18 + SearchSize * 2,
                                            oldX18 - SearchSize * 2:oldX18 + SearchSize * 2])  # Extended local view
                        keypoints = detector.detect(img1)
                        if len(keypoints) > 0:
                            oldX18 = int(keypoints[0].pt[0]) + boxes[34][0]
                            oldY18 = int(keypoints[0].pt[1]) + boxes[34][1]
                            cv2.circle(gray2, (oldX18, oldY18), 5, (0, 0, 255), 0)
                            # cv2.imshow('frame',gray2)
                            small18 = 1
                        else:
                            small18 = 0
                else:
                    img1 = cv2.subtract(gray3[boxes[34][1]:boxes[35][1], boxes[34][0]:boxes[35][0]],
                                        gray2[boxes[34][1]:boxes[35][1], boxes[34][0]:boxes[35][0]])  # global view
                    keypoints = detector.detect(img1)
                    if len(keypoints) > 0:
                        oldX18 = int(keypoints[0].pt[0]) + boxes[34][0]
                        oldY18 = int(keypoints[0].pt[1]) + boxes[34][1]
                        cv2.circle(gray2, (oldX18, oldY18), 5, (0, 0, 255), 0)
                        # cv2.imshow('frame',gray2)
                        small18 = 1
                    else:
                        small18 = 0

                if len(keypoints) > 0:
                    if small18 < 1:
                        oldL18 = 1
                        data18.append([oldX18, oldY18])
                    else:
                        data18.append([oldX18, oldY18])
                else:
                    data18.append([0, 0])
                    oldL18 = 0
            # ================================================

           # Below is for Tank 19 tracking =======================================================
            if int(HowMany) > 19:

                if oldL19 == 1:
                    img1 = cv2.subtract(
                        gray3[oldY19 - SearchSize:oldY19 + SearchSize, oldX19 - SearchSize:oldX19 + SearchSize],
                        gray2[oldY19 - SearchSize:oldY19 + SearchSize,
                        oldX19 - SearchSize:oldX19 + SearchSize])  # local view
                    keypoints = detector.detect(img1)
                    if len(keypoints) > 0:
                        oldX19 = oldX19 - (SearchSize - int(keypoints[0].pt[0]) + boxes[36][0]) + boxes[36][0]
                        oldY19 = oldY19 - (SearchSize - int(keypoints[0].pt[1]) + boxes[36][1]) + boxes[36][1]
                        cv2.circle(gray2, (oldX19, oldY19), 5, (0, 0, 255), 0)
                        # cv2.imshow('frame',gray2)
                        small19 = 1
                    else:
                        img1 = cv2.subtract(gray3[oldY19 - SearchSize * 2:oldY19 + SearchSize * 2,
                                            oldX19 - SearchSize * 2:oldX19 + SearchSize * 2],
                                            gray2[oldY19 - SearchSize * 2:oldY19 + SearchSize * 2,
                                            oldX19 - SearchSize * 2:oldX19 + SearchSize * 2])  # Extended local view
                        keypoints = detector.detect(img1)
                        if len(keypoints) > 0:
                            oldX19 = int(keypoints[0].pt[0]) + boxes[36][0]
                            oldY19 = int(keypoints[0].pt[1]) + boxes[36][1]
                            cv2.circle(gray2, (oldX19, oldY19), 5, (0, 0, 255), 0)
                            # cv2.imshow('frame',gray2)
                            small19 = 1
                        else:
                            small19 = 0
                else:
                    img1 = cv2.subtract(gray3[boxes[36][1]:boxes[37][1], boxes[36][0]:boxes[37][0]],
                                        gray2[boxes[36][1]:boxes[37][1], boxes[36][0]:boxes[37][0]])  # global view
                    keypoints = detector.detect(img1)
                    if len(keypoints) > 0:
                        oldX19 = int(keypoints[0].pt[0]) + boxes[36][0]
                        oldY19 = int(keypoints[0].pt[1]) + boxes[36][1]
                        cv2.circle(gray2, (oldX19, oldY19), 5, (0, 0, 255), 0)
                        # cv2.imshow('frame',gray2)
                        small19 = 1
                    else:
                        small19 = 0

                if len(keypoints) > 0:
                    if small19 < 1:
                        oldL19 = 1
                        data19.append([oldX19, oldY19])
                    else:
                        data19.append([oldX19, oldY19])
                else:
                    data19.append([0, 0])
                    oldL19 = 0
            # ================================================

           # Below is for Tank 20 tracking =======================================================
            if int(HowMany) > 20:

                if oldL20 == 1:
                    img1 = cv2.subtract(
                        gray3[oldY20 - SearchSize:oldY20 + SearchSize, oldX20 - SearchSize:oldX20 + SearchSize],
                        gray2[oldY20 - SearchSize:oldY20 + SearchSize,
                        oldX20 - SearchSize:oldX20 + SearchSize])  # local view
                    keypoints = detector.detect(img1)
                    if len(keypoints) > 0:
                        oldX20 = oldX20 - (SearchSize - int(keypoints[0].pt[0]) + boxes[38][0]) + boxes[38][0]
                        oldY20 = oldY20 - (SearchSize - int(keypoints[0].pt[1]) + boxes[38][1]) + boxes[38][1]
                        cv2.circle(gray2, (oldX20, oldY20), 5, (0, 0, 255), 0)
                        # cv2.imshow('frame',gray2)
                        small20 = 1
                    else:
                        img1 = cv2.subtract(gray3[oldY20 - SearchSize * 2:oldY20 + SearchSize * 2,
                                            oldX20 - SearchSize * 2:oldX20 + SearchSize * 2],
                                            gray2[oldY20 - SearchSize * 2:oldY20 + SearchSize * 2,
                                            oldX20 - SearchSize * 2:oldX20 + SearchSize * 2])  # Extended local view
                        keypoints = detector.detect(img1)
                        if len(keypoints) > 0:
                            oldX20 = int(keypoints[0].pt[0]) + boxes[38][0]
                            oldY20 = int(keypoints[0].pt[1]) + boxes[38][1]
                            cv2.circle(gray2, (oldX20, oldY20), 5, (0, 0, 255), 0)
                            # cv2.imshow('frame',gray2)
                            small20 = 1
                        else:
                            small20 = 0
                else:
                    img1 = cv2.subtract(gray3[boxes[38][1]:boxes[39][1], boxes[38][0]:boxes[39][0]],
                                        gray2[boxes[38][1]:boxes[39][1], boxes[38][0]:boxes[39][0]])  # global view
                    keypoints = detector.detect(img1)
                    if len(keypoints) > 0:
                        oldX20 = int(keypoints[0].pt[0]) + boxes[38][0]
                        oldY20 = int(keypoints[0].pt[1]) + boxes[38][1]
                        cv2.circle(gray2, (oldX20, oldY20), 5, (0, 0, 255), 0)
                        # cv2.imshow('frame',gray2)
                        small20 = 1
                    else:
                        small20 = 0

                if len(keypoints) > 0:
                    if small20 < 1:
                        oldL20 = 1
                        data20.append([oldX20, oldY20])
                    else:
                        data20.append([oldX20, oldY20])
                else:
                    data20.append([0, 0])
                    oldL20 = 0
            # ================================================

          # Below is for Tank 21 tracking =======================================================
            if int(HowMany) > 21:

                if oldL21 == 1:
                    img1 = cv2.subtract(
                        gray3[oldY21 - SearchSize:oldY21 + SearchSize, oldX21 - SearchSize:oldX21 + SearchSize],
                        gray2[oldY21 - SearchSize:oldY21 + SearchSize,
                        oldX21 - SearchSize:oldX21 + SearchSize])  # local view
                    keypoints = detector.detect(img1)
                    if len(keypoints) > 0:
                        oldX21 = oldX21 - (SearchSize - int(keypoints[0].pt[0]) + boxes[40][0]) + boxes[40][0]
                        oldY21 = oldY21 - (SearchSize - int(keypoints[0].pt[1]) + boxes[40][1]) + boxes[40][1]
                        cv2.circle(gray2, (oldX21, oldY21), 5, (0, 0, 255), 0)
                        # cv2.imshow('frame',gray2)
                        small21 = 1
                    else:
                        img1 = cv2.subtract(gray3[oldY21 - SearchSize * 2:oldY21 + SearchSize * 2,
                                            oldX21 - SearchSize * 2:oldX21 + SearchSize * 2],
                                            gray2[oldY21 - SearchSize * 2:oldY21 + SearchSize * 2,
                                            oldX21 - SearchSize * 2:oldX21 + SearchSize * 2])  # Extended local view
                        keypoints = detector.detect(img1)
                        if len(keypoints) > 0:
                            oldX21 = int(keypoints[0].pt[0]) + boxes[40][0]
                            oldY21 = int(keypoints[0].pt[1]) + boxes[40][1]
                            cv2.circle(gray2, (oldX21, oldY21), 5, (0, 0, 255), 0)
                            # cv2.imshow('frame',gray2)
                            small21 = 1
                        else:
                            small21 = 0
                else:
                    img1 = cv2.subtract(gray3[boxes[40][1]:boxes[41][1], boxes[40][0]:boxes[41][0]],
                                        gray2[boxes[40][1]:boxes[41][1], boxes[40][0]:boxes[41][0]])  # global view
                    keypoints = detector.detect(img1)
                    if len(keypoints) > 0:
                        oldX21 = int(keypoints[0].pt[0]) + boxes[40][0]
                        oldY21 = int(keypoints[0].pt[1]) + boxes[40][1]
                        cv2.circle(gray2, (oldX21, oldY21), 5, (0, 0, 255), 0)
                        # cv2.imshow('frame',gray2)
                        small21 = 1
                    else:
                        small21 = 0

                if len(keypoints) > 0:
                    if small21 < 1:
                        oldL21 = 1
                        data21.append([oldX21, oldY21])
                    else:
                        data21.append([oldX21, oldY21])
                else:
                    data21.append([0, 0])
                    oldL21 = 0
            # ================================================
            
          # Below is for Tank 22 tracking =======================================================
            if int(HowMany) > 22:

                if oldL22 == 1:
                    img1 = cv2.subtract(
                        gray3[oldY22 - SearchSize:oldY22 + SearchSize, oldX22 - SearchSize:oldX22 + SearchSize],
                        gray2[oldY22 - SearchSize:oldY22 + SearchSize,
                        oldX22 - SearchSize:oldX22 + SearchSize])  # local view
                    keypoints = detector.detect(img1)
                    if len(keypoints) > 0:
                        oldX22 = oldX22 - (SearchSize - int(keypoints[0].pt[0]) + boxes[42][0]) + boxes[42][0]
                        oldY22 = oldY22 - (SearchSize - int(keypoints[0].pt[1]) + boxes[42][1]) + boxes[42][1]
                        cv2.circle(gray2, (oldX22, oldY22), 5, (0, 0, 255), 0)
                        # cv2.imshow('frame',gray2)
                        small22 = 1
                    else:
                        img1 = cv2.subtract(gray3[oldY22 - SearchSize * 2:oldY22 + SearchSize * 2,
                                            oldX22 - SearchSize * 2:oldX22 + SearchSize * 2],
                                            gray2[oldY22 - SearchSize * 2:oldY22 + SearchSize * 2,
                                            oldX22 - SearchSize * 2:oldX22 + SearchSize * 2])  # Extended local view
                        keypoints = detector.detect(img1)
                        if len(keypoints) > 0:
                            oldX22 = int(keypoints[0].pt[0]) + boxes[42][0]
                            oldY22 = int(keypoints[0].pt[1]) + boxes[42][1]
                            cv2.circle(gray2, (oldX22, oldY22), 5, (0, 0, 255), 0)
                            # cv2.imshow('frame',gray2)
                            small22 = 1
                        else:
                            small22 = 0
                else:
                    img1 = cv2.subtract(gray3[boxes[42][1]:boxes[43][1], boxes[42][0]:boxes[43][0]],
                                        gray2[boxes[42][1]:boxes[43][1], boxes[42][0]:boxes[43][0]])  # global view
                    keypoints = detector.detect(img1)
                    if len(keypoints) > 0:
                        oldX22 = int(keypoints[0].pt[0]) + boxes[42][0]
                        oldY22 = int(keypoints[0].pt[1]) + boxes[42][1]
                        cv2.circle(gray2, (oldX22, oldY22), 5, (0, 0, 255), 0)
                        # cv2.imshow('frame',gray2)
                        small22 = 1
                    else:
                        small22 = 0

                if len(keypoints) > 0:
                    if small22 < 1:
                        oldL22 = 1
                        data22.append([oldX22, oldY22])
                    else:
                        data22.append([oldX22, oldY22])
                else:
                    data22.append([0, 0])
                    oldL22 = 0
            # ================================================
            
          # Below is for Tank 23 tracking =======================================================
            if int(HowMany) > 23:

                if oldL23 == 1:
                    img1 = cv2.subtract(
                        gray3[oldY23 - SearchSize:oldY23 + SearchSize, oldX23 - SearchSize:oldX23 + SearchSize],
                        gray2[oldY23 - SearchSize:oldY23 + SearchSize,
                        oldX23 - SearchSize:oldX23 + SearchSize])  # local view
                    keypoints = detector.detect(img1)
                    if len(keypoints) > 0:
                        oldX23 = oldX23 - (SearchSize - int(keypoints[0].pt[0]) + boxes[44][0]) + boxes[44][0]
                        oldY23 = oldY23 - (SearchSize - int(keypoints[0].pt[1]) + boxes[44][1]) + boxes[44][1]
                        cv2.circle(gray2, (oldX23, oldY23), 5, (0, 0, 255), 0)
                        # cv2.imshow('frame',gray2)
                        small23 = 1
                    else:
                        img1 = cv2.subtract(gray3[oldY23 - SearchSize * 2:oldY23 + SearchSize * 2,
                                            oldX23 - SearchSize * 2:oldX23 + SearchSize * 2],
                                            gray2[oldY23 - SearchSize * 2:oldY23 + SearchSize * 2,
                                            oldX23 - SearchSize * 2:oldX23 + SearchSize * 2])  # Extended local view
                        keypoints = detector.detect(img1)
                        if len(keypoints) > 0:
                            oldX23 = int(keypoints[0].pt[0]) + boxes[44][0]
                            oldY23 = int(keypoints[0].pt[1]) + boxes[44][1]
                            cv2.circle(gray2, (oldX23, oldY23), 5, (0, 0, 255), 0)
                            # cv2.imshow('frame',gray2)
                            small23 = 1
                        else:
                            small23 = 0
                else:
                    img1 = cv2.subtract(gray3[boxes[44][1]:boxes[45][1], boxes[44][0]:boxes[45][0]],
                                        gray2[boxes[44][1]:boxes[45][1], boxes[44][0]:boxes[45][0]])  # global view
                    keypoints = detector.detect(img1)
                    if len(keypoints) > 0:
                        oldX23 = int(keypoints[0].pt[0]) + boxes[44][0]
                        oldY23 = int(keypoints[0].pt[1]) + boxes[44][1]
                        cv2.circle(gray2, (oldX23, oldY23), 5, (0, 0, 255), 0)
                        # cv2.imshow('frame',gray2)
                        small23 = 1
                    else:
                        small23 = 0

                if len(keypoints) > 0:
                    if small23 < 1:
                        oldL23 = 1
                        data23.append([oldX23, oldY23])
                    else:
                        data23.append([oldX23, oldY23])
                else:
                    data23.append([0, 0])
                    oldL23 = 0
            # ================================================

          # Below is for Tank 24 tracking =======================================================
            if int(HowMany) > 24:

                if oldL24 == 1:
                    img1 = cv2.subtract(
                        gray3[oldY24 - SearchSize:oldY24 + SearchSize, oldX24 - SearchSize:oldX24 + SearchSize],
                        gray2[oldY24 - SearchSize:oldY24 + SearchSize,
                        oldX24 - SearchSize:oldX24 + SearchSize])  # local view
                    keypoints = detector.detect(img1)
                    if len(keypoints) > 0:
                        oldX24 = oldX24 - (SearchSize - int(keypoints[0].pt[0]) + boxes[46][0]) + boxes[46][0]
                        oldY24 = oldY24 - (SearchSize - int(keypoints[0].pt[1]) + boxes[46][1]) + boxes[46][1]
                        cv2.circle(gray2, (oldX24, oldY24), 5, (0, 0, 255), 0)
                        # cv2.imshow('frame',gray2)
                        small24 = 1
                    else:
                        img1 = cv2.subtract(gray3[oldY24 - SearchSize * 2:oldY24 + SearchSize * 2,
                                            oldX24 - SearchSize * 2:oldX24 + SearchSize * 2],
                                            gray2[oldY24 - SearchSize * 2:oldY24 + SearchSize * 2,
                                            oldX24 - SearchSize * 2:oldX24 + SearchSize * 2])  # Extended local view
                        keypoints = detector.detect(img1)
                        if len(keypoints) > 0:
                            oldX24 = int(keypoints[0].pt[0]) + boxes[46][0]
                            oldY24 = int(keypoints[0].pt[1]) + boxes[46][1]
                            cv2.circle(gray2, (oldX24, oldY24), 5, (0, 0, 255), 0)
                            # cv2.imshow('frame',gray2)
                            small24 = 1
                        else:
                            small24 = 0
                else:
                    img1 = cv2.subtract(gray3[boxes[46][1]:boxes[47][1], boxes[46][0]:boxes[47][0]],
                                        gray2[boxes[46][1]:boxes[47][1], boxes[46][0]:boxes[47][0]])  # global view
                    keypoints = detector.detect(img1)
                    if len(keypoints) > 0:
                        oldX24 = int(keypoints[0].pt[0]) + boxes[46][0]
                        oldY24 = int(keypoints[0].pt[1]) + boxes[46][1]
                        cv2.circle(gray2, (oldX24, oldY24), 5, (0, 0, 255), 0)
                        # cv2.imshow('frame',gray2)
                        small24 = 1
                    else:
                        small24 = 0

                if len(keypoints) > 0:
                    if small24 < 1:
                        oldL24 = 1
                        data24.append([oldX24, oldY24])
                    else:
                        data24.append([oldX24, oldY24])
                else:
                    data24.append([0, 0])
                    oldL24 = 0
            # ================================================        
            
            tt6[i]=int(tt4)
            if int(HowMany) > 1:
                if tt965 == 1:
                    if tt9651 + tt9652 == 0:
                        if tt9653 == 1:
                            data01Stamp.append([0-i-preset+1,0-tt6[i]])
                        else:
                            data01Stamp.append([i - preset + 1, 0 - tt6[i]])
                    elif tt9651 == 1:
                        data01Stamp.append([i-preset+1,(0-tt6[i])*10-1])  # Shaking
                    else:
                        data01Stamp.append([i-preset+1,(0-tt6[i])*10-2])  # Lighting

                else:
                    if tt9652 == 0:
                        if tt9653 == 1:
                            data01Stamp.append([0-i-preset+1,tt6[i]])
                        else:
                            data01Stamp.append([i - preset + 1, tt6[i]])
                    else:
                        if tt9653 == 1:
                            data01Stamp.append([0-i-preset+1,0-tt6[i]])  # dark during the day
                        else:
                            data01Stamp.append([i - preset + 1, 0 - tt6[i]])  # dark during the day
            if int(HowMany) > 1:
                data02Stamp.append([i-preset+1,tt6[i]])
            if int(HowMany) > 2:
                data03Stamp.append([i-preset+1,tt6[i]])
            if int(HowMany) > 3:
                data04Stamp.append([i-preset+1,tt6[i]])
            if int(HowMany) > 4:
                data05Stamp.append([i-preset+1,tt6[i]])
            if int(HowMany) > 5:
                data06Stamp.append([i-preset+1,tt6[i]])
            if int(HowMany) > 6:
                data07Stamp.append([i-preset+1,tt6[i]])
            if int(HowMany) > 7:
                data08Stamp.append([i-preset+1,tt6[i]])
            if int(HowMany) > 8:
                data09Stamp.append([i-preset+1,tt6[i]])
            if int(HowMany) > 9:
                data10Stamp.append([i-preset+1,tt6[i]])
            if int(HowMany) > 10:
                data11Stamp.append([i-preset+1,tt6[i]])
            if int(HowMany) > 11:
                data12Stamp.append([i-preset+1,tt6[i]])
            if int(HowMany) > 12:
                data13Stamp.append([i-preset+1,tt6[i]])
            if int(HowMany) > 13:
                data14Stamp.append([i-preset+1,tt6[i]])
            if int(HowMany) > 14:
                data15Stamp.append([i-preset+1,tt6[i]])
            if int(HowMany) > 15:
                data16Stamp.append([i-preset+1,tt6[i]])
            if int(HowMany) > 16:
                data17Stamp.append([i-preset+1,tt6[i]])
            if int(HowMany) > 17:
                data18Stamp.append([i-preset+1,tt6[i]])
            if int(HowMany) > 18:
                data19Stamp.append([i-preset+1,tt6[i]])
            if int(HowMany) > 19:
                data20Stamp.append([i-preset+1,tt6[i]])
            if int(HowMany) > 20:
                data21Stamp.append([i-preset+1,tt6[i]])
            if int(HowMany) > 21:
                data22Stamp.append([i-preset+1,tt6[i]])
            if int(HowMany) > 22:
                data23Stamp.append([i-preset+1,tt6[i]])
            if int(HowMany) > 23:
                data24Stamp.append([i-preset+1,tt6[i]])
            if int(HowMany) > 24:
                tank1= gray2[boxes[0][1]:boxes[15][1],boxes[0][0]:boxes[15][0]]
                tank01 = cv2.cvtColor(tank1, cv2.COLOR_BGR2GRAY)
                tank01s = cv2.resize(tank01, None, fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)
                Tank0108.write(tank01s)

                tank2= gray2[boxes[16][1]:boxes[31][1],boxes[16][0]:boxes[31][0]]
                tank02 = cv2.cvtColor(tank2, cv2.COLOR_BGR2GRAY)
                tank02s = cv2.resize(tank02, None, fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)
                Tank0916.write(tank02s)

                tank3= gray2[boxes[32][1]:boxes[47][1],boxes[32][0]:boxes[47][0]]
                tank03 = cv2.cvtColor(tank3, cv2.COLOR_BGR2GRAY)
                tank03s = cv2.resize(tank03, None, fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)
                Tank1724.write(tank03s)

                tank4= gray2[boxes[48][1]:boxes[49][1],boxes[48][0]:boxes[49][0]]
                tank04 = cv2.cvtColor(tank4, cv2.COLOR_BGR2GRAY)
                Tank25.write(tank03)

            while(int(tt4)-tt6[i] < int(1.0/framerate*100)):  # This is to control the frame rate 10 means 100 ms and this will give you about 10 fps(1000/100)
                tt = time.time()
                tt1 = str(tt).find('.',1,len(str(tt)))
                tt2 = str(tt)[tt1-8:tt1]
                tt5 = str(tt)[tt1+1:len(str(tt))]
                tt4 = tt2 + tt5.ljust(2,'0')
                tt4 = str((int(tt4) - int(tt40))).rjust(8,'0')
                cv2.imshow('frame',gray2)
                tt961ab = '2' # Delaying
        else:
            cv2.imshow('frame',gray2)
            preset = preset + 1

        
        if (i % int(framerate)) == 0:  # update the background in sync with the frame rate
            gray3 = copy.copy(frame)
            tt961ab = '3' # update background
        i=i+1
        cv2.setMouseCallback('frame',set_up_ROIs)
        if cv2.waitKey(dummy) & 0xFF == ord('q'):
            if tt92 > 2:
                save1=0
                tt963=1
            else:
                save1=1
            #ser.write("5")  # Turn off everything
            #ser.close()
            break
    except TypeError:
        tt961 = strftime("%m",) + strftime("%d",) + '_' + strftime("%H",) + strftime("%M",) + strftime("%S",)
        tt961aa = strftime("%H",) + strftime("%M",) + strftime("%S",)
        print ('No Webcam Images')
        print tt961aa
        print tt961ab
        ImageGrab.grab().save("D:\\LabRawData\\Excel\\Screen_" + tt961 + "No Webcam.jpg", "JPEG")
        time.sleep(60)
        cap.release()
        cap = cv2.VideoCapture(0)
        pass
else:
    save1=0

tt7=float((int(tt6[i-1])-int(tt6[preset])))
tt7=i/(tt7/100)

ser.write("4")  # Turn off everything
while ser.read() != '5':
    print ('Waiting')
    ser.read

ser.close()

# When everything done, release the capture


cap.release()

if save1==0:
    if int(HowMany) == 25:
        Tank0108.release()
        Tank0916.release()
        Tank1724.release()
        Tank25.release()
    tt98 = int(HowMany)
    tt96 = tt96 + 1
    if tt963 == 1:
        tt961 = strftime("%m",) + strftime("%d",) + '_' + strftime("%H",) + strftime("%M",) + strftime("%S",) + 'q'
    else:
        tt961 = strftime("%m",) + strftime("%d",) + '_' + strftime("%H",) + strftime("%M",) + strftime("%S",)
    print ('Files_' + ('%04d' % tt96) + ' were saved at ' + tt961)

    if int(HowMany) == 25:
        tt99 = Excel_Save(tt92, tt96, tt961, tt98, HowMany, GroupName, boxes, data01, data01Stamp, data02, data02Stamp, data03, data03Stamp, data04, data04Stamp, data05, data05Stamp, data06, data06Stamp, data07, data07Stamp, data08, data08Stamp, data09, data09Stamp, data10, data10Stamp, data11, data11Stamp, data12, data12Stamp, data13, data13Stamp, data14, data14Stamp, data15, data15Stamp, data16, data16Stamp, data17, data17Stamp, data18, data18Stamp, data19, data19Stamp, data20, data20Stamp, data21, data21Stamp, data22, data22Stamp, data23, data23Stamp, data24, data24Stamp, Tank0108, Tank0916, Tank1724, Tank25)
print str(tt7) + ' frame per second'
cv2.destroyAllWindows()

