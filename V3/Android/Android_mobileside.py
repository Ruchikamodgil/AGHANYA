import os
import sys
import time
from cv2 import cv2 as cv
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
import requests
import json
from twilio.rest import Client #REST API
import datetime
import smtplib 
import imghdr 
from email.message import EmailMessage 
import pyrebase
import collections
import requests
from pyowm import OWM
import sqlite3
import urllib.request

def image_resize(img):
    # import numpy as np
    # from PIL import Image
    image = Image.fromarray(img, 'RGB')
    #print(type(image))
    if image.size >(1600,1600):
        image = image.resize((1600,1600))
    # image = image.save("./image.jpg") # where to temporarily save image
    return image

def predictor_(test_data):
    # from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
    ENDPOINT = "https://centralindia.api.cognitive.microsoft.com/"

    # Replace with a valid key
    # training_key = "<your training key>"
    # prediction_key = "dac2d0a7126f4d2fb93a128c8b09c14f"
    prediction_key ="dac2d0a7126f4d2fb93a128c8b09c14f"
    prediction_resource_id = "/subscriptions/e76a64dd-9c6d-4b69-9849-b58e98aea2c5/resourceGroups/Cattle_pred/providers/Microsoft.CognitiveServices/accounts/AZURE-Student"
    predictor = CustomVisionPredictionClient(prediction_key, endpoint = ENDPOINT)
    project_id = "15d8e85f-3efe-4e32-a62c-8303c5b051a6" 
    # "15d8e85f-3efe-4e32-a62c-8303c5b051a6"
    # publish_iteration_name = "Iteration1"
    publish_iteration_name ="Iteration3"
    # FOR IMAGE FILE
    # iteration_id="d8553fa6f7664beb89a582515860d199"
    iteration_id="2b57a50938634342b5fe552de3b318e2"
    
    

    results = predictor.detect_image(project_id, publish_iteration_name, test_data,iteration_id)
    return results


config = {
    "apiKey": "AIzaSyDienGaKvTKGuSgKIFsU1pupYC1DABpeYk",
    "authDomain": "aghanya-test-py.firebaseapp.com",
    "databaseURL": "https://aghanya-test-py.firebaseio.com",
    "projectId": "aghanya-test-py",
    "storageBucket": "aghanya-test-py.appspot.com",
    "messagingSenderId": "356482709357",
    "appId": "1:356482709357:web:eeb1790474348ca3660c64",
    "measurementId": "G-MGVHBRZDTV"
    }

firebase = pyrebase.initialize_app(config)

    # database for data, storage for storing
storage = firebase.storage()
db = firebase.database()
#INITIAL

def stream_handler(message):
    # print(message["event"]) # put
    # print(message["path"]) # /-K7yGTTEp7O549EzTYtI
    # print(message["data"]) # {'title': 'Pyrebase', "body": "etc..."}
    # print(type(message["data"]))

    if message["path"] =="/": #old complaints 
        pass # ----->To be developed

    else :  #NEW complaints
        print(message["event"]) # put
        print(message["path"]) # /-K7yGTTEp7O549EzTYtI
        print(message["data"])

        x= message["data"]
        date = x['date']
        time = x['time']
        img_url = x['image_url']
        loc = "29.9652222,76.8876169" #x['location']
        # uid = x['uid']
        # E = x['E']
        i = loc.find(',')
        lat = float(loc[:i])
        lon =float(loc[i+1:])
        

        # IMAGE DOWNLOAD 
        urllib.request.urlretrieve(img_url, "IMG_mobile.jpg")
        path = "./IMG_mobile.jpg"
        img = cv.imread(path)
        # cv.imshow("img",img)
        img = cv.cvtColor(img,cv.COLOR_BGR2RGB)
        image = image_resize(img)
        image = image.save("./image.jpg") # where to temporarily save image
        with open("./image.jpg", mode ='rb') as test_data:
            results = predictor_(test_data)
        tags=[]
        prob=[]
        threshold = 60 # % threshold for prediction
        for prediction in results.predictions:
                if prediction.probability * 100 >= threshold :
                        tags.append(prediction.tag_name)
                        prob.append(prediction.probability * 100)
        if (tags !=[] and prob !=[]): # if some animal detected
            print (tags,prob)
        
        for _ in range (len(tags)):
            data ={}
            data.update({"Date":date})
            data.update({"Time":time})
            data.update({"tag":tags[_]})
            data.update({"Probability":round(prob[_],3)})
            data.update({"S":0})
            data.update({"A":0})
            data.update({"E":0}) #Emergency
            # data.update({"LOCATION":str(loc)})
            data.update({"Lat":lat})
            data.update({"lon":lon})
            data.update({"URL":img_url})
            
            result = db.child("ANDROID_WEBSIDE").push(data)
            print("STORED in db")


   
#STREAM
my_stream = db.child("cowimages").stream(stream_handler)
time.sleep(5000)

        