#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
import math
import copy 

distance = 0.4 

class PersonFollower(object):
	def __init__(self):
		rospy.init_node("follow_person")
		rospy.Subscriber("/scan", LaserScan, self.process_scan)
		self.twist_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
		lin = Vector3()
		ang = Vector3()
		self.twist = Twist(linear=lin,angular=ang)
	def process_scan(self, data):
		list2 = list(copy.deepcopy(data.ranges))		 
		try:
   			while True:
        			list2.remove(0)
		except ValueError:
   	 		pass
		min_dist = (min(list2))
		closest_dist_indx = list2.index(min_dist)
		if (closest_dist_indx >= 90) and (closest_dist_indx <= 270):
			self.twist.angular.z = 0.1
			self.twist_pub.publish(self.twist)
		else:
			if min_dist <= 0.5:
				self.twist.linear.x = 0
				self.twist_pub.publish(self.twist)
				high = (data.ranges[0] <= (min_dist + 0.05))
				low =  (data.ranges[0] >= (min_dist - 0.05))
				if not(high) and not(low): 
					self.twist.angular.z = 0.1
					self.twist_pub.publish(self.twist)
				else:
					self.twist.linear.x = 0
					self.twist.angular.z = 0
					self.twist_pub.publish(self.twist)
			else:	
				if closest_dist_indx < 179:
					self.twist.angular.z = 0.1
				else:
					self.twist.angular.z = -0.1
				self.twist_pub.publish(self.twist)
				self.twist.linear.x = 0.1
				self.twist_pub.publish(self.twist)
	
	def run(self):
		rospy.spin()
       	
if __name__ == '__main__':
   	# Declare a node and run it.
  	node = PersonFollower()
  	node.run()
