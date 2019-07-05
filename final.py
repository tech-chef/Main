import DC-mtr_mov as motor
import sonar
import time
import WaveFrontPlanner as wave
import pigpio


raw=[0,0,0,0,0,0,0,0,0,0,0]
dist=[0,0,0,0,0,0,0,0,0,0,0]

pi=pigpio.pi()

'''Collect data of the obstacle placement in front of the bot. raw list stores
information of the average distance of each obstacle in front of the bot
measured by the sensor in the front at various angles. Thee angles being
0,18,36,54 and so on till 180 degrees where the o degrees refers to the right
direction and 180 degrees refers to the left direcction. The dist list stores
100 if the obstacle is atleast more than 20 cm away from the sensor else it
stores 0. The sensor rotates due to the rotation of the servo operated using
pigpio.'''
def collectdata():
     for i in range(0,11):
        ratio=round((1000+18*i*0.5555),-1)
        pi.set_servo_pulsewidth(17,(500+(200*i)))
        time.sleep(0.01)
        raw[i]=getavgdistance()
        if raw[i]<=20:
            dist[i]=0
        else:
            dist[i]=100
    pi.set_servo_pulsewidth(17,0)

'''
def detected_object():
    for i in range(0,11):
        if (dist[i]==0):
            return 1
    return 0

def backoff(left,steps):
    for k in range(steps):
        if left>0:
            left()
        else:
            right()
        time.sleep(0.01)
        back()
        time.sleep(0.01)'''

def obstacle():
    # Data is collected using the sensor atop the servo and the raw and the
    # dist lists are updated accordingly.
    collectdata()
    # frontDist, rightDist and leftDist are calculated using the respective
    # contributions of each dist element accordingly from their respective angles
    # specified in the sonar program while collecting the data.
    frontDist=dist[5]*0.4+ dist[4]*0.2 + dist[6]*0.2 + dist[3]*0.1 + dist[7]*0.1
    rightDist=dist[0]*0.5 + dist[1]*0.3 + dist[2]*0.2
    leftDist=dist[10]*0.5 + dist[9]*0.3 + dist[8]*0.2
    flag=0
    # if no obstacle is their in front of the bot for atleast 30 cm, return
    #  flag as 1
    if frontDist>30:
        flag=1
    else:
        # if obstacle is present on the front side of the bot, and the obstacle on
        # the right is further away from the obstacle on the left, return flag as 2.
        if rightDist>leftDist and leftDist>=20:
            flag=2
        # if obstacle is preseent on the front side of the bot and the obstacle
        # is further away on the left than on the right, return flag as 3.
        elif rightDist<leftDist and rightDist>=20:
            flag=3
        # if the bot is ccovered on all sides by obstacles, return flag as 4.
        else:
            flag=4
    return(flag)
