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
        while not rospy.is_shutdown():
          data.linear.x = 0.2
          s1 = (self.s.left_third < 1000)
          s2 = (self.s.left_first < 1000)
          s3 = (self.s.right_first < 1000)
          s4 = (self.s.right_third < 1000)
          if (s1+s2+s3+s4)==0:
            u = 0.0
          else:
            u = (2.89*s1 + 1*s2 - 1*s3 - 2.89*s4)/(s1+s2+s3+s4)
          delta = math.pi/180*40*u
          data.angular.z = delta
          


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

