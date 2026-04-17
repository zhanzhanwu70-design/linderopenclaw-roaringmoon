# ROS2 Node Recipes

## 1. Minimal rclpy publisher/subscriber node

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from std_msgs.msg import String

class ExampleNode(Node):
    def __init__(self):
        super().__init__('example_node')
        self.declare_parameter('topic_name', 'chatter')
        topic = self.get_parameter('topic_name').value

        qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
        )

        self.pub = self.create_publisher(String, topic, qos)
        self.sub = self.create_subscription(String, topic, self.callback, qos)
        self.timer = self.create_timer(1.0, self.tick)
        self.count = 0

    def tick(self):
        msg = String()
        msg.data = f'hello {self.count}'
        self.pub.publish(msg)
        self.count += 1

    def callback(self, msg: String):
        self.get_logger().info(f'Received: {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    node = ExampleNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## 2. Minimal rclcpp node

```cpp
#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/string.hpp>
#include <memory>

class ExampleNode : public rclcpp::Node {
public:
  ExampleNode() : Node("example_node"), count_(0) {
    this->declare_parameter<std::string>("topic_name", "chatter");
    auto topic = this->get_parameter("topic_name").as_string();

    auto qos = rclcpp::QoS(10).reliable();
    pub_ = this->create_publisher<std_msgs::msg::String>(topic, qos);
    sub_ = this->create_subscription<std_msgs::msg::String>(
      topic, qos, [this](const std_msgs::msg::String & msg) {
        RCLCPP_INFO(this->get_logger(), "Received: %s", msg.data.c_str());
      });
    timer_ = this->create_wall_timer(std::chrono::seconds(1), [this]() {
      auto msg = std_msgs::msg::String();
      msg.data = "hello " + std::to_string(count_++);
      pub_->publish(msg);
    });
  }

private:
  int count_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr pub_;
  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr sub_;
  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char ** argv) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<ExampleNode>());
  rclcpp::shutdown();
  return 0;
}
```

## 3. ament_python package skeleton

### package.xml essentials

```xml
<package format="3">
  <name>my_ros2_pkg</name>
  <version>0.1.0</version>
  <description>Example ROS2 Python package</description>
  <maintainer email="dev@example.com">Dev</maintainer>
  <license>Apache-2.0</license>
  <buildtool_depend>ament_python</buildtool_depend>
  <exec_depend>rclpy</exec_depend>
  <exec_depend>std_msgs</exec_depend>
  <export><build_type>ament_python</build_type></export>
</package>
```

### setup.py essentials

```python
from setuptools import find_packages, setup

package_name = 'my_ros2_pkg'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/example.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'example_node = my_ros2_pkg.example_node:main',
        ],
    },
)
```

## 4. ament_cmake package skeleton

### CMakeLists.txt essentials

```cmake
cmake_minimum_required(VERSION 3.8)
project(my_ros2_cpp_pkg)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

add_executable(example_node src/example_node.cpp)
ament_target_dependencies(example_node rclcpp std_msgs)
install(TARGETS example_node DESTINATION lib/${PROJECT_NAME})

ament_package()
```

## 5. launch file template

```python
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_ros2_pkg',
            executable='example_node',
            name='example_node',
            output='screen',
            parameters=[{'topic_name': 'chatter'}],
        )
    ])
```

## 6. rosbridge note

For web / remote control workflows:

```bash
sudo apt install ros-${ROS_DISTRO}-rosbridge-server
ros2 launch rosbridge_server rosbridge_websocket_launch.xml
```

Default websocket endpoint:
- `ws://<robot-ip>:9090`

## 7. Useful commands

```bash
source /opt/ros/<distro>/setup.bash
rosdep install --from-paths src --ignore-src -y
colcon build --symlink-install
source install/setup.bash
ros2 run <pkg> <node>
ros2 launch <pkg> <launch.py>
ros2 topic list
ros2 topic info /topic -v
ros2 node list
ros2 param list /node
ros2 action list
```
