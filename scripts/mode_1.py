#! /usr/bin/env python3

# Importing Libraries
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf import transformations
from std_srvs.srv import *
import module

#Action message
Goal_msg=MoveBaseGoal()	
# Getting the ROS_parameter to enable and disable modalities
mode_ = rospy.get_param('mode')					    
desired_position_x = rospy.get_param('des_pos_x')	# X desired coordinate 
desired_position_y = rospy.get_param('des_pos_y')	# Y desired coordinate 

#Action client
client = actionlib.SimpleActionClient('/move_base', MoveBaseAction)	
#Boolean variable which is true if the robot has achieved the goal
achieved = False 

def action_client():
	#Defining the client function that constructs a SimpleActionClient 
	#in order to open a connection to the ActionServer. 
	#This function sets some parameters of the client 
	global Goal_msg
	global client

	client.wait_for_server()	#Waiting until the connection to the ActionServer is established

	# Setting some goal's fields
	Goal_msg.target_pose.header.frame_id = 'map'			
	Goal_msg.target_pose.header.stamp = rospy.Time.now()	
	Goal_msg.target_pose.pose.orientation.w = 1				


def done_cb(status, result):
	#Callback that gets called on transitions to Done.
	#The callback should take two parameters: the terminal state (as an integer from actionlib_msgs/GoalStatus) and the result.
	#This Function is called after a goal is processed. 
	#It is used to notify the client of the current status of every goal in the system.
	global client
	global achieved

	#Calling the right message for each possible status(int)
	#if status=3 notify that the goal has been achieved, so the boolean variable achieved is set to True 
	if(status==3):
		achieved = module.status(status,achieved)
	else:
		achieved = module.status(status,achieved)

def active_cb():
	#No-parameter callback that gets called on transitions to Active.
	#This function is called before the goal is processed
	print(module.bcolors.BLUE + module.bcolors.BOLD +"Goald processed..."  + module.bcolors.END)

def feedback_cb(feedback):
	#Callback that gets called whenever feedback for this goal is received. Takes one parameter: the feedback.
	
	rospy.loginfo(module.bcolors.BOLD+")\tFeedback Active, the Modality is running..."+module.bcolors.END)

def set_goal(x, y):
	# Creates a goal and sends it to the action server. 
	global Goal_msg
	global client
	Goal_msg.target_pose.pose.position.x = x
	Goal_msg.target_pose.pose.position.y = y
	client.send_goal(Goal_msg, done_cb, active_cb, feedback_cb)

def update_variables():
	#This Function updates the ROS parameters: the current madality and 
	#and the desired position
	global desired_position_x, desired_position_y, mode_
	mode_ = rospy.get_param('mode')
	desired_position_x = rospy.get_param('des_pos_x')
	desired_position_y = rospy.get_param('des_pos_y')

def main():

	global client
	global Goal_msg
	global achieved

	#Initializing the node
	rospy.init_node('mode_1') 
	#Setting goal parameters for the action
	action_client() 

	#Boolean variable that states if the previous state was Idle or not
	idle=False 

	#Printing a description of this modality on screen
	print(module.Desired_pos_msg) 

	#Cycling while the modality parameters is set by the user
	while (rospy.has_param('mode')):
		#Updating the Ros_parameters
		update_variables() 

		#executing the code if and only if the Ros_parameter mode_
		#is set by the user to 1
		if mode_==1: 
			#Setting a new goal_position if the previous state was idle
			if idle == True:	
				print(module.bcolors.GREEN + module.bcolors.UNDERLINE + "The robot is moving towards your desired target" + module.bcolors.END)
				#Setting a new goal_position
				set_goal(desired_position_x, desired_position_y)	
				#The Modality is not idle anymore
				idle = False	

		else:
			#When the modality is not active, I have to check
			#weather the previous goal has been achieved or not.
			if idle == False and achieved == False: 
				print(module.bcolors.BOLD + module.bcolors.GREEN + "Modality 1 is currently in idle state\n" + module.bcolors.END)
				#Sendig a request to server to cancel the goal
				client.cancel_goal()	
				#The modality is again in idle state
				idle = True	
			#If the goal has been achieved by the robot there's no need of
			#canceling the goal
			if achieved == True: 
				idle = True
				achieved = False

#Calling the main function
if __name__ == '__main__':
    main()




	

