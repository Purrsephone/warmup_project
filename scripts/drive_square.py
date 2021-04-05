#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import math

class DriveSquare():
	def __init__(self):
		rospy.init_node('drive_square')
		self.turn_around = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
	def run(self):
		while not rospy.is_shutdown():
			move_forward = Twist()
			move_forward.linear.x = 0.1
			self.turn_around.publish(move_forward)
			rospy.sleep(8)
			turn_ninety = Twist()
			turn_ninety.angular.z = 0.9
			self.turn_around.publish(turn_ninety)
			rospy.sleep(1.75)

		
if __name__ == '__main__':
	rosnode = DriveSquare()
	rosnode.run()
