#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
import math
import copy 

distance = 0.4 
at_45 = False 
turn_time = False 

class WallFollower(object):
	def __init__(self):
		rospy.init_node("follow_wall")
		rospy.Subscriber("/scan", LaserScan, self.process_scan)
		self.twist_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
		lin = Vector3()
		ang = Vector3()
		self.twist = Twist(linear=lin,angular=ang)
	def process_scan(self, data):
		global at_45 
		global turn_time
		list2 = list(copy.deepcopy(data.ranges))		 
		try:
   			while True:
        			list2.remove(0)
		except ValueError:
   	 		pass
		min_dist = (min(list2))
		max_dist_zero = max(data.ranges)
		closest_dist_indx = list2.index(min_dist)
		if False:
			pass
		##now, need to deal with corners, then just repeat behavior 
			
		else: 
			#if (closest_dist_indx >= 90) and (closest_dist_indx <= 270):
				#self.twist.angular.z = 0.1
				#self.twist_pub.publish(self.twist)
			if(turn_time == True):
				done = ((data.ranges[179] <= 0.5) and (data.ranges[269] <= 0.5))
				if(done == True):
					self.twist.angular.z = 0
					self.twist_pub.publish(self.twist)
					turn_time = False
					at_45 = True 
				else:
					self.twist.angular.z = 0.1
					self.twist_pub.publish(self.twist)
				
	
			elif(at_45 == True):
				if(data.ranges[0] <= data.ranges[269]):
					self.twist.linear.x = 0
					self.twist_pub.publish(self.twist)
					turn_time = True 
					at_45 = False 
					print("MEOW")
				else: 
					self.twist.angular.z = 0
					self.twist.linear.x = 0.2
					self.twist_pub.publish(self.twist)
			else:
				if min_dist <= 0.6:
					self.twist.linear.x = 0
					self.twist_pub.publish(self.twist)
					high = (data.ranges[44] <= (min_dist + 0.05))
					low =  (data.ranges[44] >= (min_dist - 0.05))
					if not(high) and not(low): 
						self.twist.angular.z = 0.1
						self.twist_pub.publish(self.twist)
					else:
						ret_bool = True 
						for x in range(259, 289):
							if not (abs(data.ranges[x] - data.ranges[269]) <= 0.02):
								ret_bool = False 
						if(ret_bool == True):
							at_45 = True 
							self.twist.angular.z = 0
							self.twist.linear.x = 0.2
							self.twist_pub.publish(self.twist)
						else: 
							self.twist.angular.z = 0.1
							self.twist_pub.publish(self.twist)
						#self.twist.linear.x = 0
						#self.twist.angular.z = 0
						#self.twist_pub.publish(self.twist)
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
  	node = WallFollower()
  	node.run()

