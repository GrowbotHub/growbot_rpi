#!/usr/bin/env python

import remi.gui as gui
from remi.gui import *
from remi import start, App
import rospy
import constants as cst
from growbot_msg.msg import User_cmd
from growbot_msg.msg import Wheel_target


counter = 0
img_wheelStatus = Image('/my_res:wheel.png')
img_cam = Image('/my_res:pic.png')
img_temp = Image('/my_res:tempPlots.png')
img_humidPower = Image('/my_res:humPowerPlots.png')
img_plantStatus = Image('/my_res:plantState.png')
usrCmdQueue = None
pub_usrCmd = None
pub_target = None

CooledDown = True
ripCheckCooledDown = True

def cb_CoolDown(self):
    global CooledDown
    CooledDown = True

def cb_ripCheckCoolDown(self):
    global ripCheckCooledDown
    ripCheckCooledDown = True

class GrowBotHubGUI(App):
    def __init__(self, *args, **kwargs):
        #DON'T MAKE CHANGES HERE, THIS METHOD GETS OVERWRITTEN WHEN SAVING IN THE EDITOR
        if not 'editing_mode' in kwargs.keys():
            #super(GrowBotHubGUI, self).__init__(*args, static_file_path={'my_res':'./img'})
            super(GrowBotHubGUI, self).__init__(*args, static_file_path={'my_res':cst._RESOURCE_FOLDER})
            #super(GrowBotHubGUI, self).__init__(*args, static_file_path={'my_res':'/home/pi/ros_catkin_ws/src/growbot_rpi/pictures'})

    def idle(self):
        #idle function called every update cycle
        if CooledDown:
            self.vertAlig.children['col2'].children['wig_actions'].children['vertAlign_actions'].children['btn_showLunarSoil'].style['background-color'] = "default"
            self.vertAlig.children['col2'].children['wig_actions'].children['vertAlign_actions'].children['btn_harvest'].style['background-color'] = "default"
        if ripCheckCooledDown :
            self.vertAlig.children['col2'].children['wig_actions'].children['vertAlign_actions'].children['btn_ripCheck'].style['background-color'] = "default"

        img_wheelStatus.attributes['src'] = gui.load_resource(cst._RESOURCE_FOLDER + "wheel.png")
        img_cam.attributes['src'] = gui.load_resource(cst._PICTURE_LOCATION + cst._PICTURE_NAME + cst._PICTURE_EXTENSION)
        img_temp.attributes['src'] = gui.load_resource(cst._RESOURCE_FOLDER + "tempPlots.png")
        img_humidPower.attributes['src'] = gui.load_resource(cst._RESOURCE_FOLDER + "humPowerPlots.png")
        img_plantStatus.attributes['src'] = gui.load_resource(cst._RESOURCE_FOLDER + "plantState.png")
    
    def main(self):
        return GrowBotHubGUI.construct_ui(self)

    def stop(self):
        self.server.server_starter_instance._alive = False
        self.server.server_starter_instance._sserver.shutdown()
        print("server stopped")
        
    @staticmethod
    def construct_ui(self):
        vertAlig = HBox()
        vertAlig.attributes.update({"editor_baseclass":"HBox","editor_tag_type":"widget","editor_newclass":"False","editor_constructor":"()","class":"HBox","editor_varname":"vertAlig"})
        vertAlig.style.update({"align-items":"center","height":"1000px","overflow":"auto","top":"40px","flex-direction":"row","width":"1920px","justify-content":"space-around","position":"absolute","margin":"0px","display":"flex","left":"0px"})

        # COL 1 
        col1 = VBox()
        col1.attributes.update({"editor_baseclass":"VBox","editor_tag_type":"widget","editor_newclass":"False","editor_constructor":"()","class":"VBox","editor_varname":"col1"})
        col1.style.update({"align-items":"center","height":"1000px","overflow":"auto","top":"0px","flex-direction":"column","order":"-1","width":"640px","justify-content":"space-around","position":"static","margin":"0px","display":"flex"})
        
        # --- temperatures
        global img_temp
        img_temp.attributes.update({"src":"/my_res:tempPlots.png","editor_newclass":"False","editor_baseclass":"Image","editor_constructor":"('tempPlots.png')","class":"Image","editor_tag_type":"widget","editor_varname":"img_temp"})
        img_temp.style.update({"width":"640px","position":"static","top":"20px","order":"-1","margin":"0px","overflow":"auto","height":"480px"})
        col1.append(img_temp,'img_temp')

        # --- humdidty power
        global img_humidPower 
        img_humidPower.attributes.update({"src":"/my_res:humPowerPlots.png","editor_newclass":"False","editor_baseclass":"Image","editor_constructor":"('humPowerPlots.png')","class":"Image","editor_tag_type":"widget","editor_varname":"img_humidPower"})
        img_humidPower.style.update({"width":"640px","position":"static","top":"390px","order":"-1","margin":"0px","overflow":"auto","height":"480px"})
        col1.append(img_humidPower,'img_humidPower')

        vertAlig.append(col1,'col1')



        # COL 2
        col2 = VBox()
        col2.attributes.update({"editor_baseclass":"VBox","editor_tag_type":"widget","editor_newclass":"False","editor_constructor":"()","class":"VBox","editor_varname":"col2"})
        col2.style.update({"align-items":"center","height":"1000px","overflow":"auto","top":"20px","flex-direction":"column","order":"-1","width":"640px","justify-content":"space-around","position":"static","margin":"0px","display":"flex"})
        vertAlig.append(col2,'col2')
        
        # --- wiget
        wig_actions = Widget()
        wig_actions.attributes.update({"editor_baseclass":"Widget","editor_tag_type":"widget","editor_newclass":"False","editor_constructor":"()","class":"Widget","editor_varname":"wig_actions"})
        wig_actions.style.update({"width":"640px","position":"static","top":"20px","order":"-1","margin":"0px","overflow":"auto","height":"480px"})
        vertAlign_actions = VBox()
        vertAlign_actions.attributes.update({"editor_baseclass":"VBox","editor_tag_type":"widget","editor_newclass":"False","editor_constructor":"()","class":"VBox","editor_varname":"vertAlign_actions"})
        vertAlign_actions.style.update({"align-items":"center","height":"480px","overflow":"auto","flex-direction":"column","width":"640px","justify-content":"space-around","position":"relative","margin":"0px","display":"flex"})
        btn_showLunarSoil = Button('Handle Lunar Soil')
        btn_showLunarSoil.attributes.update({"editor_baseclass":"Button","editor_tag_type":"widget","editor_newclass":"False","editor_constructor":"('Handle Lunar Soil')","class":"Button","editor_varname":"btn_showLunarSoil"})
        btn_showLunarSoil.style.update({"width":"222px","font-weight":"inherit","font-size":"30px","position":"static","top":"20px","order":"-1","margin":"0px","overflow":"auto","height":"86px"})
        vertAlign_actions.append(btn_showLunarSoil,'btn_showLunarSoil')
        btn_harvest = Button('Harvest a plant')
        btn_harvest.attributes.update({"editor_baseclass":"Button","editor_tag_type":"widget","editor_newclass":"False","editor_constructor":"('Harvest a plant')","class":"Button","editor_varname":"btn_harvest"})
        btn_harvest.style.update({"width":"222px","font-weight":"inherit","font-size":"30px","position":"static","top":"20px","order":"-1","margin":"0px","overflow":"auto","height":"86px"})
        vertAlign_actions.append(btn_harvest,'btn_harvest')
        btn_ripCheck = Button('Perform ripeness check')
        btn_ripCheck.attributes.update({"editor_baseclass":"Button","editor_tag_type":"widget","editor_newclass":"False","editor_constructor":"('Perform ripeness check')","class":"Button","editor_varname":"btn_ripCheck"})
        btn_ripCheck.style.update({"width":"222px","font-weight":"inherit","font-size":"30px","position":"static","top":"20px","order":"-1","margin":"0px","overflow":"auto","height":"86px"})
        vertAlign_actions.append(btn_ripCheck,'btn_ripCheck')
        wig_actions.append(vertAlign_actions,'vertAlign_actions')
        col2.append(wig_actions,'wig_actions')

        # --- cam
        global img_cam
        img_cam.attributes.update({"src":'/my_res:pic.png',"editor_newclass":"False","editor_baseclass":"Image","editor_constructor":"('pic.jpg')","class":"Image","editor_tag_type":"widget","editor_varname":"img_cam"})
        img_cam.style.update({"width":"640px","position":"static","top":"390px","order":"-1","margin":"0px","overflow":"auto","height":"480px"})
        col2.append(img_cam,'img_cam')
        
        


        # COL 3
        col3 = VBox()
        col3.attributes.update({"editor_baseclass":"VBox","editor_tag_type":"widget","editor_newclass":"False","editor_constructor":"()","class":"VBox","editor_varname":"col3"})
        col3.style.update({"align-items":"center","height":"1000px","overflow":"auto","top":"00px","flex-direction":"column","order":"-1","width":"640px","justify-content":"space-around","position":"static","margin":"0px","display":"flex"})
        vertAlig.append(col3,'col3')
        
        # --- wheel status
        global img_wheelStatus
        img_wheelStatus.attributes.update({"src":"/my_res:wheel.png","editor_newclass":"False","editor_baseclass":"Image","editor_constructor":"('wheel.png')","class":"Image","editor_tag_type":"widget","editor_varname":"img_wheelStatus"})
        img_wheelStatus.style.update({"width":"640px","position":"static","order":"-1","margin":"0px","overflow":"auto","height":"480px"})
        col3.append(img_wheelStatus,'img_wheelStatus')

        # --- plant satuts
        global img_plantStatus
        img_plantStatus.attributes.update({"src":"/my_res:plantState.png","editor_newclass":"False","editor_baseclass":"Image","editor_constructor":"('plantState.png')","class":"Image","editor_tag_type":"widget","editor_varname":"img_plantStatus"})
        img_plantStatus.style.update({"width":"640px","position":"static","top":"20px","order":"-1","margin":"0px","overflow":"auto","height":"480px"})
        col3.append(img_plantStatus,'img_plantStatus')
        
        vertAlig.children['col2'].children['wig_actions'].children['vertAlign_actions'].children['btn_showLunarSoil'].onclick.do(self.onclick_btn_showLunarSoil)
        vertAlig.children['col2'].children['wig_actions'].children['vertAlign_actions'].children['btn_harvest'].onclick.do(self.onclikc_btn_harvest)
        vertAlig.children['col2'].children['wig_actions'].children['vertAlign_actions'].children['btn_ripCheck'].onclick.do(self.onclikc_btn_ripCheck)

        self.vertAlig = vertAlig
        return self.vertAlig

    def startCooldown(self):
        global CooledDown
        rospy.loginfo("startCooldown")
        CooledDown = False
        rospy.Timer(rospy.Duration(cst._COOL_DOWN_TIME), cb_CoolDown, oneshot=True)
        self.vertAlig.children['col2'].children['wig_actions'].children['vertAlign_actions'].children['btn_showLunarSoil'].style['background-color'] = "#a0a0a0"
        self.vertAlig.children['col2'].children['wig_actions'].children['vertAlign_actions'].children['btn_harvest'].style['background-color'] = "#a0a0a0"    
        

    def onclick_btn_showLunarSoil(self, emitter):
        global CooledDown
        if CooledDown :
            msg = User_cmd()
            msg.cmdID = cst._CMDID_LS
            pub_usrCmd.publish(msg)
            self.startCooldown()
            

    def onclikc_btn_harvest(self, emitter):
        global CooledDown
        if CooledDown :
            msg = User_cmd()
            msg.cmdID = cst._CMDID_HARVEST
            pub_usrCmd.publish(msg)
            self.startCooldown()


    def onclikc_btn_ripCheck(self, emitter):
        global ripCheckCooledDown
        if ripCheckCooledDown :
            msg = User_cmd()
            msg.cmdID = cst._CMDIF_RIPCHECK
            pub_usrCmd.publish(msg)
            ripCheckCooledDown = False
            rospy.Timer(rospy.Duration(cst._RIPCHECK_COOL_DOWN_TIME), cb_ripCheckCoolDown, oneshot=True)
            self.vertAlig.children['col2'].children['wig_actions'].children['vertAlign_actions'].children['btn_ripCheck'].style['background-color'] = "#a0a0a0"
            

def initPublisher():
    global pub_usrCmd
    global pub_target
    pub_usrCmd = rospy.Publisher('/usr/cmd', User_cmd, queue_size=10)
    pub_target = rospy.Publisher('/wheel/target', Wheel_target, queue_size=10) 


def main():
    initPublisher()
    configuration = cst._SRV_CONFIG
    rospy.loginfo("gui_server : Running...")
    start(GrowBotHubGUI, address=configuration['config_address'], port=configuration['config_port'], 
                        multiple_instance=configuration['config_multiple_instance'], 
                        enable_file_cache=configuration['config_enable_file_cache'],
                        start_browser=configuration['config_start_browser'])

    print("Issue stop server cmd")
    # Making rospy spin prevents from stopping server using ^C
    #rospy.spin()


if __name__ == '__main__':
    try:
        rospy.init_node('gui_server', anonymous=True)
        main()
    except rospy.ROSInterruptException:
        pass