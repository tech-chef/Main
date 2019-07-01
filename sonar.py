# This program measures the average distance of an object/obstacle placed in
# front of th ultrasonic hc-sr04 sensor.
import RPi.GPIO as GPIO
import time

max_distance=21
min_distance=3
GPIO.setwarnings(Fal
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(led,GPIO.OUT)

GPIO.output(led,1)
 # setting up the respective GPIO pins for the TRIG and the ECHo pins of the
 # ultrasonic sensor. And an led for detection of the pulse received by the sensor.
TRIG=27
ECHO=22
led=23

def avgdistance():
    avgdistance=0
    # Take the distance readings atleast 3 times using the sensor.
    for i in range(3):
        # sending a pulse
        GPIO.output(TRIG,False)
        time.sleep(0.1)
        GPIO.output(TRIG,True)
        time.sleep(0.00001)
        GPIO.output(TRIG,False)
        # receiving the pusle and calculating the pulse duration for calculating
        # the distance between the obstacle and the sensor.
        while GPIO.input(ECHO)==0:
            GPIO.output(led,False)
        pulse_start=time.time()
        while GPIO.input(ECHO)==1:
            GPIO.output(led,False)
        pulse_end=time.time()
        pulse_duration=pulse_end-pulse_start
        distance=pulse_duration*17150
        distance=round(distance,2)
        avgdistance+=distance
    # Calculating the average distance of the object/obstacle by dividing the
    # distance sum nby 3.
    avgdistance=avgdistance/3
    return avgdistance
