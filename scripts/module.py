#! /usr/bin/env python

import rospy

# Defining colors
class bcolors:
	YELLOW = '\033[33m'
	BLUE = '\033[94m'
	CYAN = '\033[96m'
	GREEN = '\033[92m'
	RED = '\033[91m'
	END = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m' 


# User-Interface print
intro = R""" 
	 _____ _    _____       _     
	|  |  |_|  |   | |___ _| |___ 
	|  |  | |  | | | | . | . | -_|
	|_____|_|  |_|___|___|___|___|

""" + bcolors.BOLD + """ User Interface 
CHOOSE ONE OF THE FOLLOWING DRIVING MODALITIES:
"""
# Menu message showing the three modalities
UI_msg = """ """ + bcolors.BOLD + """ 
 [1] """ + bcolors.BOLD+ bcolors.GREEN +""" Autonomous Drive """ + bcolors.END + """ 
""" + bcolors.BOLD + """ [2] """ + bcolors.BOLD + bcolors.GREEN + """ Free Drive """ + bcolors.END +"""
""" + bcolors.BOLD + """ [3] """ + bcolors.BOLD + bcolors.GREEN + """ Driver Assistent """ + bcolors.END + """
""" + bcolors.BOLD + """ [4] """ + bcolors.BOLD + bcolors.RED + """ Terminate the Simulation
"""

# Autonomous Drive print
Desired_pos_msg = R""" 
	 _____     _                                   
	|  _  |_ _| |_ ___ ___ ___ _____ ___ _ _ ___   
	|     | | |  _| . |   | . |     | . | | |_ -|  
	|__|__|___|_| |___|_|_|___|_|_|_|___|___|___|  
             ____      _                
            |    \ ___|_|_ _ ___               
            |  |  |  _| | | | -_|              
            |____/|_| |_|\_/|___|              

""" + bcolors.BOLD + """
	The Robot will autonomously reach a desired position:
	Set the Goal postion in the UI terminal choosing the first modality
	The 'move_base' ActionServer and the Dijkstra's path algorithm
	will do the rest!!
""" +bcolors.END + """
"""

# Defining the function related to every modality
# each function will be called whenever the user select the corresponding key
# in the user_interface node

def mode_0():
	#by setting the mode to 0 the user will normaly do nothing, but this key will cancell the goal position
	#when the first modality is running
	rospy.set_param('mode', 0)	
	print(bcolors.GREEN + "No modality running, Select [1] [2] or [3]" + bcolors.END) # Sysytem in idle state
	

def mode_1(goal_cancel):

	#Setting initially the mode to zero, in order to change the antecedent goal
	rospy.set_param('mode', 0)  
	print(bcolors.GREEN + bcolors.BOLD + "Modality 1 is Running...")
	print(bcolors.BLUE + bcolors.BOLD + "Choose a goal position!" + bcolors.END)

	#The user inputs the desired goal position
	des_x_input = float(input(bcolors.UNDERLINE + bcolors.BLUE +"X position: " + bcolors.END))
	des_y_input = float(input(bcolors.UNDERLINE + bcolors.BLUE +"Y position: " + bcolors.END))

	print(bcolors.GREEN + bcolors.UNDERLINE + "OOKEYY Let's go to position x= " + str(des_x_input) + " y= " + str(des_y_input) + bcolors.END)	

	#Setting the ros_parameters which represent the desired selected goal
	rospy.set_param('des_pos_x', des_x_input) 
	rospy.set_param('des_pos_y', des_y_input) 
	#setting the Modality to 1
	rospy.set_param('mode', 1) 

	#boolean flag to make the user able to cancell the goal while 
	#the  robot is running 
	goal_cancel=True

	return goal_cancel

def mode_2():
	#Setting the mode parameter to two
	rospy.set_param('mode', 2) 
	print(bcolors.GREEN + bcolors.BOLD + "Modality 2 is Running..." + bcolors.END)
	print(bcolors.BOLD + bcolors.YELLOW + "'Free_Drive' Window to control the robot" + bcolors.END)

