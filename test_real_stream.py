import cv2
from mqtt import start
from datetime import datetime

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trained_model.yml') 

labels_name =['MeganFox', 'TomCruise', 'WillSmith']

address = "http://192.168.1.113:8080/video"
cap = cv2.VideoCapture(address)
counter1 = 0
counter2 = 0

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 255), 2)
        face_roi = gray[y:y+h, x:x+w]

        label, confidence = recognizer.predict(face_roi)
        
        # ##########
        if confidence <= 65 and (label == 1 or label==3):
            text = f'Person:{labels_name[int(label)-1]}-{confidence}'
            cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            counter1 += 1
            if counter1 >= 100:
                print('mqtt message sent...')
                today =  datetime.now()
                cal_time = today.strftime("%Y-%m-%d %H:%M:%S")
                start(f"{labels_name[int(label)-1]}, {cal_time}, 200")
                counter1 = 0
                
        # ##########  
        elif confidence <= 65 and (label == 2 ):
            text = f'Person:{labels_name[int(label)-1]}-{confidence}'
            cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            counter2 += 1
            if counter2 >= 100:
                print('mqtt message sent...')
                today =  datetime.now()
                cal_time = today.strftime("%Y-%m-%d %H:%M:%S")
                start(f"{labels_name[int(label)-1]}, {cal_time}, 400")
                counter2 = 0
                
        # ##########        
        else:
            text = f'Unknown Person'
            cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (128, 128, 128), 1, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (128, 128, 128), 2)
            
    cv2.imshow('Face Recognition', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
