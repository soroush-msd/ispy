#! /usr/bin/env python

from __future__ import print_function

import rospy
import sys
import actionlib
import darknet_ros_msgs.msg
import darknet_ros_msgs
from cv_bridge import CvBridge
import cv2
import roslaunch

bridge = CvBridge()

def darknet_client():
    # Creates the SimpleActionClient, passing the type of the action
    client = actionlib.SimpleActionClient('/darknet_ros/check_for_objects', darknet_ros_msgs.msg.CheckForObjectsAction)

    # Waits until the action server has started up and started
    # listening for goals.
    client.wait_for_server()

    # Creates a goal to send to the action server.
    cv_message = cv2.imread('/home/soroush/Pictures/Yellow-Lab-High-Five.jpg')
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

        uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
        roslaunch.configure_logging(uuid)

        launch = roslaunch.parent.ROSLaunchParent(uuid, ["/home/soroush/catkin_ws/src/darknet_ros/darknet_ros/launch/yolo_v3.launch"])
        launch.start()
        rospy.loginfo("started")
        init = darknet_client()
        result = darknet_client()

        for i in range(len(result.bounding_boxes.bounding_boxes)):
            print(result.bounding_boxes.bounding_boxes[i].Class)
        launch.shutdown()
        
    except rospy.ROSInterruptException:
        print("program interrupted before completion", file=sys.stderr)