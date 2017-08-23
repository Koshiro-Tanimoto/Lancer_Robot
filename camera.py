#!/usr/bin/env python
#-*- coding:utf-8 -*-

import cv2
import sys

flame_size = 2
w = 0
h = 0

if __name__ == '__main__':

    cap = cv2.VideoCapture(0)
    ret, flame = cap.read()

    while True:
        ret, flame = cap.read()
        if ret == False :
            print("Error: Camera capture failed.")
            sys.exit(1)

        height, width = flame.shape[:2]
        hflame = cv2.resize(flame,(width/flame_size,height/flame_size))
        h_height, h_width = hflame.shape[:2]

        cv2.circle(hflame,(h_width/2+w,h_height/2+h),20,(0,0,255),2)
        cv2.circle(hflame,(h_width/2+w,h_height/2+h),3,(0,0,255),-1)
        cv2.line(hflame, (h_width/2+w,h_height/2+h+20), (h_width/2+w, h_height/2+h+30), (0, 0, 255),2)
        cv2.line(hflame, (h_width/2+w,h_height/2+h-20), (h_width/2+w, h_height/2+h-30), (0, 0, 255),2)
        cv2.line(hflame, (h_width/2+w+20,h_height/2+h), (h_width/2+w+30, h_height/2+h), (0, 0, 255),2)
        cv2.line(hflame, (h_width/2+w-20,h_height/2+h), (h_width/2+w-30, h_height/2+h), (0, 0, 255),2)
        
        cv2.imshow('camera',hflame)
        if cv2.waitKey(1) == ord('p'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("End of camera")
