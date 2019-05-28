
# -*- coding: utf-8 -*-

import remi.gui as gui
from remi.gui import *
from remi import start, App


class GrowBot(App):
    def __init__(self, *args, **kwargs):
        #DON'T MAKE CHANGES HERE, THIS METHOD GETS OVERWRITTEN WHEN SAVING IN THE EDITOR
        if not 'editing_mode' in kwargs.keys():
            super(GrowBot, self).__init__(*args,static_file_path={'my_res':'./'})

    def idle(self):
        #idle function called every update cycle
        pass
    
    def main(self):
        return GrowBot.construct_ui(self)
        
    @staticmethod
    def construct_ui(self):
        #DON'T MAKE CHANGES HERE, THIS METHOD GETS OVERWRITTEN WHEN SAVING IN THE EDITOR
        wheelStatus = Widget()
        wheelStatus.attributes.update({"class":"Widget","editor_constructor":"()","editor_varname":"wheelStatus","editor_tag_type":"widget","editor_newclass":"False","editor_baseclass":"Widget"})
        wheelStatus.style.update({"margin":"0px","width":"640px","height":"520px","top":"5px","left":"5px","position":"absolute","overflow":"auto"})
        label_wheelStatus = Label('Wheel Status')
        label_wheelStatus.attributes.update({"class":"Label","editor_constructor":"('Wheel Status')","editor_varname":"label_wheelStatus","editor_tag_type":"widget","editor_newclass":"False","editor_baseclass":"Label"})
        label_wheelStatus.style.update({"margin":"0px","width":"100px","height":"30px","top":"10px","left":"75px","position":"absolute","overflow":"auto","font-weight":"bolder","right":"0px"})
        wheelStatus.append(label_wheelStatus,'label_wheelStatus')
        img_wheelStatus = Image('/my_res:img/wheel.png')
        img_wheelStatus.attributes.update({"class":"Image","src":"/my_res:img/wheel.png","editor_constructor":"('/my_res:img/wheel.png')","editor_varname":"img_wheelStatus","editor_tag_type":"widget","editor_newclass":"False","editor_baseclass":"Image"})
        img_wheelStatus.style.update({"margin":"0px","width":"640px","height":"480px","top":"40px","left":"0px","position":"absolute","overflow":"auto"})
        wheelStatus.append(img_wheelStatus,'img_wheelStatus')
        

        self.wheelStatus = wheelStatus
        return self.wheelStatus
    


#Configuration
configuration = {'config_project_name': 'GrowBot', 'config_address': '0.0.0.0', 'config_port': 8081, 'config_multiple_instance': True, 'config_enable_file_cache': True, 'config_start_browser': True}#, 'config_resourcepath': './'}

if __name__ == "__main__":
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(GrowBot, address=configuration['config_address'], port=configuration['config_port'], 
                        multiple_instance=configuration['config_multiple_instance'], 
                        enable_file_cache=configuration['config_enable_file_cache'],
                        start_browser=configuration['config_start_browser'])
