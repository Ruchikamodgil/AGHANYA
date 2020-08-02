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


def image_resize(img):
    # import numpy as np
    # from PIL import Image
    image = Image.fromarray(img, 'RGB')
    #print(type(image))
    if image.size >(1600,1600):
        image = image.resize((1600,1600))
    # image = image.save("./image.jpg") # where to temporarily save image
    return image

def predictor_(test_data): #V3
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



def checktime():
    return(time.localtime())
def firestore(tags,prob,loc,date,time):
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
        data.update({"Probability":round(prob[_],3)})
        data.update({"S":0})
        data.update({"A":0})
        data.update({"LOCATION":str(loc)})

        rslt = db.child("ANDROID_WEBSIDE").push(data)
        x = str(rslt.get('name')) # Name of child node created
        path_on_cloud = "android"+ x +".jpg" #token+.jpg
        storage.child(path_on_cloud).put(img_path)
        url1 = storage.child(path_on_cloud).get_url('token') # Downurl
        print(url1)
        # url2 = storage.child(path_on_cloud).get_url('imgPath') # Downurl
        # print(url2)
        db.child("ANDROID_WEBSIDE").child(str(rslt.get('name'))).update({"URL": url1})
    print("STORED in db")


# #Test Video
# vid_path = "./Test images/Stray Animals in India - A great concern __VET For PET__.mp4"
vid_path = ".././Test images/delhi3.mp4"
# vid_path = "./Test images/sec5_vid.mp4"
# fps = 25
vid = cv.VideoCapture(vid_path)
# vid.set(cv.CAP_PROP_FPS,fps)
delay = 500 #millisec
currentFrame=0

loc ="29.964275,76.865226" # predefined location here

loc_link = "https://www.google.com/maps/place/29%C2%B057'51.4%22N+76%C2%B051'54.8%22E/@29.964275,76.8630373,17z/data=!3m1!4b1!4m5!3m4!1s0x0:0x0!8m2!3d29.964275!4d76.865226"


# MAIN
while(True):
    tags=[]
    prob=[]
    ret,frame = vid.read()
    if ret == False:
    	continue
    currentFrame +=1
    frame = cv.cvtColor(frame,cv.COLOR_BGR2RGB) # BGR to RGB
    image = image_resize(frame)
    image = image.save("./image.jpg") #temp save of image


    with open("./image.jpg", mode ='rb') as test_data: # test images has all images
        results = predictor_(test_data)

    test_img_h, test_img_w, test_img_ch = np.array(frame).shape
    for prediction in results.predictions:
    
        if int(prediction.probability * 100) >= 60 : #thresold
            print("\t" + prediction.tag_name + ": {0:.2f}% bbox.left = {1:.2f}, bbox.top = {2:.2f}, bbox.width = {3:.2f}, bbox.height = {4:.2f}".format(prediction.probability * 100, prediction.bounding_box.left, prediction.bounding_box.top, prediction.bounding_box.width, prediction.bounding_box.height))
            tags.append(prediction.tag_name)
            prob.append(prediction.probability *  100)
            x= int(prediction.bounding_box.top * test_img_h)
            y = int(prediction.bounding_box.left * test_img_w)
            w = int(prediction.bounding_box.width * test_img_w)
            h =int(prediction.bounding_box.height * test_img_h)
            # cv.imshow("Video",frame)
            cv.putText(frame,prediction.tag_name,(y,x-10),cv.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv.LINE_AA)       
            cv.rectangle(frame,(y+10,x+10),(y+w+10,x+h+10),(0,255,255),5)
            animal = frame[x+10:x+h+10,y+10:y+w+10,:]
            cv.imshow("animal",animal) # Animal Cutout
            # cv.imshow("Video",frame)
        cv.imshow("CCTV_1_FOOTAGE",frame)
    
    if (tags !=[] and prob !=[]): # if some animal detected
        print(tags,prob)
        date  = str(datetime.date.today())
        t =checktime()
        timex = time.strftime("%H:%M:%S",t)
        # # sending sms alert
        # to = '+919996492589'
        
        # # sms(tags,prob,loc,loc_link,date,timex,cam_name,to)

        # # sending email alert with pic
        # to_ =["ankurvermaaxz@gmail.com"] # mail to send alert
        # email(tags,prob,loc,loc_link,date,timex,cam_name,to_)

        #Save image and data in firebase

        firestore(tags,prob,loc,date,timex)

    key = cv.waitKey(delay) & 0xFF
    if key == ord('q') :
        break #press q to quit
		

vid.release()
cv.destroyAllWindows()