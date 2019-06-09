#!/usr/bin/env python

import rospy
from growbot_msg.msg import Meas_sensor
from growbot_msg.msg import Wheel_target
from growbot_msg.msg import User_cmd
import constants as cst 
from gui.measurments import makeTempPlots
from gui.measurments import makeHumPowerPlots
from gui.plants import makePlantStateImg
from gui.wheel import makeWheelImg

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
new_plantState = False


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


def cb_plants(msg):
	global new_plantState
	if msg.cmdID == cst._CMDIF_RIPCHECK :
		new_plantState = True

def initPublisher():
	pass

    
def initSubscriber():
	rospy.Subscriber("/meas/airTemp", Meas_sensor, cb_airTemp)
	rospy.Subscriber("/meas/waterTemp", Meas_sensor, cb_waterTemp)
	rospy.Subscriber("/meas/humidity", Meas_sensor, cb_humidity)
	rospy.Subscriber("/wheel/target", Wheel_target, cb_target)

	# Cheating...
	rospy.Subscriber("/usr/cmd", User_cmd, cb_plants)


def initServices():
    #rospy.Service('/wheel/goTo', ImPro_doImPro, srvHdl_goTo)
    pass
    

def main():
	initSubscriber()
	initPublisher()

	rate = rospy.Rate(cst._PLOT_RATE)
	rospy.loginfo("gui_ressources : Running...")
	while not rospy.is_shutdown():
		makeTempPlots(time_airTemp, airTemp, time_waterTemp, waterTemp)
		makeHumPowerPlots(time_humidity, humidity, time_power, power)
		global new_target
		if new_target :
			new_target = False
			makeWheelImg(target)

		global new_plantState
		if new_plantState :
			new_plantState = False
			makePlantStateImg()
		rate.sleep()


if __name__ == '__main__':
	try:
		rospy.init_node('wheel_controller', anonymous=True)
		main()
	except rospy.ROSInterruptException:
		pass
		
