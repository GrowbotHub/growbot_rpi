#!/usr/bin/env python
import rospy
from growbot_tlc.msg import ImPro_img
from growbot_tlc.msg import ImPro_trig
from growbot_tlc.msg import ImPro_res

#img processing libs
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import scipy
from scipy.misc import imread
from keras.models import load_model
from skimage.transform import resize


# Constants
_MODEL_FILE = 'filename.model'
_NB_POT_PER_ROW = 4

_ROW_NAME = 0
_DECISION = 1
_PROBABILITY = 2

# Global variable
pub_res = 0


def checkRipeness(imgFileName):
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
    # check robArm not moving
    # check whell not moving
    # use srv to get image from swag interface
    #return file path to imagae
    return 'forTest/image1.jpg'


def imgProcessing(data):
    imageFilePath = getImage()
    res = checkRipeness(imageFilePath)
    for rowRes in res :
        for i in range(0,_NB_POT_PER_ROW) :
            msg_result = ImPro_res()
            msg_result.decision = rowRes[_DECISION]
            msg_result.probaility = rowRes[_PROBABILITY]
            msg_result.shelfID = 0 # TODO
            msg_result.potID = res.index(rowRes)*i
            pub_res.publish(msg_result)


def subscribe():
    pass


def initPublisher():
    global pub_res
    pub_res = rospy.Publisher('/imPro/res', ImPro_res, queue_size=10)



def main():
    subscribe()
    initPublisher()
    rospy.loginfo("image_processing : Running...")
    rospy.spin()


if __name__ == '__main__':
    try:
        rospy.init_node('image_processing', anonymous=True)
        main()
    except rospy.ROSInterruptException:
        pass

