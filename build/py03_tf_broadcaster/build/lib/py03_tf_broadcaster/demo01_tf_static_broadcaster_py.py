import rclpy
from rclpy.node import Node
import sys
from rclpy.logging import get_logger
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster
from geometry_msgs.msg import TransformStamped
import tf_transformations

# 最终结果 ro2 run 包 可执行程序 x y z roll pitch yaw frame child_frame 

class TFStaticBroadcasterPy(Node):
    def __init__(self,argv):
        super().__init__("tf_static_broadcaster_py_node")
        # 创建广播对象
        self.broadcaster = StaticTransformBroadcaster(self)
        self.pub_static_tf(argv)
    
    def pub_static_tf(self,argv):
        ts = TransformStamped()
        # 设置参数
        ts.header.stamp = self.get_clock().now().to_msg()
        # 父级坐标系
        ts.header.frame_id = argv[7]
        # 子级坐标系
        ts.child_frame_id = argv[8]
        # 设置平移
        ts.transform.translation.x = float(argv[1])
        ts.transform.translation.y = float(argv[2])
        ts.transform.translation.z = float(argv[3])
        # 设置四元数
        # 将欧拉角转换为四元数
        qtn = tf_transformations.quaternion_from_euler(
            float(argv[4]),
            float(argv[5]),
            float(argv[6])
        )  
        ts.transform.rotation.x = qtn[0]
        ts.transform.rotation.y = qtn[1]
        ts.transform.rotation.z = qtn[2]
        ts.transform.rotation.w = qtn[3]
        self.broadcaster.sendTransform(ts)
    


def main():
    if len(sys.argv)!=9:
        get_logger("rclpy").info('传入参数不合法')
        return
    rclpy.init()
    rclpy.spin(TFStaticBroadcasterPy(sys.argv))
    rclpy.shutdown()

if __name__ == '__main__':
    main()
