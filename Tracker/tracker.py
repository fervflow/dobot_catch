import cv2 as cv
from .trackerEuclidean import EuclideanDistTracker

class Tracker:
    def __init__(self, video_source=0):
        self.tracker = EuclideanDistTracker()
        self.cap = cv.VideoCapture(video_source)
        self.map_objects = cv.createBackgroundSubtractorKNN(history=150, dist2Threshold=200)

    def process_frame(self, frame):
        roi = frame[100:520, 200:880]
        mask = self.map_objects.apply(roi)
        _, mask_filtered = cv.threshold(mask, 254, 255, cv.THRESH_BINARY)
        contours, _ = cv.findContours(mask_filtered, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        found_objects = []
        for contour in contours:
            area = cv.contourArea(contour)
            if area > 1000:
                x, y, w, h = cv.boundingRect(contour)
                found_objects.append([x, y, w, h])

        box_ids = self.tracker.update(found_objects)
        for box in box_ids:
            x, y, w, h, id = box
            cv.putText(roi, f'ID {id}', (x, y+10), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return frame, box_ids

    def release(self):
        self.cap.release()
        cv.destroyAllWindows()