def Excel_Save(tt91, GroupName, boxes, data1, data1Stamp, data2, data2Stamp, Tank1, Tank2, Tank1_Raw, Tank2_Raw, FishName1,DOB1,FishType1,FishSex1,FishName2,DOB2,FishType2,FishSex2,FrameWidth1,FrameHeight1,TankWidth,save1,tt83):
    import time
    import os
    import csv
    from time import strftime
    from PIL import ImageGrab

    ComputerName = "Administrator"
    Tank1.release()
    Tank2.release()
    Tank1_Raw.release()
    Tank2_Raw.release()

    del Tank1
    del Tank2
    del Tank1_Raw
    del Tank2_Raw


    CurrentTime = strftime("%H",) + strftime("%M",) + strftime("%S",)
    CurrentDate = strftime("%y",) + strftime("%m",) + strftime("%d",)


    if not os.path.exists(tt83):
        os.makedirs(tt83)

    rows = len(data1)
    with open(tt83 + GroupName + "_Raw_"  + "Hour_" + tt91 + '_Tank1.csv', "wb") as f1:
        f=csv.writer(f1,delimiter=',')
        f1.write(time.ctime())
        f1.write('\n')
        f1.write('Tank-P1')
        f1.write('\n')
        f.writerows(boxes)
        f1.write('Tank-P2')
        f1.write('\n')
        f.writerows(boxes)
        f1.write('FishName:' + FishName1)
        f1.write('\n')
        f1.write('DOB:' + DOB1)
        f1.write('\n')
        f1.write('FishType:' + FishType1)
        f1.write('\n')
        f1.write('FishSex:' + FishSex1)
        f1.write('\n')
        f1.write('CurrentDate:' + CurrentDate)
        f1.write('\n')
        f1.write('CurrentTime:' + CurrentTime)
        f1.write('\n')
        f1.write('FrameRate:3')
        f1.write('\n')
        f1.write('FrameWidth:' + str(FrameWidth1))
        f1.write('\n')
        f1.write('FrameHeight:' + str(FrameHeight1))
        f1.write('\n')
        f1.write('TankWidth(mm):' + str(TankWidth))
        f1.write('\n')
        f1.write('Total data:' + str(rows))
        f1.write('\n')
        f.writerows(data1)



    rows = len(data2)
    with open(tt83 + GroupName + "_Raw_"  + "Hour_" + tt91 + '_Tank2.csv', "wb") as f2:
        f=csv.writer(f2,delimiter=',')
        f2.write(time.ctime())
        f2.write('\n')
        f2.write('Tank-P1')
        f2.write('\n')
        f.writerows(boxes)
        f2.write('Tank-P2')
        f2.write('\n')
        f.writerows(boxes)
        f2.write('FishName:' + FishName2)
        f2.write('\n')
        f2.write('DOB:' + DOB2)
        f2.write('\n')
        f2.write('FishType:' + FishType2)
        f2.write('\n')
        f2.write('FishSex:' + FishSex2)
        f2.write('\n')
        f2.write('CurrentDate:' + CurrentDate)
        f2.write('\n')
        f2.write('CurrentTime:' + CurrentTime)
        f2.write('\n')
        f2.write('FrameRate:3')
        f2.write('\n')
        f2.write('FrameWidth:' + str(FrameWidth1))
        f2.write('\n')
        f2.write('FrameHeight:' + str(FrameHeight1))
        f2.write('\n')
        f2.write('TankWidth(mm):' + str(TankWidth))
        f2.write('\n')
        f2.write('Total data:' + str(rows))
        f2.write('\n')
        f.writerows(data2)

    with open(tt83 + GroupName + "_Raw_"  + "Hour_" + tt91 + '_TimeStamp.csv', "wb") as f3:
        f=csv.writer(f3,delimiter=',')
        f3.write(time.ctime())
        f3.write('\n')
        f.writerows(data2Stamp)


    if save1==1:
        if not os.path.exists(tt83):
            os.makedirs(tt83)
        ImageGrab.grab().save(tt83 + GroupName + "_Raw_"  + "Hour_" + tt91 + "_quit.jpg", "JPEG")
    else:
        if not os.path.exists(tt83):
            os.makedirs(tt83)
        ImageGrab.grab().save(tt83 + GroupName + "_Raw_"  + "Hour_" + tt91 + ".jpg", "JPEG")
