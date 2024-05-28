import cv2 as cv
import numpy as np

cap = cv.VideoCapture('./video.mp4')
# cap = cv.VideoCapture(0)

RED = [(136, 87, 111), (180, 255, 255)]
GREEN = [(25, 52, 72), (102, 255, 255)]
BLUE = [(94, 80, 2), (120, 255, 255)]

RGB = {
    'red': (0, 0, 255),
    'green': (0, 255, 0),
    'blue': (255, 0, 0),
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

def draw_objects(frame, coordinates, label_color):
    for coordinate in coordinates:
        x, y, w, h, _, _ = coordinate
        cv.rectangle(frame, (x, y), (x+w, y+h), RGB[label_color], 2)
        cv.putText(frame, label_color, (x, y-10), cv.FONT_HERSHEY_SIMPLEX, 1, RGB[label_color], 2)

frame_count = -1
frame_interval = 10

last_blue_coords = []
last_red_coords = []
last_green_coords = []

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_count += 1
    if frame_count % frame_interval == 0:
        hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        
        last_red_coords = detect_color(hsv_frame, RED)
        last_green_coords = detect_color(hsv_frame, GREEN)
        last_blue_coords = detect_color(hsv_frame, BLUE)
        
        if last_blue_coords:
            print(f"Blue object coordinates: {last_blue_coords}")

    draw_objects(frame, last_red_coords, 'red')
    draw_objects(frame, last_green_coords, 'green')
    draw_objects(frame, last_blue_coords, 'blue')

    cv.imshow("Original", frame)

    if cv.waitKey(27) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
