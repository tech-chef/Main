import Recognizer
import sendvid
import ReadFromFile
import sys

count_vid = 0
while True:
    print("Please press q to exit or any other key to continue")
    s = input()
    s = s.strip()
    if s == 'q':
            sys.exit(0)
    face_recognized = Recognizer.recognize()
    if face_recognized:
        continue
    else:
        count_vid = count_vid + 1 
    sendvid.Main_vid(face_recognized, count_vid)
    #Take person to place
    #Take bot back at gate
