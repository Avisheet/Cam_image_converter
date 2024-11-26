from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='usb_cam',
            executable='usb_cam_node_exe',
            name='usb_cam_node',
            output='screen',
            parameters=[
                {'camera_name': 'default_camera'},
                {'image_width': 640},
                {'image_height': 480},
            ],
            arguments=['/dev/video0'],  # Pass video device as an argument
        ),
        Node(
            package='image_converter',
            executable='image_conversion_node',
            name='image_conversion_node',
            output='screen',
            parameters=[
                {'input_topic': 'usb_cam/image_raw'},
                {'output_topic': '/image_converted'},
            ],
        ),
    ])
