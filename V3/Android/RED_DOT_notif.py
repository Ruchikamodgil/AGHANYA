import pyrebase
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


def distance(lon1,lat1,lon2,lat2):
    from math import radians, cos, sin, asin, sqrt
    #RED DOTS
    
    lon1 = radians(lon1) 
    lon2 = radians(lon2) 
    lat1 = radians(lat1) 
    lat2 = radians(lat2) 
    # Haversine formula  
    dlon = lon2 - lon1  
    dlat = lat2 - lat1 
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))  
    # Radius of earth in kilometers. Use 3956 for miles 
    r = 6371 
    # calculate the result 
    return(c * r) 
    
def sms(to,msg):

    acc_sid = "AC53b30fe714a03aa740462bd9cb36fcf4"
    auth_token = "4c217ba652c3ead79b7bda0d3ba96c4c"

    client = Client(acc_sid,auth_token)
    # for _ in range (len(tag)):
    #     tag1 = str(tag[_])
    #     prob1 = str(prob[_])
    # msg = "Animal is detected at "+ loc +" Location link:" +link
    message = client.messages.create(
            body = msg,
            to = to,
            from_ ='+13343674489') # from is predefined


#STREAMING in "ANDROID" child
def stream_handler(message):
    # print(message["event"]) # put
    # print(message["path"]) # /-K7yGTTEp7O549EzTYtI
    # print(message["data"]) # {'title': 'Pyrebase', "body": "etc..."}
    # print(type(message["data"]))
    if message["path"] =="/": #old complaints 
        pass # ----->To be developed

    else :
        s= str(message["path"])
        #NEW ENTRY
        print(message["event"]) # put
        print(message["path"]) # /-K7yGTTEp7O549EzTYtI
        print(message["data"])
        x={}
        data= (db.child("ANDROID_WEBSIDE").child(s).get())
        for d in data.each():
            key = d.key()
            val = d.val()
            x.update({key:val})
        A= x['A']
        if A > 1: #ACCEPTED
            print(message["event"]) # put
            print(message["path"]) # /-K7yGTTEp7O549EzTYtI
            print(message["data"])


            date = (x['Date'])
            time = (x['Time'])
            # img_url = x['URL']
            lat2 = (x['Lat']) #x['location']
            lon2 = (x['lon'])
            tag = (x['tag'])
            
            # S= int(x['S']) #RESOLVED
            # E= int(x['E'])  #Emergency

            
            
            d=[] #distance betweeb node and loc.
            total_nodes = 6 #KURUKSHETRA
            nodes = {"red1" :[29.965470, 76.891908],
                        "red2" : [29.970303, 76.875890],
                        "red3" : [29.971725, 76.857072],
                        "red4" : [29.954427, 76.851762],
                        "red5" : [29.956509, 76.866385],
                        "red6" : [29.955431, 76.881695]}
            red = list(nodes.keys())
            for ix in nodes.values():
                lat1 = ix[0]
                lon1 = ix[1]
                dist = distance(lon1,lat1,lon2,lat2)
                d.append(dist)

            m = min(d) #MINIMUM DISTANCE
            num = d.index(m)
            # print(num)
            # Numbers
            n = red[num]
            # https://www.google.com/maps/place/29.9717158,76.8836256
            link = "https://www.google.com/maps/place/"+str(lat2)+","+str(lon2)
            loc = str(lat2)+","+str(lon2)
            if A == 3:  #Emergency
                msg1 =str( "!ALERT !ALERT !ALERT !ALERT !ALERT \n" + tag+" Caused an ACCIDENT at location " + loc +"\n link" +link + " on " + date+" at "+time)
                print(msg1)
                print("Local Authorities and Hospitals being Contacted")

                print("NOTIFICATION SENT TO POC: " + n)
                # print(link)
                # MESSAGING
                if num ==0 or num ==1:
                    to = '+919996492589'
                    print("MSG SENT TO ANKUR")
                    sms(to,msg1)
                elif num ==2 or num ==3:
                    to = '+917404533915'
                    print("MSG SENT TO RISHAB ")
                    sms(to,msg1)
                elif num == 4:
                    to='+918628809295'
                    print("MSG SENT TO AMAN ")
                    sms(to,msg1)
                else:
                    to='+919996195883'
                    print("MSG SENT TO AANCHAL ")
                    sms(to,msg1)
            else:
                msg2 =str(tag+" Found at location " + loc +"\n link"+ link + " on " + date+" at "+time )
                print(msg2)
                
                print("NOTIFICATION SENT TO POC: " + n)
                # print(link)
                # MESSAGING
                if num ==0 or num ==1:
                    to = '+919996492589'
                    print("MSG SENT TO ANKUR")
                    sms(to,msg2)
                elif num ==2 or num ==3:
                    to = '+917404533915'
                    print("MSG SENT TO RISHAB ")
                    sms(to,msg2)
                elif num == 4:
                    to='+918628809295'
                    print("MSG SENT TO AMAN ")
                    sms(to,msg2)
                else:
                    to='+919996195883'
                    print("MSG SENT TO AANCHAL ")
                    sms(to,msg2)

        else:
            pass
        


        


my_stream = db.child("ANDROID_WEBSIDE").stream(stream_handler)
time.sleep(5000)

