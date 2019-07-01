L"""This python program controls it's output from the RPI to the L293D IC to
drive the DC motors accordingly as mentioned in the code."""
import RPi.GPIO as GPIO
import time

m11=12
m12=16
m21=20
m22=21
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(m11,GPIO.OUT)
GPIO.setup(m12,GPIO.OUT)
GPIO.setup(m21,GPIO.OUT)
GPIO.setup(m22,GPIO.OUT)

#instruct the bot to stop.
def stop():
    GPIO.output(m11,0)
    GPIO.output(m12,0)
    GPIO.output(m21,0)
    GPIO.output(m22,0)

#instruct the bot to move forward.
def forward():
    GPIO.output(m11,1)
    GPIO.output(m12,0)
    GPIO.output(m21,1)
    GPIO.output(m22,0)

#instruct the bot to move back
def back():
    GPIO.output(m11,0)
    GPIO.output(m12,1)
    GPIO.output(m21,0)
    GPIO.output(m22,1)

#instruct the bot to move right
def right():
    GPIO.output(m11,0)
    GPIO.output(m12,1)
    GPIO.output(m21,1)
    GPIO.output(m22,0)
    time.sleep(0.5)

#instruct the bot to move left
def left():
    GPIO.output(m11,1)
    GPIO.output(m12,0)
    GPIO.output(m21,0)
    GPIO.output(m22,1)
    time.sleep(0.5)
