from launch import LaunchDescription
from launch_ros.actions import Node

# 声明参数
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # 优化坐标系的设置
    # 抽取第二个坐标系名称为一个变量
    t2 = DeclareLaunchArgument(name="t2_name",default_value="t2")

    # 1、启动turtlesim_node节点
    turtle = Node(package="turtlesim",executable="turtlesim_node")
    # 2、启动自定义的spawn节点
    spawn = Node(package= "cpp05_exercise",executable="exer01_spawn",
                parameters=[{"turtle_name":LaunchConfiguration("t2_name")}]
                )
    # 3、分别广播两只乌龟相对world的坐标变换
    broadcaster1 = Node(package="cpp05_exercise",executable="exer02_tf_broadcaster",name="broa1")
    broadcaster2 = Node(package="cpp05_exercise",executable="exer02_tf_broadcaster",name="broa2",
                        parameters=[{"turtle":LaunchConfiguration("t2_name")}]
                    )
    # 4、创建监听节点
    listener = Node(package="cpp05_exercise",executable="exer03_tf_listener",
                    parameters=[{"father_frame":LaunchConfiguration("t2_name"),"child_frame":"turtle1"}]
                ) 
    return LaunchDescription([t2,turtle,spawn,broadcaster1,broadcaster2,listener])
    