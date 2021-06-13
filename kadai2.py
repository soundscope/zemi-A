#! /usr/bin/python 
# -*- coding: utf-8 -*- 
#===============================================================================
# Date created  : 2021-06-13T09:20:40+09:00
# Date modified : 2021-06-13T10:22:40+09:00
# Author        : soundscope
# Description   : demo code zemi-A, This code is released under MIT
#===============================================================================

import cv2
import numpy as np
from math import *

importedImage = 'testX.png'
originalImg = cv2.imread(importedImage)
kernel = np.ones((3,3),np.uint8)
#erosion = cv2.erode(originalImg,kernel,iterations = 1)
edgeImg = cv2.Canny(originalImg, 75, 200)
dilation = cv2.dilate(edgeImg,kernel,iterations = 1)
key = cv2.waitKey(0)

contours, hierarchy = cv2.findContours(dilation, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
candidate_num = 5
contours = sorted(contours, key = lambda x:cv2.contourArea(x))[::-1][:candidate_num]
index = 0
def distance(x1,y1,x2,y2): return (x1 - x2) ** 2 + (y1 - y2) ** 2

new_contours = []
for cnt in contours:
    x,y,_ = originalImg.shape
    epsilon = 0.02*cv2.arcLength(cnt,True)
    approx = cv2.approxPolyDP(cnt,epsilon,True)
    approx = cv2.convexHull(approx)
    new_contours.append(approx)

contours = sorted(new_contours, key = lambda x:cv2.contourArea(x))[::-1][:candidate_num]
for approx in contours:
    vertex = [[10**10,0,0] for _ in range(4)]
    tmp_cp = originalImg.copy()
    cv2.drawContours(tmp_cp, [approx], 0, (0), 2)
    cv2.imwrite('debug'+ importedImage + str(index) + '.png', tmp_cp)
    cv2.imshow("win2", tmp_cp)
    key = cv2.waitKey(0)
    if len(approx) != 4:
        for _v in approx:
            for v in _v:
                x1, y1 = v[0], v[1]
                if distance(x1,y1,0,0) < vertex[0][0]:
                    vertex[0] = [distance(x1,y1,0,0),x1,y1]
                if distance(x1,y1,x,0) < vertex[1][0]:
                    vertex[1] = [distance(x1,y1,x,0),x1,y1]
                if distance(x1,y1,0,y) < vertex[2][0]:
                    vertex[2] = [distance(x1,y1,0,y),x1,y1]
                if distance(x1,y1,x,y) < vertex[3][0]:
                    vertex[3] = [distance(x1,y1,x,y),x1,y1]
        for i in vertex: del i[0]
      
        original = np.float32(vertex)
        area = cv2.contourArea(original)
        if area <  x * y * 0.0001: 
            vertex = [[10**10,0,0] for _ in range(4)]
            for _v in approx:
                for v in _v:
                    x1, y1 = v[0], v[1]
                    if distance(x1,y1,0,y/2) < vertex[0][0]:
                        vertex[0] = [distance(x1,y1,0,y/2),x1,y1]
                    if distance(x1,y1,x/2,0) < vertex[1][0]:
                        vertex[1] = [distance(x1,y1,x/2,0),x1,y1]
                    if distance(x1,y1,x/2,y) < vertex[2][0]:
                        vertex[2] = [distance(x1,y1,x/2,y),x1,y1]
                    if distance(x1,y1,x,y/2) < vertex[3][0]:
                        vertex[3] = [distance(x1,y1,x,y/2),x1,y1]
            for i in vertex: del i[0]
        
        original = np.float32(vertex)
        area = cv2.contourArea(original)
        if area <  x * y * 0.0001: continue
    else:
        minimum = (10**10,0)
        for i, _v in enumerate(approx):
            for v in _v:
                if minimum[0] > v[0] + v[1]:
                    minimum = (v[0] + v[1], i)
        sorted_array = []
        for i in range(2): 
            sorted_array.append(approx[(i+minimum[1])%4])
        for i in range(2,4)[::-1]: 
            sorted_array.append(approx[(i+minimum[1])%4])
        original = np.float32(sorted_array)
        area = cv2.contourArea(original)
        if area <  x * y * 0.0001: continue

    copy = originalImg.copy()
    (y, x, _) = originalImg.shape
    trans = np.float32([[0,0], [x,0], [0,y], [x,y]])
    M = cv2.getPerspectiveTransform(original, trans)
    new_img = cv2.warpPerspective(originalImg, M, (x, y))


    cv2.imwrite('result-'+ importedImage + str(index) + '.png', new_img)
    index += 1
