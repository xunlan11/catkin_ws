## 本仓库仅供课程学习使用

### 更新环境变量：
source ~/catkin_ws/devel/setup.bash

### turtlebot：
- 仿真：roslaunch turtlebot_gazebo turtlebot_world.launch
- 启动底盘：roslaunch turtlebot_bringup minimal.launch
- 键盘控制：roslaunch turtlebot_teleop keyboard_teleop.launch
- 启动Kinect相机：roslaunch freenect_launch freenect-registered-xyzrgb.launch
- GMAPPING演示：roslaunch turtlebot_gazebo gmapping_demo.launch

### 语音：
- 不连续输入，持续输出
- 语音识别：roslaunch robot_voice iat_publish.launch
- 语音控制：roslaunch robot_voice voice_control.launch

### 视觉：
- 注意发布的主题，于Template_Matching.py中修改
- 电脑摄像头（右侧拨钮开启）：roslaunch usb_cam usb_cam-test.launch
- 机器人摄像头：rosrun image_view image_view image:=/camera/rgb/image_raw
- 模版匹配：rosrun robot_view Template_Matching.py

### 建图：
- 启动底盘：roslaunch turtlebot_bringup minimal.launch
- 启动GMAPPING建图：roslaunch turtlebot_navigation gmapping_demo.launch
- 启动RViz可视化工具：roslaunch turtlebot_rviz_launchers view_navigation.launch
- 键盘控制：roslaunch turtlebot_teleop keyboard_teleop.launch
- 保存地图：rosrun map_server map_saver -f /tmp/my_map

### 导航
- 设置地图路径：echo "export TURTLEBOT_GAZEBO_WORLD_FILE=xxx" >> ~/.bashrc 
- source ~/.bashrc
- 启动底盘（世界时间）：roslaunch turtlebot_bringup minimal.launch use_sim_time:=False 
- 启动amcl定位：roslaunch turtlebot_navigation amcl_demo.launch 
- 启动rviz可视化工具（输出于当前终端）：roslaunch turtlebot_rviz_launchers view_navigation.launch --screen 
- rosrun robot_map navigation.py