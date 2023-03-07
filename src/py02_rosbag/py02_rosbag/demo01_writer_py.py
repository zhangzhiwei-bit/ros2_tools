import rclpy
from rclpy.node import Node
from rclpy.serialization import serialize_message
from geometry_msgs.msg import Twist
import rosbag2_py

class SimpleBagRecorder(Node):
    def __init__(self):
        super().__init__('simple_bag_recorder_py')
        # 创建写出对象
        self.writer = rosbag2_py.SequentialWriter()
        storage_options = rosbag2_py._storage.StorageOptions(
            uri = 'my_bag_py',
            storage_id = 'sqlite3'
        )
        converter_options = rosbag2_py.ConverterOptions('','')
        self.writer.open(storage_options,converter_options)
        topic_info = rosbag2_py.TopicMetadata(
            name = '/turtle1/cmd_vel',
            type = 'geometry_msmgs/msg/Twist',
            serialization_format = 'cdr'
        )
        self.writer.create_topic(topic_info)
        self.subscription = self.create_subscription(
            Twist,
            '/turtle1/cmd_vel',
            self.topic_callback,
            10
        )
    def topic_callback(self,msg):
        # 写出消息
        self.writer.write(
            '/turtle1/cmd_vel',
            serialize_message(msg),
            self.get_clock().now().nanoseconds
        )
        
def main(args=None):
    rclpy.init(args=args)
    sbr = SimpleBagRecorder()
    rclpy.spin(sbr)
    rclpy.shutdown()



if __name__ == '__main__':
    main()
