import sys
import serial
sys.path.append("C:\\opencv\\build\\python\\2.7")
import copy
import numpy as np
import cv2
import math
import time
from time import strftime
import os
from numpy import array
import datetime
from Test2_LarvalVA_TwoTanks_Group import Excel_Save


connected = False
ser = serial.Serial("COM3", 9600, writeTimeout = 0)
while connected == False:
    print 'Initialising Arduino...'
    ser_in = ser.read()
    connected = True
ser.write('4')  # Turn on the white light

def nothing(x):
    pass



#Experiment parameters ================================
NumberOfHours = 24 # From 1 hour up to 72 hours or more
set_frame_rate= 5 #Choose from the following 10, 20, 30
Constant_darkness = 0 # 1 means constant darkness  0 means normal light cycles
LightOnDay = 1 # If constant darkenss from above, specify after how many days the light should be turned on. Two (2) means the next next day.
FrameWidth1 = 1800  # top camera
FrameHeight1 = 600   # top camera

TankWidth = 200 # in mm
LightOffTime = '220000'
LightOnTime = '080000'
LightIndex = 0 # 0 = light On 1 = Light Off
LightIndex2 = 0
ValveIndex1 = 0
ValveIndex2 = 0
VibrationIndex = 0
tempGG=0
FishThreshold = 6
SavingSeconds = 3600*set_frame_rate

## Tank1 ======================================
## Details for saving file
FishName1 = 'Gng8+dCLK_(n=4)'
DOB1 = '10-07-2020'
FishType1 = 'AB'
FishSex1 = 'Undertermined'
#=============================================

## Tank2 ======================================
## Details for saving file
FishName2 = 'Control_Siblings_(n=4)'
DOB2 = '10-07-2020'
FishType2 = 'AB'
FishSex2 = 'Undetermined'
#=============================================

# ser = serial.Serial("COM4", 9600, writeTimeout = 0)
#while not connected:
#    serin = ser.read()
#    connected = True

stamp = np.zeros((100,200,3))
GroupName = raw_input("Enter Group Name: ")
save1=0
setupbox = 0

tt81 = "D:\Vertical Assay\EMBLarval_Video\\" + GroupName
tt82 = "D:\Vertical Assay\EMBLarval_Video\\" + GroupName
tt83 = "D:\Vertical Assay\EMBLarval_Excel\\" + GroupName + "\\"

cv2.namedWindow('frame')

# Camera Setting ====================================
# Capture image wirh specified size and frame rate
cap1 = cv2.VideoCapture(0)
cap1.set(5,set_frame_rate)  # number 5 is frame rate
cap1.set(3,FrameWidth1)  # number 3 is frame width
cap1.set(4,FrameHeight1)  # number 4 is frame height



# Assign the fourcc words and initialize the video container
fourcc = cv2.cv.CV_FOURCC('M','J','P','G')
RGB = 0

#ser.write("4")
while ser.read() != '5':
    ser.read
    print ('Waiting')


#  Below is the mouse evemt

boxes=[]
drawing = False
dummy= 0
preset=0
tt91=0
tt92=0

data1=[];
data1Stamp=[];
data2=[];
data2Stamp=[];

i=0
mode = 0
StartDate = strftime("%y",) + strftime("%m",) + strftime("%d",)
StartDate1 = strftime("%d",)
if Constant_darkness == 1:
    LightOnDay = int(StartDate1) + LightOnDay
StartTime = strftime("%H",) + strftime("%M",) + strftime("%S",)
print 'The experiment started from ...ymd & hms ____' + StartDate + ' & ' + StartTime



