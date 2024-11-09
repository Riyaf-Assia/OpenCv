import numpy as np
import cv2

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
# Define the dimensions of the image
height, width = 480, 640  # Example: 480p image (480x640 pixels)




# Ensure you have the correct path to the Haar Cascade XML file
nbPlateClassifier = cv2.CascadeClassifier('assets/haarcascade_russian_plate_number.xml')

minArea = 500
count = 1

while True:
    success, img_original = cap.read()
    img_plate = np.zeros((height, width, 3), np.uint8)
    if not success:
        break

    imgGray = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
    plates = nbPlateClassifier.detectMultiScale(imgGray, 1.1, 4)

    for (x, y, w, h) in plates:
        area = w * h
        if area > minArea:
            cv2.rectangle(img_original, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)
            cv2.putText(img_original, "Plate", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            img_plate = img_original[y:y+h, x:x+w]
            cv2.imshow('Plate Number', img_plate)

    cv2.imshow("Output", img_original)
    if cv2.waitKey(1) & 0xFF == ord('s') & np.any(img_plate):
        cv2.imwrite('plates/Number_Plate_' + str(count) + '.png', img_plate)
        cv2.rectangle(img_original, (0, 300), (640, 550), (0, 255, 175), cv2.FILLED)
        cv2.putText(img_original, "SAVED!", (200, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imshow("Output", img_original)
        cv2.waitKey(500)
        count += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
