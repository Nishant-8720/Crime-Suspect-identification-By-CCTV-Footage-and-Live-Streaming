from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.utils import np_utils
from keras.preprocessing.image import  img_to_array
import os
import numpy as np
import csv
import pandas as pd
import datetime
import tensorflow as tf
import cv2
import time
from PIL import Image
from time import sleep
import matplotlib.pyplot as plt
import time


fname="isWeapon.csv"
with open(fname, 'w') as csvfile: 
    fields = ['person','probabilities']   
    csvwriter = csv.writer(csvfile)  
    csvwriter.writerow(fields)

x=[]
m,n = 50,50
model = tf.keras.models.load_model("models\\model_latest.h5")
path = 'test\\'
files=os.listdir(path);
# t33=time.time()

# load path from main.py file / user enterd input 
def weapDetect(pathTest):
    t03=time.time()
    cam = cv2.VideoCapture(pathTest)
    currentframe = 0
    while True:
        ret, frame = cam.read() 
        if ret == False:
            break
        t33=time.time()
        # if ret:
        name = 'test/' + str(currentframe) + '.jpg'
        # print('Creating...' + name)       
        cv2.imwrite(name, frame)


        currentframe += 1
        num_seconds = t33 - t03
        if num_seconds > 30:  
            break
       
        # else:
        #     break
    cam.release()
    cv2.destroyAllWindows()
    x=[]
    for i in files:
        im = Image.open(path + i);
        imrs = im.resize((m,n))
        imrs=img_to_array(imrs)/255;
        imrs=imrs.transpose(2,0,1);
        imrs=imrs.reshape(3,m,n);
        x.append(imrs)
    x=np.array(x);
    predictions = model.predict(x)
    maxElement = np.amax(predictions)
    # pred=np.array_str(predictions)
    rows=['Speaker',maxElement]
    with open(fname, 'a') as cfile:
        csvwtr = csv.writer(cfile)
        csvwtr.writerow(rows) 
    print (predictions)
    da=pd.read_csv(fname)
    da.to_html("templates/Weapdetails.html")
    if maxElement>0.7:
        me=1
    else:
        me=0
    return me