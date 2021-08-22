import cv2
import pandas as pd
import csv
import matplotlib.pyplot as plt
from prettytable import PrettyTable
import time
# from flask import Flask, redirect, url_for, request, render_template, Response

import os
import random

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
font = cv2.FONT_HERSHEY_SIMPLEX
fname="isFace.csv"
with open(fname, 'w') as csvfile:
  fields = ['person','is']   
  csvwriter = csv.writer(csvfile)  
  csvwriter.writerow(fields)


id = 0
namex=pd.read_csv('Names.csv', index_col=0, squeeze=True).to_dict()

def predict(path):
  print("hello")
  # ---------------------------------------------------------
  """
  maindir=os.getcwd()
  fileName=file
  directroy=str(fileName)
  os.chdir(os.getcwd()+'/Record Database')
  parent_dir=os.getcwd()
  mode=0o666 
  path=os.path.join(parent_dir,directroy)
  os.mkdir(path,mode)
  os.chdir(parent_dir+'/'+directroy)
  fname="isFace.csv"
  with open(fname, 'x') as csvfile: 
    fields = ['person','is']   
    csvwriter = csv.writer(csvfile)  
    csvwriter.writerow(fields)
  os.chdir(maindir)
  """
  # ----------------------------------------------------------

  cam = cv2.VideoCapture(path)
  cam.set(3, 640) # width
  cam.set(4, 480) # height


  minW = 0.1*cam.get(3)
  minH = 0.1*cam.get(4)
  countYes=0
  countNo=0
  t0=time.time()

  while True:

      ret, img =cam.read()
      t1=time.time()
      if ret==False:
        break
      gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

      faces = detector.detectMultiScale(gray, 1.3, 5)

      for(x,y,w,h) in faces:

          cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
          roi_gray = gray[y:y + h, x:x + w]
          roi_color = img[y:y + h, x:x + w]
          eyes = eye_cascade.detectMultiScale(roi_gray,minNeighbors=15)
          id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
          for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
          # Check if confidence is less them 100 ==> "0" is perfect match 
          
          if (confidence <100):
              id = namex[id]
              confidence = "  {0}%".format(round(100 - confidence))
              rows=[id,'yes']
              countYes+=1
              with open(fname, 'a') as cfile:
                csvwtr = csv.writer(cfile)
                csvwtr.writerow(rows)
          else:
              for i in range(0,100):
                id = "unknown"+str(i)
              confidence = "  {0}%".format(round(100 - confidence))
              countNo+=1
              rows1=[id,'no']
              with open(fname, 'a') as cfile1:
                csvwtr1 = csv.writer(cfile1)
                csvwtr1.writerow(rows1)
                   
          cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
          cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
      
      cv2.imshow('camera',img)
      num_seconds = t1 - t0
      if num_seconds > 30:  
        break  


      k = cv2.waitKey(10) & 0xff 
      if k == 27:
          break
  cam.release()
  cv2.destroyAllWindows()
  da=pd.read_csv(fname)
  da.to_html("templates/Facedetails.html")
  if(countYes>countNo):
    retvar=1
  else:
    retvar=0
  return retvar
