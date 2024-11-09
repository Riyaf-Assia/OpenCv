import numpy as np
import cv2
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
#cap.set(10, 100)

myColors = [[20, 120, 190, 32, 199, 245], # yellow
            [0, 138 , 119, 6, 218, 227],  #red
            [105, 83, 50 , 129, 216, 248]] #blue

colors = [[51, 255, 255],
          [0,0,255],
          [255, 51, 51]]


My_points = [] ## [x, y, colorsId]

def findColor(img,myColors,colors):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    list_points = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = getContours(mask)
        #cv2.circle(imgResult, (x, y), 10,colors[count], cv2.FILLED)
        if x!= 0 and y!= 0 :
            list_points.append([x, y, count])
        count += 1
        #cv2.imshow(str(color[0]), mask)
    return list_points


def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500 :
            #cv2.drawContours(imgResult, cnt, -1, (0,255,0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02* peri, True)
            x, y, w, h = cv2.boundingRect(approx)

    return x + w//2, y

def drawCanvas(My_points, colors):
    for point in My_points:
        cv2.circle(imgResult, (point[0],point[1] ), 10,colors[point[2]], cv2.FILLED)



while True :
    success, img = cap.read()
    imgResult = img.copy()
    new_points = findColor(img, myColors, colors)
    if len(new_points) != 0:
        for pt in new_points:
            My_points.append(pt)
    if len(My_points) != 0:
        drawCanvas(My_points, colors)
    cv2.imshow("Result", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break