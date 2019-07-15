import csv
import pigpio
import DC_mtr_mov as motor
import sonar
import math
import time
floormap=[[000,000,000,000,000,000,000,000,000,000,000,000], \
     [000,000,000,000,000,000,000,000,000,000,000,000], \
     [000,000,000,000,000,000,000,000,000,000,000,000], \
     [000,000,000,000,000,000,000,000,000,000,000,000], \
     [000,000,000,000,000,000,000,000,000,000,000,000], \
     [000,000,000,000,000,000,000,000,000,000,000,000], \
     [000,000,000,000,000,000,000,000,000,000,000,000], \
     [000,000,000,000,000,000,000,000,000,000,000,000], \
     [000,000,000,000,000,000,000,000,000,000,000,000], \
     [000,000,000,000,000,000,000,000,000,000,000,000], \
     [000,000,000,000,000,000,000,000,000,000,000,000], \
     [000,000,000,000,000,000,000,000,000,000,000,000], \
     [000,000,000,000,000,000,000,000,000,000,000,000], \
     [000,000,000,000,000,000,000,000,000,000,000,000], \
     [000,000,000,000,000,000,000,000,000,000,000,000], \
     [000,000,000,000,000,000,000,000,000,000,000,000], \
     [000,000,000,000,000,000,000,000,000,000,000,000], \
     [000,000,000,000,000,000,000,000,000,000,000,000], \
     [000,000,000,000,000,000,000,000,000,000,000,000]]

speed=3      # change this to change sample_dist
delay=1      # set it to change the time for which the bot moves forward or backward. Change this to change speed of mapping.
sample_dist=speed*delay
raw=[0,0,0,0,0,0,0,0,0,0,0]
dist=[0,0,0,0,0,0,0,0,0,0,0]

pi=pigpio.pi()

robot_x=0
robot_y=0
point_dir='s'

def collectdata():
    global raw
    global dist
    ratio=500
    for i in range(0,11):
        pi.set_servo_pulsewidth(17,ratio)
        raw[i]=sonar.avgdistance()
        if raw[i]<=20:
            dist[i]=0
        else:
            dist[i]=100
        ratio+=200
    pi.set_servo_pulsewidth(17,0)

#If the mapping algorithm is not working as expected if it is not detecting the obstacle in the front, change the list used in mapping() function from raw[] to dist[]
#and change sample_dist to 10. Then try running this program again.Even if it is not working then, keep changing the sample_dist till you can see the obstacle in the
#front of the map easily, then keep the changes.

def mapping():
    global point_dir
    global robot_x
    global robot_y
    global floormap
    if(point_dir=='s'):
        for i in range(0,11):
            index_y=int((raw[i]*math.cos(math.radians(18*i)))//sample_dist)
            index_y=robot_y-index_y
            index_x=int((raw[i]*math.sin(math.radians(18*i)))//sample_dist)
            index_x=robot_x+index_x
            if (index_x<19) and (index_y<12) and (index_x>=0) and (index_y>=0):
                floormap[index_x][index_y]=999
    elif(point_dir=='n'):
        for i in range(0,11):
            index_y=int((raw[i]*math.cos(math.radians(18*i)))//sample_dist)
            index_y=robot_y+index_y
            index_x=int((raw[i]*math.sin(math.radians(18*i)))//sample_dist)
            index_x=robot_x-index_x
            if (index_x<19) and (index_y<12) and (index_x>=0) and (index_y>=0):
                floormap[index_x][index_y]=999
    elif(point_dir=='e'):
        for i in range(0,11):
            index_x=(int(raw[i]*math.cos(math.radians(18*i)))//sample_dist)
            index_x=robot_x+index_x
            index_y=int((raw[i]*math.sin(math.radians(18*i)))//sample_dist)
            index_y=robot_y+index_y
            if (index_x<19) and (index_y<12) and (index_x>=0) and (index_y>=0):
                floormap[index_x][index_y]=999
    elif(point_dir=='w'):
        for i in range(0,11):
            index_x=int((raw[i]*math.cos(math.radians(18*i)))//sample_dist)
            index_x=robot_x-index_x
            index_y=int((raw[i]*math.sin(math.radians(18*i)))//sample_dist)
            index_y=robot_y-index_y
            if (index_x<19) and (index_y<12) and (index_x>=0) and (index_y>=0):
                floormap[index_x][index_y]=999

def obstacle():
    global point_dir
    global robot_x
    global robot_y
    frontDist=dist[5]*0.4 + dist[6]*0.2 + dist[4]*0.2 + dist[3]*0.1 + dist[7]*0.1
    rightDist=dist[0]*0.5 + dist[1]*0.3 + dist[2]*0.2
    leftDist=dist[10]*0.5 + dist[9]*0.3 + dist[8]*0.2
    if frontDist>30:
            motor.forward()
            time.sleep(delay)
            if(point_dir=='n'):
                robot_x-=1
            elif(point_dir=='s'):
                robot_x+=1
            elif(point_dir=='e'):
                robot_y+=1
            elif(point_dir=='w'):
                robot_y-=1
    else:
        if rightDist>leftDist and leftDist>20:
            motor.right()
            motor.forward()
            time.sleep(delay)
            if(point_dir=='n'):
                point_dir=='e'
                robot_y+=1
            elif(point_dir=='s'):
                point_dir=='w'
                robot_y-=1
            elif(point_dir=='e'):
                point_dir=='s'
                robot_x+=1
            elif(point_dir=='w'):
                point_dir=='n'
                robot_x-=1
        elif rightDist<leftDist and rightDist>20:
            motor.left()
            motor.forward()
            time.sleep(delay)
            if(point_dir=='n'):
                point_dir=='w'
                robot_y-=1
            elif(point_dir=='s'):
                point_dir=='e'
                robot_y+=1
            elif(point_dir=='e'):
                point_dir=='n'
                robot_x-=1
            elif(point_dir=='w'):
                point_dir=='s'
                robot_x+=1
        else:
            motor.back()
            time.sleep(delay)
            motor.right()
            if(point_dir=='n'):
                point_dir=='e'
            elif(point_dir=='s'):
                point_dir=='w'
            elif(point_dir=='e'):
                point_dir=='s'
            elif(point_dir=='w'):
                point_dir=='n'
    motor.stop()

def process():
    collectdata()
    mapping()
    obstacle()

def savemap():          # This function updates the map as a .csv file
    global floormap
    with open('map.csv',mode='w') as file:
        writer=csv.writer(file,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
        for i in range(19):
            writer.writerow(floormap[i])
                


