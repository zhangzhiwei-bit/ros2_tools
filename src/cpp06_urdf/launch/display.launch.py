from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_directory
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # 1、启动robot_state_publisher节点，该节点要以参数的方式加载urdf文件
    # p_value = ParameterValue(Command(["xacro ",get_package_share_directory("cpp06_urdf")+"/urdf/urdf/demo01_helloworld.urdf"]))
    # 这时的调用格式：ros2 launch cpp06_urdf display.launch.py model:=`ros2 pkg prefix --share cpp06_urdf`/urdf/urdf/test.urdf
    model = DeclareLaunchArgument(name="model",default_value=get_package_share_directory("cpp06_urdf")+"/urdf/urdf/demo01_helloworld.urdf")
    p_value = ParameterValue(Command(["xacro ",LaunchConfiguration("model")]))
    robot_state_pub = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description":p_value}]
        )
    
    joint_state_pub = Node(
            package="joint_state_publisher",
            executable="joint_state_publisher"
        )
    rviz2 = Node(
        package = "rviz2",
        executable="rviz2",
        arguments=["-d",get_package_share_directory("cpp06_urdf")+"/rviz/urdf.rviz"]
        )
    return LaunchDescription([model,robot_state_pub, joint_state_pub, rviz2])