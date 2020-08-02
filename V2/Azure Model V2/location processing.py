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

path = ".././Test images/test5.jpg"
loc ="29.965223,76.887212" # predefined location here
cam_name = "cam1" #predefined cam name
loc_link = "https://www.google.com/maps/place/29%C2%B057'54.8%22N+76%C2%B053'14.0%22E/@29.965223,76.8850233,17z/data=!3m1!4b1!4m5!3m4!1s0x0:0x0!8m2!3d29.965223!4d76.887212"


# Get an image
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
    prediction_key = "dac2d0a7126f4d2fb93a128c8b09c14f"
    prediction_resource_id = "/subscriptions/e76a64dd-9c6d-4b69-9849-b58e98aea2c5/resourceGroups/Cattle_pred/providers/Microsoft.CognitiveServices/accounts/AZURE-Student"
    predictor = CustomVisionPredictionClient(prediction_key, endpoint = ENDPOINT)
    project_id = "15d8e85f-3efe-4e32-a62c-8303c5b051a6" 
    publish_iteration_name = "Iteration1"
    # FOR IMAGE FILE
    iteration_id="d8553fa6f7664beb89a582515860d199"

    results = predictor.detect_image(project_id, publish_iteration_name, test_data,iteration_id)
    return results

def sms(tag,prob,loc,loc_,date,time,cam,to_tx):
    acc_sid = "AC53b30fe714a03aa740462bd9cb36fcf4"
    auth_token = "4c217ba652c3ead79b7bda0d3ba96c4c"

    client = Client(acc_sid,auth_token)
    for _ in range (len(tag)):
        tag1 = str(tag[_])
        prob1 = str(prob[_])
        msg = "Animal"+tag1+"is detected "+ cam +" with a confidence of"+prob1 +"at location"+loc+"on"+ date +"at"+ time +" Location link:" +loc_
        message = client.messages.create(
            body = msg,
            to = to_tx,
            from_ ='+13343674489') # from is predefined


def email(tag,prob,loc,loc_,date,time,cam,email_rx):
    email_tx = "sihjune2020@gmail.com"
    pass_tx = "Asdfgh1234@"
    msg = EmailMessage()
    msg['Subject']= 'ANIMAL DETECTED!'
    msg['From'] = email_tx
    msg['To'] = email_rx
    for _ in range (len(tag)):
        tag1 = str(tag[_])
        prob1 = str(prob[_])
        msg_ = "Animal "+tag1+" is detected in "+ cam +" with a confidence of "+prob1 +" at location "+loc+ "Location link: "+loc_+" on "+ date +" at "+ time+" Image attached " 
        msg.set_content(msg_)

    with open ("./image.jpg", 'rb') as f: #path where frame is saved temporarirly
        file_data = f.read()
        #imghdr 
        file_name = f.name 
        file_type = imghdr.what(f.name)

    msg.add_attachment(file_data, maintype ='image', subtype = file_type, filename = file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_tx,pass_tx)
        smtp.send_message(msg)

def firestore(tags,prob,loc,date,time,cam_name):
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
    
    img_path = "./image.jpg" #image of  currentframe

    firebase = pyrebase.initialize_app(config)

    # database for data, storage for storing
    storage = firebase.storage()
    db = firebase.database()
    # data ={} #data to be stored
    for _ in range (len(tags)):
        data ={}
        data.update({"Date":date})
        data.update({"Time":time})
        data.update({"tag":tags[_]})
        data.update({"Probability":prob[_]})
        # data.update({"tag":tags[_]})
        rslt = db.child(cam_name).push(data)

        path_on_cloud = cam_name+str(rslt.get('name'))+".jpg" #token+.jpg
        storage.child(path_on_cloud).put(img_path)

        



# MAIN
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
        # print(prediction.bounding_box
        # x= int(prediction.bounding_box.top)
        # y = int(prediction.bounding_box.left)
        # w = int(prediction.bounding_box.width)
        # h =int(prediction.bounding_box.height)
        print("\t" + prediction.tag_name + ": {0:.2f}% ".format(prediction.probability * 100))    
        #     cv.putText(frame,prediction.tag_name,(x,y-10),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,125),2,cv.LINE_AA)       
        #     cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),5)
        # cv.imshow("Faces",frame)
        if prediction.probability * 100 >= threshold :
                tags.append(prediction.tag_name)
                prob.append(prediction.probability * 100)


if (tags !=[] and prob !=[]): # if some animal detected
    print (tags,prob)
    date  = str(datetime.date.today())
    t =time.localtime()
    time = time.strftime("%H:%M:%S",t)
    # sending sms alert
    to ='+919996492589' # no. to send sms alert
    sms(tags,prob,loc,loc_link,date,time,cam_name,to)

    # sending email alert with pic
    to_ =["ankurvermaaxz@gmail.com"] # mail to send alert
    email(tags,prob,loc,loc_link,date,time,cam_name,to_)

    #Save image and data in firebase

    firestore(tags,prob,loc,date,time,cam_name)
