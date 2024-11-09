import numpy as np
import cv2

def empty(a) :
    pass


path = 'assets/car.jfif'
cv2.namedWindow('TrackBars')
cv2.resizeWindow('TrackBars', 640, 240)
cv2.createTrackbar('Hue Min', 'TrackBars', 0, 179, empty)
cv2.createTrackbar('Hue Max', 'TrackBars', 63, 179, empty)
cv2.createTrackbar('Sat Min', 'TrackBars', 44, 255, empty)
cv2.createTrackbar('Sat Max', 'TrackBars', 255, 255, empty)
cv2.createTrackbar('Val Min', 'TrackBars', 121, 255, empty)
cv2.createTrackbar('Val Max', 'TrackBars', 255, 255, empty)


while True:
    img = cv2.imread(path)
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos('Hue Min', 'TrackBars')
    h_max = cv2.getTrackbarPos('Hue Max', 'TrackBars')
    sat_min = cv2.getTrackbarPos('Sat Min', 'TrackBars')
    sat_max = cv2.getTrackbarPos('Sat Max', 'TrackBars')
    val_min = cv2.getTrackbarPos('Val Min', 'TrackBars')
    val_max = cv2.getTrackbarPos('Val Max', 'TrackBars')
    print(h_min, h_max, sat_min, sat_max, val_min, val_max)
    lower = np.array([h_min, sat_min, val_min])
    upper = np.array([h_max, sat_max, val_max])
    mask = cv2.inRange(imgHSV, lower, upper)
    result = cv2.bitwise_and(img, img, mask=mask)


    cv2.imshow("original", img)
    cv2.imshow("HSV", imgHSV)
    cv2.imshow("mask", mask)
    cv2.imshow("result", result)
    cv2.waitKey(1)