def mode_3():
	#Setting the mode parameter to three
	rospy.set_param('mode', 3) 
	print(bcolors.GREEN + bcolors.BOLD + "Modality 3 is Running..." + bcolors.END)
	print(bcolors.BOLD + bcolors.BLUE + "'Driver_Assistent' Window to control the robot" + bcolors.END)
	

def mode_4():
	#Terminate the all the processs using a SIGKILL signal
	print(bcolors.RED + bcolors.BOLD + "Exiting..." + bcolors.END)
	os.kill(os.getpid(), signal.SIGKILL) # Kill the current process

def default():
	#Default function called whenever the user choose a wrong iput
	print(bcolors.RED + bcolors.BOLD + "Wrong key! Use the shown modalitys " + bcolors.END)

#Dictionary used to call the right modality function

switcher = {

    0: mode_0,

    1: mode_1,

    2: mode_2,

    3: mode_3,

    4: mode_4

    }

def mode(mode,goal_cancel):
	#function that manage the input modality and the right mode_function to call
	#When mode 1 is call the goal_cancel variable is pass to the function
	function = switcher.get(mode, default)
	if(mode == 1):
		return function(goal_cancel)
	else:
		return function()

#Defining all the functions called by the action server in the first modality
#When ever a new status is read by the client 

def status_2():
	#Goal cancel
	print(bcolors.RED + "CANCEL REQUEST RECIEVED! Stopping Execution...." + bcolors.END)
	return
def status_3(achieved):
	#Goal achieved, boolean variable managed 
	print(bcolors.GREEN + bcolors.UNDERLINE + bcolors.BOLD + "GOAL ACHIEVED!" + bcolors.END)
	achieved = True
	return achieved
def status_4():
	#Timeout
	print(bcolors.RED + "TIMEOUT! Desired poition not reachable. GOAL CANCELED."  + bcolors.END)
	return
def status_5():
	#Goal Rejected 
	print(bcolors.RED + "GOAL REJECTED" + bcolors.END)
	return

def status_6():
	print(bcolors.RED + "goal received a cancel request but the server has not yet completed execution"+ bcolors.END)
	return

def status_8():
	print(bcolors.RED + "goal received a cancel request, cancelled succesfully."+ bcolors.END)
	return

def no_status():
	#Wrong status value
	print(bcolors.RED + "wrong status value"+ bcolors.END)

#Dictionary usefull to call the right function

switch_status = {

    2: status_2,

    3: status_3,

    4: status_4,

    5: status_5,

    6: status_6,

    8: status_8,

    }

def status(status,achieved):
	#Function to call the right status function
	#Boolean variable achieved managed if the status is equal to three
	function = switch_status.get(status, no_status)
	if(status==3):
		return function(achieved)
	else:
		return function()

#Driver Assistant print 
avoid_msg = R"""
	 ____      _                _____         _     _           _   
	|    \ ___|_|_ _ ___ ___   |  _  |___ ___|_|___| |_ ___ ___| |_ 
	|  |  |  _| | | | -_|  _|  |     |_ -|_ -| |_ -|  _| -_|   |  _|
	|____/|_| |_|\_/|___|_|    |__|__|___|___|_|___|_| |___|_|_|_| 
""" + bcolors.BOLD +"""
Reading from the keyboard.... 
""" + bcolors.END + bcolors.BLUE + bcolors.BOLD + """
[i] go straight    
[j] turn left
[l] turn right
[k] go backwards
""" + bcolors.YELLOW + bcolors.BOLD +"""
[q]/[z] : increase/decrease max speeds 
[w]/[x] : increase/decrease linear speed 
[e]/[c] : increase/decrease angular speed 
""" + bcolors.END + """
"""

