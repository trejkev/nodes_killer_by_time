#! /usr/bin/env python

__author__      = "Kevin Trejos Vargas"
__email__       = "kevin.trejosvargas@ucr.ac.cr"

"""
    Description:
        Node to save the map and kill the session when the turtlebot3_nav node
        disappears. But before doing so, it will save the map into
        /Documents/Maps
"""

import rospy                                                                                  # Needed for ros and python interaction
import os                                                                                     # Needed to interact with ros terminal
import time
from datetime import datetime

#Global variables
ReviewRate  = 1                                                                               # Rate to check the existence of the flagger node, in Hz
Timer_sec   = 240                                                                             # How long, in seconds, the session will stay up
warmupTime  = 5                                                                               # Warmup time needed to let ROS lauch all the nodes (may vary depending on the speed of the computer)

rospy.init_node('time_nodes_killer')                                                          # Session Killer node creation
rate = rospy.Rate(ReviewRate)                                                                 # Samples per second to retrieve the robot pose

time.sleep(warmupTime)                                                                        # Sleep time to let ros launch and run all the nodes

init = time.time()

while not rospy.is_shutdown():
    end = time.time()
    if int(end-init) >= Timer_sec:
        nodes = os.popen("rosnode list").readlines()                                          # Gets the list of nodes
        for index in range(len(nodes)):
            nodes[index] = nodes[index].replace("\n", "")                                     # Removes the next line text from each node name

        killAttempt = 0
        for node in nodes:
            # Saves an image of the map
            if killAttempt == 0:
                date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
                os.system("rosrun map_server map_saver -f ~/Documents/Maps/SLAM_Map_{}".format(date))
                time.sleep(5)

            # Kills all the nodes excepting /session_killer
            if node is not "/time_nodes_killer":
                os.system("rosnode kill " + node)
            killAttempt += 1

        # Kills itself after killing all the nodes in the session
        os.system("rosnode kill /session_killer")

    rate.sleep()
