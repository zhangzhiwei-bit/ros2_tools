import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
from turtlesim.msg import Pose
from geometry_msgs.msg import TransformStamped
import tf_transformations

from geometry_msgs.msg import PointStamped

# 发布相对于laser坐标系的数据
class PointBroadcasterPy(Node):

    def __init__(self):
        super().__init__("tf_point_broadcaster_py_node")
        # 创建发布方
        self.point_pub = self.create_publisher(PointStamped,'point',10)
        # 创建定时器
        self.timer = self.create_timer(1.0,self.on_timer)
        self.x = 0.2
    
    # 回调函数组织发布数据
    def on_timer(self):
        # 组织数据
        ps = PointStamped()
        ps.header.stamp = self.get_clock().now().to_msg()
        ps.header.frame_id = "laser"
        self.x += 0.05
        ps.point.x = self.x
        ps.point.y = 0.0
        ps.point.z = 0.3
        # 发布数据
        self.point_pub.publish(ps)

   

def main():
    rclpy.init()
    rclpy.spin(PointBroadcasterPy())
    rclpy.shutdown()

if __name__ == 'main':
    main()