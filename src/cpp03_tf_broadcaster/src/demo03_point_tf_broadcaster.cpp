#include "rclcpp/rclcpp.hpp"
#include "tf2_ros/transform_broadcaster.h"
#include "turtlesim/msg/pose.hpp"
#include "geometry_msgs/msg/transform_stamped.hpp"
#include "tf2/LinearMath/Quaternion.h"

#include "geometry_msgs/msg/point_stamped.hpp"

// 发布相对于laser坐标系的坐标点信息

using namespace std::chrono_literals;

class PointBroadcaster:public rclcpp::Node
{
    public:
        PointBroadcaster():Node("point_broadcaster_node"),x(0.0)
        {
            //创建发布方
            point_pub_ = this->create_publisher<geometry_msgs::msg::PointStamped>("point",10);
            // 创建定时器
            timer_ = this->create_wall_timer(1s,std::bind(&PointBroadcaster::on_timer,this));
        }
    private:
        void on_timer()
        {
            // 组织消息
            geometry_msgs::msg::PointStamped ps;
            ps.header.stamp = this->now();
            ps.header.frame_id = "laser";
            x+=0.05;
            ps.point.x = x;
            ps.point.y = 0.1;
            ps.point.z = -0.1;
            // 发布消息
            point_pub_->publish(ps);
        }
        rclcpp::Publisher<geometry_msgs::msg::PointStamped>::SharedPtr point_pub_;
        rclcpp::TimerBase::SharedPtr timer_;
        double_t x;
};

int main(int argc,char *argv[])
{
    rclcpp::init(argc,argv);
    rclcpp::spin(std::make_shared<PointBroadcaster>());
    rclcpp::shutdown();
    return 0;
}