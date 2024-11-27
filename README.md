# Image Converter ROS 2 Package

This ROS 2 package provides functionality to stream images from a USB or laptop camera, convert the images between grayscale and RGB modes, and republish them.
The package allows users to switch between the modes dynamically using a ROS 2 service. In the future, AI-based detection can be integrated to process the images further.

## Features
  - **Camera Support**: Streams images from both USB and laptop cameras.
  - **Image Conversion**: Converts the images between grayscale and RGB modes.
  - **Dynamic Mode Switching**: Allows users to change between grayscale and RGB modes via a ROS 2 service.

## Dependencies

  - ROS 2 (any distribution, e.g., Foxy, Galactic, Humble)
  - usb_cam package (for USB camera support)
  - cv_bridge (for converting between ROS images and OpenCV images)
  - sensor_msgs (for image message types)
  - std_srvs (for creating ROS 2 services)

## Installation Instructions

**Install the usb_cam package (if using a USB camera):**

```

sudo apt install ros-<ros2-distro>-usb-cam

```
Replace <ros2-distro> with your ROS 2 distribution (e.g., foxy, galactic, humble).

**Create the ROS 2 package:**

```

ros2 pkg create --build-type ament_python image_converter --dependencies rclpy sensor_msgs cv_bridge std_srvs

```

**Clone or download the image_converter package into your ROS workspace and build the package:**

```

git clone https://github.com/Avisheet/Cam_image_converter.git

```


## Launching the Nodes

**1. To launch the USB camera node and the image conversion node, use the following launch command:**

```

ros2 launch image_converter image_conversion_launch.py

```

This will start:

  - The usb_cam node to stream images from the camera.
  - The image_conversion_node to convert and publish images in grayscale or RGB modes.

**2. Using the Laptop Camera**

If you want to use the laptop camera instead of a USB camera, you can run the following Python file directly. This will allow you to capture images from your laptop's webcam and process them:

```

ros2 run image_converter cam_image.py

```

This will start the camera stream from the laptop's webcam and process the images as per the selected mode (grayscale or RGB).


**3. Changing Modes**

You can change the image conversion mode (between grayscale and RGB) using the following ROS 2 service calls:

- To switch to grayscale (mode 1):


```

ros2 service call /change_mode std_srvs/srv/SetBool "{data: true}"

```

- To switch back to RGB (color mode, mode 2):
  
```

ros2 service call /change_mode std_srvs/srv/SetBool "{data: false}"

```
