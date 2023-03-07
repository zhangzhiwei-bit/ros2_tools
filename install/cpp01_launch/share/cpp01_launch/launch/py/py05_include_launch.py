from launch_ros.actions import Node
from launch import LaunchDescription

from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from ament_index_python.packages import get_package_share_directory
import os
'''
文件包含实现，在当前launch文件中包含其它的launch文件
'''
def generate_launch_description():
    include = IncludeLaunchDescription(
        launch_description_source=PythonLaunchDescriptionSource(
            launch_file_path=os.path.join(
                get_package_share_directory("cpp01_launch"),
                "launch/py",
                "py04_args_launch.py"
            )
        ),
        launch_arguments=[("backg_r","80"),("backg_g","180"),("backg_b","150")]
    )
    return LaunchDescription([include])
