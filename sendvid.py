import numpy as np
import cv2
import time
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os


def recordvid(vidno):
    # The duration in seconds of the video captured
    capture_duration = 5

    # InputCamera

    cap = cv2.VideoCapture(0)

    fourcc = cv2.VideoWriter_fourcc(*'X264')
    out = cv2.VideoWriter('vid.avi', fourcc, 20.0, (640, 480))
    time.sleep(0.1)
    start_time = time.time()
    while(int(time.time() - start_time) < capture_duration):
        ret, frame = cap.read()
        if ret == True:
            out.write(frame)
            cv2.imshow('frame', frame)
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


def send_mail(vidno):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    msg = MIMEMultipart()
    msg["From"] = "techchefofficial@gmail.com"
    msg["To"] = "techchefsecuritas@gmail.com"
    msg["subject"] = "Intruder Alert!"
    message = "An intruder has been noticed at {a}".format(a = dt_string)
    msg.attach(MIMEText(message, 'plain'))
    attachment = open(
        r'/home/pi/Desktop/Main/vid.avi', "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition',
                 "attachment; filename= vid{v}.avi".format(v=str(vidno)))

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(str(msg["From"]), "IITBombay")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(str(msg["From"]), str(msg["To"]), text)

    # terminating the session
    s.quit()


def Main_vid(condition, vidno):
    if not condition:
        recordvid(vidno)
        time.sleep(5)
        send_mail(vidno)
        time.sleep(5)
        os.remove('vid.avi')
