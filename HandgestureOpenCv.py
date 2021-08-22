

import numpy as np
from keras.preprocessing import image
from keras.models import load_model
import cv2
import pandas as pd
import csv
import matplotlib.pyplot as plt
import time

newmod=load_model('hand_gestures.h5')

background = None


accumulated_weight = 0.5

roi_top = 200
roi_bottom = 450
roi_right = 200
roi_left = 400
# t01=time.time()

fname="isHand.csv"
with open(fname, 'w') as csvfile: 
    fields = ['Name', 'Gesture']   
    csvwriter = csv.writer(csvfile)  
    csvwriter.writerow(fields) 

def calc_accum_avg(frame, accumulated_weight):

    global background
    

    if background is None:
        background = frame.copy().astype("float")
        return None

    cv2.accumulateWeighted(frame, background, accumulated_weight)


def segment(frame, threshold=20):
    global background
    

    diff = cv2.absdiff(background.astype("uint8"), frame)

    _ , thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)

 
    contours, hierarchy = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        return None
    else:
        hand_segment = max(contours, key=cv2.contourArea)
        return (thresholded, hand_segment)
 

def thres_display(img):
    width=64
    height=64
    dim=(width,height)
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    test_img=image.img_to_array(resized)
    test_img=np.expand_dims(test_img,axis=0)
    result= newmod.predict(test_img)
    val=[index for index,value in enumerate(result[0]) if value ==1]
    return val

def handGes(path):   
    t01=time.time()
    cam = cv2.VideoCapture(path)

   
    num_frames = 0

  
    while True:

        ret, frame = cam.read()
        t11=time.time()
        if ret==False:
            break
        frame = cv2.flip(frame, 1)
        frame_copy = frame

 
        roi = frame[roi_top:roi_bottom, roi_right:roi_left]

        # Apply grayscale and blur to ROI
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        if num_frames < 60:
            calc_accum_avg(gray, accumulated_weight)
            if num_frames <= 59:
                cv2.putText(frame_copy, "WAIT! GETTING BACKGROUND AVG.", (200, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                    
        else:
        
            cv2.putText(frame_copy, "Place your hand in side the box", (330, 340), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),1)
            cv2.putText(frame_copy, "Index 0: Fist", (330, 355), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),1)
            cv2.putText(frame_copy, "Index 1: Five", (330, 370), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),1)
            cv2.putText(frame_copy, "Index 2: None", (330, 385), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),1)
            cv2.putText(frame_copy, "Index 3: Okay", (330, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),1)
            cv2.putText(frame_copy, "Index 4: Peace", (330, 415), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),1)
            cv2.putText(frame_copy, "Index 5: Rad", (330, 430), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),1)
            cv2.putText(frame_copy, "Index 6: Straight", (330, 445), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),1)
            cv2.putText(frame_copy, "Index 7: Thumbs", (330, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),1)

        
            hand = segment(gray)

          
            if hand is not None:
                thresholded, hand_segment = hand
                
               
                cv2.drawContours(frame_copy, [hand_segment + (roi_right, roi_top)], -1, (255, 0, 0),1)

               
                cv2.imshow("Thresholded Image", thresholded)
                res=thres_display(thresholded)
                
                if len(res)==0:
                    cv2.putText(frame_copy, str('None'), (70, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                else:
                    x='index'+str(res[0])
                    cv2.putText(frame_copy, str(x), (70, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                    rows=[['Speaker',x]]
                    with open(fname, 'a') as cfile:
                        csvwtr = csv.writer(cfile) 
                        csvwtr.writerows(rows)
                
        
        cv2.rectangle(frame_copy, (roi_left, roi_top), (roi_right, roi_bottom), (0,0,255), 2)

       
        num_frames += 1

        cv2.imshow("Hand Gestures", frame_copy)

        
        k = cv2.waitKey(1) & 0xFF
        num_seconds = t11 - t01
        if num_seconds > 30:  
            break
        if k == 27:
            break
        
    cam.release()
    cv2.destroyAllWindows()
    da=pd.read_csv(fname)
    da.to_html("templates/Handdetails.html")

    
    return path