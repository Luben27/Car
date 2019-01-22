#!/usr/bin/env python
import cv2
import threading
import Queue as que
import time
import numpy as np

import roslib
import sys
import rospy

import importlib
import cPickle
import genpy.message
from rospy import ROSException
import sensor_msgs.msg
import actionlib
import rostopic
import rosservice
from rosservice import ROSServiceException

from slidewindow import SlideWindow
from warper import Warper
from pidcal import PidCal

from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

from ackermann_msgs.msg import AckermannDriveStamped
from Preparation import Preparation
pre = Preparation()
warper = Warper()
slidewindow  = SlideWindow()
pidcal = PidCal()

q1 = que.Queue()
bridge = CvBridge()

cv_image = None
ack_publisher = None
car_run_speed = 0.5
def img_callback(data):
    global cv_image
    try:
      cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)
  
def auto_drive(pid, mode):
    global car_run_speed

    w = 0
    a = 10
    if mode == 0:
        a = 10
    	if -0.065 < pid and pid < 0.065:
            w = 1.95
    	else:
            w = 1.3
    elif mode == 1:
	car_run_speed = 0
	pid = 0
    elif mode == 2:
	a = 10
    	if -0.065 < pid and pid < 0.065:
            w = 1.2
    	else:
            w = 0.7
    elif mode == 3:
        a = 10
        if -0.065 < pid and pid < 0.065:
            w = 1.0
    	else:
            w = 0.6
    if car_run_speed < 1.0 * w:
        car_run_speed += (0.009 * a)
    else:
        car_run_speed -= 0.010 * a    
    ack_msg = AckermannDriveStamped()
    ack_msg.header.stamp = rospy.Time.now()
    ack_msg.header.frame_id = ''
    ack_msg.drive.steering_angle = pid
    ack_msg.drive.speed = car_run_speed
    ack_publisher.publish(ack_msg)
    #print 'speed: ' 
    #print car_run_speed 

def main():
    global cv_image
    global ack_publisher
    rospy.sleep(3)
    bridge = CvBridge()
    image_sub = rospy.Subscriber("/usb_cam/image_raw/",Image,img_callback)
    angle_cnt = 0
    rospy.init_node('auto_xycar', anonymous=True)

    #ack_publisher = rospy.Publisher('vesc/low_level/ackermann_cmd_mux/input/teleop', AckermannDriveStamped, queue_size=1)
    ack_publisher = rospy.Publisher('ackermann_cmd_mux/input/teleop', AckermannDriveStamped, queue_size=1)
    # record the origin
    #out = cv2.VideoWriter('/home/nvidia/Desktop/outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 30, (640,480))

    # record the processed
    #out2 = cv2.VideoWriter('/home/nvidia/Desktop/oripy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 30, (640,480))

    round_map = 0
    state = 0
    flag = 0
    angle_flag = 0
    y_ = 0
    curTime = 0
    firstTime = 0
    pastTime = 0
    peakTime = 0
    prevTime = 0
    sum_time = 0
    sec = 0
    last_flag = 0
    while cv_image != None:
      edge, img1, x_location = process_image(cv_image)
      #cv2.imshow('result', img1)
 #     arr, harris = corner(edge, cv_image)
#      cv2.imshow('harris',harris)

      #if arr > 1000 :
      
#	  state = 1
#
 #     else :
#	  if state == 1:
 #         	state = 2+
  #        	round_map +=1
   #   
      
      if x_location != None:
          pid = round(pidcal.pid_control(int(x_location)), 6)
	  if peakTime < 1:
	  	firstTime = time.time()
          	sec = firstTime - pastTime
          	peakTime += sec
          	pastTime = firstTime
          else :
		if abs(pid) > 0.16 and angle_flag == 0:
			angle_cnt += 1
			angle_flag = 1
		elif abs(pid) <0.06 and angle_flag == 1:
			angle_flag = 0
		if angle_cnt >=6:
			Yellow,y_ = line_detect(cv_image)
			if y_>700 and flag == 0 :
				flag = 1
				if round_map == 2:
					last_flag =1
	      		elif y_ < 400 and flag == 1:
		  		flag = 0
		  		round_map += 1
				angle_cnt = 0
          #print pid
	  if round_map <3:
		if last_flag == 1:
			auto_drive(pid,3)		
		elif angle_cnt >=6 :
			auto_drive(pid, 2)
		else :
			auto_drive(pid, 0)          
          elif round_map >= 3:
		curTime = time.time()
		sec = curTime - prevTime
		prevTime = curTime
		sum_time += sec
	  	if sum_time > 0.03:
			auto_drive(pid,1)
		else:
			auto_drive(pid,0)

      if cv2.waitKey(1) & 0xFF == ord('q'):
          break
      #out.write(img1)
      #out2.write(cv_image)
      if round_map >2:
	auto_drive(pid, 1)
    try:
      rospy.spin()
    except KeyboardInterrupt:
      print("Shutting down")
    cv2.destroyAllWindows() 

def process_image(frame):
    
    # grayscle
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    # blur
    kernel_size = 5
    blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size), 0)
    # canny edge
    low_threshold = 60#60
    high_threshold = 70# 70
    edges_img = cv2.Canny(np.uint8(blur_gray), low_threshold, high_threshold)
    # warper
    img = warper.warp(edges_img)
    img1, x_location = slidewindow.slidewindow(img)
    
    return edges_img, img1, x_location
def line_detect(img):
    height,width = img.shape[:2]
    Roi_image = img[height*0.7:height*0.9,0:width-1]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    dst = pre.Yellow_detect(hsv)
    array = img[dst == 255].shape[0]
    return pre.Yellow_detect(hsv),array

def corner(edge, origin):
    height,width = origin.shape[:2]
    Roi_image = edge[height*0.7:height*0.9,0:width-1]
    Roi_origin = origin[height*0.7:height*0.9,0:width-1]
    gray = np.float32(Roi_image)
    dst = cv2.cornerHarris(gray,2,3,0.21)
    dst = cv2.dilate(dst,None) 
    Roi_origin[dst > 0.01 * dst.max()] = [0,0,255]
    array = Roi_origin[dst > 0.01 * dst.max()].shape[0]
    return array, Roi_origin

if __name__ == '__main__':
    main()
