#!/usr/bin/env python3

# Importing Libraries
from __future__ import print_function
import threading
from sensor_msgs.msg import LaserScan
import roslib; roslib.load_manifest('teleop_twist_keyboard')
import rospy
from geometry_msgs.msg import Twist
import time
from std_srvs.srv import *
import sys, select, termios, tty
import module


#Declaring Boolean variables to know 
#if there's an obstacle near the robot

#True if there's no obstacle on the left , otherwise False
free_left = True      
#True if there's no obstacle on the right , otherwise False
free_right = True     
#True if there's no obstacle on the right , otherwise False
free_front = True  

#Declaring the Dictionary to manage 
#the robot's movement 
moveBindings = {
        'i':(1,0,0,0),  #Straight
        'j':(0,0,0,1),  #Left
        'l':(0,0,0,-1), #Right
        'k':(-1,0,0,0), #Retro
    }

#Declaring the Dictionary to control the velocity
speedBindings={
        'q':(1.1,1.1),
        'z':(.9,.9),
        'w':(1.1,1),
        'x':(.9,1),
        'e':(1,1.1),
        'c':(1,.9),
    }

class PublishThread(threading.Thread):
    def __init__(self, rate):
        super(PublishThread, self).__init__()
        self.publisher = rospy.Publisher('cmd_vel', Twist, queue_size = 1) #Publisher on the 'cmd_vel' topic
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.th = 0.0
        self.speed = 0.0
        self.turn = 0.0
        self.condition = threading.Condition()
        self.done = False

        # Set timeout to None if rate is 0 (causes new_message to wait forever
        # for new data to publish)
        if rate != 0.0:
            self.timeout = 1.0 / rate
        else:
            self.timeout = None

        self.start()

    def wait_for_subscribers(self):
        i = 0
        while not rospy.is_shutdown() and self.publisher.get_num_connections() == 0:
            if i == 4:
                print("Waiting for subscriber to connect to {}".format(self.publisher.name))
            rospy.sleep(0.5)
            i += 1
            i = i % 5
        if rospy.is_shutdown():
            raise Exception("Got shutdown request before subscribers connected")

    def update(self, x, y, z, th, speed, turn):
        self.condition.acquire()
        self.x = x
        self.y = y
        self.z = z
        self.th = th
        self.speed = speed
        self.turn = turn
        # Notify publish thread that we have a new message.
        self.condition.notify()
        self.condition.release()

    def stop(self):
        self.done = True
        self.update(0, 0, 0, 0, 0, 0)
        self.join()

    def STOP(self):
        #Funtion to stop the robot movement, 
        #This function publish on the topic cmd_vel
        twist = Twist()
        twist.linear.x = 0
        twist.linear.y = 0
        twist.linear.z = 0
        twist.angular.x = 0
        twist.angular.y = 0
        twist.angular.z = 0
        # Publish.
        self.publisher.publish(twist)

    def run(self):
        twist = Twist()
        while not self.done:
            self.condition.acquire()
            # Wait for a new message or timeout.
            self.condition.wait(self.timeout)

            # Copy state into twist message.
            twist.linear.x = self.x * self.speed
            twist.linear.y = self.y * self.speed
            twist.linear.z = self.z * self.speed
            twist.angular.x = 0
            twist.angular.y = 0
            twist.angular.z = self.th * self.turn

            self.condition.release()

            # Publish.
            self.publisher.publish(twist)

        # Publish stop message when thread exits.
        twist.linear.x = 0
        twist.linear.y = 0
        twist.linear.z = 0
        twist.angular.x = 0
        twist.angular.y = 0
        twist.angular.z = 0
        self.publisher.publish(twist)


def getKey(key_timeout): # Getting the input key
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], key_timeout)
    if rlist:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings_new)
        key = sys.stdin.read(1) # Get input key from standard input
    else:
        key = ''
    
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings_old)
    return key

