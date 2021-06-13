#! /usr/bin/python 
# -*- coding: utf-8 -*- 
#===============================================================================
# Date created  : 2021-06-13T09:21:05+09:00
# Date modified : 2021-06-13T09:21:44+09:00
# Author        : soundscope
# Description   : demo code for zemi-A, this code is released under MIT 
#===============================================================================

import cv2
import numpy as np


FILEPATH  = "test.png"

points2D = []
def chose_points(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        if (x,y) in points2D: print("error")
        else: 
            cv2.circle(copy_img,(x,y),5,(0,255,0), 2)
            if points2D != []:
                cv2.line(copy_img, points2D[-1],(x, y),(255,0,0,5),2)
            if len(points2D) == 3:
                cv2.line(copy_img, points2D[-1],(x, y),(255,0,0),2)
                cv2.line(copy_img, points2D[0],(x, y),(255,0,0),2)
            points2D.append((x,y))
        if len(points2D) == 5:
            cv2.namedWindow(winname="win2")
            new_img = perspectiveTransform(img)
            cv2.imshow("win2", new_img)

def perspectiveTransform(img):
    original = np.float32(points2D[:2] + points2D[2:4][::-1])
    (y, x, _) = img.shape
    trans = np.float32([[0,0], [x,0], [0,y], [x,y]])
    cv2.moveWindow('win2', x + 100, 100)

    M = cv2.getPerspectiveTransform(original, trans)
    return cv2.warpPerspective(img, M, (x, y))
#cv2.startWindowThread()

def make_window(copy_img):
    while True: 
        cv2.imshow("win1",copy_img)
        key = cv2.waitKey(10)
        if key == 27: break #ESC
        if key == ord('q'): break
        if cv2.getWindowProperty("win1", cv2.WND_PROP_AUTOSIZE) == -1: break
        if key == 13 and len(points2D) == 4: 
            new_img = perspectiveTransform(img)
            cv2.namedWindow(winname="win2")
            cv2.imshow("win2", new_img)

img = cv2.imread(FILEPATH)
copy_img = img.copy()
cv2.namedWindow(winname="win1")
cv2.moveWindow('win1', 1, 100)

cv2.setMouseCallback("win1", chose_points)

make_window(copy_img)

