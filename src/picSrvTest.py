#!/usr/bin/env python

import rospy
from growbot_msg.srv import ImPro_getImg

def callServ():
    rospy.wait_for_service('/imPro/getImg')
    try:
        getPic = rospy.ServiceProxy('/imPro/getImg', ImPro_getImg)
        print(getPic())
    except rospy.ServiceException as e:
        print("Service call failed: %s", e)

if __name__ == "__main__":
    rospy.loginfo("Running...")
    callServ()
    rospy.loginfo("Done")

    