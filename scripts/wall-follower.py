#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
import math
import copy 

#object oriented wall follower code 
class WallFollower(object):
	#initialize node, publishers, and subscribers for scan/cmd_vel 
	def __init__(self):
		rospy.init_node("follow_wall")
		rospy.Subscriber("/scan", LaserScan, self.process_scan)
		self.twist_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
		#initialize linar and angular velocity 
		lin = Vector3()
		ang = Vector3()
		self.twist = Twist(linear=lin,angular=ang)
		
	#follow walls of a room by respondiing to scan data
	def process_scan(self, data):
	
		#get dist from front of bot, account for noise by 
		#using avr. of max/min of small range of front angles 
		front_min = min(data.ranges[0:2] + data.ranges[-2:])
		front_max = max(data.ranges[0:2] + data.ranges[-2:])
		front = ((front_min + front_max) / 2.0)
		
		#get value of distance from right front 
		#(359 + 269)/2 = 314
		#avr to account for noise 
		right_front_min = min(data.ranges[312:316])
		right_front_max = max(data.ranges[312:316])
		right_front = ((right_front_min + right_front_max) / 2.0)
		
		#started too close to wall, back up 	
		if(front < 0.2):
			self.twist.linear.x = -0.6
			self.twist_pub.publish(self.twist)
			
		#out of range, need to turn around 
		if((front < 0.9) and (front >= 0.2)  or right_front < 0.6): 
			self.twist.angular.z = 0.3
			self.twist.linear.x = 0.1
			self.twist_pub.publish(self.twist)
			
		#special case of out of range 
		elif(front < 1.2): 
			self.twist.angular.z = 0.3
			self.twist.linear.z = 0.3
			self.twist_pub.publish(self.twist)
			
		#too far from wall, move toward 	
		if(front >= 1.2):
			if(right_front > 0.6):
				self.twist.angular.z = -0.1
				self.twist.linear.x = 0.1
				self.twist_pub.publish(self.twist)
			else:
				self.twist.angular.z = 0.3
				self.twist.linear.x = 0.0
				self.twist_pub.publish(self.twist)
		
		#have reached an appropriate distance from wall, reset linear to 0 	
		else:
			self.twist.linear.x = 0.0
			self.twist_pub.publish(self.twist)

	#make program run indefinitely 
	def run(self):
		rospy.spin()
		
#upon executioni, run wall follower node 	
if __name__ == '__main__':
   	# Declare a node and run it.
  	node = WallFollower()
  	node.run()



#all the code that did not work :( 
'''
distance = 0.4 
at_45 = False 
turn_time = False 
dist_270 = 0
dist_0 = 0
start = True 
turn_45 = False
true_front = 0 
turn_time = False 
true_back = 0
true_left = 0 
true_right = 0 
going_straight = False 
curr_angle = 0 
des_angle = ((90 * 2 * math.pi)/360.0)
t1 = 0 
t0 = 0 
gone_once = False 
correction = False 
'''
'''
		global start 
		global turn_45 
		global curr_angle 
		global t1 
		global t0 
		global correction
		global gone_once 
		right_min = min(data.ranges[265:273])
		right_max = max(data.ranges[265:273])
		right = ((right_min + right_max) / 2.0)
		right_bot_min =  min(data.ranges[220:228])
		right_bot_max =  max(data.ranges[220:228])
		right_bot = ((right_bot_min + right_bot_max) / 2.0)
		right_top_min =  min(data.ranges[310:318])
		right_top_max =  max(data.ranges[310:318])
		right_top = ((right_top_min + right_top_max) / 2.0)
		front_min = min(data.ranges[0:5] + data.ranges[-4:])
		front_max = max(data.ranges[0:5] + data.ranges[-4:])
		front = ((front_min + front_max) / 2.0)
		if(start == True):
			print("ang vel:")
			print(self.twist.angular.z)
			curr_angle = 0 
			print("start")
		#fix vertical 
			if(abs(front - 0.8) <= 0.08):
				self.twist.linear.x = 0
				self.twist_pub.publish(self.twist)
				start = False 
				turn_45 = True 
				t0 = rospy.Time.now().to_sec()
				#true_front = front 
				#true_back = back 
				#true_left = left 
				#true_right = right 
			else: 
				err = abs(0.5 - front)
				k_p = 0.1
				self.twist.linear.x = k_p * err
				self.twist_pub.publish(self.twist)
		if turn_45 == True:
			print("turn") 
			if(gone_once == False):
				if(curr_angle < des_angle):
					self.twist.angular.z = 0.05
					self.twist_pub.publish(self.twist)
					t1 = rospy.Time.now().to_sec()
					curr_angle = 0.05 * (t1 - t0)
				else: 
					turn_45 = False 
					correction = True 
					self.twist.angular.z = 0.0
					self.twist_pub.publish(self.twist)
			else: 
				#right 
				cond1 = (right - 0.8) <= 0.08 
				#back 
				cond2 = (back - 0.8) <= 0.08 
				if(cond1 and cond2):
					self.twist.angular.z = 0.0
					self.twist_pub.publish(self.twist)
					turn_45 = False 
					correction = True 
				else: 
					self.twist.angular.z = 0.05 
					self.twist_pub.publish(self.twist)
				
		if(correction == True): 
			if(right_top < right):
				self.twist.angular.z = 0.05
				self.twist_pub.publish(self.twist)
				print("top")
			if(right_bot < right):
				self.twist.angular.z = -0.05
				self.twist_pub.publish(self.twist) 
				#need to tilt 
				print("bot")
			else:
				self.twist.angular.z = 0
				self.twist_pub.publish(self.twist)
				correction = False 
				gone_once - True
				start = True 
				print("we sleep") 
				rospy.sleep(1)
			
		'''
			
	
	
