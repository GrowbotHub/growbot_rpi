#!/usr/bin/env python

import rospy
from growbot_msg.msg import Meas_sensor
from growbot_msg.msg import Wheel_target
import constants as cst 
from gui.measurments import makeTempPlots
from gui.measurments import makeHumPowerPlots
from gui.wheel import makeWheelImg
from server_v2 import main as initServer 

airTemp = []
time_airTemp = []
waterTemp = []
time_waterTemp = []
humidity = []
time_humidity = []
power = []
time_power = []
new_target = False
target = 0


def cb_airTemp(msg):
	airTemp.append(msg.value)
	time_airTemp.append(msg.measurmentTime.secs)
	

def cb_waterTemp(msg):
	waterTemp.append(msg.value)
	time_waterTemp.append(msg.measurmentTime.secs)


def cb_humidity(msg):
	humidity.append(msg.value)
	time_humidity.append(msg.measurmentTime.secs)

def cb_target(msg):
	global new_target
	global target
	new_target = True
	target = msg.target*360/cst._P_PER_ROTATION


def initPublisher():
	pass

    
def initSubscriber():
	rospy.Subscriber("/meas/airTemp", Meas_sensor, cb_airTemp)
	rospy.Subscriber("/meas/waterTemp", Meas_sensor, cb_waterTemp)
	rospy.Subscriber("/meas/humidity", Meas_sensor, cb_humidity)
	rospy.Subscriber("/wheel/target", Wheel_target, cb_target)


def initServices():
    #rospy.Service('/wheel/goTo', ImPro_doImPro, srvHdl_goTo)
    pass
    

def main():
	initSubscriber()
	initPublisher()
	#initServer()
	rate = rospy.Rate(cst._PLOT_RATE)
	rospy.loginfo("wheel_controller : Running...")
	while not rospy.is_shutdown():
		makeTempPlots(time_airTemp, airTemp, time_waterTemp, waterTemp)
		makeHumPowerPlots(time_humidity, humidity, time_power, power)
		global new_target
		if new_target :
			new_target = False
			makeWheelImg(target)
		rate.sleep()


if __name__ == '__main__':
	try:
		rospy.init_node('wheel_controller', anonymous=True)
		main()
	except rospy.ROSInterruptException:
		pass
