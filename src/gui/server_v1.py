#!/usr/bin/env python

import remi.gui as gui
from remi.gui import *
from remi import start, App
import rospy

counter = 0
img_wheelStatus = Image('/my_res:wheel.png')

class untitled(App):
    def __init__(self, *args, **kwargs):
        #DON'T MAKE CHANGES HERE, THIS METHOD GETS OVERWRITTEN WHEN SAVING IN THE EDITOR
        if not 'editing_mode' in kwargs.keys():
            #super(untitled, self).__init__(*args, static_file_path={'my_res':'./img'})
            super(untitled, self).__init__(*args, static_file_path={'my_res':'/home/pi/ros_catkin_ws/src/growbot_rpi/src/gui/img'})

    def idle(self):
        #idle function called every update cycle

        img_wheelStatus.attributes['src'] = gui.load_resource("/home/pi/ros_catkin_ws/src/growbot_rpi/src/gui/img/wheel.png")
        pass
    
    def main(self):
        return untitled.construct_ui(self)
        
    @staticmethod
    def construct_ui(self):
        #print(gui.to_uri(gui.load_resource("./img/wheel.png")))
        #DON'T MAKE CHANGES HERE, THIS METHOD GETS OVERWRITTEN WHEN SAVING IN THE EDITOR
        mainLatAlign = VBox()
        mainLatAlign.attributes.update({"editor_baseclass":"VBox","editor_tag_type":"widget","editor_newclass":"False","editor_constructor":"()","class":"VBox","editor_varname":"mainLatAlign"})
        mainLatAlign.style.update({"align-items":"center","font-size":"20px","height":"3000px","overflow":"auto","font-style":"inherit","top":"0px","flex-direction":"column","width":"640px","justify-content":"space-around","position":"absolute","font-weight":"bolder","margin":"0px","display":"flex","left":"0px"})
        
        wig_actions = Widget()
        wig_actions.attributes.update({"editor_baseclass":"Widget","editor_tag_type":"widget","editor_newclass":"False","editor_constructor":"()","class":"Widget","editor_varname":"wig_actions"})
        wig_actions.style.update({"width":"640px","position":"static","top":"20px","order":"-1","margin":"0px","overflow":"auto","height":"480px"})
        vertAlign_actions = HBox()
        vertAlign_actions.attributes.update({"editor_baseclass":"HBox","editor_tag_type":"widget","editor_newclass":"False","editor_constructor":"()","class":"HBox","editor_varname":"vertAlign_actions"})
        vertAlign_actions.style.update({"align-items":"center","height":"480px","overflow":"auto","flex-direction":"row","width":"640px","justify-content":"space-around","position":"relative","margin":"0px","display":"flex"})
        btn_showLunarSoil = Button('Show Lunar Soil')
        btn_showLunarSoil.attributes.update({"editor_baseclass":"Button","editor_tag_type":"widget","editor_newclass":"False","editor_constructor":"('Show Lunar Soil')","class":"Button","editor_varname":"btn_showLunarSoil"})
        btn_showLunarSoil.style.update({"width":"222px","font-weight":"inherit","font-size":"30px","position":"static","top":"20px","order":"-1","margin":"0px","overflow":"auto","height":"86px"})
        vertAlign_actions.append(btn_showLunarSoil,'btn_showLunarSoil')
        wig_actions.append(vertAlign_actions,'vertAlign_actions')
        mainLatAlign.append(wig_actions,'wig_actions')
        
        img_plantStatus = Image('/my_res:plantState.png')
        img_plantStatus.attributes.update({"src":"/my_res:plantState.png","editor_newclass":"False","editor_baseclass":"Image","editor_constructor":"('plantState.png')","class":"Image","editor_tag_type":"widget","editor_varname":"img_plantStatus"})
        img_plantStatus.style.update({"width":"640px","position":"static","top":"20px","order":"-1","margin":"0px","overflow":"auto","height":"480px"})
        mainLatAlign.append(img_plantStatus,'img_plantStatus')
        
        global img_wheelStatus
        img_wheelStatus.attributes.update({"src":"/my_res:wheel.png","editor_newclass":"False","editor_baseclass":"Image","editor_constructor":"('wheel.png')","class":"Image","editor_tag_type":"widget","editor_varname":"img_wheelStatus"})
        img_wheelStatus.style.update({"width":"640px","position":"static","order":"-1","margin":"0px","overflow":"auto","height":"480px"})
        mainLatAlign.append(img_wheelStatus,'img_wheelStatus')
        
        img_temp = Image('/my_res:tempPlots.png')
        img_temp.attributes.update({"src":"/my_res:tempPlots.png","editor_newclass":"False","editor_baseclass":"Image","editor_constructor":"('tempPlots.png')","class":"Image","editor_tag_type":"widget","editor_varname":"img_temp"})
        img_temp.style.update({"width":"640px","position":"static","top":"20px","order":"-1","margin":"0px","overflow":"auto","height":"480px"})
        mainLatAlign.append(img_temp,'img_temp')
        
        img_humidPower = Image('/my_res:humPowerPlots.png')
        img_humidPower.attributes.update({"src":"/my_res:humPowerPlots.png","editor_newclass":"False","editor_baseclass":"Image","editor_constructor":"('humPowerPlots.png')","class":"Image","editor_tag_type":"widget","editor_varname":"img_humidPower"})
        img_humidPower.style.update({"width":"640px","position":"static","top":"390px","order":"-1","margin":"0px","overflow":"auto","height":"480px"})
        mainLatAlign.append(img_humidPower,'img_humidPower')

        img_cam = Image('/my_res:cam.jpg')
        img_cam.attributes.update({"src":"/my_res:cam.jpg","editor_newclass":"False","editor_baseclass":"Image","editor_constructor":"('cam.jpg')","class":"Image","editor_tag_type":"widget","editor_varname":"img_cam"})
        img_cam.style.update({"width":"640px","position":"static","top":"390px","order":"-1","margin":"0px","overflow":"auto","height":"480px"})
        mainLatAlign.append(img_cam,'img_cam')
        
        mainLatAlign.children['wig_actions'].children['vertAlign_actions'].children['btn_showLunarSoil'].onclick.do(self.onclick_btn_showLunarSoil)
        

        self.mainLatAlign = mainLatAlign
        return self.mainLatAlign
    
    def onclick_btn_showLunarSoil(self, emitter):
        pass



#Configuration
configuration = {'config_multiple_instance': False, 'config_address': '0.0.0.0', 'config_start_browser': False, 'config_enable_file_cache': False, 'config_project_name': 'GrowBotHub', 'config_port': 8081}


def main():
    rospy.loginfo("gui_server : Running...")
    start(untitled, address=configuration['config_address'], port=configuration['config_port'], 
                        multiple_instance=configuration['config_multiple_instance'], 
                        enable_file_cache=configuration['config_enable_file_cache'],
                        start_browser=configuration['config_start_browser'])

    #rospy.spin()


if __name__ == '__main__':
    try:
        rospy.init_node('gui_server', anonymous=True)
        main()
    except rospy.ROSInterruptException:
        pass