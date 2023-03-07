from launch import LaunchDescription
from launch_ros.actions import Node
from launch.event_handlers import OnProcessStart,OnProcessExit
from launch.actions import ExecuteProcess,RegisterEventHandler,LogInfo
'''
    为turtlesim_node节点绑定事件，节点启动时，执行生成新的乌龟，
    节点关闭执行日志输出
'''

def generate_launch_description():
    turtle = Node(
        package="turtlesim",
        executable="turtlesim_node"
    )

    spawn = ExecuteProcess(
        cmd=["ros2 service call /spawn turtlesim/srv/Spawn \"{'x':8.0,'y':3.0}\""],
        output="both",
        shell=True
    )

    # 注册事件
    event_start = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=turtle,
            on_start=spawn
        )
    )

    # 乌龟退出输出日志
    event_exit = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=turtle,
            on_exit=[LogInfo(msg="turtlesim_node exit!")]
        )
    )

    return LaunchDescription([turtle,event_start,event_exit])