#Free Drive print
teleop_msg = R"""
	 _____                ____      _         
	|   __|___ ___ ___   |    \ ___|_|_ _ ___ 
	|   __|  _| -_| -_|  |  |  |  _| | | | -_|
	|__|  |_| |___|___|  |____/|_| |_|\_/|___ 
""" + bcolors.END + bcolors.BLUE + bcolors.BOLD + """
Moving around:
   u    i    o
   j    k    l
   m    ,    .
""" + bcolors.END + bcolors.YELLOW + bcolors.BOLD + """ For Holonomic mode (strafing), hold down the shift key:
   U    I    O
   J    K    L
   M    <    >

t : up (+z)
b : down (-z)
""" + bcolors.END + """ anything else : stop """ + bcolors.YELLOW + bcolors.BOLD +"""
q/z : increase/decrease max speeds by 10%
w/x : increase/decrease only linear speed by 10%
e/c : increase/decrease only angular speed by 10% """+ bcolors.END +""" 
"""


def pop_dictionary(dictionary,free_left,free_right,free_front):

# Function that removes commands from the dictionary when an obstacle is detected. In this way, when an obstacle is detected,
# the movement in that direction is disabled
    
    #Here all the following cases

    if not free_front and not free_right and not free_left: # Obstacles in every direction
        # Disable all the three commands 
        popped1 = dictionary.pop('i')   # Disable the front movement 
        popped2 = dictionary.pop('j')   # Disable the left turn movement   
        popped3 = dictionary.pop('l')   # Disable the right turn movement 
        print(bcolors.RED + bcolors.BOLD +"Key 'i' disabled" + bcolors.END , end="\r")
        print(bcolors.RED + bcolors.BOLD + "Key 'j' disabled" + bcolors.END , end="\r")
        print(bcolors.RED + bcolors.BOLD + "Key 'l' disabled" + bcolors.END , end="\r")
    elif not free_left and not free_front and free_right: # Obstacles on the left and in the front direction, so right direction is free
        popped1 = dictionary.pop('i')   # Disable the front movement 
        popped2 = dictionary.pop('j')   # Disable the left turn movement
        print(bcolors.RED + bcolors.BOLD + "Key 'i' disabled" + bcolors.END , end="\r")
        print(bcolors.RED + bcolors.BOLD + "Key 'j' disabled" + bcolors.END , end="\r")
    elif free_left and not free_front and not free_right: # Obstacles on the right and in the front direction, so left direction is free
        popped1 = dictionary.pop('i')   # Disable the front movement 
        popped2 = dictionary.pop('l')   # Disable the right turn movement
        print(bcolors.RED + bcolors.BOLD + "Key 'i' disabled" + bcolors.END , end="\r")
        print(bcolors.RED + bcolors.BOLD + "Key 'l' disabled" + bcolors.END , end="\r")
    elif not free_left and free_front and not free_right: # Obstacles on the right and on the left, so the front direction is free
        popped1 = dictionary.pop('l')   # Disable the right turn movement
        popped2 = dictionary.pop('j')   # Disable the left turn movement
        print(bcolors.RED + bcolors.BOLD + "Key 'l' disabled" + bcolors.END , end="\r")
        print(bcolors.RED + bcolors.BOLD + "Key 'j' disabled" + bcolors.END , end="\r")
    elif free_left and not free_front and free_right: # Obstacles only in the front direction, so the left and right directions are free
        popped1 = dictionary.pop('i')   # Disable the front movement 
        print(bcolors.RED + bcolors.BOLD + "Key 'i' disabled" + bcolors.END , end="\r")
    elif not free_left and free_front and free_right: # Obstacles only in the left direction, so the front and right directions are free
        popped1 = dictionary.pop('j')   # Disable the left turn movement 
        print(bcolors.RED + bcolors.BOLD + "Key 'j' disabled" + bcolors.END , end="\r")
    elif free_left and free_front and not free_right: # Obstacles only in the right direction, so the front and left directions are free
        popped1 = dictionary.pop('l')   # Disable the right turn movement 
        print(bcolors.RED + bcolors.BOLD + "Key 'l' disabled" + bcolors.END , end="\r")

