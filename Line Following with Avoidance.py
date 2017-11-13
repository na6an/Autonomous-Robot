import packages.initialization
import pioneer3dx as p3dx
p3dx.init()
import cv2
import numpy
## Detect wall
def is_obstacle_detected():
    if min(p3dx.distance[3:5]) > 0.5:
        return False
    else:
        print('Obstacle detected')
        return True
## Follow lane
def follow_line():
    print('Following the line')
    while not is_obstacle_detected():
        try:
            width = p3dx.image.shape[1]
            hsv = cv2.cvtColor(p3dx.image, cv2.COLOR_RGB2HSV)
            lower_cyan = numpy.array([80, 100, 100])
            upper_cyan = numpy.array([100, 255, 255])
            mask = cv2.inRange(hsv, lower_cyan, upper_cyan)

            M = cv2.moments(mask)
            if M['m00'] !=0:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
            else:
                cx, cy = 0, 0
            err = cx - width/2
            linear = 2
            angular = -0.1*err
            move(linear, angular)
        except is_obstacle_detected():
            move(0,0)
## Follow wall
def getWall():
    frontSide = min(p3dx.distance[3:5])
    while frontSide < 1:
        move(0,1)
        frontSide = min(p3dx.distance[3:5])
## Detect lane ##
def is_line_detected():
    width = p3dx.image.shape[1]
    hsv = cv2.cvtColor(p3dx.image, cv2.COLOR_RGB2HSV)
    lower_cyan = numpy.array([80, 100, 100])
    upper_cyan = numpy.array([100, 255, 255])
    mask = cv2.inRange(hsv, lower_cyan, upper_cyan)
    mask[0:80, 0:150] = 0
    M = cv2.moments(mask)
    if M['m00'] != 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        print('Line detected')
        return True
    else:
        cx, cy = 0, 0
        return False
##
def follow_wall():
    print('Following the wall')
    while not is_line_detected():
        p3dx.tilt(-0.47)
        try:
            frontSide = min(p3dx.distance[3:5])
            rightSide = min(p3dx.distance[5:])
            xSpeed = 1
            yawSpeed = 0.5
            if rightSide < 0.5:
                xSpeed  = 0.5
                yawSpeed = 0.2
            else:
                if rightSide > 0.5:
                    xSpeed  = 0.5
                    yawSpeed = -2
            move(xSpeed,yawSpeed)
        except is_line_detected():
            move(0,0)
##
def getLine():
    while is_line_detected():
        xSpeed  = 0.5
        yawSpeed = 0.2
        move(xSpeed,yawSpeed)
    print('Line aligned')
##
# Lower-level functions
def move(V_robot,w_robot):
    r = 0.1953 / 2
    L = 0.33
    w_r = (2 * V_robot + L * w_robot) / (2*r)
    w_l = (2 * V_robot - L * w_robot) / (2*r)
    p3dx.move(w_l, w_r)
##
p3dx.tilt(-0.47)
try:
    while True:
        follow_line()
        getWall()
        follow_wall()
        getLine()
except KeyboardInterrupt:
    move(0,0)
