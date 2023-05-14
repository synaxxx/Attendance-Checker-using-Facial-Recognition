from sklearn.neighbors import KNeighborsClassifier
from datetime import datetime
from win32com.client import Dispatch

import cv2
import pickle
import numpy as np
import os
import csv
import time

#this will open webcam
video = cv2.VideoCapture(0)

#this will enable the CascaseClassifier funtion from cv2 and get the data from xml file
facedetect = cv2.CascadeClassifier('data/hardcascade_frontalface_default.xml')

#this funtion are used to have a alert message of attendance have been taken when you press the certain button
def speak(str1):
    speak = Dispatch(("SAPI.SpVoice"))
    speak.Speak(str1)

#this will open the given dataset that we have on pickle file named names
with open('data/names.pkl', 'rb') as f:
    LABELS = names = pickle.load(f)

#this will open the given dataset that we have on pickle file named faces_data
with open('data/faces_data.pkl', 'rb') as f:
    FACES = pickle.load(f)

knn = KNeighborsClassifier(n_neighbors = 5)
knn.fit(FACES, LABELS)

#this will be the array that we can use to store the name and time of the attendance
COL_NAMES = ['NAME', 'TIME']

#while true the given code below will be running
while True:
    #this is to read the video into the webcam
    ret, frame = video.read()

    #to create the frame of the webcam we will use
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)

    for(x,y,w,h) in faces:
        crop_img = frame[y:y+h, x:x+w, :]
        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)

        output = knn.predict(resized_img)

        #we can store the given time using the time function and stored it to the ts variable
        ts = time.time()

        #this well be used to set the day - month - year
        date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")

        #this will be used to set the hours - minutes - seconds of the data
        tiemstamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")

        #this will create the file on the attendace folder with the date variables saved as csv file
        exist = os.path.isfile("attendance/attendance_" + date + ".csv")

        #this will be used to set the frame of the cam and put the text on it
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 1)
        cv2.rectangle(frame, (x,y), (x+w,y+h), (50,50,255), 2)
        cv2.rectangle(frame, (x,y-40), (x+w, y), (50,50,255), -1)
        cv2.putText(frame, str(output[0]), (x,y-15), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1, (255,255,255), 1)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (50,50,255), 3)

        #this will create the timestamp of the attendance
        attendance = [str(output[0]), str(tiemstamp)]

    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1)

    #if youe click o it will take the attendance
    if k == ord('o'):
        speak("Attendance taken!")
        time.sleep(5)

        #this will be used to write the attendance to the csv file
        if exist:
            with open("attendance/attendance_" + date + ".csv", "+a") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(attendance)
            csvfile.close()
        else:
            with open("attendance/attendance_" + date + ".csv", "+a") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(COL_NAMES)
                writer.writerow(attendance)
            csvfile.close()
    #if you user click q it will terminate the system
    if k == ord('q'):
        break

video.release()
cv2.destroyAllWindows()