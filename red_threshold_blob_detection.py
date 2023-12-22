#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import cv2
import os.path
import time



# NB! This function will be re-used in the future labs
def get_values_from_file(path_of_text_file):
    l_lines = []
    if os.path.exists(path_of_text_file):
        f = open(path_of_text_file,'r')
        for lines in f:
            l_lines.append(int(lines[0:]))
        print(l_lines)
        f.close()
        
        
    else:
        print('Error while opening the file! Using predefined values:')
        lH = 0
        lS = 0
        lV = 0
        hH = 180
        hS = 255
        hV = 255
        ex = 148
        wb = 3523
        l_lines = [lH,lS,lV,hH,hS,hV,ex,wb]
    
    """
    This function reads the text file and returns all of the trackbar values
    """

    return l_lines

### TODO 1: Add code from task 5
### TODO 2: Once the main loop is exited, new trackbar values should be written into a text file (that is going to be in a specific lab folder)
### TODO 3: Fill in the get_values_from_file() function which reads in the text file and outputs trackbar values
### TODO 4: Run this program at least twice to make sure the trackbar values are written and read from the text file 

# This function should run successfully even when there is no text file in the folder
# get_values_from_file(###add text file path here###)


#path = '/home/robo-student01/robotics-i-loti.05.010-22-23a-c09294-stepan-strelchenko/labs/lab05/trackbar_defaults.txt'
path = '/home/stepan/robotics_g10_repos/trackbar_values_txt'
values = get_values_from_file(path)
print(values)
lH = values[0]
lS = values[1]
lV = values[2]
hH = values[3]
hS = values[4]
hV = values[5]
ex = values[6]
wb = values[7]
n = 7
def update_lH(new_lH):
    global lH
    lH = new_lH
def update_lS(new_lS):
    global lS
    lS = new_lS
def update_lV(new_lV):
    global lV
    lV = new_lV
def update_hH(new_hH):
    global hH
    hH = new_hH
def update_hS(new_hS):
    global hS
    hS = new_hS
def update_hV(new_hV):
    global hV
    hV = new_hV
    
def update_exposure(new_ex):
    global ex
    ex = new_ex
def update_wbt(new_wb):
    global wb
    wb = new_wb

def update_n(new_n):
    global n
    n = new_n






def main():
    
    previous_time = 0
    new_time = 0
    #pass # remove this after adding the code
    camera = cv2.VideoCapture(6)
    camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    camera.set(cv2.CAP_PROP_AUTO_WB, 0)
    
    
    
    
    cv2.namedWindow("Colour trackbars")
    cv2.createTrackbar("n for kernel", "Colour trackbars",n , 15, update_n)
    cv2.createTrackbar("exposure", "Colour trackbars",ex , 500, update_exposure)
    
    cv2.createTrackbar("wbt", "Colour trackbars",wb, 6500, update_wbt)
    
    
    cv2.createTrackbar("lH", "Colour trackbars", lH, 180, update_lH)
    cv2.createTrackbar("lS", "Colour trackbars", lS, 255, update_lS)
    cv2.createTrackbar("lV", "Colour trackbars", lV, 255, update_lV)
    cv2.createTrackbar("hH", "Colour trackbars", hH, 180, update_hH)
    cv2.createTrackbar("hS", "Colour trackbars", hS, 255, update_hS)
    cv2.createTrackbar("hV", "Colour trackbars", hV, 255, update_hV)
    
    blobparams = cv2.SimpleBlobDetector_Params()
    blobparams.filterByArea = True
    blobparams.minArea = 100
    blobparams.maxArea = 10000

  # in case the blob is not perfectly circular
    blobparams.filterByCircularity = False

  # and could be a bit wonky
    blobparams.filterByInertia = False

  # and might have holes inside
    blobparams.filterByConvexity = False

  # don't want to detect every single small speck in the proximity
    blobparams.minDistBetweenBlobs = 50
    
    detector = cv2.SimpleBlobDetector_create(blobparams)
    while True:
        # Read the image from the camera
        ret, frame = camera.read()
        frame = frame[215:265]
        
        width = frame.shape[1]
        height = frame.shape[0]
        
        new_time = time.time()
        
        camera.set(cv2.CAP_PROP_EXPOSURE,ex)
        
        camera.set(cv2.CAP_PROP_WB_TEMPERATURE,wb)
        
        fps = round(1/(new_time - previous_time),0)
        #print(fps)
        fps_str = str(fps)
        previous_time = new_time
        
        lowerLimits = np.array([lH, lS, lV])
        upperLimits = np.array([hH, hS, hV])

        # Our operations on the frame come here
        if n% 2 != 0:
            blur = cv2.GaussianBlur(frame,(n,n),0)
            #blur = cv2.blur(frame,(n,n),0)
        frame_HSV = cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)
        thresholded = cv2.inRange(frame_HSV, lowerLimits, upperLimits)
        thresholded = cv2.rectangle(thresholded, (0, 0), (width-1, height-1), (0, 0, 0), 2)
        inverted_img = cv2.bitwise_not(thresholded)
        
    
        # Display the resulting frame
        cv2.imshow("Thresholded", inverted_img)
        
        keypoints = detector.detect(inverted_img)
        frame = cv2.drawKeypoints(frame, keypoints, None, (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        
        #print out the coordinates
        for keypoint in keypoints:
            x = int(keypoint.pt[0])
            y = int(keypoint.pt[1])
            str_x = str(x)
            str_y = str(y)
            cv2.putText(frame,str_x + ',', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(frame,str_y, (x+70, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        
        
                
            
        if len(keypoints) == 2:
            
            print(keypoints[0].pt[0])
            print(keypoints[0].pt[1])
        elif len(keypoints) == 1:
            print(keypoints[0].pt[0])
            
        
        
        cv2.putText(frame, fps_str, (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Original", frame)
        # Quit the program when "q" is pressed
        if (cv2.waitKey(1) & 0xFF) == ord("q"):
            break
          
    # When everything done, release the camera
    new_values = [lH,lS,lV,hH,hS,hV,ex,wb]
    f = open(path,'w')
    for x in new_values:
            
        f.write(str(x)+'\n')
    f.close()
    print("closing program")
    camera.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()
