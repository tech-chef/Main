import keyboard
import Recognizer
import sendvid
import ReadFromFile
import
import
import

count_vid = 0
while True:
    if keyboard.is_pressed('Esc'):
            print("\nExiting.")
            sys.exit(0)
    face_recognized = Recognizer.recognize()
    count_vid = count_vid + 1 if not face_recognized else pass
    if face_recognized:
        continue
    sendvid.Main_vid(face_recognized, count_vid)
    pos = ReadFromFile.compare_file()
    #Take person to place
    #Take bot back at gate
