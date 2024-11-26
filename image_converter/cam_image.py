import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

class CameraNode(Node):
    def __init__(self, mode='gray'):
        super().__init__('camera_node')
        self.publisher_ = self.create_publisher(Image, '/image_converted', 10)
        self.bridge = CvBridge()
        self.capture = cv2.VideoCapture(0)  # Use 0 for the default laptop webcam

        if not self.capture.isOpened():
            self.get_logger().error('Could not open camera')
            return

        self.mode = mode  # Set the mode to the provided argument (default 'gray')

        self.timer = self.create_timer(0.1, self.timer_callback)  # Timer to read and publish images at a fixed rate

    def timer_callback(self):
        ret, frame = self.capture.read()  # Read a frame from the webcam
        if not ret:
            self.get_logger().error('Failed to capture image')
            return

        # Convert the image based on the selected mode
        if self.mode == 'gray':
            converted_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
            encoding = "mono8"
        elif self.mode == 'rgb':
            converted_image = frame  # Use the original RGB image
            encoding = "bgr8"
        else:
            self.get_logger().error(f"Unknown mode: {self.mode}")
            return

        # Convert the OpenCV image (numpy array) to ROS Image message
        ros_image = self.bridge.cv2_to_imgmsg(converted_image, encoding=encoding)
        self.publisher_.publish(ros_image)

        # Display the image in OpenCV window
        cv2.imshow("Converted Image", converted_image)
        cv2.waitKey(1)  # Refresh the window every frame

def main(args=None):
    rclpy.init(args=args)

    # Prompt the user to select a mode
    print("Select Mode:")
    print("1: Greyscale")
    print("2: Color (RGB)")

    choice = input("Enter mode number (1/2): ").strip()

    if choice == '1':
        mode = 'gray'  # Greyscale mode
    elif choice == '2':
        mode = 'rgb'   # Color (RGB) mode
    else:
        print("Invalid choice! Defaulting to greyscale mode.")
        mode = 'gray'  # Default to grayscale if invalid input

    # Start the camera node with the selected mode
    camera_node = CameraNode(mode=mode)

    try:
        rclpy.spin(camera_node)  # Keeps the node running
    except KeyboardInterrupt:
        pass
    finally:
        camera_node.capture.release()  # Release the camera when done
        cv2.destroyAllWindows()  # Close OpenCV windows
        rclpy.shutdown()

if __name__ == '__main__':
    main()
