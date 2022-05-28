#!/usr/bin/python3

# Importing Libraries
import rospy
import os
import signal
import module

goal_cancel = False #Boolean variable to know if the first modality is active or not

def UI():

	#Function that receives inputs and sets all the ROS parameters

	global goal_cancel   

	#Printing the UI interface 
	print(module.UI_msg)

	#Getting the modality desired by the user 
	modality = int(input(module.bcolors.YELLOW + 'Choose a modality: \n' + module.bcolors.END)) # Stores the input key

	#Calling the desired modality, if the user chooses the first modality goal_cancel turns to True
	if (modality == 1): 
		goal_cancel = module.mode(modality,goal_cancel)
	else:
		module.mode(modality,goal_cancel)

	#if the the robot is reaching the goal the user can press [0] and cancell it 
	if goal_cancel == True:
		print(module.bcolors.CYAN + module.bcolors.BOLD + "Press [0] to cancel the goal" + module.bcolors.END)
		goal_cancel = False

def main():
	
	#printing the first graphic part of the user interface
	print(module.intro)
	#cycling till ros is running
	while not rospy.is_shutdown():
		#calling the UI function created before in the code
		UI()

#Calling the main function
if __name__ == '__main__':
    main()

