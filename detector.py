import numpy as np
import cv2
from os.path import exists

def get_values_from_file(filename):
    
    filename_exists = exists(filename)
    
    if filename_exists == True:
        f = open(filename)
        trackbar_value_h_low = int(f.readline())
        trackbar_value_s_low = int(f.readline())
        trackbar_value_v_low = int(f.readline())
        trackbar_value_h_high = int(f.readline())
        trackbar_value_s_high = int(f.readline())
        trackbar_value_v_high = int(f.readline())
        trackbar_value_exposure = int(f.readline())
        trackbar_value_wb_temp = int(f.readline())
        trackbar_value_gaussian = int(f.readline())
        f.close()
    
    else:
        trackbar_value_h_low = 27
        trackbar_value_s_low = 27
        trackbar_value_v_low = 27
        trackbar_value_h_high = 127
        trackbar_value_s_high = 127
        trackbar_value_v_high = 127
        trackbar_value_exposure = 127
        trackbar_value_wb_temp = 127
        trackbar_value_gaussian = 1
    
    values = [trackbar_value_h_low, trackbar_value_s_low, trackbar_value_v_low, trackbar_value_h_high, trackbar_value_s_high, trackbar_value_v_high, trackbar_value_exposure, trackbar_value_wb_temp, trackbar_value_gaussian]
    return values

def update_h_low(new):
    global trackbar_value_h_low
    trackbar_value_h_low = new
def update_v_low(new):
    global trackbar_value_v_low
    trackbar_value_v_low = new
def update_s_low(new):
    global trackbar_value_s_low
    trackbar_value_s_low = new
def update_h_high(new):
    global trackbar_value_h_high
    trackbar_value_h_high = new
def update_s_high(new):
    global trackbar_value_s_high
    trackbar_value_s_high = new
def update_v_high(new):
    global trackbar_value_v_high
    trackbar_value_v_high = new
def update_exposure(new):
    global trackbar_value_exposure
    trackbar_value_exposure = new
def update_wb_temp(new):
    global trackbar_value_wb_temp
    trackbar_value_wb_temp = new
def update_gaussian(new):
    global trackbar_value_gaussian
    if new % 2 == 0:
        trackbar_value_gaussian = new + 1
    else:
        trackbar_value_gaussian = new

     
def main():
    global values
    camera = cv2.VideoCapture(1)

    
    camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    camera.set(cv2.CAP_PROP_AUTO_WB, 0)
     
    cv2.namedWindow("Parameters")
    cv2.createTrackbar("Hue low", "Parameters", values[0], 179, update_h_low)
    cv2.createTrackbar("Saturation low", "Parameters", values[1], 255, update_s_low)
    cv2.createTrackbar("Value low", "Parameters", values[2], 255, update_v_low)
    cv2.createTrackbar("Hue high", "Parameters", values[3], 179, update_h_high)
    cv2.createTrackbar("Saturation high", "Parameters", values[4], 255, update_s_high)
    cv2.createTrackbar("Value high", "Parameters", values[5], 255, update_v_high)
    cv2.createTrackbar("Exposure", "Parameters", values[6], 500, update_exposure)
    cv2.createTrackbar("White balance temperature", "Parameters", values[7], 6500, update_wb_temp)   
    cv2.createTrackbar("Gaussian blurring", "Parameters", values[8], 25, update_gaussian)
    
    while True:
        ret, frame = camera.read()
        
        blur_gaussian = cv2.GaussianBlur(frame,(trackbar_value_gaussian, trackbar_value_gaussian),0)
 
        frame = cv2.cvtColor(blur_gaussian, cv2.COLOR_BGR2HSV)
                 
        lH = trackbar_value_h_low
        lS = trackbar_value_s_low
        lV = trackbar_value_v_low
        hH = trackbar_value_h_high
        hS = trackbar_value_s_high
        hV = trackbar_value_v_high
         
        camera.set(cv2.CAP_PROP_EXPOSURE, trackbar_value_exposure)
        camera.set(cv2.CAP_PROP_WB_TEMPERATURE, trackbar_value_wb_temp)
        
        lowerLimits = np.array([lH, lS, lV])
        upperLimits = np.array([hH, hS, hV])
         
        thresholded = cv2.inRange(frame, lowerLimits, upperLimits)
         
        thresholded = cv2.bitwise_not(thresholded)
        
        contours, _= cv2.findContours(thresholded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        for cnt in contours :

            approx = cv2.approxPolyDP(cnt, 0.5 * cv2.arcLength(cnt, True), True)
            
            n = approx.ravel() 
            i = 0

            for j in n : 
                if(i % 2 == 0): 
                    x = n[i] 
                    y = n[i + 1]
            
                    string = str(x) + ", " + str(y) 

                cv2.putText(frame, string, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0)) 
                i = i + 1                
         
        cv2.imshow("Original", frame)
         
        cv2.imshow("Thresholded", thresholded)
         
        if (cv2.waitKey(1) & 0xFF) == ord("q"):
            values = [str(trackbar_value_h_low), str(trackbar_value_s_low), str(trackbar_value_v_low), str(trackbar_value_h_high), str(trackbar_value_s_high), str(trackbar_value_v_high), str(trackbar_value_exposure), str(trackbar_value_wb_temp), str(trackbar_value_gaussian)]
            f = open(filename,"w")
            for i in range(len(values)):
                f.write(values[i])
                f.write("\n")
             
            f.close()
            break
 
    camera.release()
    cv2.destroyAllWindows()
    

filename = "red.txt"

values = get_values_from_file(filename)

     
if __name__ == "__main__":
    main()