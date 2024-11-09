import numpy as np
import cv2


# fct to return the extreme external contours
def getContours(image):

    contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return contours

# fct to draw the contours
def drawContours(img_contours,img_draw):

    contours = getContours(img_contours)
    cv2.drawContours(img_draw, contours, -1, (0, 255, 0), 3) # green contour, # -1 to draw all the contours


# fct to calculate the area of the shapes :

def areaContours(img):

    contours = getContours(img)
    for i,cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        print(f'the area of the shape number {i} is : {area}')


# fct to detect the shapes :

def detectShape(img_contours,img_draw):

    contours = getContours(img_contours)

    for i,cnt in enumerate(contours):

        # get the contour approximative points of the contour
        # calcuate the length of the curves :
        curves = cv2.arcLength(cnt, True) #assuming the shapes are closed
        approx_points = cv2.approxPolyDP(cnt, 0.02*curves, True) # 0.02 can be chaged
        x,y,w,h = cv2.boundingRect(approx_points)
        # draw the bounding Rectangle
        cv2.rectangle(img_draw,(x,y),(x+w,y+h),(255,0,0,3))
        cnt_number_corners = len(approx_points)
        if cnt_number_corners == 3 :
            shape = "tri"
        elif cnt_number_corners == 4 :
            ratio = w/float(h)
            if ratio > 0.95 and ratio < 1.05 : shape = "square"
            else : shape = "rectangle"
        elif cnt_number_corners > 4 : shape = "circle"
        else : shape = "Undefined"
        # draw the name of the shape :
        cv2.putText(img_draw,shape,(x+(w//2) - 10 ,y+(h//2)),cv2.GShape_GOPAQUE, 0.5,(0,0,0),2)



img = cv2.imread('assets/shapes.png')
img = cv2.resize(img,(500,500))
img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(img_grey, (7,7), 1)
imgCanny = cv2.Canny(imgBlur, 50, 50)

copyImage = img.copy()

cv2.imshow('original image', img)
#cv2.imshow('grey image', img_grey)
#cv2.imshow('blurred image', imgBlur)
#cv2.imshow('Canny image', imgCanny)
#cv2.imshow('Copy_canny image', copyImage)


cv2.waitKey(0)
drawContours(imgCanny, copyImage)
cv2.imshow('image with contours', copyImage)
detectShape(imgCanny, copyImage)
cv2.imshow('image with contours', copyImage)
cv2.waitKey(0)




