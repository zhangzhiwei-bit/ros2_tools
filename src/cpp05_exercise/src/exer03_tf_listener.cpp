#include "rclcpp/rclcpp.hpp"
#include "tf2_ros/buffer.h"
#include "tf2_ros/transform_listener.h"
#include "geometry_msgs/msg/twist.hpp"

using namespace std::chrono_literals;

class Exer03TFListener:public rclcpp::Node{
    public:
        Exer03TFListener():Node("exer01_tf_listener_node_cpp"){
            // 声明参数服务
            this->declare_parameter("father_frame","turtle2");
            this->declare_parameter("child_frame","turtle1");
            father_frame = this->get_parameter("father_frame").as_string();
            child_frame = this->get_parameter("child_frame").as_string();
            // 创建缓存
            buffer_ = std::make_shared<tf2_ros::Buffer>(this->get_clock());
            // 创建监听器
            listener_ = std::make_shared<tf2_ros::TransformListener>(*buffer_);
            // 创建速度发布方
            cmd_pub_ = this->create_publisher<geometry_msgs::msg::Twist>("/"+father_frame+"/cmd_vel",10);
            // 创建一个定时器，实现坐标变换，并生成速度指令发布
            timer_ = this->create_wall_timer(1s,std::bind(&Exer03TFListener::on_timer,this));
        }
    private:
        void on_timer()
        {
            try {
                 // 实现坐标变换
                // son 相对与 father的坐标关系，然后father向son移动
                auto ts = buffer_->lookupTransform(father_frame,child_frame,tf2::TimePointZero);
                // 组织并发布速度指令
                // 计算线速度的x和角速度的z
                /*
                    线速度=系数*开方(x^2+y^2)
                    角速度=系数*反正切(y/x)
                */
                geometry_msgs::msg::Twist twist;
                twist.linear.x = 0.5 * sqrt(pow(ts.transform.translation.x,2)+pow(ts.transform.translation.y,2));
                twist.angular.z = 1.0 * atan2(ts.transform.translation.y,ts.transform.translation.x);
                cmd_pub_->publish(twist);
            }catch(tf2::LookupException &e){
                RCLCPP_INFO(this->get_logger(),"异常提示：%s",e.what());
            }
        }
        std::string father_frame;
        std::string child_frame;
        std::shared_ptr<tf2_ros::Buffer> buffer_;
        std::shared_ptr<tf2_ros::TransformListener> listener_;
        rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr cmd_pub_;
        rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc,char const *argv[])
{
    rclcpp::init(argc,argv);
    rclcpp::spin(std::make_shared<Exer03TFListener>());
    rclcpp::shutdown();
    return 0;
}