import cv2
import pickle
import numpy as np
import os

# This is to open the video capture funtion of cv2
video = cv2.VideoCapture(0)

#to pass the cascadeclassifier data that we got from the xml file to the facedetect
facedetect = cv2.CascadeClassifier('data/hardcascade_frontalface_default.xml')

faces_data=[]

i=0

#will prompt the user to enter their name
name = input("Enter Your Name: ")


while True:
    #this is to read the video into the webcam
    ret,frame = video.read()

    #to create the frame of the webcam we will use
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3 ,5)
    for (x,y,w,h) in faces:
        crop_img=frame[y:y+h, x:x+w, :]
        resized_img=cv2.resize(crop_img, (50,50))
        if len(faces_data)<=100 and i%10==0:
            faces_data.append(resized_img)
        i=i+1

        #this will put the text on the frame(number of face data) and the rectangle square that will detect the face
        cv2.putText(frame, str(len(faces_data)), (50,50), cv2.FONT_HERSHEY_COMPLEX, 1, (50,50,255), 1)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (50,50,255), 1)
    cv2.imshow("Frame",frame)
    k=cv2.waitKey(1)

    #this will be used to quit the frame using the q key
    if k==ord('q') or len(faces_data)==100:
        break

    #after the user to click the q key it will terminate the frame
video.release()
cv2.destroyAllWindows()

#this will store the faces_data into an array
faces_data=np.asarray(faces_data)
faces_data=faces_data.reshape(100, -1)

#after the face data is complete to 100 the entered name will be stored in names.pkl file
if 'names.pkl' not in os.listdir('data/'):
    names=[name]*100
    with open('data/names.pkl', 'wb') as f:
        pickle.dump(names, f)
else:
    with open('data/names.pkl', 'rb') as f:
        names=pickle.load(f)
    names=names+[name]*100
    with open('data/names.pkl', 'wb') as f:
        pickle.dump(names, f)
        
#after the face data is complete to 100 the scanned face will be stored in faces_data.pkl file
if 'faces_data.pkl' not in os.listdir('data/'):
    with open('data/faces_data.pkl', 'wb') as f:
        pickle.dump(faces_data, f)
else:
    with open('data/faces_data.pkl', 'rb') as f:
        faces=pickle.load(f)
    faces=np.append(faces, faces_data, axis=0)
    with open('data/faces_data.pkl', 'wb') as f:
        pickle.dump(faces, f)