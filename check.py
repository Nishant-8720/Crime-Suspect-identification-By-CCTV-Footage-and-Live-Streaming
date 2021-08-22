import numpy as np 
import cv2 


cap = cv2.VideoCapture("V_850.mp4")
fourcc = cv2.VideoWriter_fourcc('m','p','4','v') 
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640,480)) 




while(True): 

    ret, frame = cap.read()


    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 


    out.write(gray)


    cv2.imshow('Original', frame) 

   
    cv2.imshow('frame', gray) 


    if cv2.waitKey(1) & 0xFF == ord('a'): 
        break



cap.release() 

cv2.destroyAllWindows()