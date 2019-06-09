#!/usr/bin/env python

import rospy
import RPi.GPIO as GPIO
import constants as cst 
from growbot_msg.msg import Dispenser_cmd
from growbot_msg.msg import Dispenser_moving


GPIO.setmode(GPIO.BOARD)

pub_dispMov = None
pwm = None

_PIN_DIS_DIR = 16
_PIN_DIS_STEP = 18


def cb_dispenser_cmd(data):
    rospy.loginfo("Recieved dispenser trigger, waiting a bit")
    rospy.sleep(5)
    msg = Dispenser_moving()
    msg.isMoving = False
    pub_dispMov.publish(msg)
    rospy.loginfo("Dispenser done")

def initPublisher():
    global pub_dispMov
    pub_dispMov = rospy.Publisher('/dispenser/moving', Dispenser_moving, queue_size=10)
    
    
def initSubscriber():
    rospy.Subscriber("/dispenser/cmd", Dispenser_cmd, cb_dispenser_cmd)

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
    #pinSetup()
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
