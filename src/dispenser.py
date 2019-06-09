#!/usr/bin/env python

import rospy
import RPi.GPIO as GPIO
import constants as cst 
from growbot_msg.msg import Dispenser_cmd
from growbot_msg.msg import Dispenser_moving


GPIO.setmode(GPIO.BOARD)

pub_done = None
pwm = None

_PIN_DIS_DIR = 16
_PIN_DIS_STEP = 18

def initPublisher():
    global pub_done
    #pub_done = rospy.Publisher('/dispenser/done', Dispenser_cmd, queue_size=10)

    
def initSubscriber():
    pass
    #rospy.Subscriber("/dispenser/cmd", Wheel_target, cb_target)

def pinSetup():
    GPIO.setup(_PIN_DIS_STEP, GPIO.OUT)
    GPIO.setup(_PIN_DIS_DIR, GPIO.OUT)

    GPIO.output(_PIN_DIS_DIR, GPIO.LOW)
    #GPIO.output(_PIN_DIS_STEP, GPIO.HIGH)

    global pwm
    pwm = GPIO.PWM(_PIN_DIS_STEP, 100)
    pwm.start(50)
    rospy.loginfo("PWM started")


def main():
    global target
    pinSetup()
    initSubscriber()
    initPublisher()
    rospy.loginfo("dispenser : Running...")
    rospy.spin()


if __name__ == '__main__':
    try:
        rospy.init_node('dispenser', anonymous=True)
        main()
        GPIO.cleanup()
    except rospy.ROSInterruptException:
        pass
