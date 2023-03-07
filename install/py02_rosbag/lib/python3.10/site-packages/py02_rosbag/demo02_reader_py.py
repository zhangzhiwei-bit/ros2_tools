import rclpy
from rclpy.node import Node
import rosbag2_py
from rclpy.logging import get_logger

class SimpleBagPlayer(Node):
    def __init__(self):
        super().__init__('simple_bag_player_py')
        self.reader = rosbag2_py.SequentialReader()
        storage_options = rosbag2_py._storage.StorageOptions(
            uri = 'my_bag_py',
            storage_id = 'sqlite3'
        )
        converter_options = rosbag2_py._storage.ConverterOptions('','')
        self.reader.open(storage_options,converter_options)

    def read(self):
        # 读消息
        while self.reader.has_next():
            msg = self.reader.read_next()
            get_logger("rclpy").info("topic = %s,time= %d,value= %s " %(msg[0],msg[2],msg[1]))

def main(args = None):
    rclpy.init(args = args)
    reader = SimpleBagPlayer()
    reader.read()

if __name__ == '__main__':
    main()
