import numpy as np
import math
import cv2

# Load the pre-trained Haar Cascade classifier for hand detection
hand_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_upperbody.xml')

external_cam_index = 2  # Change this index accordingly

# Open the webcam (default webcam, can be changed if multiple webcams are connected)
cap = cv2.VideoCapture(external_cam_index, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_SETTINGS, 1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Couldn't open the webcam")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # If frame is not read correctly, exit the loop
    if not ret:
        print("Error: Can't receive frame from the webcam")
        break
    

    _, img = cap.read()
    cv2.rectangle(img, (500, 700), (100, 100), (0, 255, 0), 0) # 2 pts and 
    crop_img = img[100:300, 100:300]
    grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    value = (35, 35)
    blurred_ = cv2.GaussianBlur(grey, value, 0)
    _, thresholded = cv2.threshold(blurred_, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    contours, hierarchy = cv2.findContours(thresholded.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) # no need image
    count1 = max(contours, key=lambda x: cv2.contourArea(x))
    x, y, w, h = cv2.boundingRect(count1)
    cv2.rectangle(crop_img, (x, y), (x + w, y + h), (0, 0, 255), 0)
    hull = cv2.convexHull(count1)
    drawing = np.zeros(crop_img.shape, np.uint8)
    cv2.drawContours(drawing, [count1], 0, (0, 255, 0), 0)
    cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 0)
    hull = cv2.convexHull(count1, returnPoints=False)
    defects = cv2.convexityDefects(count1, hull)

    count_defects = 0
    cv2.drawContours(thresholded, contours, -1, (0, 255, 0), 3)

    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        start = tuple(count1[s][0])
        end = tuple(count1[e][0])
        far = tuple(count1[f][0])
        a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
        b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
        c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
        angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 57

        if angle <= 90:
            count_defects += 1
            cv2.circle(crop_img, far, 1, [0, 0, 255], -1)

        cv2.line(crop_img, start, end, [0, 255, 0], 2)

    if count_defects == 1:
        cv2.putText(img, "2 fingers", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255))
    elif count_defects == 2:
        str = "3 fingers"
        cv2.putText(img, str, (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
    elif count_defects == 3:
        cv2.putText(img, "4 fingers", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255))
    elif count_defects == 4:
        cv2.putText(img, "5 fingers", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255))
    elif count_defects == 0:
        cv2.putText(img, "one", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255))

    cv2.imshow('main window', img)
    all_img = np.hstack((drawing, crop_img))
    cv2.imshow('Contours', all_img)

    # cv2.imshow('Original', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()