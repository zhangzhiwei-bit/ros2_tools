#include "rclcpp/rclcpp.hpp"
#include "tf2_ros/transform_broadcaster.h"
#include "turtlesim/msg/pose.hpp"
#include "geometry_msgs/msg/transform_stamped.hpp"
#include "tf2/LinearMath/Quaternion.h"

/*
    启动turtlesim_node节点，发布乌龟(turtle1)相对于窗体(world)的位姿
*/
class TfDynamicBroadcaster:public rclcpp::Node
{
    public:
        TfDynamicBroadcaster():Node("tf_dynamic_broadcaster_node")
        {
            // 创建动态广播器
            broadcaster_ = std::make_shared<tf2_ros::TransformBroadcaster>(this);
            // 创建一个乌龟位姿订阅方
            pose_sub_ = this->create_subscription<turtlesim::msg::Pose>("/turtle1/pose",10,
                std::bind(&TfDynamicBroadcaster::do_pose,this,std::placeholders::_1)
            );
        }
    private:
        // 回调函数中，获取乌龟位姿并生成相关信息进行发布
        void do_pose(const turtlesim::msg::Pose & pose)
        {
            // 组织消息
            geometry_msgs::msg::TransformStamped ts;
            ts.header.stamp = this->now();
            ts.header.frame_id = "world";
            ts.child_frame_id = "turtle1";

            ts.transform.translation.x = pose.x;
            ts.transform.translation.y = pose.y;
            ts.transform.translation.z = 0.0;

            // 从欧拉角转换为四元数
            // 乌龟的欧拉角只有 yaw上的取值，没有 roll 和 pith
            tf2::Quaternion qtn;
            qtn.setRPY(0,0,pose.theta);
            
            ts.transform.rotation.x = qtn.x(); 
            ts.transform.rotation.y = qtn.y(); 
            ts.transform.rotation.z = qtn.z(); 
            ts.transform.rotation.w = qtn.w(); 
            // 发布
            broadcaster_ ->sendTransform(ts);
        }
        std::shared_ptr<tf2_ros::TransformBroadcaster> broadcaster_;
        rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr pose_sub_;
};

int main(int argc,char *argv[])
{
    rclcpp::init(argc,argv);
    rclcpp::spin(std::make_shared<TfDynamicBroadcaster>());
    rclcpp::shutdown();
    return 0;
}