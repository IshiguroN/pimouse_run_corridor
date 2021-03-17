#!/usr/bin/env python
#encoding: utf-8

import rospy,copy,math
from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger, TriggerResponse
from mymouse_ros.msg import MyLightSensorValues

class LineTrace():
    def __init__(self):
        self.cmd_vel = rospy.Publisher('/cmd_vel',Twist,queue_size=1)

        self.s = MyLightSensorValues()
        rospy.Subscriber('/lightsensors', MyLightSensorValues, self.callback_lightsensors)

    def callback_lightsensors(self,messages):
        self.s = messages

    def run(self):
        rate = rospy.Rate(20)
        data = Twist()
        u_ = 0
        while not rospy.is_shutdown():
          data.angular.x = 0.2
          s1 = (self.s.left_third > 2000)
          s2 = (self.s.left_first > 2000)
          s3 = (self.s.right_first > 2000)
          s4 = (self.s.right_third > 2000)

          u = (3*s1 + 1*s2 - 1*s3 -3*s4)/(s1+s2+s3+s4+0.1)
          delta = math.pi/180*(40*u + 0.4*(u-u_)*20)
          data.angular.z = 0.0
            
          u_ = u
          self.cmd_vel.publish(data)
          rate.sleep()

if __name__ == '__main__':
    rospy.init_node('line_trace')

    rospy.wait_for_service('/motor_on')
    rospy.wait_for_service('/motor_off')
    rospy.on_shutdown(rospy.ServiceProxy('/motor_off',Trigger).call)
    rospy.ServiceProxy('/motor_on',Trigger).call()

    w = LineTrace()
    w.run()

