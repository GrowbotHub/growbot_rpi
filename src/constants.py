
# GPIO DEFINITION 
# pin 7 does not work for event detection 
_PIN_ENC_A = 36
_PIN_ENC_B = 38 
_PIN_ENC_Z = 40

_PIN_DIR = 19
_PIN_PWM = 21

_PIN_DHT_SIG = 2# old 24 
_PIN_DHT_G = 5

_PIN_W1_1_3V3 = 8
_PIN_W1_1_SIG = 10 # GPIO15 

_PIN_TIM = 35
_PIN_TIM_G = 31 
_PIN_CS = 33
_PIN_CS_G = 37
_PIN_AWO_G = 29
_PIN_BUTAWO = 15
_PIN_ALM_G = 23

_PIN_BUT_IN = 11


# WHEEL CONTROLER CONSTANTS
_MAX_SPEED = 150
_MIN_SPEED = 5
_DUTY_CYCLE = 50
_P_PER_ROTATION = 8000
_ACCELERATION_FACTOR = 3


# SERVER
_RESOURCE_FOLDER = '/home/pi/ros_catkin_ws/src/growbot_rpi/src/gui/img/'
_MAX_PLOT_PTS = 100
_PLOT_RATE = 0.1
_SRV_CONFIG = {'config_multiple_instance': False, 'config_address': '0.0.0.0', 'config_start_browser': False, 'config_enable_file_cache': False, 'config_project_name': 'GrowBotHub', 'config_port': 8081}

# SENSOR INTERFACE
_MEAS_RATE = 0.1 #Hz
_PIC_LOGGING = False #if True save
_PICTURE_LOCATION = '/home/pi/ros_catkin_ws/src/growbot_rpi/pictures/'
_PICTURE_NAME = 'pic'
_PICTURE_EXTENSION = '.jpg'

# WHEEL IMAGE
_ACTIVE_LOWER_TRESH = 30
_ACTIVE_UPPER_TRESH = 60

# GENERAL BEHVIOUR
_COOL_DOWN_TIME = 5 # in seconds