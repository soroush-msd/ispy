#!/usr/bin/env python

from time import sleep
import rospy
import smach
import smach_ros
import sys
import roslaunch
import actionlib
import darknet_ros_msgs.msg
import darknet_ros_msgs
from cv_bridge import CvBridge
import cv2
import roslaunch
import random
from sensor_msgs.msg import Image


bridge = CvBridge()
counter = 0
#asks = ""

# define state Foo
class Human(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                            outcomes=['robot_turn', 'exit_success', 'exit_fail'],
                            input_keys=['human_letter', 'robot_guesses', 'asks', 'object_names'],
                            output_keys=['human_letter', 'asks'])

    def execute(self, userdata):
        rospy.loginfo('Executing state HUMAN')

        if(userdata.asks == ""):
            turn = raw_input("Welcome to ISpy! type either (H)uman or (R)obot to continue: ")

            if turn == "h" or turn == "H":
                print("you chose Human")
                userdata.human_letter = raw_input("type the first letter of the object: ")
                print("you selected: " + userdata.human_letter)
                userdata.asks = "h"
                return 'robot_turn'

            elif turn == "r" or turn == "R": 
                print("you chose Robot")
                userdata.asks = "r"
                print("Please wait")
                return 'robot_turn'

            # loop until correct usage instead of crashing the program
            else:
                sys.exit("usage: H/h || R/r")

        else:
            #print("1111111111111111111111111111111111111111111111*")
            if(userdata.asks == "h"):
                #print("222222222222222222222222222222222222222222")
                if(len(userdata.robot_guesses) == 0):
                    print("Object that starts with " + userdata.human_letter + " not found!")
                    return 'exit_fail'
                for i in range(len(userdata.robot_guesses)):
                    print("*********************************************")
                    print("The object that starts with " + userdata.human_letter+ " is " + userdata.robot_guesses[i])
                    return 'exit_success'

            elif(userdata.asks == "r"):
                print("robot chose the letter: " + userdata.robot_guesses[0])
                human_guess = raw_input("what is the object?")
                #for i in range(len(userdata.object_names)):
                if(human_guess == userdata.object_names[0] and human_guess[0] == userdata.robot_guesses[0]):
                    print("YAAY, The Object is " + userdata.object_names[0])
                    return 'exit_success'
                    
                print("Oh No!, you guessed wrong" + "The correct object is " +  userdata.object_names[0])
                return 'exit_fail'
        #print("3333333333333333333333333333333333333333333333333333")
                        
                
        


# define state Bar
class Robot(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                            outcomes=['perception', 'robot_responds_human', 'exit_success', 'exit_fail'],
                            input_keys=['human_letter_to_robot', 'object_names', 'robot_response', 'asks'])

    def execute(self, userdata):

        rospy.loginfo('Executing state ROBOT')
        global counter

        if(userdata.asks=="h"):
            if((len(userdata.object_names) == 0)):
                if counter < 3:
                    print("Robot searching for an object that starts with <<" + userdata.human_letter_to_robot + ">>...")
                    counter += 1
                    return 'perception'
                else:
                    print("NO object found")
                    return 'exit_fail'
        
            elif((len(userdata.object_names) != 0)):
                print("Objects detected are:")
                for i in range(len(userdata.object_names)):
                    if(userdata.object_names[i][0] == userdata.human_letter_to_robot):
                        userdata.robot_response.append( userdata.object_names[i])
                    #print(userdata.object_names[i])
                return 'robot_responds_human'

        elif(userdata.asks =="r"):
            if((len(userdata.object_names) == 0)):
                if counter < 3:
                    print("looking around")
                    counter += 1
                    return 'perception'
                else:
                    print("NO object found")
                    return 'exit_fail'

            elif((len(userdata.object_names) != 0)):
                random_word = random.choice(userdata.object_names)
                userdata.object_names[0] = random_word
                userdata.robot_response.append(random_word[0])
                return 'robot_responds_human'

        
        #return 'robot_responds_human'
        
        
        
