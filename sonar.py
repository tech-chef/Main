# This program measures the average distance of an object/obstacle placed in
# front of th ultrasonic hc-sr04 sensor.
import RPi.GPIO as GPIO
import time

max_distance=21
min_distance=3
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(led,GPIO.OUT)

GPIO.output(led,1)
 # setting up the respective GPIO pins for the TRIG and the ECHO pins of the
 # Ultrasonic sensor. And an led for detection of the pulse received by the sensor.
TRIG=27
ECHO=22
led=23

def avgdistance():
    MeasuredDistance=0
    # Take the distance readings atleast 3 times using the sensor.
    for i in range(3):
        # sending a short low pulse before to get a clean high
        GPIO.output(TRIG,False)
        time.sleep(0.0001) 
        GPIO.output(TRIG,True) #high pulse
        time.sleep(0.01)
        GPIO.output(TRIG,False)
        pulse_start=time.time() #time when pulse originated
        
        #Receiving the pulse & calculating obstacle distance
        while GPIO.input(ECHO)==0:
            GPIO.output(led,False)
        while GPIO.input(ECHO)==1:
            GPIO.output(led,true) #LED lights up
        pulse_end=time.time() 
        
        pulse_duration=pulse_end-pulse_start
        MeasuredDistance=pulse_duration*17150 
        MeasuredDistance=round(distance,2)
        MeasuredDistance+= MeasuredDistance
        
   #avgdistance = sum/(no. of readings=3)
    avgdistance= MeasuredDistance/3
    return avgdistance
