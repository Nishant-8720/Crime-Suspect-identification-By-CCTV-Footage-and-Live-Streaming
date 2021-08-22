


import cv2
import pickle
import argparse
import importlib
import pandas as pd
import datetime
import csv
from transformer import PoseExtractor
import matplotlib.pyplot as plt
import time

fname="isPose.csv"
with open(fname, 'w') as csvfile: 
    fields = ['person','probabilities']   
    csvwriter = csv.writer(csvfile)  
    csvwriter.writerow(fields)

config = importlib.import_module('config.' + "conf")


def pose(path):
    model = pickle.load(open(config.classifier_model, 'rb'))
    t02=time.time()
    extractor = PoseExtractor()
    cap = cv2.VideoCapture(path)
    while(cap.isOpened()):
        ret, image = cap.read()
        if ret == False:
            break
        t12=time.time()
        sample = extractor.transform([image])
        prediction = model.predict(sample.reshape(1, -1))
            # print(prediction[0])
        rows=[['Speaker',prediction[0]]]
        cv2.imshow("Hand Gestures", image)
        with open(fname, 'a') as cfile:
            csvwtr = csv.writer(cfile) 
            csvwtr.writerows(rows)
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        num_seconds = t12 - t02
        if num_seconds > 30:  
            break
        

    cap.release()
    cv2.destroyAllWindows()
    da=pd.read_csv(fname)
    da.to_html("templates/Posedetails.html")
    
    return path