class Perception(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                            outcomes=['objects', 'vision'],
                            input_keys=['human_letter_to_robot', 'objects_detected', 'image_received'],
                            output_keys=['image_received'])

    def execute(self, userdata):
        print("Running darknet_ros...")
        rospy.loginfo('Executing state PERCEPTION')

        if userdata.image_received == 0:
            return 'vision'

        uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
        roslaunch.configure_logging(uuid)

        launch = roslaunch.parent.ROSLaunchParent(uuid, ["/home/kinovagen3/catkin_ws/src/darknet_ros/darknet_ros/launch/yolo_v3.launch"])
        launch.start()
        #rospy.loginfo("started")
        client = actionlib.SimpleActionClient('/darknet_ros/check_for_objects', darknet_ros_msgs.msg.CheckForObjectsAction)
        client.wait_for_server()
        cv_message = cv2.imread('/home/kinovagen3/catkin_ws/camera_image_hmmm.jpeg')
        image_message = bridge.cv2_to_imgmsg(cv_message, encoding="rgb8")
        goal = darknet_ros_msgs.msg.CheckForObjectsGoal(image=image_message)
        client.send_goal(goal)
        client.wait_for_result()
        result = client.get_result()
        #print(result)

        i = 0

        while i < 1:
            client.send_goal(goal)
            client.wait_for_result()
            result = client.get_result()
            i = i + 1

        for i in range(len(result.bounding_boxes.bounding_boxes)):
                userdata.objects_detected.append(result.bounding_boxes.bounding_boxes[i].Class)
                #print()

        #rospy.sleep(20)
        launch.shutdown()

        return 'objects'


class Vision(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                            outcomes=['send_vision_to_perception'],
                            input_keys=['image_send'],
                            output_keys=['image_send'])

    def execute(self, userdata):
        print("Running Kortex_vision...")
        rospy.loginfo('Executing state VISION')

        uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
        roslaunch.configure_logging(uuid)

        launch = roslaunch.parent.ROSLaunchParent(uuid, ["/home/kinovagen3/catkin_ws/src/ros_kortex_vision/launch/kinova_vision.launch"])
        launch.start()
        msg = rospy.wait_for_message("/camera/color/image_raw", Image)
        cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
        cv2.imwrite('camera_image_hmmm.jpeg', cv2_img)
        rospy.sleep(10) 
        launch.shutdown()
        userdata.image_send = 1
        return 'send_vision_to_perception'



# main
def main():
    #global counter
    
    rospy.init_node('ISpy_state_machine')

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['failed', 'successfull'])
    sm.userdata.sm_letter = ""
    sm.userdata.guess_list = []
    sm.userdata.final_guess = []
    sm.userdata.ask = ""
    sm.userdata.image_status = 0
    
    #sm.userdata.bridge = CvBridge()

    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('HUMAN', Human(), 
                               transitions={'robot_turn' : 'ROBOT' ,
                                            'exit_success' : 'successfull',
                                            'exit_fail' : 'failed'},
                               remapping={'human_letter' : 'sm_letter',
                               "robot_guesses" : "final_guess",
                               "asks" : "ask",
                               "object_names" : "guess_list"})

        smach.StateMachine.add('ROBOT', Robot(), 
                               transitions={'perception' : 'PERCEPTION',
                               "robot_responds_human" : "HUMAN",
                               'exit_success' : 'successfull',
                               'exit_fail' : 'failed'},
                               remapping={"human_letter_to_robot" : "sm_letter",
                               "object_names" : "guess_list",
                               "robot_response" : "final_guess",
                               "asks" : "ask"})

        smach.StateMachine.add('PERCEPTION', Perception(), 
                               transitions={'objects' : 'ROBOT',
                               "vision" : "VISION"},
                               remapping={"human_letter_to_robot" : "sm_letter",
                               "objects_detected" : "guess_list",
                               "image_received" : "image_status"})
        
        smach.StateMachine.add('VISION', Vision(), 
                               transitions={'send_vision_to_perception' : 'PERCEPTION'},
                               remapping={"image_send" : "image_status"})

    image_topic = "/camera/color/image_raw"
    # Set up your subscriber and define its callback
    
    
    #rospy.Subscriber(image_topic, Image, image_callback)
    #counter = 1
    #rospy.spin()
    sis = smach_ros.IntrospectionServer('ispy', sm, '/SM_ROOT')
    sis.start()
    outcome = sm.execute()
    #rospy.spin()
    sis.stop()

    # Execute SMACH plan
    
    


if __name__ == '__main__':
    main()
