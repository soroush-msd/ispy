#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2

bridge = CvBridge()

def speaker():
    pub = rospy.Publisher('/camera/rgb/image_raw', Image, queue_size=1)
    rospy.init_node('image', anonymous=True)
    rate = rospy.Rate(1) # 10hz
    while not rospy.is_shutdown():
        cv_message = cv2.imread('/home/soroush/Pictures/dog-puppy-on-garden-royalty-free-image-1586966191.jpg')
        image_message = bridge.cv2_to_imgmsg(cv_message, encoding="rgb8")
        pub.publish(image_message)
        rate.sleep()


if __name__ == '__main__':
    try:
        speaker()
    except rospy.ROSInterruptException:
        pass