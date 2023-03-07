from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

'''
    在launch文件启动时动态的设置turtlesim_node的背景颜色
'''

def generate_launch_description():
    bg_r = DeclareLaunchArgument(name="backg_r",default_value="255")
    bg_g = DeclareLaunchArgument(name="backg_g",default_value="255")
    bg_b = DeclareLaunchArgument(name="backg_b",default_value="255")
    turtle = Node(
        package="turtlesim",
        executable="turtlesim_node",
        parameters=[{
            "background_r":LaunchConfiguration("backg_r"),
            "background_g":LaunchConfiguration("backg_g"),
            "background_b":LaunchConfiguration("backg_b")
            }]
    )
    # ros2 launch cpp01_launch py04_args_launch.py backg_r:=0
    return LaunchDescription([bg_r,bg_g,bg_b,turtle])