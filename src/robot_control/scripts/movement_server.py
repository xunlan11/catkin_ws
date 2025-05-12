#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import sys, select, termios, tty

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

def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def vels(speed,turn):
    return "当前:\t速度 %s\t转向 %s " % (speed,turn)

if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)
    
    rospy.init_node('movement_server')
    cmd_pub = rospy.Publisher('movement_commands', String, queue_size=5)
    
    speed = .2
    turn = 1
    
    msg = """
控制你的机器人!
---------------------------
移动:
   u    i    o
   j    k    l
   m    ,    .

q/z : 增加/减少最大速度 10%
w/x : 增加/减少线性速度 10%
e/c : 增加/减少角速度 10%
空格键, k : 强制停止
其他按键 : 平滑停止

CTRL-C 退出
"""
    
    print(msg)
    print(vels(speed,turn))
    
    try:
        while not rospy.is_shutdown():
            key = getKey()
            
            # 发送按键命令给客户端
            if key:
                cmd_pub.publish(key)
                
                # 更新并显示速度信息
                if key in speedBindings.keys():
                    speed = speed * speedBindings[key][0]
                    turn = turn * speedBindings[key][1]
                    print(vels(speed,turn))
            
            if (key == '\x03'):  # CTRL-C
                break
            
    except Exception as e:
        print(e)

    finally:
        # 发送停止命令
        cmd_pub.publish(' ')
        
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
