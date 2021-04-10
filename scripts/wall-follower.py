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
dist_270 = 0
dist_0 = 0

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
		global dist_270 
		global dist_0 
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
				#done = ((data.ranges[179] <= 0.5) and (data.ranges[269] <= 0.5))
				#done = abs(data.ranges[269] 
				done = (abs(data.ranges[179] - dist_270) <= 0.09 and (abs(data.ranges[269] - dist_0) <= 0.09) and (data.ranges[0] > 2.5) and (data.ranges[89] > 2.5))
				if(done == True):
					self.twist.angular.z = 0
					self.twist_pub.publish(self.twist)
					turn_time = False
					at_45 = True 
					print("DONE TURNING") 
				else:
					self.twist.angular.z = 0.1
					self.twist_pub.publish(self.twist)
				
	
			elif(at_45 == True):
				print("along wall")
				print(data.ranges[269])
				if(data.ranges[0] <= 0.5):
					self.twist.linear.x = 0
					self.twist_pub.publish(self.twist)
					dist_270 = data.ranges[269]
					dist_0 = data.ranges[0]
					turn_time = True 
					at_45 = False 
					print("TURN TIME")
				elif(data.ranges[269] == 0.5):
					self.twist.angular.z = 0
					self.twist.linear.x = 0.2
					self.twist_pub.publish(self.twist)
				elif(data.ranges[269] < 0.5):
					self.twist.linear.x = 0.2
					self.twist.angular.z = 0.02
					self.twist_pub.publish(self.twist)
				elif(data.ranges[269] > 0.5):
					self.twist.linear.x = 0.2
					self.twist.angular.z = -0.02
					self.twist_pub.publish(self.twist)
				else:
					prini("BAD")
				#else: 
					#self.twist.angular.z = 0
					#self.twist.linear.x = 0.2
					#self.twist_pub.publish(self.twist)
			else:
				if min_dist <= 0.5:
					self.twist.linear.x = 0
					self.twist_pub.publish(self.twist)
					high = (data.ranges[44] <= (min_dist + 0.05))
					low =  (data.ranges[44] >= (min_dist - 0.05))
					if not(high) and not(low): 
						self.twist.angular.z = 0.1
						self.twist_pub.publish(self.twist)
					else:
						ret_bool = True 
						if not (abs(data.ranges[269] - min_dist) <= 0.005):
								#print("LETS GO") 
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

