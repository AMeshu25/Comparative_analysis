import datetime

import Settings as s
import socket
import select
import threading
from Realsense import Realsense
from Joint import joint
import time
import math
import random
import Excel
import numpy as np
import keyboard

class Camera(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        # Create socket for client-server communication
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = ('localhost', 8888)
        self.sock.bind(self.server_address)
        print ("CAMERA: init")

    # Start camera skeleton tracking application
    def playRealsense(self):
        rStart = Realsense()
        rStart.start()

    # Stop camera skeleton tracking application
    def stopRealsense(self):
        rStop = Realsense()
        rStop.stop()

    # Client - read messages
    def get_skeleton_data(self):
        '''
        The function takes the received data and return a list of joints.
        Using the defined socket to receive skeleton data messages from the cpp code (Cubemos SDK sampels)
        The message structure is : {joint_id,x,y,z/joint_id,x,y,z/...} 1,-0.01,-0.22,1.10/2,0.16,-0.25,1.18/
        '''
        self.sock.settimeout(1.0)  # for check naama change to 10 instad 5
        try:
            # data, address = self.sock.recvfrom(4096)
            data = str(self.sock.recvfrom(4096))
            self.sock.settimeout(None)  # to check
            data = data.split('/')
            jointsStr = []
            for i in data:
                joint = i.split(',')
                jointsStr.append(joint)
                if (joint[0]=='3'):
                    joint4=['4', joint[4], joint[5], joint[6]]
                    jointsStr.append(joint4)
            # now change to float values
            joints = []  # joints data
            for j in jointsStr:
                joints.append(self.create_joint(j))
            return joints
        except socket.timeout:  # fail after 1 second of no activity
            print("Didn't receive data! [Timeout] - (Camera class)")
            # TODO Maybe add a meesage to the user that the camera don't recieve data?
            return None

    def create_joint(self, jointList):
        '''
        :param jointList: joint data as a string
        :return: Joint object or False if there is no data for creating Joint
        The y values of the joints are upside-down (as received from app), therefore is multiple by -1
        '''
        try:
            if (float(jointList[1]) == 0 or float(jointList[2])==0 or float(jointList[3])==0):
                print("CAMERA: could not create new joint: All coordinates are 0")
                return False
            else:
                new_joint = joint(jointList[0], float(jointList[1]) , float(jointList[2]), float(jointList[3]))
                return new_joint
        except:
            print("CAMERA: could not create new joint: list index out of range")
            return False

    # input - , required joint number ; output -
    def find_joint_data(self, jointsList, jointNumber):
        '''
        :param jointsList: List of all joints which is not None!
        :param jointNumber: The number of the required joint
        :return: The required joint only or False if the joint not exist in the recieved message data
        '''
        for i in jointsList:
            if i is False:
                return False
            else:
                if i.type == jointNumber:
                    return i
        return False

    # Calculate distance between two joints
    def calc_dist(self, joint1, joint2):
        distance = math.hypot(joint1.x - joint2.x, joint1.y - joint2.y)
        return distance

    # Calculate angle between joints according to the law of cosines
    def calc_angle(self, joint1, joint2, joint3):
        '''
        :param joint1: Point C
        :param joint2: Point B
        :param joint3: Point A
        :return: ACB angle in degrees
        '''
        a = self.calc_dist(joint1, joint2)
        b = self.calc_dist(joint1, joint3)
        c = self.calc_dist(joint2, joint3)
        try:
            rad_angle = math.acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b))
            deg_angle = (rad_angle * 180) / math.pi
            return round(deg_angle, 2)
        except:
            print("CAMERA: could not calculate the angle")

    def all_joints_data(self):
        list_joints = [["1", "2", "3", "4", "5", "6", "7", "8", "9", "11", "12", "13", "14", "15", "17", "18", "19", "21", "22", "23"]]
        joints = self.get_skeleton_data()
        list_joints.append(joints)

        while (True):
            joint1 = self.find_joint_data(joints, "1")
            joint2 = self.findJointData(joints, "2")
            joint3 = self.findJointData(joints, "3")
            joint4 = self.findJointData(joints, "4")
            joint5 = self.findJointData(joints, "5")
            joint6 = self.findJointData(joints, "6")
            joint7 = self.findJointData(joints, "7")
            joint8 = self.findJointData(joints, "8")
            joint9 = self.findJointData(joints, "9")
            joint11 = self.findJointData(joints, "11")
            joint12 = self.findJointData(joints, "12")
            joint13 = self.findJointData(joints, "13")
            joint14 = self.findJointData(joints, "14")
            joint15 = self.findJointData(joints, "15")
            joint17 = self.findJointData(joints, "17")
            joint18 = self.findJointData(joints, "18")
            joint19 = self.findJointData(joints, "19")
            joint21 = self.findJointData(joints, "21")
            joint22 = self.findJointData(joints, "22")
            joint23 = self.findJointData(joints, "23")

            print(joint1)
            print(joint4)
            # allJoints=[joint1, joint2, joint3,joint4,joint5[i],joint6[i],joint7[i],joint8[i],
            #                 joint9[i],joint11[i],joint12[i],joint13[i],joint14[i],joint15[i],joint17[i],joint18[i],
            #                  joint19[i],joint21[i],joint22[i],joint23[i]]
            # if not joint1 or not joint2 or not joint3:
            #     continue
            for i in range(0, len(joint1)):
                new_entry = [joint1[i], joint2[i], joint3[i],joint4[i],joint5[i],joint6[i],joint7[i],joint8[i],
                            joint9[i],joint11[i],joint12[i],joint13[i],joint14[i],joint15[i],joint17[i],joint18[i],
                             joint19[i],joint21[i],joint22[i],joint23[i]]

                list_joints.append(new_entry)

if __name__ == '__main__':
    s.realsense_path = R'C:\Users\TEMP.NAAMA\PycharmProjects\Nuitrack\nuitrack\Examples\nuitrack_console_sample\out\build\x64-Debug\nuitrack_console_sample.exe'
    s.excel_path = R'C:\Users\TEMP.NAAMA\PycharmProjects\Nuitrack\excel_folder/'
    # current_time = datetime.datetime.now()
    # worksheet_name = str(current_time.day) + "." + str(current_time.month) + " " + str(current_time.hour) + "." + \
    #                  str(current_time.minute) + "." + str(current_time.second) + ".xlsx"

    #naama to change
    subjectNum="28"
    sessionNum="S3"
    worksheet_name=subjectNum+"_Nuitrack_"+sessionNum+'.xlsx'
    Excel.create_workbook(worksheet_name)

    rStart = Realsense()
    rStart.start()
    c = Camera()
    list_joints = [["1", "2", "3", "4", "5", "6", "7", "8", "9", "11", "12", "13", "14", "15", "17", "18", "19", "21", "22", "23"]]
    i=1
    while(True):
        joints = c.get_skeleton_data()
        print("frame"+str(i))
        #print(joints.__str__())
        list_joints.append(joints)
        if (keyboard.is_pressed('q')):
            print("inside")
            break
        i=i+1

    rStart.stop()
    Excel.wf_joints("walking", list_joints)
    s.excel_workbook.close()
