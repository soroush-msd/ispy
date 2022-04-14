#!/usr/bin/env python

from __future__ import print_function

#import sys
import rospy
#from beginner_tutorials.srv import *
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from perception.srv import *

def send_darknet(data):
    rospy.wait_for_service('yoloService')
    try:
        yoloService = rospy.ServiceProxy('yoloService', ObjectRecog)
        resp1 = yoloService(image_message)
        return resp1.objectClass
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

#def usage():
    #return "%s [x y]"%sys.argv[0]

if __name__ == "__main__":
    #if len(sys.argv) == 3:
        #x = int(sys.argv[1])
        #y = int(sys.argv[2])
    #else:
        #print(usage())
        #sys.exit(1)
   #print("Requesting %s+%s"%(x, y))
   bridge = CvBridge()
   cv_message = cv2.imread('/home/soroush/Pictures/dog-puppy-on-garden-royalty-free-image-1586966191.jpg')
   image_message = bridge.cv2_to_imgmsg(cv_message, encoding="rgb8")
   print("%s"%(send_darknet(image_message)))