# warmup_project

*For this problem, I needed to 1) make the robot move forward in a straight line and 2) make the robot turn 90 degrees 3) repeat 1 & 2. I used the Twist library, which allowed me to set a linear (moving forward) and angular (turning) velocity. I used rospy.sleep to control the timing. I determined the sleep values experimentally. 

*My code follows a simple object oriented template of an init and run function. The init function initializes the node and publisher. The run function moves the robot forward, turns hit approx. 90 degrees, and repeats.

![Square][./square.gif]