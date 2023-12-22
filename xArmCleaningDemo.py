"""
Description: Move Joint
"""

import os
import sys
import time
import math

sys.path.append("./xArm-Python-SDK-master/")
from xarm.wrapper import XArmAPI

ip = '192.168.1.216'

arm = XArmAPI(ip)
arm.motion_enable(True)
arm.clean_error()
arm.set_mode(0)
arm.set_state(0)
time.sleep(1)
speed = 50

code = arm.set_gripper_mode(0)
code = arm.set_gripper_enable(True)
code = arm.set_gripper_speed(5000)

def robot_pickup():
    arm.set_servo_angle(angle=[-38.5, -72.6, -27.9, 23.3, -98, 10.2, 69.9], speed=speed, wait=True)

    arm.set_servo_angle(angle=[-55.8, -19.1, -6, 25.9, -178.8, -45, 89.9], speed=speed, wait=True)

    code = arm.set_gripper_position(600, wait=True)

    arm.set_servo_angle(angle=[-48.0, -3.1, -16.3, 21.3, -175.5, -25, 83.9], speed=speed, wait=True)

    code = arm.set_gripper_position(498, wait=True, speed=8000)

    arm.set_servo_angle(angle=[-38.5, -72.6, -27.9, 23.3, -98, 10.2, 69.9], speed=speed, wait=True)

def all_squares():
    
    z = 811
    arm.set_position(roll=95.4, pitch=-89.7, yaw=84.1)
    for rows in range(1,5):
        y = 242.4
        for colums in range(1,10):
            arm.set_position(x=270.6, y=y, z=z)
            y = 242.4 - (46* colums)
        z = 811 - (50*rows)
        
##Initial position: arm.set_servo_angle(angle=[-39.2, -116.8, 17.3, 10.1, -18.6, 42.4, 30.1], speed=speed, wait=True)

#arm.set_servo_angle(angle=[-103.8, -29.2, 56.1, 97.4, -19.8, 29.9, 42], speed=speed, wait=True)
#arm.set_servo_angle(angle=[-60.2, -17.3, 28.9, 96, -52.7, 37.9, 55.7], speed=speed, wait=True)


#robot_pickup()

robot_pickup()
all_squares()

arm.disconnect()