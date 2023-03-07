#include "rclcpp/rclcpp.hpp"
#include "turtlesim/srv/spawn.hpp"

// 编写客户端实现，发送请求生成一只新的小乌龟
// 使用参数服务生成新的乌龟信息

using namespace std::chrono_literals;

class Exer01Spawn:public rclcpp::Node{
    public:
        Exer01Spawn():Node("exer01_spawn_node_cpp"){
            this->declare_parameter("x",3.0);
            this->declare_parameter("y",3.0);
            this->declare_parameter("theta",0.0);
            this->declare_parameter("turtle_name","turtle2");

            x = this->get_parameter("x").as_double();
            y = this->get_parameter("y").as_double();
            theta = this->get_parameter("theta").as_double();
            turtle_name = this->get_parameter("turtle_name").as_string();

            // 创建客户端
            spawn_client_ = this->create_client<turtlesim::srv::Spawn>("/spawn");
        }

        // 连接服务端
        bool connect_server(){
            while(!spawn_client_->wait_for_service(1s)){
                if(!rclcpp::ok())
                {
                    RCLCPP_INFO(rclcpp::get_logger("rclcpp"),"强制退出");
                    return false;
                }
                RCLCPP_INFO(this->get_logger(),"服务连接中");
            }
            return true;
        }
        // 组织并发布数据
            rclcpp::Client<turtlesim::srv::Spawn>::FutureAndRequestId requset(){
            auto req = std::make_shared<turtlesim::srv::Spawn_Request>();
            req->x = x;
            req->y = y;
            req->theta = theta;
            req->name = turtle_name;
            return spawn_client_->async_send_request(req);
        }
    private:

        double_t x,y,theta; 
        std::string turtle_name;
        rclcpp::Client<turtlesim::srv::Spawn>::SharedPtr spawn_client_;
};

int main(int argc,char const *argv[])
{

    rclcpp::init(argc,argv);
    // 创建自定义的节点类对象，组织函数，处理响应结果
    auto client_ = std::make_shared<Exer01Spawn>();
    bool flag = client_->connect_server();
    if(!flag){
        RCLCPP_INFO(rclcpp::get_logger("rclcpp"),"服务连接失败");
        return 1;
    }
    // 发送请求
    auto response = client_->requset();
    // 处理响应
    if(rclcpp::spin_until_future_complete(client_,response)==rclcpp::FutureReturnCode::SUCCESS)
    {
        RCLCPP_INFO(client_->get_logger(),"响应成功!");
        // 如果生成新乌龟，新乌龟重名了，也会响应成功但是并没有生成
        // 此时的返回结果中返回的是空字符串(正常是请求的乌龟的名称)
        std::string name=response.get()->name;
        if(name.empty()){
            RCLCPP_INFO(client_->get_logger(),"您生成的乌龟因为重名导致失败");
        }else{
            RCLCPP_INFO(client_->get_logger(),"您生成的乌龟成功");
        }
    }else{
        RCLCPP_INFO(client_->get_logger(),"响应失败！");
    }
    rclcpp::shutdown();
    return 0;
}