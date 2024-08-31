import cv2
import os
import numpy as np
import csv

dataset_path = 'dataset/'

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

images = []
labels = []
labels_name =['Kiarash','Brad pitt', 'Hugh Jackman']
with open('labels.csv') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  
    for row in reader:
        image_path = os.path.join(dataset_path, row[0])
        label = row[1]

        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        # image = cv2.resize(image, (500, 500))
        images.append(image)
        labels.append(int(label))

def read_training_data():
    return np.array(images), np.array(labels)

def train_recognizer():
    images, labels = read_training_data()
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(images, labels)
    recognizer.save('trained_model.yml')  
    return recognizer

recognizer = train_recognizer()
print("the model trained")
