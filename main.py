import threading
import dobot
import color

class CoordHandler:
    def __init__(self):
        self.last_coords = None

    def set_coords(self, coords):
        self.last_coords = coords

    def get_coords(self):
        return self.last_coords

def main():
    # Initialize Dobot
    dobot_arm = dobot.initialize_dobot()
    dobot.print_position(dobot_arm)

    # Coordinate destinations (you can adjust these as needed)
    coords = [
        (0, 0),  # Placeholder for origin (x, y)
        (180, -200)  # Destination (x, y)
    ]
    # 181, 78
    # 240, 187
    # -59, -109
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
                coord_handler.set_coords(None)  # Reset after processing
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        dobot.close_dobot(dobot_arm)
        video_thread.join()

if __name__ == "__main__":
    main()
