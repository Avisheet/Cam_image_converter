from setuptools import setup, find_packages
import os
from glob import glob

package_name = 'image_converter'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    install_requires=['setuptools', 'cv_bridge', 'usb_cam'],
    zip_safe=True,
    maintainer='Avisheet Srivastava',
    maintainer_email='avisheetsrivastava@gmail.com',
    description='A package for converting camera images in ROS 2',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'image_conversion_node = image_converter.image_conversion_node:main',
            'cam_image = image_converter.cam_image:main',
        ],
    },
    data_files=[
        # Install the package index marker
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        # Install the package.xml
        ('share/' + package_name, ['package.xml']),
        # Install the launch files
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
    ],
)
