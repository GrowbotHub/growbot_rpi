#!/usr/bin/env python

import rospy
from growbot_msg.msg import Meas_sensor
from growbot_msg.srv import ImPro_getImg
import time
from picamera import PiCamera
from w1thermsensor import W1ThermSensor
import Adafruit_DHT
import rospy
from math import floor
import constants as cst
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)


# Global Variable
pub_airTemp = 0
pub_waterTemp = 0
pub_humidity = 0
pub_img = 0

logFileName = cst._DATA_LOCATION + "sensorLog_" +str(int(floor(time.time()))) + ".txt"


def pinSetup():
    GPIO.setup(cst._PIN_DHT_G, GPIO.OUT)
    GPIO.output(cst._PIN_DHT_G, GPIO.LOW)

    GPIO.setup(cst._PIN_W1_1_3V3, GPIO.OUT)
    GPIO.output(cst._PIN_W1_1_3V3, GPIO.HIGH)  
    GPIO.setup(cst._PIN_W1_1_SIG, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def takePic():
    imgFileName = cst._PICTURE_LOCATION + cst._PICTURE_NAME + cst._PICTURE_EXTENSION

    camera = PiCamera()
    camera.rotation = 90
    camera.resolution = (1280, 720) #(860, 480) #(1280, 720) # (1640, 1232) # (320, 240) # optimal: (640, 480)
    camera.start_preview()
    time.sleep(2)
    camera.capture(imgFileName)
    if cst._PIC_LOGGING :
        imgFileNameLOG = cst._PICTURE_LOCATION + cst._PICTURE_NAME + str(int(floor(time.time()))) + cst._PICTURE_EXTENSION
        camera.capture(imgFileNameLOG)
    camera.stop_preview()
    camera.close()
    return imgFileName


def logSensorData(humidity, temp_air, temp_water, measTime):
    logFile = open(logFileName, "a")
    logFile.write(str(measTime) + ", " + str(humidity) + ", " + str(temp_air) + ", " + str(temp_water) + ";\n")
    logFile.close()


def getSensorReading():
    measTime = time.time()
    humidity, temp_air = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, cst._PIN_DHT_SIG)
    temp_water = None
    #DS18B20 = W1ThermSensor()
    #temp_water = DS18B20.get_temperature()
    
    if humidity is None or temp_air is None: 
        rospy.logwarn("None value for Adafruit DHT")
        humidity = 0
        temp_air = 0

    if temp_water is None: 
        rospy.logwarn("None value for W1ThermSensor")
        temp_water = 0
    
    #rospy.loginfo("Humid : %lf, air : %lf, water : %lf",humidity, temp_air, temp_water)
    if cst._DATA_LOGGING :
        logSensorData(humidity, temp_air, temp_water, measTime)
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
    msg_airTemp .measurmentTime.nsecs = nsec
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
    pinSetup()
    rate = rospy.Rate(cst._MEAS_RATE)
    rospy.loginfo("swag_interface : Running...")
    while not rospy.is_shutdown():
        publishMeasurements()
        rate.sleep()

    GPIO.cleanup()

if __name__ == '__main__':
    try:
        rospy.init_node('sensor_interface', anonymous=True)
        main()
    except rospy.ROSInterruptException:
        pass
