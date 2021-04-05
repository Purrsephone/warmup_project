#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import math

#object oriented class 
class DriveSquare():
	#initalize node and publisher 
	def __init__(self):
		rospy.init_node('drive_square')
		self.turn_around = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
	#make robot drive in square 
	def run(self):
		#repeat movement until shutdown 
		while not rospy.is_shutdown():
			#set linear velocity (moving forward)
			move_forward = Twist()
			move_forward.linear.x = 0.1
			self.turn_around.publish(move_forward)
			rospy.sleep(8)
			#set angular velocity (turning) 
			turn_ninety = Twist()
			turn_ninety.angular.z = 0.9
			self.turn_around.publish(turn_ninety)
			rospy.sleep(1.75)

#runs functions upon execution 		
if __name__ == '__main__':
	rosnode = DriveSquare()
	rosnode.run()
