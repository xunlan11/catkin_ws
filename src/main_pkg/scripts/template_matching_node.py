# filepath: /home/robot/catkin_ws/src/visual_servo_pkg/scripts/template_matching_node.py
#!/usr/bin/env python3

from cv_bridge import CvBridge, CvBridgeError
import rospy
import cv2
from sensor_msgs.msg import Image
from std_msgs.msg import Float64

def call_back(data):
    global object_pos_pub # 确保可以访问全局发布者
    try:
        bridge = CvBridge()
        cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
        
        # cv2.imshow("src", cv_image) # 可以取消注释以进行调试
        # cv2.waitKey(1)
        
        # template matching
        # 重要: 请确保模板路径正确，或者将模板文件也放在您的新包中并使用相对路径或rospkg获取路径
        template_path = rospy.get_param('~template_path', '/home/robot/catkin_ws/src/robot_view/template.bmp')
        template = cv2.imread(template_path)
        
        if template is None:
            rospy.logerr(f"无法加载模板图像: {template_path}")
            return
            
        # cv2.imshow("template", template) # 可以取消注释以进行调试
        # cv2.waitKey(1)
        
        img_h, img_w = cv_image.shape[:2] 
        h, w = template.shape[:2]
        
        if img_w == 0 or w == 0: # 防止除以零
            rospy.logwarn("图像或模板宽度为零")
            return

        res = cv2.matchTemplate(cv_image, template, cv2.TM_SQDIFF_NORMED) # 使用归一化的方法可能更鲁棒
        
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        
        # 对于TM_SQDIFF_NORMED, 最小值是最佳匹配
        top_left = min_loc
        center_x = top_left[0] + w / 2.0
        normalized_x = center_x / img_w
        
        object_pos_pub.publish(Float64(normalized_x))
        # rospy.loginfo(f"Published normalized_x: {normalized_x}") # 可以取消注释以进行调试

        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(cv_image, top_left, bottom_right, (0, 255, 0), 2) # 用绿色矩形
        
        cv2.imshow("dst_visual_servo", cv_image) # 使用不同的窗口名称以避免冲突
        cv2.waitKey(1)
    
    except CvBridgeError as e:
        rospy.logerr(f"CvBridge Error: {e}")
    except Exception as e:
        rospy.logerr(f"Template matching error: {e}")

if __name__ == '__main__':
    rospy.init_node('template_matching_node', anonymous=False)
    
    global object_pos_pub
    object_pos_pub = rospy.Publisher('/detected_object/normalized_x', Float64, queue_size=10)

    img_topic = rospy.get_param('~image_topic', '/camera/rgb/image_raw')
    template_default_path = '/home/robot/catkin_ws/src/robot_view/template.bmp' # 默认模板路径
    # 您也可以将模板路径作为参数传入
    # template_path = rospy.get_param('~template_path', template_default_path)
    
    image_sub = rospy.Subscriber(img_topic, Image, call_back, queue_size=1, buff_size=2**24) # 增加buff_size
    
    rospy.loginfo(f"模板匹配节点已启动，订阅图像话题: {img_topic}")
    rospy.loginfo(f"将发布物体位置到 /detected_object/normalized_x")
    rospy.loginfo(f"请确保模板文件路径正确。当前默认模板路径: {template_default_path}")
    
    try:
        rospy.spin()
    except KeyboardInterrupt:
        rospy.loginfo("关闭模板匹配节点...")
    
    cv2.destroyAllWindows()