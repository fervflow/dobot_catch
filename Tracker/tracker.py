import cv2 as cv

from trackerEuclidian import EuclideanDistTracker

tracker = EuclideanDistTracker()

# cap = cv.VideoCapture('./Tracker/highway.mp4')
cap = cv.VideoCapture(0)

# map_objects = cv.createBackgroundSubtractorMOG2(history=100, varThreshold=20)
map_objects = cv.createBackgroundSubtractorKNN(history=100, dist2Threshold=600)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    roi = frame[340:800, 500:800]
    mask = map_objects.apply(roi)
    # Remove shadows
    _, mask_filtered = cv.threshold(mask, 254, 255, cv.THRESH_BINARY)
    contours, _ = cv.findContours(mask_filtered, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    # print(mask_grouping)

    found_objects = []
    for contour in contours:
        area = cv.contourArea(contour)
        if area > 150:
            x, y, w, h = cv.boundingRect(contour)
            found_objects.append([x, y ,w, h])

    box_ids = tracker.update(found_objects)
    for box in box_ids:
        x, y, w, h, id = box
        cv.putText(roi, str(id), (x, y), cv.FONT_ITALIC, 1, (255, 0, 0), 4)
        cv.rectangle(roi, (x, y), (w+x, h+y), (0, 255, 0), 4)

    cv.imshow('Original', frame)
    cv.imshow('Mask', mask)
    cv.imshow('Mask Filtered Binary', mask_filtered)

    if cv.waitKey(27) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
