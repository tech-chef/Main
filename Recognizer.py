import cv2
import numpy as np
import os
import time
import csv

def recognize():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    font = cv2.FONT_HERSHEY_SIMPLEX

    any_face_detected = False
    any_face_recognized = False
    security_threat = False
    filename = r'names.csv'

    # names related to ids: example ==> Harshit : 1, Shaan : 2, etc.
    names = ['none']
    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        count_row = 0
        for row in csvreader:
            if count_row == 0:
                header = row
                count_row = count_row + 1
                continue
            names.append(str(row)[2:-2])

    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video widht
    cam.set(4, 480) # set video height

    # Define min window size to be recognized as a face
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)
    start_time = time.time()


    while True:
        ret, img =cam.read()
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
           )

        for (x,y,w,h) in faces:
            any_face_detected = True
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

            # Check if confidence is less them 100 ==> "0" is perfect match
            if (confidence < 100):
                any_face_recognized = True
                id = names[id]
                confidence = "  {0}%".format(round(100 - confidence))
                print("Welcome " + id + '\n' )
                break
            else:
                any_face_recognized = False
                id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))

            cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
            cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)



        cv2.imshow('camera',img)
        security_threat = time.time() - start_time > 3.0 and any_face_detected == True and any_face_recognized == False


        k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video if code does not work
        if k == 27 or any_face_recognized or security_threat:
            break

    # Do a bit of cleanup
    cam.release()
    cv2.destroyAllWindows()
    if any_face_recognized == True:
        print("Welcome " + id )
    else:
        print("Intruder Alert")
    return any_face_recognized
