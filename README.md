# Artificial Vision and Robotic Arm Object Classification

## Introduction
This project involves developing an artificial vision system for color-based object detection, using a Dobot Magician robotic arm for object classification. The object detection is performed using a static webcam that captures real-time images, which are processed to identify the positions of specific colored objects. Based on the coordinates provided by the vision system, the robotic arm grabs and moves the objects to predefined locations.

## Objective
The main objective of this project is to implement an automated system that combines artificial vision and robotics for color-based object classification. Specifically, the goals are:
- Develop an algorithm capable of detecting specific colored objects using a webcam.
- Implement control of a robotic arm to grab and move the detected objects to determined positions.
- Efficiently integrate both systems to achieve automatic object classification.

## Project Development
### Algorithms and Libraries
Several key libraries and algorithms were used for the implementation of this project:

- **OpenCV**: Used for image processing and color detection. OpenCV (Open Source Computer Vision Library) is a computer vision library providing tools for capturing and processing images.
- **NumPy**: Used for handling mathematical operations and matrices, essential for image processing and transformation calculations.
- **pydobot**: Library used for communication and control of the Dobot Magician robotic arm.

### Color Detection Algorithm
The color detection algorithm converts the captured image from the camera to the HSV (Hue, Saturation, Value) color space. Color masks are applied to identify specific regions in the image. The contours of these regions are detected, and their central coordinates are calculated.

### Coordinate Transformation
To transform the coordinates from the camera's frame to the Dobot's coordinate system, a homography matrix is used. This transformation considers the spatial relationship between the two coordinate systems.

### System Integration
The system integrates color detection with robotic arm control. When an object is detected and the 'b' key is pressed, the coordinates of the object are transformed and sent to the robotic arm to perform the grab and move action.

## Conclusion
The project demonstrated the feasibility of integrating artificial vision and robotics for automated color-based object classification. The results show that the system can accurately detect and classify objects. However, areas for improvement were identified, such as camera and robotic arm calibration to increase precision and system robustness. Future improvements could include implementing machine learning algorithms to enhance object detection and classification.

## Additional Information
- **Webcam Resolution**: The webcam used had a resolution of 800x600 (4:3).
- **Demo Video**: [demo](./demo.mp4).
