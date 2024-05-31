import threading
import dobot
import cam
import cv2 as cv
import numpy as np

class CoordHandler:
    def __init__(self):
        self.last_coords = None

    def set_coords(self, coords):
        self.last_coords = coords

    def get_coords(self):
        return self.last_coords
    
def translate_coords(x, y, homography_matrix):
    webcam_point = np.array([[x, y]], dtype=np.float32)
    webcam_point = np.array([webcam_point])

    # Transform the point using the homography matrix
    dobot_point = cv.perspectiveTransform(webcam_point, homography_matrix)

    dobot_x, dobot_y = dobot_point[0][0]
    
    # return dobot_point[0][0][0], dobot_point[0][0][1]
    return dobot_y, dobot_x

def main():
    webcam_points = np.array([
        [22, 10],    # upper_left
        [22, 169],   # lower_left
        [460, 18],   # upper_right
        [460, 172]   # lower_right
    ], dtype=np.float32)

    dobot_points = np.array([
        [170, -172],    # upper_left
        [294, -161],    # lower_left
        [167, 174],     # upper_right
        [290, 190]      # lower_right
    ], dtype=np.float32)

    # Calculate the homography matrix
    homography_matrix, _ = cv.findHomography(webcam_points, dobot_points)
    
    # Initialize Dobot
    dobot_arm = dobot.initialize_dobot()
    dobot.print_position(dobot_arm)

    coords = [
        (0, 0),  # Placeholder for origin (x, y)
        (180, -200)  # Destination (x, y)
    ]
    
    coord_handler = CoordHandler()

    # Start the video feed in a separate thread
    video_thread = threading.Thread(target=cam.main_loop, args=(coord_handler.set_coords,))
    video_thread.start()

    try:
        while True:
            if coord_handler.get_coords():
                last_coods = coord_handler.get_coords()
                last_x = last_coods[4]
                last_y = last_coods[5]
                new_x, new_y = translate_coords(last_x, last_y, homography_matrix)
                coords[0] = (new_x, new_y)
                print()
                dobot.agarrar_objeto(dobot_arm, coords[0], coords[1], 90)
                coord_handler.set_coords(None)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        dobot.close_dobot(dobot_arm)
        video_thread.join()

if __name__ == "__main__":
    main()
