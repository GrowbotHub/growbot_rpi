#!/usr/bin/env python

import rospy
from growbot_rpi.msg import Meas_sensor
from growbot_rpi.srv import ImPro_getImg
import time
from picamera import PiCamera
from w1thermsensor import W1ThermSensor
import Adafruit_DHT
import rospy
from math import floor

# Constants
_RATE = 10 #Hz
_PIC_LOGGING = False

# Global Variable
pub_airTemp = 0
pub_waterTemp = 0
pub_humidity = 0
pub_img = 0


def takePic():
    if _PIC_LOGGING :
        imgFileName = '/home/pi/ros_catkin_ws/src/growbot_rpi/pictures/pic' + str(int(floor(time.time()))) + '.jpg'
    else :
        imgFileName = '/home/pi/ros_catkin_ws/src/growbot_rpi/pictures/pic.jpg'

    camera = PiCamera()
    camera.rotation = 90
    camera.resolution = (1280, 720) #(860, 480) #(1280, 720) # (1640, 1232) # (320, 240) # optimal: (640, 480)
    camera.start_preview()
    time.sleep(2)
    camera.capture(imgFileName)
    camera.stop_preview()
    camera.close()
    return imgFileName


def getSensorReading():
	measTime = time.time()
	humidity, temp_air = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 24)
	DS18B20 = W1ThermSensor()
	temp_water = DS18B20.get_temperature()

	if humidity is None or temp_air is None: 
		rospy.logwarn("None value for Adafruit DHT")
		humidity = 0
		temp_air = 0

	if temp_water is None: 
		rospy.logwarn("None value for W1ThermSensor")
		temp_water = 0
	
	#rospy.loginfo("Humid : %lf, air : %lf, water : %lf",humidity, temp_air, temp_water)
	return humidity, temp_air, temp_water, measTime

def srvHdl_getImg(req):
	imgFileName = takePic()
	return str(imgFileName)


def initPublisher():
    global pub_airTemp
    global pub_waterTemp
    global pub_humidity
    
    pub_airTemp = rospy.Publisher('/meas/airTemp', Meas_sensor, queue_size=10)
    pub_waterTemp = rospy.Publisher('/meas/waterTemp', Meas_sensor, queue_size=10)
    pub_humidity = rospy.Publisher('/meas/humidity', Meas_sensor, queue_size=10)
    

def initServices():
    rospy.Service('/imPro/getImg', ImPro_getImg, srvHdl_getImg)


def publishMeasurements():
    humidity, temp_air, temp_water, measTime = getSensorReading()
    sec = int(floor(measTime))
    nsec = int((measTime - sec)*1e9)
    #airTemp    
    msg_airTemp = Meas_sensor()
    msg_airTemp.value = temp_air
    msg_airTemp.measurmentTime.secs = sec
    msg_airTemp	.measurmentTime.nsecs = nsec
    pub_airTemp.publish(msg_airTemp)

    #waterTemp    
    msg_waterTemp = Meas_sensor()
    msg_waterTemp.value = temp_water
    msg_waterTemp.measurmentTime.secs = sec
    msg_waterTemp.measurmentTime.nsecs = nsec
    pub_waterTemp.publish(msg_waterTemp)

    #humidity    
    msg_humidity = Meas_sensor()
    msg_humidity.value = humidity
    msg_humidity.measurmentTime.secs = sec
    msg_humidity.measurmentTime.nsecs = nsec
    pub_humidity.publish(msg_humidity)


def main():
    initPublisher()
    initServices()
    rate = rospy.Rate(_RATE)
    rospy.loginfo("swag_interface : Running...")
    while not rospy.is_shutdown():
        publishMeasurements()
        rate.sleep()


if __name__ == '__main__':
    try:
        rospy.init_node('sensor_interface', anonymous=True)
        main()
    except rospy.ROSInterruptException:
        pass
