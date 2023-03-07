#include <cstdio>
#include "rclcpp/rclcpp.hpp"
#include "tf2_ros/transform_listener.h"
#include "tf2_ros/buffer.h"
#include "tf2/LinearMath/Quaternion.h"

using namespace std::chrono_literals;

/*
  先发布laser到base_link的坐标系相对关系，在发布camera到base_link的坐标系相对关系
  求解laser到camera的坐标系相对关系
*/

class TFListener:public rclcpp::Node{
  public:
    TFListener():Node("tf_listener_node_cpp"){
      // 缓存对象的创建
      buffer_ = std::make_unique<tf2_ros::Buffer>(this->get_clock());
      // 创建一个监听器，绑定缓存对象，会将所有广播器广播的对象写入缓存
      listener_ = std::make_shared<tf2_ros::TransformListener>(*buffer_,this);
      // 编写一个定时器，循环实现转换
      timer_ = this->create_wall_timer(1s,std::bind(&TFListener::on_timer,this));
    }
  private:
    void on_timer()
    {
      // 实现坐标系转换
      /*
        geometry_msgs::msg::TransformStamped 
        lookupTransform(const std::string &target_frame, 
                      const std::string &source_frame, 
                      const tf2::TimePoint &time) 
      */
     /*
      A相对于B的坐标系关系
      参数1：目标坐标系 B
      参数2：源坐标系 A
      参数3：间隔时间，取最短 tf2::TimePointZero
      lookupTransform(B,A)
      父级：B 子级：A
      比如：B(3,0,0) A(5,0,0)
      则上面的函数返回值t.transform.translation.x=2
      tf2::TimePointZero意思是转换最新时刻的坐标帧
      */
     try {
       auto ts=buffer_->lookupTransform("camera","laser",tf2::TimePointZero);
       RCLCPP_INFO(this->get_logger(),"-----转换完成的坐标帧信息-----");
       RCLCPP_INFO(this->get_logger(),
        "新坐标帧:父坐标系:%s,子坐标系:%s,偏移量:(%.2f,%.2f,%.2f)",
        ts.header.frame_id.c_str(),//camera
        ts.child_frame_id.c_str(),//laser
        ts.transform.translation.x,
        ts.transform.translation.y,
        ts.transform.translation.z
        );
        
     }
     catch(const tf2::LookupException & e)
     {
      RCLCPP_INFO(this->get_logger(),"异常提示：%s",e.what());
     }
     
    }
    // 创建一个缓存对象，融合多个坐标系相对关系为一颗坐标树
    std::unique_ptr<tf2_ros::Buffer> buffer_;
    std::shared_ptr<tf2_ros::TransformListener> listener_;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc,argv);
  rclcpp::spin(std::make_shared<TFListener>());
  rclcpp::shutdown();
  return 0;
}
