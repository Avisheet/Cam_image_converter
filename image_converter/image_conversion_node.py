import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from std_srvs.srv import SetBool

class ImageConversionNode(Node):
    def __init__(self):
        super().__init__('image_conversion_node')
        
        # Declare parameters
        self.declare_parameter('input_image_topic', 'usb_cam/image_raw')
        self.declare_parameter('output_image_topic', '/image_converted')

        # Get parameters
        self.input_image_topic = self.get_parameter('input_image_topic').get_parameter_value().string_value
        self.output_image_topic = self.get_parameter('output_image_topic').get_parameter_value().string_value

        # Initialize variables
        self.bridge = CvBridge()
        self.mode = 2  # Default to color mode (Mode 2)

        # Subscriber and Publisher
        self.image_sub = self.create_subscription(Image, self.input_image_topic, self.image_callback, 10)
        self.image_pub = self.create_publisher(Image, self.output_image_topic, 10)

        # Service
        self.service = self.create_service(SetBool, 'change_mode', self.change_mode_callback)
        
        self.get_logger().info(f'ImageConversionNode started with mode: Color (2)')

    def change_mode_callback(self, request, response):
        # Switch mode
        if request.data:
            self.mode = 1
            self.get_logger().info('Mode changed to: Greyscale (1)')
        else:
            self.mode = 2
            self.get_logger().info('Mode changed to: Color (2)')
        response.success = True
        response.message = f'Mode changed to: {"Greyscale" if self.mode == 1 else "Color"}'
        return response

    def image_callback(self, msg):
        try:
            # Log input image info
            self.get_logger().info(f"Received image with encoding: {msg.encoding}")

            # Convert ROS image to OpenCV image
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

            # Log OpenCV image conversion success
            self.get_logger().info(f"Converted image to OpenCV format")

            # Apply conversion based on mode
            if self.mode == 1:
                cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

            # Display the image in a window
            if self.mode == 1:
                cv2.imshow("Converted Image (Grayscale)", cv_image)  # Show grayscale image
            else:
                cv2.imshow("Converted Image (RGB)", cv_image)  # Show color image

            # Wait for a key press and update the window
            cv2.waitKey(1)  # Wait for a short time to refresh the window

            # Convert OpenCV image back to ROS message
            ros_image = self.bridge.cv2_to_imgmsg(cv_image, encoding='mono8' if self.mode == 1 else 'bgr8')

            # Publish the converted image
            self.image_pub.publish(ros_image)

        except Exception as e:
            self.get_logger().error(f"Failed to process image: {e}")




def main(args=None):
    rclpy.init(args=args)
    node = ImageConversionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
