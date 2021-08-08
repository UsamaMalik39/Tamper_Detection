#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 18:16:07 2020

@author: aliabdullah
"""

import cv2 as cv
import numpy as np

def transImage (inpImage, distance):
    """We create a transformation matrix  """
    outImage = np.zeros(inpImage.shape, dtype='u1')
    
    if ((distance[1] >= 0) and (distance[0] >= 0)):
        outImage[distance[1]:, distance[0]:] = inpImage[:(inpImage.shape[0]-distance[1]),:(inpImage.shape[1]-distance[0])]
    elif ((distance[1] >= 0) and (distance[0] < 0)):
        outImage[distance[1]:, :(inpImage.shape[1]-abs(distance[0]))] = inpImage[:(inpImage.shape[0]-distance[1]),abs(distance[0]):]
    elif ((distance[1] < 0) and (distance[0] >= 0)):
        outImage[:(inpImage.shape[0]-abs(distance[1])), distance[0]:] = inpImage[abs(distance[1]):,:(inpImage.shape[1]-distance[0])]
    else:
        outImage[:(inpImage.shape[0]-abs(distance[1])), :(inpImage.shape[1]-abs(distance[0]))] = inpImage[abs(distance[1]):,abs(distance[0]):]
    return outImage

def meanSquareDiff (imageRef,imageTamp,d):
    """sd """
    #d[1] =y -->rows ,d[0] =x -->columns
    if ((d[1] >= 0) and (d[0] >= 0)):
        sd = np.sum((imageRef[d[1]:,d[0]:].astype("float")- imageTamp[d[1]:,d[0]:].astype("float"))**2)
        return sd/(3*float((imageRef.shape[1]-d[1]) * (imageTamp.shape[0]-d[0])))
    
    elif ((d[1]<0) and (d[0] >= 0)):
        sd = np.sum((imageRef[:(imageRef.shape[1]+d[1]),d[0]:].astype("float")- imageTamp[: (imageTamp.shape[1]+d[1]),d[0]:].astype("float"))**2)
        return sd/(3*float((imageRef.shape[1]+d[1]) * (imageTamp.shape[0]-d[0])))
    
    elif(d[1]>=0 and d[0] <0):
        sd = np.sum((imageRef[d[1]:,:(imageRef.shape[0]+d[0])].astype("float")- imageTamp[d[1]:,:(imageTamp.shape[0]+d[0])].astype("float"))**2)
        return sd/(3*float((imageRef.shape[1]-d[1]) * (imageTamp.shape[0]+d[0])))
    
    else:
        sd = np.sum((imageRef[:(imageRef.shape[1]+d[1]),:(imageRef.shape[0]+d[0])].astype("float")- imageTamp[:(imageTamp.shape[1]+d[1]),:(imageTamp.shape[0]+d[0])].astype("float"))**2)
        return sd/(3*float((imageRef.shape[1]+d[1]) * (imageTamp.shape[0]+d[0])))


pathOneRef= "/home/aliabdullah/Downloads/DIP Assign/data/hw1_painting_2_reference.jpg" # change path for image One
imgRef = cv.imread(pathOneRef)
pathOneTamp= "/home/aliabdullah/Downloads/DIP Assign/data/hw1_painting_2_tampered.jpg" # change path for image One
imgTamp = cv.imread(pathOneTamp)

sqMeanNew = 0
sqMeanOld = 10000
xt = 0
yt = 0
for i in range(-10,10):
    for j in range(-10,10):
       nImgTamp = transImage(imgTamp,[i,j])
       sqMeanNew = meanSquareDiff(imgRef,nImgTamp,np.array([i,j]))
       if (sqMeanNew< sqMeanOld):
           sqMeanOld = sqMeanNew
           xt = j
           yt = i

newImageTamp  =transImage(imgTamp,[yt,xt])
print ("Mean Square Error = "+str(sqMeanOld)+ "\n displacement in x = " + str(xt)+"\ndisplacement in y = "+str(yt))
imgBinary = np.zeros((newImageTamp.shape[0],newImageTamp.shape[1],1))
image = cv.subtract(newImageTamp,imgRef)
imgGray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
(thresh, imgBinary) = cv.threshold(imgGray, 127, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
cv.imshow('image',imgBinary)
cv.waitKey(0)
cv.destroyAllWindows()