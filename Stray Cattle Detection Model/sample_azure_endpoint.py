from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
import os
import sys

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

tags=[]
prob=[]
# to be run in iterations.
with open("Test images/test2.jpg", mode ='rb') as test_data: # test images has all images
    results = predictor.detect_image(project_id, publish_iteration_name, test_data,iteration_id)
for prediction in results.predictions:
    print("\t" + prediction.tag_name + ": {0:.2f}% bbox.left = {1:.2f}, bbox.top = {2:.2f}, bbox.width = {3:.2f}, bbox.height = {4:.2f}".format(prediction.probability * 100, prediction.bounding_box.left, prediction.bounding_box.top, prediction.bounding_box.width, prediction.bounding_box.height))    
    if prediction.probability * 100 >=75: #thresold
        tags.append(prediction.tag_name)
        prob.append(prediction.probability * 100)

# to be run in iterations
# print(tags)
# print(prob)

# writing a file







