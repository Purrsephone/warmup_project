#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
import math
import copy 

#object oriented person follower code 
class PersonFollower(object):
	#initialize node, publishers, and subscribers for scan/cmd_vel 
	def __init__(self):
		rospy.init_node("follow_person")
		rospy.Subscriber("/scan", LaserScan, self.process_scan)
		self.twist_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
		#initialize linar and angular velocity
		lin = Vector3()
		ang = Vector3()
		self.twist = Twist(linear=lin,angular=ang)
		
	#follow person/object by respondiing to scan data
	def process_scan(self, data):
		#define true front of robot 
		front = data.ranges[0]
		
		#case where object/person is out of range, just spin until in range 
		if(front > 3):
			self.twist.angular.z = 0.2
			self.twist_pub.publish(self.twist)
			
		#case where object/person is more than safe distance away, move toward it linearly 
		elif(front >= 0.5):
			#err = 0.5 - front
			#k_p = 0.1
			self.twist.linear.x = 0.1
			self.twist.angular.z = 0
			self.twist_pub.publish(self.twist)
		
		#case where bot's inital position was too close to object/person, back up 	
		elif(front < 0.2):
			self.twist.linear.x = -0.1
			self.twist_pub.publish(self.twist)
		
		#at safe distance, stop moving 
		else: 
			self.twist.linear.x = 0
			self.twist_pub.publish(self.twist)
			
	#make program run indefinitely 
	def run(self):
		rospy.spin()
  
 #upon execution, run person follower node     	
if __name__ == '__main__':
   	# Declare a node and run it.
  	node = PersonFollower()
  	node.run()
