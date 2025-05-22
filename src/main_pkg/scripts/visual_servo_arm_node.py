# filepath: /home/robot/catkin_ws/src/visual_servo_pkg/scripts/visual_servo_arm_node.py
#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float64

class VisualServoArm:
    def __init__(self):
        rospy.init_node('visual_servo_arm_node', anonymous=True)
        rospy.on_shutdown(self.cleanup)

        # 机械臂关节控制器的话题
        self.arm_command_topic = rospy.get_param('~arm_command_topic', '/tilt_controller/command')
        self.arm_command_pub = rospy.Publisher(self.arm_command_topic, Float64, queue_size=1)
        
        # 订阅物体位置话题
        self.object_pos_topic = rospy.get_param('~object_pos_topic', '/detected_object/normalized_x')
        self.object_pos_sub = rospy.Subscriber(self.object_pos_topic, Float64, self.object_pos_callback)
        
        # 从参数服务器获取机械臂关节的运动范围
        self.min_arm_command = rospy.get_param('~min_arm_command', 0.5)  # 对应 normalized_x = 0
        self.max_arm_command = rospy.get_param('~max_arm_command', 1.5)  # 对应 normalized_x = 1
        self.center_arm_command = rospy.get_param('~center_arm_command', (self.min_arm_command + self.max_arm_command) / 2.0)

        # PID 控制参数 (可选，用于更平滑的跟踪)
        self.kp = rospy.get_param('~kp', 1.0) # 比例增益 (max_arm_command - min_arm_command)
        # self.ki = rospy.get_param('~ki', 0.0)
        # self.kd = rospy.get_param('~kd', 0.0)
        # self.prev_error = 0.0
        # self.integral = 0.0
        
        rospy.loginfo(f"视觉伺服机械臂节点已启动。")
        rospy.loginfo(f"订阅物体位置: {self.object_pos_topic}")
        rospy.loginfo(f"发布机械臂指令到: {self.arm_command_topic}")
        rospy.loginfo(f"机械臂指令范围: [{self.min_arm_command}, {self.max_arm_command}]")
        rospy.loginfo(f"PID Kp: {self.kp}")


    def object_pos_callback(self, msg):
        normalized_x = msg.data # 物体在图像中的归一化位置 (0.0 左, 0.5 中, 1.0 右)
        
        # 目标是让物体在图像中心 (normalized_x = 0.5)
        error = 0.5 - normalized_x # 如果物体在右边(>0.5)，error为负，机械臂应向“左”移动（命令值减小）
                                   # 如果物体在左边(<0.5)，error为正，机械臂应向“右”移动（命令值增大）

        # 简单的比例控制
        # 假设机械臂命令值增大，其在相机视野中看起来是向“右”移动
        # 调整量 = Kp * error
        # 新命令 = 当前命令 + 调整量 (或者更简单地，直接映射)
        
        # 直接映射方法：
        # arm_command_val = self.min_arm_command + normalized_x * (self.max_arm_command - self.min_arm_command)
        # 如果 normalized_x = 0.5 (中心), arm_command_val 应该是中心命令值
        # 我们希望当 normalized_x = 0.5 时，输出是机械臂的中心位置。
        # 当 normalized_x < 0.5 (物体在左)，我们希望机械臂向“左”看，即命令值减小（假设）
        # 当 normalized_x > 0.5 (物体在右)，我们希望机械臂向“右”看，即命令值增大（假设）

        # 假设控制器的中心位置对应图像中心
        # 偏移量与error成正比，作用于中心命令值
        # 如果error > 0 (物体在左)，command 应该增加 (假设命令增加使机械臂向左看)
        # 如果error < 0 (物体在右)，command 应该减小 (假设命令减小使机械臂向右看)
        # 这个映射关系需要根据您的机械臂实际运动方向和相机视野来调整
        # 例如，如果命令值增加使机械臂向右移动（在相机视野中），则应该是 -self.kp * error
        
        # 让我们假设：增大命令值使机械臂向右移动（在相机视野中）
        # 如果物体在图像左侧 (normalized_x < 0.5)，error > 0。我们希望机械臂向左移动，即减小命令值。
        # 如果物体在图像右侧 (normalized_x > 0.5)，error < 0。我们希望机械臂向右移动，即增大命令值。
        # 所以，调整量应该是 -self.kp * error
        
        adjustment = -self.kp * error # 注意这里的负号，需要根据实际情况调整
        arm_command_val = self.center_arm_command + adjustment

        # 限制指令在合理范围内
        arm_command_val = max(self.min_arm_command, min(self.max_arm_command, arm_command_val))
        
        arm_command_msg = Float64()
        arm_command_msg.data = arm_command_val
        
        self.arm_command_pub.publish(arm_command_msg)
        # rospy.loginfo(f"Obj_X: {normalized_x:.2f}, Err: {error:.2f}, Adjust: {adjustment:.2f}, Cmd: {arm_command_val:.2f}")

    def cleanup(self):
        rospy.loginfo("关闭视觉伺服机械臂节点...")
        # 可以选择在关闭时将机械臂移动到一个安全/初始位置
        # safe_pos_msg = Float64()
        # safe_pos_msg.data = self.center_arm_command 
        # self.arm_command_pub.publish(safe_pos_msg)
        # rospy.sleep(0.5) # 给一点时间发送命令

if __name__ == '__main__':
    try:
        VisualServoArm()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass