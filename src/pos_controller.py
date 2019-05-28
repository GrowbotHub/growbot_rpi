#!/usr/bin/env python

import rospy
import RPi.GPIO as GPIO
from growbot_rpi.msg import Wheel_moving
from growbot_rpi.msg import Wheel_target

GPIO.setmode(GPIO.BOARD)

# pin 7 does not work for event detection 
pinA = 10
pinB = 11 
pinZ = 5

pin_dir = 21
pin_pwm = 37

_MAX_SPEED = 150
_MIN_SPEED = 5
_DUTY_CYCLE = 50

pos = 0
pwm = None
target = 0
distanceTraveled = 0

pub_done = 0

def saturatedSpeed(s):
	if abs(s) > _MAX_SPEED :
		return _MAX_SPEED
	elif abs(s) < _MIN_SPEED :
		return _MIN_SPEED
	else :
		return s

def cb_counter(channel):
	global pos
	global distanceTraveled

	if GPIO.input(pinB) :
		pos = pos - 1
	else :
		pos = pos + 1

	if pos % 10 == 0 :
		pass
		#print("Current pos : " + str(pos))

	distanceTraveled = distanceTraveled + 1
	goTo()


def pinSetup():
	GPIO.setup(pinA, GPIO.IN)
	GPIO.setup(pinB, GPIO.IN)
	GPIO.setup(pinZ, GPIO.IN)

	GPIO.setup(pin_dir, GPIO.OUT)
	GPIO.setup(pin_pwm, GPIO.OUT)

	GPIO.add_event_detect(pinA, GPIO.RISING, callback=cb_counter)
	#GPIO.add_event_detect(pinA, GPIO.RISING)  
	global pwm
	pwm = GPIO.PWM(pin_pwm, 5)


def goTo(init=False):
	global distanceTraveled
	global target
	if init == True :
		distanceTraveled = 0
		msg = Wheel_moving()
		msg.isMoving = True
		pub_done.publish(msg)

	error = target - pos
	pwm.start(_DUTY_CYCLE)

	if error > 0 :
		GPIO.output(pin_dir, True)
	else :
		GPIO.output(pin_dir, False)

	if not error == 0 :
		#print("error : %d", error)
		pwm.ChangeFrequency(min([saturatedSpeed(abs(error)), saturatedSpeed(distanceTraveled)]))
		error = target - pos
	else :
		pwm.stop()
		print("Target reached, current pos : " + str(pos))
		msg = Wheel_moving()
		msg.isMoving = False
		pub_done.publish(msg)

def cb_target(data):
	global target
	target = data.target
	goTo(init=True)

def initPublisher():
    global pub_done
    pub_done = rospy.Publisher('/wheel/done', Wheel_moving, queue_size=10)
    
def initSubscriber():
	rospy.Subscriber("/wheel/target", Wheel_target, cb_target)

def initServices():
    #rospy.Service('/wheel/goTo', ImPro_doImPro, srvHdl_goTo)
    pass
    

def main():
	global target
	pinSetup()
	initSubscriber()
	initPublisher()
	#target = 1000
	#goTo(init=True)
	rospy.loginfo("wheel_controller : Running...")
	rospy.spin()


if __name__ == '__main__':
	try:
		rospy.init_node('wheel_controller', anonymous=True)
		main()
	except rospy.ROSInterruptException:
		GPIO.cleanup()
		pass


#pinSetup()
#target = -2000
#goTo(init=True)

#raw_input('Press any key to stop\n')
#GPIO.cleanup()