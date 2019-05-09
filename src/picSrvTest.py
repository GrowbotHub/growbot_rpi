#!/usr/bin/env python

import rospy
from growbot_rpi.srv import *

def add_two_ints_client(x, y):
    rospy.wait_for_service('add_two_ints')
    try:
        add_two_ints = rospy.ServiceProxy('add_two_ints', AddTwoInts)
        resp1 = add_two_ints(x, y)
        return resp1.sum
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def usage():
    return "%s [x y]"%sys.argv[0]

def callServ():
    rospy.wait_for_service('/imPro/getImg')
    try:
        getPic = rospy.ServiceProxy('/imPro/getImg', ImPro_getImg)
        print(getPic())
    except rospy.ServiceException, e:
        print("Service call failed: %s", e)

if __name__ == "__main__":
    rospy.loginfo("Running...")
    callServ()
    rospy.loginfo("Done")

    