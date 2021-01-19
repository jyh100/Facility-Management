#!/usr/bin/env python3.6.8
# -*- coding: utf-8 -*-
# Copyright:    Yuhan Jiang
# Email:        yuhan.jiang@marquette.edu
# Date:         11/05/2020
# Discriptions : image_label augmentation with projection

import numpy as np
import cv2 as cv
import random
import Image_Color_Adjustment as ColorAdj

img=cv.imread('D:/CentOS/Drawing/M1/M1.png')
label=cv.imread('D:/CentOS/Drawing/M1/M1Label_image.jpg')
def find_margin_corners(img,qsize=128,savefile_bool=True):#return x,y
    margin_map=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    imgH,imgW=margin_map.shape[0:2]
    min_x,max_x,min_y,max_y=0,imgW,0,imgH
    for i in range(1,imgW-1):
        min_x=i
        if np.any(margin_map[:,i]!=255):
            #print("Left M",i)
            break
    for i in range(imgW-1,1,-1):
        max_x=i
        if np.any(margin_map[:,i]!=255):
            #print("Right M",i)
            break
    for i in range(1,imgH-1):
        min_y=i
        if np.any(margin_map[i,:]!=255):
            #print("Upper M",i)
            break
    for i in range(imgH-1,1,-1):
        max_y=i
        if np.any(margin_map[i,:]!=255):
            #print("Bottom M",i)
            break
    if savefile_bool:
        #print('Keep Whilte Margin to be mutiple of 32-pixel')
        if (max_x-min_x)%qsize!=0:
            max_x=min_x+int((max_x-min_x)/qsize+1)*qsize
        if (max_y-min_y)%qsize!=0:
            max_y=min_y+int((max_y-min_y)/qsize+1)*qsize
    print(min_x,max_x,min_y,max_y)
    return min_x,max_x,min_y,max_y
def image_label_augmentation(img,label):

    height,width=img.shape[:2]
    rdmflip=random.randint(0,1)
    if rdmflip:
        img=cv.flip(img,1) #Flipped Horizontally
        label=cv.flip(label,1)
    #        img=cv.flip(img,0)#Flipped Vertically
    #        hv_flip=cv.flip(img,-1)    Flipped Horizontally & Vertically
    #        M=cv.getRotationMatrix2D((width/2,height/2),45,1)        img=cv.warpAffine(img,M,(width,height),borderValue=(255,255,255))# rotation 45 degrees
    rdms=1/10*random.randint(5,10)
    img=cv.resize(img,(int(rdms*width),int(rdms*height)))#resize
    label=cv.resize(label,(int(rdms*width),int(rdms*height)))
    #region Perspective
    rows,cols=img.shape[:2]
    rdmp=random.randint(0,3)
    c=1/10*random.randint(1,10)
    if rdmp==0:
        a1=cols/10*random.randint(1,4)
        a2=cols/10*random.randint(6,9)
        SrcPointsA=np.float32([[0,0],[cols,0],[0,rows],[cols,rows]])# up fix
        CanvasPointsA=np.float32([[0,0],[cols,0],[a1,rows*c],[a2,rows*c]])
        PerspectiveMatrix = cv.getPerspectiveTransform(np.array(SrcPointsA), np.array(CanvasPointsA))
    elif rdmp==1:
        a1=cols/10*random.randint(1,4)
        a2=cols/10*random.randint(6,9)#cols-a1
        SrcPointsA=np.float32([[0,0],[cols,0],[0,rows],[cols,rows]])# bottom fix
        CanvasPointsA=np.float32([[a1,rows*(1-c)],[a2,rows*(1-c)],[0,rows],[cols,rows]])
        PerspectiveMatrix = cv.getPerspectiveTransform(np.array(SrcPointsA), np.array(CanvasPointsA))
    elif rdmp==2:
        b1=rows/10*random.randint(1,4)
        b2=rows/10*random.randint(6,9)#rows-b1
        SrcPointsA=np.float32([[0,0],[cols,0],[0,rows],[cols,rows]])# left fix
        CanvasPointsA=np.float32([[0,0],[cols*c,b1],[0,rows],[cols*c,b2]])
        PerspectiveMatrix = cv.getPerspectiveTransform(np.array(SrcPointsA), np.array(CanvasPointsA))
    elif rdmp==3:
        b1=rows/10*random.randint(1,4)
        b2=rows/10*random.randint(6,9)#rows-b1
        SrcPointsA=np.float32([[0,0],[cols,0],[0,rows],[cols,rows]])# right fix
        CanvasPointsA=np.float32([[cols*(1-c),b1],[cols,0],[cols*(1-c),b2],[cols,rows]])
        PerspectiveMatrix = cv.getPerspectiveTransform(np.array(SrcPointsA), np.array(CanvasPointsA))
    img=cv.warpPerspective(img,PerspectiveMatrix,(cols,rows),borderValue=(255,255,255))
    label=cv.warpPerspective(label,PerspectiveMatrix,(cols,rows),borderValue=(255,255,255))
    #endregion
    img=ColorAdj.Image_Color_Adjustment(img)
    min_x,max_x,min_y,max_y=find_margin_corners(np.array(img),qsize=128,savefile_bool=True)
    return img[min_y:max_y,min_x:max_x],label[min_y:max_y,min_x:max_x]

#=============================================================================
import time
if __name__ == '__main__':
    for i in range(1):
        imgA,labelA=image_label_augmentation(img,label)
        cv.imshow("iamge"+str(i),imgA)
        cv.imshow("label"+str(i),labelA)
    cv.waitKey(0)
    time.sleep(2)
