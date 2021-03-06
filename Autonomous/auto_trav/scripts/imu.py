#!/usr/bin/env python
import smbus
import time
import math
import rospy
from std_msgs.msg import String
import threading
heading=0
bus = smbus.SMBus(1)
pi = 3.14159265358979
a=0
v_heading=0
bus = smbus.SMBus(1)
pi = 3.14159265358979
bus.write_byte_data(0x6B, 0x20, 0x0F)
bus.write_byte_data(0x6B, 0x23, 0x30)
bus.write_byte_data(0x1D, 0x20, 0x67)
bus.write_byte_data(0x1D, 0x21, 0x20)
bus.write_byte_data(0x1D, 0x24, 0x70)
bus.write_byte_data(0x1D, 0x25, 0x60)
bus.write_byte_data(0x1D, 0x26, 0x00)
time.sleep(0.5)
data1 = bus.read_byte_data(0x1D, 0x2D)
def get_imu_head():
        while True:
                data0 = bus.read_byte_data(0x1D, 0x08)
                data1 = bus.read_byte_data(0x1D, 0x09)
                xMag = data1 * 256 + data0
                if xMag > 32767 :
                        xMag -= 65536
                data0 = bus.read_byte_data(0x1D, 0x0A)
                data1 = bus.read_byte_data(0x1D, 0x0B)
                yMag = data1 * 256 + data0
                if yMag > 32767 :
                        yMag -= 65536
                data0 = bus.read_byte_data(0x1D, 0x0C)
                data1 = bus.read_byte_data(0x1D, 0x0D)
                zMag = data1 * 256 + data0
                if zMag > 32767 :
                        zMag -= 65536
                h= math.atan2(yMag,xMag)
		v = math.atan2(zMag,xMag)
		s = math.atan2(zMag,yMag)
                if(h > 2*pi):
                        h=h-2*pi
		if(v > 2*pi):
                        v=v-2*pi
		if(s > 2*pi):
                        s=s-2*pi
                if(h<0):
                        h=h+2*pi
		if(v<0):
                        v=v+2*pi
		if(s<0):
                        s=s+2*pi
                ha=int(h* 180/pi)
		va=int(v* 180/pi)
		sa=int(s* 180/pi)
                ha = ha+7
		va = va+7
		sa = sa+7
                if ha>359:
                        ha = ha-360
		if va>359:
                        va = va-360
		if sa>359:
                        sa = sa-360
                return ha,va,sa
 
def headpub():
        global heading
        pubhead=rospy.Publisher("heading",String, queue_size=1)
	pubvhead=rospy.Publisher("v_heading",String, queue_size=1)
	pubshead=rospy.Publisher("s_heading",String, queue_size=1)
        rospy.init_node("IMU",anonymous=True)
        rate=rospy.Rate(10)
        while not rospy.is_shutdown():
                heading,v_heading,s_heading=get_imu_head()
      		pubvhead.publish(str(v_heading))
		pubshead.publish(str(s_heading))
                pubhead.publish(str(heading))
                rate.sleep()

if __name__=='__main__':
        try:
                headpub()
        except rospy.ROSInterruptException:
                pass        
                
 
