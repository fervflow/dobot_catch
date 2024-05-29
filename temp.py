def main():
    # Points in the webcam frame
    webcam_points = np.array([
        [23, 18],    # upper_left
        [24, 167],   # lower_left
        [453, 19],   # upper_right
        [456, 169]   # lower_right
    ], dtype=np.float32)

    # Corresponding points in the Dobot's coordinate system
    dobot_points = np.array([
        [196, -147],    # upper_left
        [307, -128],    # lower_left
        [154, 194],     # upper_right
        [270, 210]      # lower_right
    ], dtype=np.float32)

    # Calculate the homography matrix
    homography_matrix, _ = cv.findHomography(webcam_points, dobot_points)

    # Initialize Dobot
    dobot_arm = dobot.initialize_dobot()
    dobot.print_start_position(dobot_arm)

    # Coordinate destinations (you can adjust these as needed)
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
                last_coords = coord_handler.get_coords()
                last_coords_x, last_coords_y = last_coords[4], last_coords[5]
                translated_x, translated_y = translate_coords(last_coords_x, last_coords_y, homography_matrix)
                coords[0] = (translated_x, translated_y)
                dobot.agarrar_objeto(dobot_arm, coords[0], coords[1])
                coord_handler.set_coords(None)  # Reset after processing
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        dobot.close_dobot(dobot_arm)
        video_thread.join()

if __name__ == "__main__":
    main()