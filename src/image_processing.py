#!/usr/bin/env python
_FAKE_IMPRO = True

import rospy
from growbot_msg.srv import ImPro_doImPro
from growbot_msg.srv import ImPro_getImg

#img processing libs
if(not _FAKE_IMPRO) :
    import tensorflow as tf
    import numpy as np
    import matplotlib
    matplotlib.use("Pdf")
    import matplotlib.pyplot as plt
    from PIL import Image
    import scipy
    from scipy.misc import imread
    from keras.models import load_model
    from skimage.transform import resize


# Constants
_MODEL_FILE = '/home/pi/ros_catkin_ws/src/growbot_rpi/imPro/filename.model'
_NB_POT_PER_ROW = 4

_ROW_NAME = 0
_DECISION = 1
_PROBABILITY = 2

# Global variable
pub_res = 0


def checkRipeness(imgFileName):
    if _FAKE_IMPRO :
        return [('top', 0, 0.99),('middle', 1, 0.69),('bottom', 0, 0.89)]
    # load the model
    model = load_model(_MODEL_FILE)

    im = scipy.misc.imread(imgFileName)

    top = im[0:350,400:1300,:] #A
    mid = im[350:750,400:1300,:] #B
    bot = im[725:1125,400:1300,:] #C

    fig_top = plt.figure()
    plt.imshow(top)
    plt.savefig('forTest/image_top.png')
    plt.figure()
    plt.imshow(mid)
    plt.savefig('forTest/image_middle.png')
    plt.figure()
    plt.imshow(bot)
    plt.savefig('forTest/image_bottom.png')

    def load(filename):
        np_image = Image.open(filename)
        np_image = np.array(np_image).astype('float32')
        np_image = resize(np_image, (100, 300, 3))
        #plt.imshow(np_image/255)
        np_image = np.expand_dims(np_image, axis=0)
        return np_image

    three_list = ['top','middle','bottom']
    resTot = []
    for t in three_list:
        image_name = 'forTest/image_'+t+'.png'
        image = load(image_name)
        
        # prediction
        pred = model.predict(image)
        #print(pred)
        decision = np.argmax(pred)
        print(t+' image')
        
        if decision == 0:
            print('Not ready to harvest yet. Probability: {}'.format(pred[0][0]))
            resTot.append((t, decision, pred[0][0]))
        else:
            print('Ready to harvest. Probability: {}'.format(pred[0][1]))
            resTot.append((t, decision, pred[0][1]))

    return resTot

def getImage():
    # TODO check robArm not moving
    # TODO check whell not moving
    rospy.wait_for_service('/imPro/getImg')
    try:
        getPic = rospy.ServiceProxy('/imPro/getImg', ImPro_getImg)
        return getPic()
    except rospy.ServiceException, e:
        rospy.logerr("Service call failed: %s", e)
        rospy.logwarn("Returned default image path")
        return '/home/pi/ros_catkin_ws/src/growbot_rpi/pictures/pic.jpg'


def srvHdl_imgProcessing(req):
    # TODO check if img processing available for given shelfID
    imageFilePath = getImage()
    res = checkRipeness(imageFilePath)

    potID = []
    decision = []
    probability = []
    shelfID = req.shelfID
    for rowRes in res :
        for i in range(0,_NB_POT_PER_ROW) :
            decision.append(bool(rowRes[_DECISION]))
            probability.append(rowRes[_PROBABILITY])
            potID.append(int(res.index(rowRes)*_NB_POT_PER_ROW + i))

    return {'shelfID' : shelfID, 'potID' : potID, 'descision' : decision, 'probability' : probability}


def subscribe():
    pass


def initPublisher():
    pass

def initServices():
    rospy.Service('/imPro/doImPro', ImPro_doImPro, srvHdl_imgProcessing)
    



def main():
    subscribe()
    initPublisher()
    initServices()
    rospy.loginfo("image_processing : Running...")
    rospy.spin()


if __name__ == '__main__':
    try:
        rospy.init_node('image_processing', anonymous=True)
        main()
    except rospy.ROSInterruptException:
        pass

