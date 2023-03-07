import rclpy
from rclpy.node import Node
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from rclpy.time import Time

class TFListenerPy(Node):
    def __init__(self):
        super().__init__("tf_listener_py_node")
        # 创建一个缓存对象，融合多个坐标系相对关系为一颗坐标树
        self.buffer = Buffer()
        # 创建一个监听器，绑定缓存对象，会将所有的广播数据写入缓存
        self.listener = TransformListener(self.buffer,self)
        # 编写一个监听器
        self.timer = self.create_timer(1.0,self.on_timer)
    def on_timer(self):
        # 判读是否可以实现转换，可以通过异常处理也可以通过下面的方法判断
        if self.buffer.can_transform("camera","laser",Time()):
            ts = self.buffer.lookup_transform("camera","laser",Time())
            self.get_logger().info("-----转换后的数据-----")
            self.get_logger().info(
                "转换结果，父坐标系:%s,子坐标系:%s,偏移量:(%.2f,%.2f,%.2f)"
                %( 
                    ts.header.frame_id  ,#camera
                    ts.child_frame_id, #laser
                    ts.transform.translation.x,
                    ts.transform.translation.y,
                    ts.transform.translation.z)
            )
        else:
            self.get_logger().info("转换失败")


def main():
    rclpy.init()
    rclpy.spin(TFListenerPy())
    rclpy.shutdown()

if __name__ == '__main__':
   main
