import cv2
import os
import numpy as np
import csv
dataset_path = 'dataset/'
from mqtt import start
from datetime import datetime
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

images = []
labels = []
labels_name = ['Kiarash','Salman khan','Brad pitt','Will smith', 'Jennifer']

with open('labels.csv') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  
    for row in reader:
        image_path = os.path.join(dataset_path, row[0])
        label = row[1]


        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        image = cv2.resize(image, (960, 1280))
        images.append(image)
        labels.append(int(label))


def read_training_data():
    return np.array(images), np.array(labels)


def train_recognizer():
    images, labels = read_training_data()
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(images, labels)
    return recognizer


recognizer = train_recognizer()


address = "http://192.168.1.113:8080/video"
cap = cv2.VideoCapture(address)  
counter = 0
while True:

    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,255), 2)
        face_roi = gray[y:y+h, x:x+w]


        label, confidence = recognizer.predict(face_roi)
        if confidence <= 30 and label == 1:
            text = f'Person:{labels_name[int(label)-1]} - {confidence}'
            cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            counter += 1
            if counter >= 100:
                print('mqtt message sent...')
                today =  datetime.now()
                cal_time = today.strftime("%Y-%m-%d %H:%M:%S")
                start(f"{labels_name[int(label)-1]}, {cal_time}, 200")
                counter = 0
            
        elif confidence <= 30 and label == 2:
            text = f'Person:{labels_name[int(label)-1]} - {confidence}'
            cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            counter += 1
            if counter >= 100:
                print('mqtt message sent...')
                today =  datetime.now()
                cal_time = today.strftime("%Y-%m-%d %H:%M:%S")
                start(f"{labels_name[int(label)-1]}, {cal_time}, 400")
                counter = 0
        else:
            text = f'Unkown Person'
            cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            

    cv2.imshow('Face Recognition', frame)

  
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