def set_up_ROIs(event,x,y,flags,param):
    if len(boxes) <= 4:
        global boxnumber, drawing, img, gray2, arr, arr1, arr2, arr3, arr4, arr5, dummy, mode, tank1a, tank2a, tank3a, tank4a, tank5a, tank6a
        boxnumner = 0
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            sbox = [x, y]
            boxes.append(sbox)
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing == True:
                if len(boxes) == 1:
                    arr = array(gray5)
                    cv2.rectangle(arr,(boxes[-1][0],boxes[-1][-1]),(x, y),(0,0,255),1)
                    cv2.imshow('frame',arr)
                    stamp = np.zeros((100,200,3))
                elif len(boxes) == 3:
                    arr1 = array(gray5)
                    cv2.rectangle(arr1,(boxes[-1][0],boxes[-1][-1]),(x, y),(0,0,255),1)
                    cv2.imshow('frame',arr1)
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = not drawing
            ebox = [x, y]
            boxes.append(ebox)
            cv2.rectangle(gray5,(boxes[-2][-2],boxes[-2][-1]),(boxes[-1][-2],boxes[-1][-1]), (0,0,255),1)
            cv2.imshow('frame',gray5)
            if len(boxes) == 2:
                if not os.path.exists(tt81):
                    os.makedirs(tt81)
            elif len(boxes) == 4:
                if not os.path.exists(tt82):
                    os.makedirs(tt82)
            if len(boxes) == 4:
                mode = 1
                dummy = 1
                cap1.set(5,set_frame_rate)
                i=0



# ====================================================

LightOffTime5a = '225500' # Faster fps
LightOffTime5b = '230800' # Back to normal fps
LightOffTime5c = '105500' # Faster fps
LightOffTime5d = '110800' # Back to normal fps



LightOffTime1a = '225530' # Vibration On
LightOffTime1b = '225532' # Vibration Off
LightOffTime1c = '225630' # Vibration On
LightOffTime1d = '225632' # light
LightOffTime1e = '225730' # Vibration On
LightOffTime1f = '225732' # light

LightOffTime1g = '105530' # Vibration On
LightOffTime1h = '105532' # Vibration Off
LightOffTime1i = '105630' # Vibration On
LightOffTime1j = '105632' # light
LightOffTime1k = '105730' # Vibration On
LightOffTime1l = '105732' # light

LightOffTime3a = '230000' # Valve1 On
LightOffTime3b = '230004' # Valve1 Off
LightOffTime3c = '230010' # Valve2 On
LightOffTime3d = '230014' # valve2 Off

LightOffTime3e = '110000' # Valve1 On
LightOffTime3f = '110004' # Valve1 Off
LightOffTime3g = '110010' # Valve2 On
LightOffTime3h = '110014' # valve2 Off


LightOffTime2a = '230530' # Vibration On
LightOffTime2b = '230532' # Vibration Off
LightOffTime2c = '230630' # Vibration On
LightOffTime2d = '230632' # Vibration Off
LightOffTime2e = '230730' # Vibration On
LightOffTime2f = '230732' # Vibration Off

LightOffTime2g = '110530' # Vibration On
LightOffTime2h = '110532' # Vibration Off
LightOffTime2i = '110630' # Vibration On
LightOffTime2j = '110632' # Vibration Off
LightOffTime2k = '110730' # Vibration On
LightOffTime2l = '110732' # Vibration Off


