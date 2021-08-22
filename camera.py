import cv2
from model import FacialExpressionModel
import numpy as np
import csv
import pandas as pd
import datetime
import matplotlib.pyplot as plt

facec = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
model = FacialExpressionModel("model.json", "model_weights.h5")
font = cv2.FONT_HERSHEY_SIMPLEX
fname="isExp.csv"
with open(fname, 'w') as csvfile: 
    fields = ['Name', 'Expression', 'Time']   
    csvwriter = csv.writer(csvfile)  
    csvwriter.writerow(fields) 


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        

    def __del__(self):
        self.video.release()

    def get_frame(self):
        _, fr = self.video.read()
        gray_fr = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
        faces = facec.detectMultiScale(gray_fr, 1.3, 5)
        # f = open("test.txt", "a")  
        frame_number = self.video.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = int(self.video.get(cv2.CAP_PROP_FPS))
        timestamps = [self.video.get(cv2.CAP_PROP_POS_MSEC)] 
        for (x, y, w, h) in faces:
            fc = gray_fr[y:y+h, x:x+w]

            roi = cv2.resize(fc, (48, 48))
            pred = model.predict_emotion(roi[np.newaxis, :, :, np.newaxis])
            rows=[['Speaker',pred,timestamps]]
            cv2.putText(fr, pred, (x, y), font, 1, (255, 255, 0), 2)
            cv2.rectangle(fr,(x,y),(x+w,y+h),(255,0,0),2)
            with open(fname, 'a') as cfile:
                csvwtr = csv.writer(cfile) 
                csvwtr.writerows(rows)
        da=pd.read_csv(fname)
        da.to_html("templates/Exprdetails.html")


        _, jpeg = cv2.imencode('.jpg', fr)
        return jpeg.tobytes()
