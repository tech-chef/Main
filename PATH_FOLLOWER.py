import DC_mtr_mov as motor
import sonar
import WavefrontPlanner as wave
import mapping
import final
delay=1   # change this according to the dimensions of the map set by the sample_sit in the mapping() program

def mapper():

    floormap = [[000,000,000,000,000,000,000,000,000,000,000,000], \
            [000,000,999,999,999,999,999,999,000,000,000,000], \
            [000,000,999,000,000,000,000,999,999,999,999,999], \
            [000,000,999,000,999,999,000,000,000,000,999,000], \
            [000,999,999,000,000,999,000,000,000,000,999,000], \
            [000,999,000,000,999,999,999,999,999,000,999,000], \
            [000,999,000,000,999,000,000,000,999,000,999,000], \
            [000,999,000,999,999,999,000,000,999,000,999,999], \
            [000,999,000,000,000,000,000,000,999,000,000,000], \
            [000,999,999,999,999,999,999,000,999,000,999,999], \
            [000,000,000,999,000,000,000,000,999,000,999,000], \
            [000,999,999,999,999,999,999,999,999,000,000,000], \
            [000,000,000,000,000,000,000,000,999,000,000,000], \
            [000,999,000,000,000,000,000,000,999,000,000,000], \
            [000,999,000,999,000,999,999,000,999,999,999,000], \
            [000,999,000,999,000,999,000,999,000,000,000,000], \
            [000,999,000,999,000,000,000,000,000,999,000,000], \
            [000,999,999,000,000,999,000,000,000,000,999,000], \
            [000,000,000,999,000,000,000,999,000,999,000,000]]

    for i in range(30):                 '''This loop is controlling the mapping process. During testing comment this out.'''
        mapping.process()
    mapping.savemap()
    with open('map.csv',mode='rt') as f: # This reads the map from the .csv file
        reader=csv.reader(f)
        i=0
        for row in reader:
            s = list(map(int,row))
            if (row):
                floormap[i]=s
                i+=1



def move(path,point_dir):
    global planner
    x1, y1=path[0]
    x2, y2=path[1]
    if(x2>x1):                        # This means the bot needs to move downward in the map
        if (point_dir=='s'):          # This if-else ladder handles the direction in which the sensor is pointing and accordingly moves downward in the map
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
    elif(x2<x1):                    # This means the bot needs to move upward in the map
        if (point_dir=='s'):        # This if-else ladder handles the direction in which the sensor is pointing and accordingly moves upward in the map
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
    elif(y2>y1):                    # This means the bot needs to move rightward in the map
        if(point_dir=='s'):         # This if-else ladder handles the direction in which the sensor is pointing and accordingly moves rightward in the map
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
    elif(y2<y1):                    # This means the bot needs to move leftward in the map
        if(point_dir=='s'):         # This if-else ladder handles the direction in which the sensor is pointing and accordingly moves leftward in the map
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
    time.sleep(delay)
    planner.setRobotPosition(x2,y2)
    motor.stop()

def follower(X1,X2):
    g1,g2 = X1, X2
    planner=wave.waveFrontPlanner(False,floormap)

    point_dir='s'

    r1,r2=planner.robotPosition()
    planner.setGoalPosition(g1,g2)
    while (r1!=g1) and (r2!=g2):            # Move until the robot location and the goal locations are the same.
        flag=final.obstacle()
        if flag==1:                         # This means no obstacle is detected in the path
            path=planner.run(False)         # So bot will move as planned
            move(path,point_dir)
        elif flag==2:                       # This means an obstacle is there in the front and bot can move right as the there is relatively less obstacles to the right of the bot than the left
            motor.right()
            x,y=planner.robotPosition()
            if point_dir=='s':              # We will then update the robot position as per the direction in which the sensor is pointing using this if-else ladder
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
            path=planner.run(False)
            move(path,point_dir)
        elif flag==3:                         # This means an obstacle is there in the front and bot can move left as the there is relatively less obstacles to the right of the bot than the right.
            motor.left()
            x,y=planner.robotPosition()
            if point_dir=='s':                # We will then update the robot position as per the direction in which the sensor is pointing using this if-else ladder
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
            path=planner.run(False)
            move(path,point_dir)
        elif flag==4:
            motor.stop()
            time.sleep(1)
        planner.setRobotPosition(r1,r2)

    print("Goal Location Reached !!")        # Goal location Reached
    time.sleep(10)                           # Robot is idle for 10 seconds after reaching the required goal location.
    planner.setGoalPosition(0,0)             # Set the new goal location to the original location of the top left-most location on the map.

    while (r1!=g1) and (r2!=g2):             # We do the same thing for returning to the originial position too.
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
            path=planner.run(False)
            move(path,point_dir)
        elif flag==4:
            motor.stop()
            time.sleep(1)
        planner.setRobotPosition(r1,r2)

    print("Original Position Reached !!")    # Original position reached.
    time.sleep(5)                            # Robot stays idle for 5 seconds after reaching the original position.