kernel = np.ones((5, 5), np.uint8)
ret, gray4 = cap1.read()
gray4 = np.float32(gray4)
gray7 = np.float32(gray4)
BackUpdate = 0
while(int(tt91)<NumberOfHours):  # check !
    # capture frame-by-frame
    CurrentTime1 = strftime("%H",) + strftime("%M",) + strftime("%S",)

    if CurrentTime1 == LightOffTime5a:
        set_frame_rate= 10
        print 'The frame rate is set to 10 fps at ...' + CurrentTime1 + ' at Frame-' + str(i-preset+1-int(tt91)*SavingSeconds)
        cap1.set(5,set_frame_rate)
    if CurrentTime1 == LightOffTime5b:
        set_frame_rate= 5
        print 'The frame rate is set back to 5 fps at ...' + CurrentTime1 + ' at Frame-' + str(i-preset+1-int(tt91)*SavingSeconds)
        cap1.set(5,set_frame_rate)
    if CurrentTime1 == LightOffTime5c:
        set_frame_rate= 10
        print 'The frame rate is set to 10 fps at ...' + CurrentTime1 + ' at Frame-' + str(i-preset+1-int(tt91)*SavingSeconds)
        cap1.set(5,set_frame_rate)
    if CurrentTime1 == LightOffTime5d:
        set_frame_rate= 5
        print 'The frame rate is set back to 5 fps at ...' + CurrentTime1 + ' at Frame-' + str(i-preset+1-int(tt91)*SavingSeconds)
        cap1.set(5,set_frame_rate)

    if CurrentTime1 == LightOffTime1a:
        if VibrationIndex ==0:
            VibrationIndex = 1
            ser.write('15')  # Turn on vibration
            print 'The 1st vibration was turned on at ...' + CurrentTime1 + ' at Frame-' + str(i-preset+1-int(tt91)*SavingSeconds)
    if CurrentTime1 == LightOffTime1b:
        if VibrationIndex == 1:
            VibrationIndex = 0
            ser.write('16')  # Turn on vibration
            print 'The 1st vibration was turned off at ...' + CurrentTime1 + ' at Frame-' + str(i-preset+1-int(tt91)*SavingSeconds)
    if CurrentTime1 == LightOffTime1c:
        if VibrationIndex ==0:
            VibrationIndex = 1
            ser.write('15')  # Turn on vibration
            print 'The 2nd vibration was turned on at ...' + CurrentTime1 + ' at Frame-' + str(i-preset+1-int(tt91)*SavingSeconds)
    if CurrentTime1 == LightOffTime1d:
        if VibrationIndex == 1:
            VibrationIndex = 0
            ser.write('16')  # Turn on vibration
            print 'The 2nd vibration was turned off at ...' + CurrentTime1 + ' at Frame-' + str(i-preset+1-int(tt91)*SavingSeconds)
    if CurrentTime1 == LightOffTime1e:
        if VibrationIndex ==0:
            VibrationIndex = 1
            ser.write('15')  # Turn on vibration
            print 'The 3rd vibration was turned on at ...' + CurrentTime1 + ' at Frame-' + str(i-preset+1-int(tt91)*SavingSeconds)
    if CurrentTime1 == LightOffTime1f:
        if VibrationIndex == 1:
            VibrationIndex = 0
            ser.write('16')  # Turn on vibration
            print 'The 3rd vibration was turned off at ...' + CurrentTime1 + ' at Frame-' + str(i-preset+1-int(tt91)*SavingSeconds)


    if CurrentTime1 == LightOffTime1g:
        if VibrationIndex ==0:
            VibrationIndex = 1
            ser.write('15')  # Turn on vibration
            print 'The 1st vibration was turned on at ...' + CurrentTime1 + ' at Frame-' + str(i-preset+1-int(tt91)*SavingSeconds)
    if CurrentTime1 == LightOffTime1h:
        if VibrationIndex == 1:
            VibrationIndex = 0
            ser.write('16')  # Turn on vibration
            print 'The 1st vibration was turned off at ...' + CurrentTime1 + ' at Frame-' + str(i-preset+1-int(tt91)*SavingSeconds)
    if CurrentTime1 == LightOffTime1i:
        if VibrationIndex ==0:
            VibrationIndex = 1
            ser.write('15')  # Turn on vibration
            print 'The 2nd vibration was turned on at ...' + CurrentTime1 + ' at Frame-' + str(i-preset+1-int(tt91)*SavingSeconds)
    if CurrentTime1 == LightOffTime1j:
        if VibrationIndex == 1:
            VibrationIndex = 0
            ser.write('16')  # Turn on vibration
            print 'The 2nd vibration was turned off at ...' + CurrentTime1 + ' at Frame-' + str(i-preset+1-int(tt91)*SavingSeconds)
    if CurrentTime1 == LightOffTime1k:
        if VibrationIndex ==0:
            VibrationIndex = 1
            ser.write('15')  # Turn on vibration
            print 'The 3rd vibration was turned on at ...' + CurrentTime1 + ' at Frame-' + str(i-preset+1-int(tt91)*SavingSeconds)
    if CurrentTime1 == LightOffTime1l:
        if VibrationIndex == 1:
            VibrationIndex = 0
            ser.write('16')  # Turn on vibration
            print 'The 3rd vibration was turned off at ...' + CurrentTime1 + ' at Frame-' + str(i-preset+1-int(tt91)*SavingSeconds)



    if CurrentTime1 == LightOffTime2a:
        if VibrationIndex ==0:
            VibrationIndex = 1
            ser.write('15')  # Turn on vibration
            print 'The 1st vibration was turned on at ...' + CurrentTime1 + ' at Frame-' + str(i-preset+1-int(tt91)*SavingSeconds)
    if CurrentTime1 == LightOffTime2b:
        if VibrationIndex == 1:
            VibrationIndex = 0
            ser.write('16')  # Turn on vibration
            print 'The 1st vibration was turned off at ...' + CurrentTime1 + ' at Frame-' + str(i-preset+1-int(tt91)*SavingSeconds)
    if CurrentTime1 == LightOffTime2c:
        if VibrationIndex ==0:
            VibrationIndex = 1
            ser.write('15')  # Turn on vibration
            print 'The 2nd vibration was turned on at ...' + CurrentTime1 + ' at Frame-' + str(i-preset+1-int(tt91)*SavingSeconds)
    if CurrentTime1 == LightOffTime2d:
        if VibrationIndex == 1:
            VibrationIndex = 0
            ser.write('16')  # Turn on vibration
            print 'The 2nd vibration was turned off at ...' + CurrentTime1 + ' at Frame-' + str(i-preset+1-int(tt91)*SavingSeconds)
    if CurrentTime1 == LightOffTime2e:
        if VibrationIndex ==0:
            VibrationIndex = 1
            ser.write('15')  # Turn on vibration
            print 'The 3rd vibration was turned on at ...' + CurrentTime1 + ' at Frame-' + str(i-preset+1-int(tt91)*SavingSeconds)
    if CurrentTime1 == LightOffTime2f:
        if VibrationIndex == 1:
            VibrationIndex = 0
            ser.write('16')  # Turn on vibration
            print 'The 3rd vibration was turned off at ...' + CurrentTime1 + ' at Frame-' + str(i-preset+1-int(tt91)*SavingSeconds)

    if CurrentTime1 == LightOffTime2g:
        if VibrationIndex ==0:
            VibrationIndex = 1
            ser.write('15')  # Turn on vibration
            print 'The 1st vibration was turned on at ...' + CurrentTime1 + ' at Frame-' + str(i-preset+1-int(tt91)*SavingSeconds)
    if CurrentTime1 == LightOffTime2h:
        if VibrationIndex == 1:
            VibrationIndex = 0
            ser.write('16')  # Turn on vibration
            print 'The 1st vibration was turned off at ...' + CurrentTime1 + ' at Frame-' + str(i-preset+1-int(tt91)*SavingSeconds)
    if CurrentTime1 == LightOffTime2i:
        if VibrationIndex ==0:
            VibrationIndex = 1
            ser.write('15')  # Turn on vibration
            print 'The 2nd vibration was turned on at ...' + CurrentTime1 + ' at Frame-' + str(i-preset+1-int(tt91)*SavingSeconds)
    if CurrentTime1 == LightOffTime2j:
        if VibrationIndex == 1:
            VibrationIndex = 0
            ser.write('16')  # Turn on vibration
            print 'The 2nd vibration was turned off at ...' + CurrentTime1 + ' at Frame-' + str(i-preset+1-int(tt91)*SavingSeconds)
    if CurrentTime1 == LightOffTime2k:
        if VibrationIndex ==0:
            VibrationIndex = 1
            ser.write('15')  # Turn on vibration
            print 'The 3rd vibration was turned on at ...' + CurrentTime1 + ' at Frame-' + str(i-preset+1-int(tt91)*SavingSeconds)
    if CurrentTime1 == LightOffTime2l:
        if VibrationIndex == 1:
            VibrationIndex = 0
            ser.write('16')  # Turn on vibration
            print 'The 3rd vibration was turned off at ...' + CurrentTime1 + ' at Frame-' + str(i-preset+1-int(tt91)*SavingSeconds)


    if CurrentTime1 == LightOffTime3a:
        if ValveIndex1 ==0:
            ValveIndex1 = 1
            ser.write('11')  # Turn on 1st valve
            print 'The valve1 was turned on at ...' + CurrentTime1 + 'at Frame-' + str(i-preset+1-int(tt91)*SavingSeconds)
    if CurrentTime1 == LightOffTime3b:
        if ValveIndex1 == 1:
            ValveIndex1 = 0
            ser.write('12')  # Turn off 1st valve
            print 'The valve1 was turned off at ...' + CurrentTime1 + 'at Frame-' + str(i-preset+1-int(tt91)*SavingSeconds)
    if CurrentTime1 == LightOffTime3c:
        if ValveIndex2 ==0:
            ValveIndex2 = 1
            ser.write('13')  # Turn on 2nd valve
            print 'The valve2 was turned on at ...' + CurrentTime1 + 'at Frame-' + str(i-preset+1-int(tt91)*SavingSeconds)
    if CurrentTime1 == LightOffTime3d:
        if ValveIndex2 == 1:
            ValveIndex2 = 0
            ser.write('14')  # Turn off 2nd valve
            print 'The valve2 was turned off at ...' + CurrentTime1 + 'at Frame-' + str(i-preset+1-int(tt91)*SavingSeconds)

    if CurrentTime1 == LightOffTime3e:
        if ValveIndex1 ==0:
            ValveIndex1 = 1
            ser.write('11')  # Turn on 1st valve
            print 'The valve1 was turned on at ...' + CurrentTime1 + 'at Frame-' + str(i-preset+1-int(tt91)*SavingSeconds)
    if CurrentTime1 == LightOffTime3f:
        if ValveIndex1 == 1:
            ValveIndex1 = 0
            ser.write('12')  # Turn off 1st valve
            print 'The valve1 was turned off at ...' + CurrentTime1 + 'at Frame-' + str(i-preset+1-int(tt91)*SavingSeconds)
    if CurrentTime1 == LightOffTime3g:
        if ValveIndex2 ==0:
            ValveIndex2 = 1
            ser.write('13')  # Turn on 2nd valve
            print 'The valve2 was turned on at ...' + CurrentTime1 + 'at Frame-' + str(i-preset+1-int(tt91)*SavingSeconds)
    if CurrentTime1 == LightOffTime3h:
        if ValveIndex2 == 1:
            ValveIndex2 = 0
            ser.write('14')  # Turn off 2nd valve
            print 'The valve2 was turned off at ...' + CurrentTime1 + 'at Frame-' + str(i-preset+1-int(tt91)*SavingSeconds)



    if int(tt91) >= 0:
        if CurrentTime1 == LightOffTime:
            if LightIndex == 0:
                LightIndex = 1
                ser.write('3')  # Turn off the white light
                print 'The light was turned off at ...' + CurrentTime1
        if CurrentTime1 == LightOnTime:
            if LightIndex == 1:
                ser.write('4')  # Turn on the white light
                LightIndex = 0
                print 'The light was turned on at ...' + CurrentTime1

    ret, frame = cap1.read()
    gray2 = frame [:]
    gray6 = copy.deepcopy(frame)

    if dummy == 1:
        if setupbox == 0:
            starttime = datetime.datetime.now()
            frametime = starttime
            setupbox = 1
            if RGB == 1:
                #Below is for RGB
                Tank1= cv2.VideoWriter(tt81 + '\\Tank1.avi',fourcc, 20.0, (boxes[1][0]-boxes[0][0],boxes[1][1]-boxes[0][1]))
            else:
                #Below is for B/W
                Tank1= cv2.VideoWriter(tt81 + '\\Tank1_Hour_01.avi',fourcc, 20, (boxes[1][0]-boxes[0][0],boxes[1][1]-boxes[0][1]),0)
                Tank2= cv2.VideoWriter(tt82 + '\\Tank2_Hour_01.avi',fourcc, 20, (boxes[3][0]-boxes[2][0],boxes[3][1]-boxes[2][1]),0)
                Tank1_Raw= cv2.VideoWriter(tt81 + '\\Tank1_Raw_Hour_01.avi',fourcc, 20, (boxes[1][0]-boxes[0][0]+100,boxes[1][1]-boxes[0][1]+60),0)
                Tank2_Raw= cv2.VideoWriter(tt82 + '\\Tank2_Raw_Hour_01.avi',fourcc, 20, (boxes[3][0]-boxes[2][0]+100,boxes[3][1]-boxes[2][1]+60),0)

    if mode==1:
        cv2.rectangle(gray2,(boxes[0][0],boxes[0][1]),(boxes[1][0],boxes[1][1]), (0,0,255),1)
        cv2.rectangle(gray2,(boxes[0][0]-60,boxes[0][1]-30),(boxes[1][0]+40,boxes[1][1]+30), (0,255,0),1)
        cv2.rectangle(gray2,(boxes[2][0],boxes[2][1]),(boxes[3][0],boxes[3][1]), (0,0,255),1)
        cv2.rectangle(gray2,(boxes[2][0]-30,boxes[2][1]-30),(boxes[3][0]+60,boxes[3][1]+30), (0,255,0),1)

        if (i-preset+1) % SavingSeconds == 0:  # save every 3600 seconds
            CurrentTime = strftime("%H",) + strftime("%M",) + strftime("%S",)
            tt91 = '%02d' % int((i-preset+1) / SavingSeconds)
            tt92 = '%02d' % (int((i-preset+1) / SavingSeconds)+1)
            print ('Files_' + tt91 + ' were saved at ' + CurrentTime)
            tt99 = Excel_Save(tt91, GroupName, boxes, data1, data1Stamp, data2, data2Stamp, Tank1, Tank2, Tank1_Raw, Tank2_Raw, FishName1,DOB1,FishType1,FishSex1,FishName2,DOB2,FishType2,FishSex2, FrameWidth1,FrameHeight1,TankWidth,save1, tt83)
            if int(tt91)<NumberOfHours:
                Tank1= cv2.VideoWriter(tt81 + '\\Tank1' + '_Hour_' + tt92 + '.avi',fourcc, 20, (boxes[1][0]-boxes[0][0],boxes[1][1]-boxes[0][1]),0)
                Tank2= cv2.VideoWriter(tt82 + '\\Tank2' + '_Hour_' + tt92 + '.avi',fourcc, 20, (boxes[3][0]-boxes[2][0],boxes[3][1]-boxes[2][1]),0)
                Tank1_Raw= cv2.VideoWriter(tt81 + '\\Tank1_Raw_' + 'Hour_' + tt92 + '.avi',fourcc, 20, (boxes[1][0]-boxes[0][0]+100,boxes[1][1]-boxes[0][1]+60),0)
                Tank2_Raw= cv2.VideoWriter(tt82 + '\\Tank2_Raw_' + 'Hour_' + tt92 + '.avi',fourcc, 20, (boxes[3][0]-boxes[2][0]+100,boxes[3][1]-boxes[2][1]+60),0)
                data1=[];
                data1Stamp=[];
                data2=[];
                data2Stamp=[];
                BackUpdate = 0
                gray7 = np.float32(gray2)
        if BackUpdate <=30:
            cv2.accumulateWeighted(gray2,gray7,0.1)
            gray8 = cv2.convertScaleAbs(gray7)
            BackUpdate = BackUpdate + 1
        else:
            if BackUpdate == 31:
                gray5 = gray8
                BackUpdate = 0
                #print 'Background updated at ' + CurrentTime1

        elapsed_time=(datetime.datetime.now() - starttime).total_seconds()
        if LightIndex2 == 1:
            if LightIndex == 0:
                elapsed_time=-(elapsed_time)
        elif LightIndex2 == 0:
            if LightIndex == 1:
                elapsed_time=-(elapsed_time)

        # Below is for Tank 1 tracking =======================================================
        img1 = cv2.subtract(gray2[boxes[0][1]:boxes[1][1],boxes[0][0]:boxes[1][0]],gray5[boxes[0][1]:boxes[1][1],boxes[0][0]:boxes[1][0]]) # global view
        img1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
        img1a = cv2.GaussianBlur(img1,(25,25),0)
        img1a = cv2.dilate(img1a,kernel,iterations=1)
        ret, img1b = cv2.threshold(img1a,FishThreshold,255,0)

        edged = cv2.Canny(img1b,25,200)
        (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        cnts = sorted(cnts, key=cv2.contourArea, reverse = True)[:30]
        if len(cnts) == 0:
            x = 0
            y = 0
            w = 0
            h = 0
            data1.append([i-preset+1,elapsed_time,0, 0, 0, 0, 0, 0])
        else:
            x1=0
            y1=0
            w1=0
            h1=0
            x2=0
            y2=0
            w2=0
            h2=0
            k2=0
            for m in range(len(cnts)):
                [x, y, w, h] = cv2.boundingRect(cnts[m])
                if w * h > 256:
                    if w * h < 1600:
                        if w < 50:
                            if h < 50:
                                if x1*y1*w1*h1 == x*y*w*h:
                                    x=x
                                else:
                                    if k2 > 2:
                                        if x2*y2*w2*h2 == x*y*w*h:
                                            x=x
                                        else:
                                            data1.append([i-preset+1,elapsed_time,x+w/2+boxes[0][0], y+h/2+boxes[0][1], x, y, w, h])
                                            cv2.rectangle(gray2,(x-2+boxes[0][0],y-2++boxes[0][1]),(x+w+2+boxes[0][0],y+h+2++boxes[0][1]),(0,255,0),2)
                                            cv2.circle(gray2, (x+w/2+boxes[0][0], y+h/2+boxes[0][1]), 3, (0,0,255),-1)
                                            k2=k2+1
                                            if k2 >=2:
                                                x2=x1
                                                y2=y1
                                                w2=w1
                                                h2=h1
                                            x1=x
                                            y1=y
                                            w1=w
                                            h1=h
                                    else:
                                        data1.append([i-preset+1,elapsed_time,x+w/2+boxes[0][0], y+h/2+boxes[0][1], x, y, w, h])
                                        cv2.rectangle(gray2,(x-2+boxes[0][0],y-2++boxes[0][1]),(x+w+2+boxes[0][0],y+h+2++boxes[0][1]),(0,255,0),2)
                                        cv2.circle(gray2, (x+w/2+boxes[0][0], y+h/2+boxes[0][1]), 3, (0,0,255),-1)
                                        k2=k2+1
                                        if k2 >=2:
                                            x2=x1
                                            y2=y1
                                            w2=w1
                                            h2=h1
                                        x1=x
                                        y1=y
                                        w1=w
                                        h1=h
        # Below is for Tank 2 tracking =======================================================
        img2 = cv2.subtract(gray2[boxes[2][1]:boxes[3][1],boxes[2][0]:boxes[3][0]],gray5[boxes[2][1]:boxes[3][1],boxes[2][0]:boxes[3][0]]) # global view
        img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
        img2a = cv2.GaussianBlur(img2,(15,15),0)
        img2a = cv2.dilate(img2a,kernel,iterations=1)
        ret, img2b = cv2.threshold(img2a,FishThreshold,255,0)
        edged = cv2.Canny(img2b,25,200)
        (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        cnts = sorted(cnts, key=cv2.contourArea, reverse = True)[:30]
        if len(cnts) == 0:
            x = 0
            y = 0
            w = 0
            h = 0
            if VibrationIndex == 1:
                data2.append([0-i-preset+1,elapsed_time,0, 0, 0, 0, 0, 0])
            else:
                if (ValveIndex1 + ValveIndex2) == 1:
                    data2.append([0-i-preset+1,elapsed_time,0, 0, 0, 0, 0, 0])
                else:
                    data2.append([i-preset+1,elapsed_time,0, 0, 0, 0, 0, 0])
        else:
            x1=0
            y1=0
            w1=0
            h1=0
            x2=0
            y2=0
            w2=0
            h2=0
            k1=0
            k2=0
            tempGG=0
            for m in range(len(cnts)):
                [x, y, w, h] = cv2.boundingRect(cnts[m])
                if w * h > 256:
                    if w * h < 1600:
                        if w < 50:
                            if h < 50:
                                if x1*y1*w1*h1 == x*y*w*h:
                                    x=x
                                else:
                                    if k2 > 2:
                                        if x2*y2*w2*h2 == x*y*w*h:
                                            x=x
                                        else:
                                            tempGG=1
                                            if VibrationIndex == 1:
                                                data2.append([0-i-preset+1,elapsed_time,x+w/2+boxes[2][0], y+h/2+boxes[2][1], x, y, w, h])
                                            else:
                                                if (ValveIndex1 + ValveIndex2) == 1:
                                                    data2.append([0-i-preset+1,elapsed_time,x+w/2+boxes[2][0], y+h/2+boxes[2][1], x, y, w, h])
                                                else:
                                                    data2.append([i-preset+1,elapsed_time,x+w/2+boxes[2][0], y+h/2+boxes[2][1], x, y, w, h])
                                            cv2.rectangle(gray2,(x-2+boxes[2][0],y-2++boxes[2][1]),(x+w+2+boxes[2][0],y+h+2++boxes[2][1]),(0,255,0),2)
                                            cv2.circle(gray2, (x+w/2+boxes[2][0], y+h/2+boxes[2][1]), 3, (0,0,255),-1)
                                            k2=k2+1
                                            if k2 >=2:
                                                x2=x1
                                                y2=y1
                                                w2=w1
                                                h2=h1
                                            x1=x
                                            y1=y
                                            w1=w
                                            h1=h
                                    else:
                                        tempGG=1
                                        if VibrationIndex == 1:
                                            data2.append([0-i-preset+1,elapsed_time,x+w/2+boxes[2][0], y+h/2+boxes[2][1], x, y, w, h])
                                        else:
                                            if (ValveIndex1 + ValveIndex2) == 1:
                                                data2.append([0-i-preset+1,elapsed_time,x+w/2+boxes[2][0], y+h/2+boxes[2][1], x, y, w, h])
                                            else:
                                                data2.append([i-preset+1,elapsed_time,x+w/2+boxes[2][0], y+h/2+boxes[2][1], x, y, w, h])
                                        cv2.rectangle(gray2,(x-2+boxes[2][0],y-2++boxes[2][1]),(x+w+2+boxes[2][0],y+h+2++boxes[2][1]),(0,255,0),2)
                                        cv2.circle(gray2, (x+w/2+boxes[2][0], y+h/2+boxes[2][1]), 3, (0,0,255),-1)
                                        k2=k2+1
                                        if k2 >=2:
                                            x2=x1
                                            y2=y1
                                            w2=w1
                                            h2=h1
                                        x1=x
                                        y1=y
                                        w1=w
                                        h1=h


        if tempGG ==0:
            if VibrationIndex == 1:
                data2.append([0-i-preset+1,elapsed_time,0, 0, 0, 0, 0, 0])
            else:
                if (ValveIndex1 + ValveIndex2) == 1:
                    data2.append([0-i-preset+1,elapsed_time,0, 0, 0, 0, 0, 0])
                else:
                    data2.append([i-preset+1,elapsed_time,0, 0, 0, 0, 0, 0])

        cv2.imshow('frame',gray2)

        gray2 = cv2.cvtColor(gray2,cv2.COLOR_BGR2GRAY)
        gray6 = cv2.cvtColor(gray6,cv2.COLOR_BGR2GRAY)

        tank1 = gray2[boxes[0][1]:boxes[1][1],boxes[0][0]:boxes[1][0]]
        tank1_raw = gray6[boxes[0][1]-30:boxes[1][1]+30,boxes[0][0]-60:boxes[1][0]+40]
        Tank1.write(tank1)
        Tank1_Raw.write(tank1_raw)

        tank2 = gray2[boxes[2][1]:boxes[3][1],boxes[2][0]:boxes[3][0]]
        tank2_raw = gray6[boxes[2][1]-30:boxes[3][1]+30,boxes[2][0]-40:boxes[3][0]+60]
        Tank2.write(tank2)
        Tank2_Raw.write(tank2_raw)
        if VibrationIndex == 1:
            data2Stamp.append([-(i-preset+1),elapsed_time])
        else:
            if (ValveIndex1 + ValveIndex2) == 1:
                data2Stamp.append([-(i-preset+1),elapsed_time])
            else:
                data2Stamp.append([i-preset+1,elapsed_time])

        frametime = datetime.datetime.now()
        elapsed_time = 0


    else:
        preset = preset + 1
        if preset < 30:
            cv2.accumulateWeighted(gray2,gray4,0.1)
            gray5 = cv2.convertScaleAbs(gray4)
            cv2.imshow('frame',gray5)
        else:
            cv2.imshow('SelectROIs',gray2)

    i=i+1
    cv2.setMouseCallback('frame',set_up_ROIs)
    if cv2.waitKey(dummy) & 0xFF == ord('q'):
        save1=1
        break

# When everything is done release the capture

if save1==1:
    CurrentTime = strftime("%H",) + strftime("%M",) + strftime("%S",)
    tt91 = '%02d' % int((i-preset+1) / SavingSeconds)
    tt92 = '%02d' % (int((i-preset+1) / SavingSeconds)+1)
    tt91 = int(tt91) + 1
    tt91 = str(tt91)
    print ('Files_' + tt91 + '_quit were saved at ' + CurrentTime)
    tt99 = Excel_Save(tt91, GroupName, boxes, data1, data1Stamp, data2, data2Stamp, Tank1, Tank2, Tank1_Raw, Tank2_Raw, FishName1,DOB1,FishType1,FishSex1,FishName2,DOB2,FishType2,FishSex2,FrameWidth1,FrameHeight1,TankWidth,save1,tt83)

cap1.release()


CurrentDate = strftime("%y",) + strftime("%m",) + strftime("%d",)
CurrentTime = strftime("%H",) + strftime("%M",) + strftime("%S",)
print 'The experiment ended at ...ymd & hms ____' + CurrentDate + ' & ' + CurrentTime

cv2.destroyAllWindows()