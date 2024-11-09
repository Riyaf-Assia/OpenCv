import numpy as np
import cv2

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)


def preprocess(frame):
    imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imgBlurr = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlurr, 200, 200)
    kernel = np.ones((5, 5))
    imgDilation = cv2.dilate(imgCanny, kernel, iterations=2)
    imgEroded = cv2.erode(imgDilation, kernel, iterations=1)
    return imgEroded


def getContours(img, imgResult):
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    maxArea = 0
    biggestContour = np.array([])
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 5000:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            if len(approx) == 4 and area > maxArea:
                maxArea = area
                biggestContour = approx
    if biggestContour.size != 0:
        for point in biggestContour:
            cv2.circle(imgResult, tuple(point[0]), 5, (255, 0, 0), 6, cv2.FILLED)
    return biggestContour


def reorderPoints(biggsetContour):
    if biggsetContour.size == 0:
        return np.array([])  # Return an empty array if there is no contour
    new_points = []
    next_points = np.zeros((4, 2), dtype=np.float32)
    for point in biggsetContour:
        new_points.append(list(point[0]))
    new_points = np.array(new_points)
    tab_sum = np.sum(new_points, axis=1)
    tab_diff = np.diff(new_points, axis=1)
    next_points[0] = new_points[np.argmin(tab_sum)]
    next_points[3] = new_points[np.argmax(tab_sum)]
    next_points[1] = new_points[np.argmin(tab_diff)]
    next_points[2] = new_points[np.argmax(tab_diff)]
    return next_points


def wrapImage(img, new_approx):
    pts1 = new_approx
    pts2 = np.float32([[0, 0], [frameWidth, 0], [0, frameHeight], [frameWidth, frameHeight]])
    transform_matrix = cv2.getPerspectiveTransform(pts1, pts2)
    out_img = cv2.warpPerspective(img, transform_matrix, (frameWidth, frameHeight))
    # add code to resize it a little bit !
    return out_img


while True:
    success, img_original = cap.read()
    if not success:
        break
    imgResult = img_original.copy()
    result_img = preprocess(img_original)
    approx = getContours(result_img, imgResult)
    # approx could be an empty numpy array ! and we won't have the corners in the result image !
    new_approx = reorderPoints(approx)
    # if approx is empty there are no re-ordered points
    if new_approx.size != 0:
        output_image = wrapImage(img_original, new_approx)
    else:
        output_image = img_original

    cv2.imshow("Original image", img_original)
    cv2.imshow("Pre-processed image", result_img)
    cv2.imshow("Image corners", imgResult)
    cv2.imshow("Output", output_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
