import cv2 as cv
import numpy as np
from Tracker.tracker import Tracker

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
    contornos, _ = cv.findContours(color_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    coordinates = []
    for contorno in contornos:
        area = cv.contourArea(contorno)

        if area > 1000:
            x, y, w, h = cv.boundingRect(contorno)
            x_center = x + w//2
            y_center = y + h//2
            coordinates.append((x, y, w, h, x_center, y_center))

    return coordinates

def draw_contours(frame, coordinates, label_color):
    for coordinate in coordinates:
        x, y, w, h, _, _ = coordinate
        cv.rectangle(frame, (x, y), (x+w, y+h), BGR[label_color], 2)
        cv.putText(frame, label_color, (x, y-10), cv.FONT_HERSHEY_SIMPLEX, 1, BGR[label_color], 2)


def main_loop():
    tracker = Tracker(video_source='./video.mp4')

    while True:
        ret, frame = tracker.cap.read()
        if not ret:
            break
        
        frame, box_ids = tracker.process_frame(frame)
        hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        blue_coords = detect_color(hsv_frame, BLUE)
        green_coords = detect_color(hsv_frame, GREEN)
        red_coords = detect_color(hsv_frame, RED)
            
        for box in box_ids:
            x, y, w, h, id = box
            for coords in [blue_coords, green_coords, red_coords]:
                for (cx, cy, _, _, x_center, y_center) in coords:
                    if x < x_center < x + w and y < y_center < y + h:
                        color_label = "blue" if coords == blue_coords else "green" if coords == green_coords else "red"
                        cv.putText(frame, f'ID {id} {color_label}', (x, y-10), cv.FONT_HERSHEY_SIMPLEX, 1, BGR[color_label], 2)

        draw_contours(frame, blue_coords, 'blue')
        draw_contours(frame, green_coords, 'green')
        draw_contours(frame, red_coords, 'red')

        cv.imshow("Original", frame)
        
        if cv.waitKey(20) & 0xFF == ord('q'):
            break

    tracker.release()

if __name__ == "__main__":
    main_loop()
    