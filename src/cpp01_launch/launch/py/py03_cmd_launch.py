from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import ExecuteProcess

# 生成turtlesim_node节点，并调用指令打印乌龟的位姿信息

def generate_launch_description():

    turtle = Node(
        package = "turtlesim",
        executable = "turtlesim_node"
    )
    # 封装指令
    cmd = ExecuteProcess(
        cmd=["ros2 topic echo /turtle1/pose"],
        output="both",
        shell=True
    )

    return LaunchDescription([turtle,cmd])