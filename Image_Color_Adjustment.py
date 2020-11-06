#!/usr/bin/env python3.6.8
# -*- coding: utf-8 -*-
# Copyright:    Yuhan Jiang
# Email:        yuhan.jiang@marquette.edu
# Date:         11/05/2020
# Discriptions : image brightness / color/ contrast/ sharpness adjustment
from PIL import Image
from PIL import ImageEnhance
import cv2 as cv
import random
import numpy as np

def Image_Color_Adjustment(image):# input bgr, provess by rgb , covert back and return bgr
    image=cv.cvtColor(image,cv.COLOR_BGR2RGB)
    image=Image.fromarray(image.astype('uint8'),'RGB')

    rdmbright=random.randint(0,3)
    if rdmbright==0:#birght
        enh_bri=ImageEnhance.Brightness(image)
        brightness=1.5
        image=enh_bri.enhance(brightness)
    elif rdmbright==1:# color
        enh_col=ImageEnhance.Color(image)
        color=1.5
        image=enh_col.enhance(color)
    elif rdmbright==2:# contrast
        enh_con=ImageEnhance.Contrast(image)
        contrast=1.5
        image=enh_con.enhance(contrast)
    elif rdmbright==3:# sharpness
        enh_sha=ImageEnhance.Sharpness(image)
        sharpness=3.0
        image=enh_sha.enhance(sharpness)
    image=np.array(image)
    image=cv.cvtColor(image,cv.COLOR_RGB2BGR)
    return image
#=============================================================================
import time
if __name__ == '__main__':
    image=cv.imread('D:/CentOS/Drawing/M1/M1.png')
    for i in range(20):
        imgA=Image_Color_Adjustment(image)
        cv.imshow("image"+str(i),imgA)
    cv.waitKey(0)
    time.sleep(2)
