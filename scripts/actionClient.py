#! /usr/bin/env python

from __future__ import print_function
from email.mime import image

import rospy

# Brings in the SimpleActionClient
import sys
import actionlib
import rospy
from std_msgs.msg import Int8, String
import darknet_ros_msgs.msg
import darknet_ros_msgs
#from darknet_ros_msgs.action import CheckForObjects
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2

bridge = CvBridge()


# Brings in the messages used by the fibonacci action, including the
# goal message and the result message.
import actionlib_tutorials.msg

def darknet_client():
    # Creates the SimpleActionClient, passing the type of the action
    # (FibonacciAction) to the constructor.
    client = actionlib.SimpleActionClient('/darknet_ros/check_for_objects', darknet_ros_msgs.msg.CheckForObjectsAction)

    # Waits until the action server has started up and started
    # listening for goals.
    client.wait_for_server()

    # Creates a goal to send to the action server.
    cv_message = cv2.imread('/home/soroush/Pictures/dog-puppy-on-garden-royalty-free-image-1586966191.jpg')
    image_message = bridge.cv2_to_imgmsg(cv_message, encoding="rgb8")
    goal = darknet_ros_msgs.msg.CheckForObjectsGoal(image=image_message)

    # Sends the goal to the action server.
    client.send_goal(goal)

    # Waits for the server to finish performing the action.
    client.wait_for_result()

    # Prints out the result of executing the action
    return client.get_result()

if __name__ == '__main__':
    try:
        # Initializes a rospy node so that the SimpleActionClient can
        # publish and subscribe over ROS.
        rospy.init_node('darknet_client_py')
        init = darknet_client()
        result = darknet_client()
        #rospy.loginfo(result.id)
        for i in range(len(result.bounding_boxes.bounding_boxes)):
            print(result.bounding_boxes.bounding_boxes[i].Class)
        #rospy.loginfo(result.bounding_boxes.bounding_boxes[0].Class)
        #rospy.loginfo(result)
        
    except rospy.ROSInterruptException:
        print("program interrupted before completion", file=sys.stderr)