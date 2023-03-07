import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
from turtlesim.msg import Pose
from geometry_msgs.msg import TransformStamped
import tf_transformations

class TfDynamicBroadcasterPy(Node):

    def __init__(self):
        super().__init__("tf_dynamic_broadcaster_py_node")
        # 创建一个动态广播器
        self.boradcaster = TransformBroadcaster(self)
        # 创建一个乌龟位姿订阅方
        self.sub = self.create_subscription(
            Pose,
            "/turtle1/pose",
            self.do_pose,
            10
        )

    # 回调函数中获取乌龟位姿并生成相对关系发布
    def do_pose(self,pose:Pose):
        # 组织transform
        ts = TransformStamped()
        ts.header.stamp = self.get_clock().now().to_msg()
        ts.header.frame_id = "world"
        ts.child_frame_id = "turtle1"

        # 偏移量
        ts.transform.translation.x = pose.x
        ts.transform.translation.y = pose.y
        ts.transform.translation.z = 0.0

        # 四元数
        qtn = tf_transformations.quaternion_from_euler(0.0,0.0,pose.theta)
        ts.transform.rotation.x = qtn[0]
        ts.transform.rotation.y = qtn[1]
        ts.transform.rotation.z = qtn[2]
        ts.transform.rotation.w = qtn[3]
        # 发布transform
        self.boradcaster.sendTransform(ts)

def main():
    rclpy.init()
    rclpy.spin(TfDynamicBroadcasterPy())
    rclpy.shutdown()

if __name__ == 'main':
    main()