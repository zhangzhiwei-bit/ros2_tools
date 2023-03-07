from launch_ros.actions import Node
from launch import LaunchDescription

# 获取功能包下的share路径
from ament_index_python.packages import get_package_share_directory

import os

def generate_launch_description():
    turtle1 = Node(
        package="turtlesim",
        executable="turtlesim_node",
        exec_name="my_label",#设置程序标签
        ros_arguments=["--remap","__ns:=/t2"]
        #执行时 ros2 run turtlesim turtlesim_node --ros-args --remap __ns:=/t2
        )
    turtle2 = Node(
        package="turtlesim",
        executable="turtlesim_node",
        name="turtle2",
        # 方式一
        # parameters=[{"background_r":255,"background_g":0,"background_b":0}]
        # 方式二 读取yaml文件
        parameters=[os.path.join(get_package_share_directory("cpp01_launch"),"config","turtle2.yaml")]
        )
    return LaunchDescription([turtle2])

"""
导出yaml文件可以使用命令
ros2 param dump turtle2 --output-dir src/cpp01_launch/config
"""