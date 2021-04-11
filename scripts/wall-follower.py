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
start = True 
turn_45 = False

class WallFollower(object):
	def __init__(self):
		rospy.init_node("follow_wall")
		rospy.Subscriber("/scan", LaserScan, self.process_scan)
		self.twist_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
		lin = Vector3()
		ang = Vector3()
		self.twist = Twist(linear=lin,angular=ang)
	def process_scan(self, data):
		global start 
		global turn_45
		front_min = min(data.ranges[0:5] + data.ranges[-4:])
		front_max = max(data.ranges[0:5] + data.ranges[-4:])
		front = ((front_min + front_max) / 2.0)
		back_min = min(data.ranges[175:183])
		back_max = max(data.ranges[175:183])
		back = ((back_min + back_max) / 2.0)
		left_min = min(data.ranges[85:93])
		left_max = max(data.ranges[85:193])
		left = ((left_min + left_max) / 2.0)
		right_min = min(data.ranges[265:273])
		right_max = max(data.ranges[265:273])
		right = ((right_min + right_max) / 2.0)
		if(start == True):
			if(abs(front - 0.5) <= 0.05):
				self.twist.linear.x = 0
				self.twist_pub.publish(self.twist)
				start = False 
				turn_45 = True 
			err = abs(0.5 - data.ranges[0])
			k_p = 0.1
			self.twist.linear.x = k_p * err
			self.twist_pub.publish(self.twist)
			#print(data.ranges[0])
		'''
		if(turn_45 == True):
			cond1 = abs(right - 0.5) <= 0.01
			if(cond1):
				self.twist.angular.z = 0.0
				self.twist.linear.x = 0.1
				self.twist_pub.publish(self.twist)
				print("forward") 
				turn_45 = False
				start = True 
			else: 
				err = abs(0.5 - right)
				k_p = 0.05
				self.twist.angular.z = k_p * err
				self.twist_pub.publish(self.twist)
		'''
		'''
		if(turn_45 == True):
			cond1 = abs(data.ranges[269] - 0.5) <= 0.05
			cond2 = abs(data.ranges[224] - (0.5 * math.sqrt(2))) <= 0.05
			cond3 = abs(data.ranges[314] - (0.5 * math.sqrt(2))) <= 0.05
			if(cond1 and cond2 and cond3):
				self.twist.angular.z = 0.0
				self.twist.linear.x = 0.1
				self.twist_pub.publish(self.twist)
				print("forward") 
				turn_45 = False
				start = True 
			else: 
				err = abs(0.5 - data.ranges[269])
				k_p = 0.05
				self.twist.angular.z = k_p * err
				self.twist_pub.publish(self.twist)
		'''
			
		'''
			if((data.ranges[0] - 0.5) < -0.04):
				self.twist.linear.x = -0.01
				self.twist_pub.publish(self.twist)
			elif(abs(data.ranges[0] - 0.5) <= 0.04):
				self.twist.linear.x = 0.0
				self.twist_pub.publish(self.twist)
				print("happy")
				start = False 
				turn_45 = True
				#now time for 45 degrees 
			else:
				self.twist.linear.x = 0.1
				self.twist_pub.publish(self.twist)
		'''
		'''
		if(turn_45 == True):
			cond1 = abs(data.ranges[269] - 0.5) <= 0.04
			cond2 = abs(data.ranges[224] - (0.5 * math.sqrt(2))) <= 0.06
			cond3 = abs(data.ranges[314] - (0.5 * math.sqrt(2))) <= 0.06
			if(not cond1):
				print(cond1)
			if(not cond2):
				print(cond2)
			if(not cond3):
				print(cond3)	
			if(cond1 and cond2 and cond3):
				self.twist.angular.z = 0.0
				self.twist.linear.x = 0.1
				self.twist_pub.publish(self.twist)
				print("forward") 
				#tiime to go forward
				turn_45 = False
				start = True 
			else:
				self.twist.angular.z = 0.03
				self.twist_pub.publish(self.twist)
		'''
	
		'''
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
				done = (abs(data.ranges[179] - dist_270) <= 0.1 and (abs(data.ranges[269] - dist_0) <= 0.1) and (data.ranges[0] > 2.5) and (data.ranges[89] > 2.5))
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
					print("less than 0.5")
					self.twist.linear.x = 0.2
					self.twist.angular.z = 0.03
					self.twist_pub.publish(self.twist)
				elif(data.ranges[269] > 0.5):
					print("greater than 0.5") 
					self.twist.linear.x = 0.2
					self.twist.angular.z = -0.03
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
			'''
	
	def run(self):
		rospy.spin()
       	
if __name__ == '__main__':
   	# Declare a node and run it.
  	node = WallFollower()
  	node.run()

