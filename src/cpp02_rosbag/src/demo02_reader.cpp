#include "rclcpp/rclcpp.hpp"
#include "rosbag2_cpp/reader.hpp"
#include "geometry_msgs/msg/twist.hpp"

class SimpleBagPlay:public rclcpp::Node
{
  public:
    SimpleBagPlay():Node("simple_bag_play_node_cpp")
    {
      RCLCPP_INFO(this->get_logger(),"消息回放对象创建");
      // 创建一个回放对象
      reader_ = std::make_unique<rosbag2_cpp::Reader>();
      // 设置被读取的文件
      reader_->open("my_bag");
      // 读消息
      while(reader_->has_next())
      {
        auto twist = reader_->read_next<geometry_msgs::msg::Twist>();
        RCLCPP_INFO(this->get_logger(),"线速度:%.2f,角速度:%.2f",twist.linear.x,twist.angular.z);
      }
      // 关闭文件
      reader_->close();
    }
  private:
    std::unique_ptr<rosbag2_cpp::Reader> reader_;
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc,argv);
  rclcpp::spin(std::make_shared<SimpleBagPlay>());
  rclcpp::shutdown();
  return 0;
}
