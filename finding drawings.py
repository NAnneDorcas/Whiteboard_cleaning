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
        #print(l_lines)
        f.close()
        
        
    else:
        print('Error while opening the file! Using predefined values:')

        
        ex = 148
        wb = 3523
        n = 7
        l_lines = [ex,wb,n]
    
    """
    This function reads the text file and returns all of the trackbar values
    """

    return l_lines




path = '/home/stepan/trackbar_values_txt'
values = get_values_from_file(path)
#print(values)

ex = values[0]
wb = values[1]
n = values[2]
    
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
    coordinates = []
    previous_time = 0
    new_time = 0
    #pass # remove this after adding the code
#     camera = cv2.VideoCapture(0)
#     camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
#     camera.set(cv2.CAP_PROP_AUTO_WB, 0)
    
    
    
    
#     cv2.namedWindow("Colour trackbars")
#     cv2.createTrackbar("n for kernel", "Colour trackbars",n , 15, update_n)
#     cv2.createTrackbar("exposure", "Colour trackbars",ex , 500, update_exposure)
#     
#     cv2.createTrackbar("wbt", "Colour trackbars",wb, 6500, update_wbt)
    
    frame = cv2.imread('new2.png')
    framegray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    print(framegray)
    #ret, thresh = cv2.threshold(framegray, 127, 255, 0)
    #thresh = cv2.adaptiveThreshold(framegray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
    thresh = cv2.adaptiveThreshold(framegray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print(contours)
    
    
    area = []
    img_cont = cv2.drawContours(frame, contours, 1, (0,255,0), 2)
    for cont in contours:
        if cv2.contourArea(cont) >= 101551.5 or cv2.contourArea(cont) <= 20.0:
            pass
        else:
            area.append(cv2.contourArea(cont))
            x,y,w,h = cv2.boundingRect(cont)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
    print(area)
   # while True:
        # Read the image from the camera
#     ret, frame = camera.read()
   # frame = frame[215:265]
   # frame = frame[100:265]
    width = frame.shape[1]
    height = frame.shape[0]
    #new_time = time.time()
    
#     camera.set(cv2.CAP_PROP_EXPOSURE,ex)
#     
#     camera.set(cv2.CAP_PROP_WB_TEMPERATURE,wb)
    
#     fps = round(1/(new_time - previous_time),0)
#     #print(fps)
#     fps_str = str(fps)
#     previous_time = new_time
    
    
    

    # Our operations on the frame come here
#     if n% 2 != 0:
#         blur = cv2.GaussianBlur(frame,(n,n),0)
        #blur = cv2.blur(frame,(n,n),0)
    
    

    # Display the resulting frame
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("b and w", frame)
    print(frame)
    
    # Drawing the lines
   # cv2.line(frame, (0, 0), (width, 0), (0, 0, 255), 5)
   # cv2.line(frame, (0, 0), (0, height), (0, 0, 255), 5)
    rows = height
    columns = width
    print(frame.shape)
    print(frame.min())
    print(frame.max())
    #for i in range(rows):
      #  for j in range(columns):
           #print(frame[i,j])
           
                
    
    

   # cv2.putText(frame, fps_str, (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
   # cv2.imshow("Original", frame)
        # Quit the program when "q" is pressed
        #if (cv2.waitKey(1) & 0xFF) == ord("q"):
           # break
          
#     # When everything done, release the camera
#     new_values = [ex,wb,n]
#     f = open(path,'w')
#     for x in new_values:
#             
#         f.write(str(x)+'\n')
#     f.close()
#     print("closing program")
   # print(coordinates)
   # cv2.imwrite("Whiteboard.png", gray)
    #camera.release()
    cv2.waitKey()
    #cv2.destroyAllWindows()
if __name__ == "__main__":
    main()

