import cv2 as cv
import numpy as np
from Tracker.trackerEuclidean import EuclideanDistTracker

BLUE = [(94, 80, 2), (120, 255, 255)]
GREEN = [(25, 52, 72), (102, 255, 255)]
RED = [(136, 87, 111), (180, 255, 255)]

BGR = {
    'blue': (255, 0, 0),
    'green': (0, 255, 0),
    'red': (0, 0, 255),
}

def detect_color(hsv_frame, color_bounds):
    color_lower = np.array(color_bounds[0], np.uint8)
    color_upper = np.array(color_bounds[1], np.uint8)
    color_mask = cv.inRange(hsv_frame, color_lower, color_upper)

    kernel = np.ones((5, 5), "uint8")
    color_mask = cv.dilate(color_mask, kernel)
    contours, _ = cv.findContours(color_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    coordinates = []
    for contour in contours:
        area = cv.contourArea(contour)
        if area > 1000:
            x, y, w, h = cv.boundingRect(contour)
            coordinates.append((x, y, w, h))
    
    return coordinates

def draw_objects(frame, objects, color_label):
    for (x, y, w, h, object_id) in objects:
        cv.rectangle(frame, (x, y), (x+w, y+h), BGR[color_label], 2)
        cv.putText(frame, f'{color_label} ID: {object_id}', (x, y-10), cv.FONT_HERSHEY_SIMPLEX, 1, BGR[color_label], 2)

def main():
    tracker = EuclideanDistTracker()
    cap = cv.VideoCapture('./video.mp4')

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        blue_coords = detect_color(hsv_frame, BLUE)
        green_coords = detect_color(hsv_frame, GREEN)
        red_coords = detect_color(hsv_frame, RED)

        all_objects = blue_coords + green_coords + red_coords
        tracked_objects = tracker.update(all_objects)

        blue_tracked = [(x, y, w, h, id) for (x, y, w, h, id) in tracked_objects if (x, y, w, h) in blue_coords]
        green_tracked = [(x, y, w, h, id) for (x, y, w, h, id) in tracked_objects if (x, y, w, h) in green_coords]
        red_tracked = [(x, y, w, h, id) for (x, y, w, h, id) in tracked_objects if (x, y, w, h) in red_coords]

        draw_objects(frame, blue_tracked, 'blue')
        draw_objects(frame, green_tracked, 'green')
        draw_objects(frame, red_tracked, 'red')

        cv.imshow('Frame', frame)

        if cv.waitKey(20) == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()