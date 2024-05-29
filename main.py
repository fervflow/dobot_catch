import threading
import dobot
import color
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
    # Point in the webcam frame
    webcam_point = np.array([[x, y]], dtype=np.float32)
    webcam_point = np.array([webcam_point])

    # Transform the point using the homography matrix
    dobot_point = cv.perspectiveTransform(webcam_point, homography_matrix)

    return dobot_point[0][0][0], dobot_point[0][0][1]

def main():
    # Initialize Dobot
    dobot_arm = dobot.initialize_dobot()
    dobot.print_position(dobot_arm)

    coords = [
        (0, 0),  # Placeholder for origin (x, y)
        (180, -200)  # Destination (x, y)
    ]
    
    coord_handler = CoordHandler()

    # Start the video feed in a separate thread
    video_thread = threading.Thread(target=color.main_loop, args=(coord_handler.set_coords,))
    video_thread.start()

    try:
        while True:
            if coord_handler.get_coords():
                last_coords_x = coord_handler.get_coords()[4] - 59
                last_coords_y = coord_handler.get_coords()[5] - 109
                coords[0] = (last_coords_x, last_coords_y)
                print()
                dobot.agarrar_objeto(dobot_arm, coords[0], coords[1], 0)
                coord_handler.set_coords(None)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        dobot.close_dobot(dobot_arm)
        video_thread.join()

if __name__ == "__main__":
    main()
