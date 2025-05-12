#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String

moveBindings = {
        'i':(1,0),
        'o':(1,-1),
        'j':(0,1),
        'l':(0,-1),
        'u':(1,1),
        ',':(-1,0),
        '.':(-1,1),
        'm':(-1,-1),
           }

speedBindings={
        'q':(1.1,1.1),
        'z':(.9,.9),
        'w':(1.1,1),
        'x':(.9,1),
        'e':(1,1.1),
        'c':(1,.9),
          }

class MovementClient:
    def __init__(self):
        rospy.init_node('movement_client')
        
        # 订阅来自服务端的命令
        self.cmd_sub = rospy.Subscriber('movement_commands', String, self.command_callback)
        
        # 发布Twist消息控制机器人
        self.vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=5)
        
        # 机器人运动参数
        self.speed = 0.2
        self.turn = 1
        
        self.x = 0
        self.th = 0
        self.count = 0
        self.control_speed = 0
        self.control_turn = 0
        
        rospy.loginfo("移动客户端已初始化，等待命令...")
    
    def command_callback(self, msg):
        key = msg.data
        rospy.loginfo("收到命令: %s", key)
        
        if key in moveBindings.keys():
            self.x = moveBindings[key][0]
            self.th = moveBindings[key][1]
            self.count = 0
        elif key in speedBindings.keys():
            self.speed = self.speed * speedBindings[key][0]
            self.turn = self.turn * speedBindings[key][1]
            self.count = 0
            rospy.loginfo("速度: %s, 转向: %s", self.speed, self.turn)
        elif key == ' ' or key == 'k':
            self.x = 0
            self.th = 0
            self.control_speed = 0
            self.control_turn = 0
        else:
            self.count = self.count + 1
            if self.count > 4:
                self.x = 0
                self.th = 0
    
    def update_movement(self):
        # 计算目标速度
        target_speed = self.speed * self.x
        target_turn = self.turn * self.th

        # 平滑加减速
        if target_speed > self.control_speed:
            self.control_speed = min(target_speed, self.control_speed + 0.02)
        elif target_speed < self.control_speed:
            self.control_speed = max(target_speed, self.control_speed - 0.02)
        else:
            self.control_speed = target_speed

        if target_turn > self.control_turn:
            self.control_turn = min(target_turn, self.control_turn + 0.1)
        elif target_turn < self.control_turn:
            self.control_turn = max(target_turn, self.control_turn - 0.1)
        else:
            self.control_turn = target_turn
        
        # 发布控制命令
        twist = Twist()
        twist.linear.x = self.control_speed
        twist.linear.y = 0
        twist.linear.z = 0
        twist.angular.x = 0
        twist.angular.y = 0
        twist.angular.z = self.control_turn
        self.vel_pub.publish(twist)
    
    def run(self):
        rate = rospy.Rate(10)  # 10Hz
        try:
            while not rospy.is_shutdown():
                self.update_movement()
                rate.sleep()
        except Exception as e:
            rospy.logerr("错误: %s", e)
        finally:
            # 停止机器人
            twist = Twist()
            twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
            self.vel_pub.publish(twist)

if __name__ == "__main__":
    try:
        client = MovementClient()
        client.run()
    except rospy.ROSInterruptException:
        pass