'''
		global start 
		global turn_45
		global true_front
		global true_back 
		global true_left 
		global true_right
		global turn_time
		global going_straight 
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
		right_bot_min =  min(data.ranges[220:228])
		right_bot_max =  max(data.ranges[220:228])
		right_bot = ((right_bot_min + right_bot_max) / 2.0)
		right_top_min =  min(data.ranges[310:318])
		right_top_max =  max(data.ranges[310:318])
		right_top = ((right_top_min + right_top_max) / 2.0)
		
		if(start == True):
			#print(abs(front - 1.0)) 
			#print("HERE")
			if(abs(front - 1.0) <= 0.1):
				self.twist.linear.x = 0
				self.twist_pub.publish(self.twist)
				start = False 
				turn_45 = True 
				true_front = front 
				true_back = back 
				true_left = left 
				true_right = right 
			else: 
				err = abs(0.5 - front)
				k_p = 0.1
				self.twist.linear.x = k_p * err
				self.twist_pub.publish(self.twist)
		if(turn_45 == True):
			print(true_front)
			print(true_back)
			print(true_left)
			print(true_right) 
			cond1 = abs(true_left - front) <= 0.1
			cond2 = abs(true_right - back) <= 0.1
			cond3 = abs(true_back - left) <= 0.1
			cond4 = (right - true_front <= 0.05)
			if(true_left == "inf"):
				print("NFINITY MOTHFUCKA") 
			if(cond4): 
			#if(cond1 and cond2 and cond3 and cond4):
				self.twist.angular.z = 0
				self.twist_pub.publish(self.twist)
				turn_45 = False
				#start = True
				going_straight = True 
			else:
				self.twist.angular.z = 0.05
				self.twist_pub.publish(self.twist)
			#print(front)
			#print("\n")
			#print(data.ranges[179])
		if(going_straight == True):
			self.twist.linear.x = 0.1
			self.twist_pub.publish(self.twist)
			if((right - 1.0) > 0.05):
				self.twist.angular.z = 0.05
				self.twist_pub.publish(self.twist)
			if((right - 1.0) < -0.05):
				self.twist.angular.z = -0.05
				self.twist_pub.publish(self.twist)
		'''
			
'''

		elif(turn_45 == True):
				print("along wall")
				print(data.ranges[269])
				if(data.ranges[0] <= 0.5):
					self.twist.linear.x = 0
					self.twist_pub.publish(self.twist)
					dist_270 = data.ranges[269]
					dist_0 = data.ranges[0]
					turn_time = True 
					turn_45 = False 
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
		if(turn_time == True):
			#done = ((data.ranges[179] <= 0.5) and (data.ranges[269] <= 0.5))
			#done = abs(data.ranges[269] 
			done = (abs(data.ranges[179] - dist_270) <= 0.1 and (abs(data.ranges[269] - dist_0) <= 0.1) and (data.ranges[0] > 2.5) and (data.ranges[89] > 2.5))
			if(done == True):
				self.twist.angular.z = 0
				self.twist_pub.publish(self.twist)
				turn_time = False
				turn_45 = True 
				print("DONE TURNING") 
			else:
				self.twist.angular.z = 0.1
				self.twist_pub.publish(self.twist)
				'''
				
'''
		if(turn_45 == True):
			min_dist = (min(data.ranges))
			print("min dist:") 
			print(min_dist) 
			print(right - min_dist)
			print(abs(right_top - (min_dist * math.sqrt(2))))
			cond1 = (right - min_dist) <= 0.08
			cond2 = abs(right_bot - (min_dist * math.sqrt(2))) <= 0.08
			cond3 = abs(right_top - (min_dist * math.sqrt(2))) <= 0.08
			#if(not cond1):
				#print(cond1)
			#if(not cond2):
				#print(cond2)
			#if(not cond3):
			if(cond3):
				print(cond3)	
			if(cond1):
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
