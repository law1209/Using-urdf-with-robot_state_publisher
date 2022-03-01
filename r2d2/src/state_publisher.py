#!/usr/bin/env python

import rospy
import math
import tf_conversions

import tf2_ros
import sensor_msgs.msg
import geometry_msgs.msg


if __name__ == '__main__':
  
   rospy.init_node('state_publisher', anonymous=True)
   
   joint_pub = rospy.Publisher("joint_states", sensor_msgs.msg.JointState, queue_size=1) 

   broadcaster = tf2_ros.TransformBroadcaster()
   loop_rate = rospy.Rate(30)

   degree = math.pi/180
   tilt=0; tinc=degree; swivel=0; angle=0; height=0; hinc=0.005
   
   odom_trans  = geometry_msgs.msg.TransformStamped()
   odom_trans.header.frame_id = 'odom'
   odom_trans.child_frame_id = 'axis'

  
   joint_state = sensor_msgs.msg.JointState()

   while not rospy.is_shutdown():
        joint_state.header.stamp = rospy.Time.now() 

        joint_state.name=["swivel","tilt","periscope"]
        joint_state.position = [1,2,3]
        joint_state.position[0]= swivel
        joint_state.position[1]= tilt
        joint_state.position[2]= height
  

        odom_trans.header.stamp = rospy.Time.now() 
        odom_trans.transform.translation.x = math.cos(angle)*2
        odom_trans.transform.translation.y = math.sin(angle)*2
        odom_trans.transform.translation.z = .7
        q = tf_conversions.transformations.quaternion_from_euler(0, 0, angle+math.pi/2)
        odom_trans.transform.rotation.x=q[0]
        odom_trans.transform.rotation.y=q[1]
        odom_trans.transform.rotation.z=q[2]
        odom_trans.transform.rotation.w=q[3]

       
        joint_pub.publish(joint_state)
        broadcaster.sendTransform(odom_trans)


        tilt += tinc
        if tilt<-0.5 or tilt>0:
            tinc *= -1
        height += hinc
        if height>0.2 or height<0:
            hinc *= -1
        swivel += degree
        angle += degree/4


        loop_rate.sleep()