def clbk_laser(msg):

    #Callback on the Laser Scanner, sensor to detect obstacles

    global free_left
    global free_right
    global free_front
    # Detecting obstacles on the right of the robot
    right = min(min(msg.ranges[0:143]), 1)  
    # Detecting obstacles in front of the robot    
    front = min(min(msg.ranges[288:431]), 1)  
    # Detecting obstacles on the left of the robot  
    left = min(min(msg.ranges[576:719]), 1)     

    if right != 1.0:        #No obstacles detected on the right at a distance less than 1 meter
        free_right =False
    else:                   #Obstacle detected on the right of the robot
        free_right =True

    if front != 1.0:        #No obstacles detected in the front direction at a distance less than 1 meter
        free_front =False
    else:                   #Obstacle detected in front of the robot
        free_front =True

    if left != 1.0:         #No obstacles detected on the left at a distance less than 1 meter
        free_left =False
    else:                   #Obstacle detected on the left of the robot
        free_left =True

def vels(speed, turn):
    return "currently:\tspeed %s\tturn %s " % (speed,turn)

if __name__=="__main__":

    #Termios Library Settings to disable the print on terminal
    settings_old = termios.tcgetattr(sys.stdin) 
    settings_new = settings_old
    settings_new[3] = settings_new[3] & ~termios.ECHO

    #Initializing the Node
    rospy.init_node('mode_3') 
    #Getting the Ros_parameter mode: modality choosen by the user
    mode_=rospy.get_param("/mode")  
    #Setting the boolean variable to true
    #it represent the state of the modality 
    idle = True 
    
    #Setting some starting parameters
    speed = rospy.get_param("~speed", 0.5)
    turn = rospy.get_param("~turn", 1.0)
    repeat = rospy.get_param("~repeat_rate", 0.0)
    #Timeout set at 0.1 seconds. That means that the user needs to keep the key pushed for moving the robot.
    key_timeout = rospy.get_param("~key_timeout", 0.1)
    #Subscription to the scan topic to recieve informations 
    #about close obstacles
    sub = rospy.Subscriber('/scan', LaserScan, clbk_laser)
    #Starting the timeout to zero
    if key_timeout == 0.0:
        key_timeout = None

    pub_thread = PublishThread(repeat)

    x = 0
    y = 0
    z = 0
    th = 0
    status = 0

    rate = rospy.Rate(5)
    pub_thread.wait_for_subscribers()
    pub_thread.update(x, y, z, th, speed, turn)
    #Initializing a free dictionary
    moveBindings_temp = {}
    #Printing some instructions on screen about the third modality
    print(module.avoid_msg)
    #printig velocity and orientation
    print(vels(speed,turn))
    #Cycling while the modality parameters is set by the user
    while(rospy.has_param("/mode")):
        #Getting the modality set by the user
        mode_=rospy.get_param("/mode")
        #Copying the entire dictionary in order to pop commands without 
        #changing the main dictionary
        moveBindings_temp = moveBindings.copy()
        #Mode 3 choosen by the user
        if mode_ == 3:
            key = getKey(key_timeout)
            #Popping from the copied dictionary the commands that would bring the robot 
            #to an obstacle
            module.pop_dictionary(moveBindings_temp,free_left,free_right,free_front)

            if key in moveBindings_temp.keys():

                x = moveBindings_temp[key][0] 
                y = moveBindings_temp[key][1]
                z = moveBindings_temp[key][2]
                th = moveBindings_temp[key][3]

            elif key in speedBindings.keys():
                speed = speed * speedBindings[key][0]
                turn = turn * speedBindings[key][1]

                print(vels(speed,turn))
                if (status == 14):
                    print(module.avoid_msg)
                status = (status + 1) % 15
            else:
                # Skip updating cmd_vel if key timeout and robot already
                # stopped.
                if key == '' and x == 0 and y == 0 and z == 0 and th == 0:
                    continue
                x = 0
                y = 0
                z = 0
                th = 0
                if (key == '\x03'):
                    break

            pub_thread.update(x, y, z, th, speed, turn)
            #the Modality is not idle anymore
            idle = True

        else:
            #Stopping the robot movement: the user has choosen another modality
            if idle == True:
                pub_thread.STOP() 
                print(module.bcolors.GREEN + module.bcolors.BOLD + "Modality 3 is currently in idle state\n" + module.bcolors.END)
            idle = False

        rate.sleep()


