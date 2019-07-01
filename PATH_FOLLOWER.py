"""This python program combines all the movement program codes to move the bot
successfully from its original position to the goal position. """
import DC_mtr_mov as motor
import sonar
import WavefrontPlanner as wave
import mapper
import final

# First we will map the floor with the bot moving for 20 cycles.
floormap=mapper.process()
for i in range(20):
    flooramp=mapper.process(floormap)

mapper.printmap(floormap)
# We then make a waveFrontPlanner object using the floormap.
planner=wave.waveFrontPlanner(False,floormap)
# We assume that the bot is placed pointing in the downeard/south direction at
# the beginning of it's path
point_dir='s'
# This function is used to move the bot from one path point to the other and
# correspondingly update the robot coordinates and the direction in which the
# bot is pointing towards after the movement.

def move(path,point_dir):
    global planner
    x1,y1=path[0]
    x2,y2=path[1]
    if(x2>x1):
        if (point_dir=='s'):
            motor.forward()
        elif(point_dir=='n'):
            motor.right()
            motor.right()
            motor.forward()
        elif(point_dir=='e'):
            motor.right()
            motor.forward()
        elif(point_dir=='w'):
            motor.left()
            motor.forward()
        point_dir='s'
    elif(x2<x1):
        if (point_dir=='s'):
            motor.right()
            motor.right()
            motor.forward()
        elif(point_dir=='n'):
            motor.forward()
        elif(point_dir=='e'):
            motor.left()
            motor.forward()
        elif(point_dir=='w'):
            motor.right()
            motor.forward()
        point_dir='n'
    elif(y2>y1):
        if(point_dir=='s'):
            motor.left()
            motor.forward()
        elif(point_dir=='n'):
            motor.right()
            motor.forward()
        elif(point_dir=='e'):
            motor.forward()
        elif(point_dir=='w'):
            motor.right()
            motor.right()
            motor.forward()
        point_dir='e'
    elif(y2<y1):
        if(point_dir=='s'):
            motor.right()
            motor.forward()
        elif(point_dir=='n'):
            motor.left()
            motor.forward()
        elif(point_dir=='w'):
            motor.forward()
        elif(point_dir=='e'):
            motor.right()
            motor.right()
            motor.forward()
        point_dir='w'
    time.sleep(1)
    planner.setRobotPosition(x2,y2)

r1,r2=planner.robotPosition()
g1,g2=planner.goalPosition()

# Thsi loop controls how the bot moves from its original position to the it's
# goal position. After each movement the robot coordiantes are updated and if
# the robot moves against its path list as it encounters an unexpected obstacle,
# it again changes its shortest path using the updtaed robot coordinates and
# the loop continues likee this until the bot reaches its goal position.

while (r1!=g1) and (r2!=g2):
    flag=final.obstacle()
    if flag==1:
        path=planner.run(False)
        move(path,point_dir)
    elif flag==2:
        motor.right()
        x,y=planner.robotPosition()
        if point_dir=='s':
            point_dir='w'
            y-=1
        elif point_dir=='n':
            point_dir='e'
            y+=1
        elif point_dir=='e':
            point_dir='s'
            x+=1
        elif point_dir=='w':
            point_dir='n'
            x-=1
        motor.forward()
        time.sleep(1)
        motor.stop()
        planner.setRobotPosition(x,y)
        path=planner.run(False)
        move(path,point_dir)
    elif flag==3:
        motor.left()
        x,y=planner.robotPosition()
        if point_dir=='s':
            point_dir='e'
            y+=1
        elif point_dir=='n':
            point_dir='w'
            y-=1
        elif point_dir=='e':
            point_dir='n'
            x-=1
        elif point_dir=='w':
            point_dir='s'
            x+=1
        motor.forward()
        time.sleep(1)
        motor.stop()
        planner.setRobotPosition(x,y)
        path=planner.run(False)
        move(path,point_dir)
    elif flag==4:
        motor.stop()
        time.sleep(1)
    r1=x
    r2=y
