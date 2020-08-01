import os
import sys 
import cv2

video_path ="./Test images/Stray Animals in India - A great concern __VET For PET__.mp4"
#directory = "<directory for saving images>"
directory= os.getcwd() # comment this to use custom directory
# print(directory)
os.chdir(directory) # saving images in current working directory
cap = cv2.VideoCapture(video_path)
os.mkdir("data") # data folder in current directory, to save the images

#FPS mode
# fps = 25
# cap.set(cv.CAP_PROP_FPS,fps)

# delay mode (millisec)
delay = 10000 # 10sec delay : can be adjusted based on video length : 1 frame in every <delay> second
currentFrame=0
while(True):
    ret,frame =cap.read()
    if ret == False:
        	continue
    #saving the frames
    name = "data/frame"+str(currentFrame) + ".jpg" # saving image in data folder as frame1.jpg...
    # print(name)
    cv2.imwrite(name,frame)
    cv2.imshow("img",frame)
    currentFrame +=1 # increassing current frame
    key = cv2.waitKey(delay) & 0xFF
    if key == ord('q') :
        break #press q to quit , press q in video display window
    
		

cap.release()
cv2.destroyAllWindows()


