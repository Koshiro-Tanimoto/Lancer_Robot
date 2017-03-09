#!/usr/bin/env python
#-*- coding:utf-8 -*-

import cv2
import io
import numpy as np
import serial
import picamera

#Algorithm parameters
flame_size = 3    #Frame reduction parameter
Gauss = (9,9)     #Gaussbluer filter parameter 
threshold = 230   #Threshold of binarization (max:254)
min_area = 1000   #Area filter pareater
#camera_width = 160
#camera_height = 120

#Line trace algorithm 
def line_trace():

    while True:
        
        #Video capture
        ret , flame = cap.read()
        if ret == False :
            print("Error: Camera capture failed.")
            break
        
        #Resize of window scale
        height , width = flame.shape[:2]
        hflame = cv2.resize(flame,(width/flame_size,height/flame_size))
        h_height, h_width = hflame.shape[:2]
        result = hflame

        #Gray scale , noise filter and binarization
        gray = cv2.cvtColor(hflame,cv2.COLOR_RGB2GRAY)
        gray = cv2.GaussianBlur(gray,(Gauss),0)
        ret , bimg = cv2.threshold(gray,threshold,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        
        #Contour detection
        line , cont , hier = cv2.findContours(bimg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        #Extract line center
        cnt = cont[0]
        m = cv2.moments(cnt)

        if m['m10'] != 0 and m['m01'] != 0 and m['m00'] > min_area :
            
            #Calculation of line center
            cx = int(m['m10']/m['m00'])
            cy = int(m['m01']/m['m00'])
             
            #Calculation of deviation (center)
            dev = h_width/2-cx
             
            #Draw objects (Dev ceter ver)
            result = cv2.drawContours(hflame,cont,-1,(0,255,0),3)
            cv2.circle(result,(cx,cy),4,(255,0,0),-1)
            cv2.line(result,(cx,cy),(h_width/2,cy),(255,255,0),2)
        
        else :
            dev = 0 
            cy = h_height/2    

        #Draw objects
        cv2.circle(result,(h_width/2,cy),4,(0,0,255),-1)
        cv2.putText(result,"Dev(x_axis) : "+str(abs(dev)),(65,155),cv2.FONT_HERSHEY_PLAIN,1.0,(0,0,255))
        cv2.imshow('Line Teace',result)

        #Send results to mbed
        #ser.write(str(dev)+" ")

        #End process
        if cv2.waitKey(1) == ord('q'):
            break

#Main function
if __name__ == '__main__':
    
    #Serail config (to mbed)
    #ser = serial.Serial('/dev/ttyACM0',115200)
    
    #Open the camera
    cap = cv2.VideoCapture(0)
    
    #stream = io.BytesIO()
    #with picamera.PiCamera() as camera:
    #   camera.resolution = (camera_width, camera_height)
    #    camera.capture(stream, format='jpeg')
    #data = np.fromstring(stream.getvalue(), dtype=np.uint8)
    #hflame = cv2.imdecode(data, 1)

    line_trace()

    cap.release()
    cv2.destroyAllWindows()
    #ser.close

    print("End of line trace algorithm.")
