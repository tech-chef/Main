""" This python program contains all the functions neccessary to map the
surroundings of the bot which will be used in the PATH_FOLLOWER.py program."""
import pigpio
import motor
import sonar
import math

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

# set the speed accordingly as it also determines sample_dist which ultimately
# is equivalent to the distance a robot moves before it rescans its surroundings.
# It is the pixel size of the map.
speed=3
delay=1
sample_dist=speed*delay
raw=[0,0,0,0,0,0,0,0,0,0,0]
dist=[0,0,0,0,0,0,0,0,0,0,0]

pi=pigpio.pi()
# The bot starts mapping from (0,0) and pointing in the downward or south direction
# where x is increases as we go down the map
# and y increases as we move right in the map.
robot_x=0
robot_y=0
point_dir='s'

#collectdata similar to the way we are collecting data in the final.py program.
def collectdata():
    global raw
    global dist
    for i in range(0,11):
        ratio=round((1000+18*(i-5)*0.5555),-1)
        pi.set_servo_pulsewidth(17,(500+(200*i)))
        time.sleep(0.01)
        raw[i]=getavgdistance()
        if raw[i]<=20:
            dist[i]=0
        else:
            dist[i]=100
    pi.set_servo_pulsewidth(17,0)

"""This is the actual function that does the mapping.It accesses the global
robot coordinates and the direction the bot is pointing towards.It then uses
the angles in which the data is collected to effectively place obstacles in the
map using trigonometric ratios and then the floormap is updated."""

def mapping(map_):
    global point_dir
    global robot_x
    global robot_y
    if(point_dir=='s'):
        for i in range(0,11):
            index_y=(raw[i]*math.cos(math.radians(18*i)))//sample_dist
            index_y=robot_y-index_y
            index_x=(raw[i]*math.sin(math.radians(18*i)))//sample_dist
            index_x=robot_x+index_x
            if (index_x<19) || (index_y<12) || (index_x>0) || (index_y>0):
                map_[index_x][index_y]=999
    elif(point_dir=='n'):
        for i in range(0,11):
            index_y=(raw[i]*math.cos(math.radians(18*i)))//sample_dist
            index_y=robot_y+index_y
            index_x=(raw[i]*math.sin(math.radians(18*i)))//sample_dist
            index_x=robot_x-index_x
            if (index_x<19) || (index_y<12) || (index_x>0) || (index_y>0):
                map_[index_x][index_y]=999
    elif(point_dir=='e'):
        for i in range(0,11):
            index_x=(raw[i]*math.cos(math.radians(18*i)))//sample_dist
            index_x=robot_x+index_x
            index_y=(raw[i]*math.sin(math.radians(18*i)))//sample_dist
            index_y=robot_y+index_y
            if (index_x<19) || (index_y<12) || (index_x>0) || (index_y>0):
                map_[index_x][index_y]=999
    elif(point_dir=='w'):
        for i in range(0,11):
            index_x=(raw[i]*math.cos(math.radians(18*i)))//sample_dist
            index_x=robot_x-index_x
            index_y=(raw[i]*math.sin(math.radians(18*i)))//sample_dist
            index_y=robot_y-index_y
            if (index_x<19) || (index_y<12) || (index_x>0) || (index_y>0):
                map_[index_x][index_y]=999

# This is the same as the obstacle function in the final.py program and is
# different only by the fact that the robot coordinates are changed each time
# the robot moves from the obstacle accordingly.
def obstacle():
    global point_dir
    global robot_x
    global robot_y
    frontDist=dist[5]*0.4 + dist[6]*0.2 + dist[4]*0.2 + dist[3]*0.1 + dist[7]*0.1
    rightDist=dist[0]*0.5 + dist[1]*0.3 + dist[2]*0.2
    leftDist=dist[10]*0.5 + dist[9]*0.3 + dist[8]*0.2
    if frontDist>30:
            motor.forward()
            time.sleep(1)
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
            time.sleep(1)
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
            time.sleep(1)
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
        else
            motor.stop()
    motor.stop()

# This function returns the updated map.
def process(map_=floormap):
    collectdata()
    mapping(map_)
    obstacle()
    return(map_)

#This function returns the floormap in a readable format.
def printmap(map_):
    msg=''
    for x in range(19):
        for y in range(12):
            if map_[x][y]==0:
                msg+='O  '
            elif map_[x][y]==999:
                msg+='#  '
        msg+='\n'
    print(msg)
