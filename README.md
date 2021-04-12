# warmup_project

## Drive in a square 
*For this problem, I needed to 1) make the robot move forward in a straight line and 2) make the robot turn 90 degrees 3) repeat 1 & 2. I used the Twist library, which allowed me to set a linear (moving forward) and angular (turning) velocity. I used rospy.sleep to control the timing. I determined the sleep values experimentally. 

*My code follows a simple object oriented template of an init and run function. The init function initializes the node and publisher. The run function moves the robot forward, turns hit approx. 90 degrees, and repeats.

![square](./square.gif)

## Person Follower 

To solve ths problem, i needed to 1) make the robot continuosly follow an object at a fixed distance 2) make the robot face the object 3) deal with an edge case.  I divided the code into a couple different cases based on the starting position of the robot and object. For each case, i adjusted the linear/angular velocity as needed and set a threshhold for closeness. I made small adjustments on a rapid basis, as the robot needs to be reactive to changes in the object's position. 

My code follows a simple object oriented template of an init and run function, plus a proces scan function that does the heavy lifting. The init function initializes the node and publisher. The run function calls spin, which runs process scan on a constant basis. Process scan has 4 cases. First, the case where an object is not in sight, in which case the robot spins with the goal of aligning it's front scanner with the object. Next, the case in which the object is more than a safe distance away, in which case the robot moves toward it linearly. Next, the case where the robot is placed too close to the object, in which case it backs away to a safer distance. Finally, the case in which the robot is at a safe distance and can stop movinig. 


![person-follow](./person-follow.gif) 


## Wall Follower 

To solve this problem, I needed to 1) make the robot find a startng wall 2) OR backup if starting point was too close to a wall 3) keep robot a fixed distance from wall while moving linearly 4) turn corners. I divided the code into a couple different cases based on the relative positions of the robot and wall according to the scanner data. For each case, i adjusted the linear/angular velocity as needed and set a threshhold for closeness. I made small adjustments on a rapid basis, as the robot needs to be reactive to constant movement, drift, and upcoming obstacles. 

My code follows a simple object oriented template of an init and run function, plus a proces scan function that does the heavy lifting. The init function initializes the node and publisher. The run function calls spin, which runs process scan on a constant basis. Process scan has several cases, including 1) backing up after starting too close to the wall 2) reached an appropriate distance 3) constantly adjusting position relative to wall based on front/right side scanner data. The numerical velocity values were determined experimentally through much trial and error. Additionally, I defined the front as the average of the min and max of a small range of degrees near 0 to account for noise. 


![wall-follow](./wall-follow.gif) 


## Challenges 

I had a lot of trouble dealing with noise and imprecision in the robot motion and scan reads. Several of my approaches (see hundreds of lines of commented out code) depended on a level of precision that just wasn't possible. For instance, I tried to turn exactly 45 degrees using a time-based approach or calculate correct distance from corner using trigonometry. Ultimately, I opted for a more-forgiving but less clean approach that relied on constant measurements and small adjustments. I also had trouble determining sensible velocities magnitudes. For the most part, I just used guess and check. 

## Future Work 

If I had more time. I would want to explore my initial ideas to see if they were viable. I think if I had figured out how to navigate imprecise readings, I could have made one of my approahces work, and that the 
