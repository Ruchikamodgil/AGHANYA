# https://notebooks.azure.com/FrankLa/projects/mlprimers/html/09%20-%20Object%20Detection%20with%20the%20Custom%20Vision%20Service.ipynb
from cv2 import cv2 as cv
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os 
import sys
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient

def resize_down_to_1600_max_dim(image):
    h, w = image.shape[:2]
    if (h < 1600 and w < 1600):
        return image

    new_size = (1600 * w // h, 1600) if (h > w) else (1600, 1600 * h // w)
    return cv.resize(image, new_size, interpolation = cv.INTER_LINEAR)

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



# vid_path = "./Test images/Stray Animals in India - A great concern __VET For PET__.mp4"
vid_path = "./Test images/Cows roam among people on the streets of Delhi.mp4"
# vid_path = "./Test images/sec5_vid.mp4"

# fps = 25
vid = cv.VideoCapture(vid_path)
# vid.set(cv.CAP_PROP_FPS,fps)
delay = 500 #millisec
currentFrame=0
while(True):
    tags=[]
    prob=[]
    ret,frame = vid.read()
    if ret == False:
    	continue
    #saving the frames
    # name = "./data/frame"+ str(currentFrame) + ".jpg"
    # cv.imwrite(name,frame)
    # cv.imshow("img",frame)

    # cv.imshow("CCTV_1_FOOTAGE",frame)
    currentFrame +=1
    # # our model here<>
    # print ("detecting...")
    # print(type(frame))

    # Resizing
    image = Image.fromarray(frame, 'RGB')
    #print(type(image))
    if image.size >(1600,1600):
        image = image.resize((1600,1600))
    image = image.save("./img_test/image.jpg")


    with open("./img_test/image.jpg", mode ='rb') as test_data: # test images has all images
        results = predictor.detect_image(project_id, publish_iteration_name, test_data,iteration_id)

    # print(results)
    test_img_h, test_img_w, test_img_ch = np.array(frame).shape
    for prediction in results.predictions:
        # print(prediction.bounding_box
        # x= int(prediction.bounding_box.top)
        # y = int(prediction.bounding_box.left)
        # w = int(prediction.bounding_box.width)
        # h =int(prediction.bounding_box.height)
        # print("\t" + prediction.tag_name + ": {0:.2f}% bbox.left = {1:.2f}, bbox.top = {2:.2f}, bbox.width = {3:.2f}, bbox.height = {4:.2f}".format(prediction.probability * 100, prediction.bounding_box.left, prediction.bounding_box.top, prediction.bounding_box.width, prediction.bounding_box.height))    
        # cv.putText(frame,prediction.tag_name,(x,y-10),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,125),2,cv.LINE_AA)       
        # cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),5)
    # cv.imshow("Video",frame)
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
        

    key = cv.waitKey(delay) & 0xFF
    if key == ord('q') :
        break #press q to quit
		

vid.release()
cv.destroyAllWindows()


