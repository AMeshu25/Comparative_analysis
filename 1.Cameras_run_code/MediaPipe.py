import cv2 as cv
import mediapipe as mp
import xlsxwriter
from mediapipe.framework.formats import landmark_pb2
import time
import pandas as pd
import datetime
import os

def wf_joints(folder_name, worksheet_name, list_joints, allFlag):
    '''
    Writing joints data for an exercise in Excel file in two versions
    :param ex_name:
    :param list_joints:
    :return:
    '''
    if(allFlag==False):
        jointsNumber = {"0":1, "1": 4, "2": 7, "3":10, "4":13, "5":16, "6":19, "7":22, "8":25, "9":28, "10":31, "11":34, "12":37,
                    "13":40, "14":43, "15":46, "16":49, "17":52, "18":55, "19":58, "20":61, "21":64, "22":67,
                    "23": 70, "24": 73, "25": 76, "26": 79, "27": 82, "28": 85, "29": 88, "30": 91, "31": 94, "32": 97}
    else:
        jointsNumber = {"0": 1, "1": 5, "2": 9, "3": 13, "4": 17, "5": 21, "6": 25, "7": 29, "8": 33, "9": 37,
                        "10": 41, "11": 45, "12": 49, "13": 53, "14": 57, "15": 61, "16": 65, "17": 69, "18": 73, "19": 77,
                        "20": 81, "21": 85, "22": 89, "23": 93, "24": 97, "25": 101, "26": 105, "27": 109, "28": 113, "29": 117,
                        "30": 121, "31": 125, "32": 127}
    excel_workbook = xlsxwriter.Workbook(folder_name + "/" + worksheet_name)
    current_time = datetime.datetime.now()
    name = "mediaPipe" + str(current_time.minute) + str(current_time.second)
    worksheet = excel_workbook.add_worksheet(name)
    worksheet.write(0, 0, 'Key Point Number->')
    for x, y in jointsNumber.items():
        worksheet.write(0, y, x)
    frame_number = 1
    row = 1
    for jointFrame in list_joints: #specific frame
        worksheet.write(row, 0, frame_number)
        for j in jointFrame:  # specific joint - data inside the frame - same row all the joints in the frame
            col=jointsNumber.get(str(j[0]))
            for i in range(1, len(j)): #data of the joint
                worksheet.write(row, col, str(j[i]) )
                col += 1
        frame_number += 1
        row += 1

    excel_workbook.close()

def live_pose():
    #cap = cv.VideoCapture(0)# For webcam input:
    cap = cv.VideoCapture(0) #camera input usb near headphone
    print (cap.grab())
    frameNumber = 0
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    #name=time.strftime("%Y_%m_%d_%H_%M_%S")
    #naama to change!!
    subjectNum="28"
    sessionNum="S2"
    name=subjectNum+"_MediaPipe_"+sessionNum
    folder_name='DataFromCode/Data_'+name

    os.mkdir(folder_name)
    list_joints=[]
    list_joints_all=[]

    # For Video input:
    prevTime = 0
    with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.5) as pose:
        nolist = True
        landmarkes_data = pd.DataFrame()
        landmarkes_data_all = pd.DataFrame()  # for test
        while cap.isOpened():  # testing only this class
            #print("Inside")
            # while (not s.finish_workout): #for the all components
            success, image = cap.read()
            image_width = cap.get(cv.CAP_PROP_FRAME_WIDTH)  # float `width`
            image_height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)  # float `height`

            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # Convert the BGR image to RGB - change the colors.
            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            results = pose.process(image)


            if not results.pose_landmarks:
                continue  # back to the beginning of the loop

            # Draw the pose annotation on the image.
            image.flags.writeable = True
            image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
            frameNumber = frameNumber + 1
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            cv.putText(image, f'FrameNumber: {int(frameNumber)}', (20, 70), cv.FONT_HERSHEY_PLAIN, 3, (0, 196, 255), 2)
            # path = R'C:\Users\TEMP.NAAMA\Desktop\ImageFromCode' + "\\" + str(frameNumber) + ".jpg"
            # cv.imwrite(path, image)
            cv.imshow('Final_Project', image)  # show the picture
            path = folder_name + "\\" + str(frameNumber) + ".jpg"
            cv.imwrite(path, image)# save the picture to a new folder
            #all the joint mediaPipe can predict
            # joint_human_dict={'nose': "0",
            #                   'L_eye_inner': "1", 'L_eye': "2", "L_eye_outer": "3",
            #                   'R_eye_inner': "4", 'R_eye': "5", "R_eye_outer": "6",
            #                   'L_ear': "7", 'R_ear': "8", "L_mouth": "9","R_mouth": "10",
            #                   'L_Shoulder': "11", 'R_Shoulder': "12", 'L_Elbow': "13", 'R_Elbow': "14",
            #                   'L_Wrist': "15", 'R_Wrist': "16",
            #                   'L_pinky': "17", 'R_pinky': "18", 'L_index': "19", 'R_index': "20",
            #                   'L_thumb': "21", 'R_thumb': "22", 'L_hip': "23", 'R_hip': "24",
            #                   'L_knee': "25", 'R_knee': "26", 'L_ankle': "27", 'R_ankle': "28",
            #                   'L_heel': "29", 'R_heel': "30", 'L_foot_index': "31", 'R_foot_index': "32"}
            #
            # joint_humam_dict_exist = {'frameNumber': [frameNumber, 'x', 'y', 'z']}
            # joint_humam_dict_all = {'frameNumber': [frameNumber, 'x', 'y', 'z', ""]}
            jointsFrame = []
            jointsFrameAll = []
            for jointNum in range(0,33):
                if (results.pose_landmarks.landmark[jointNum].visibility >= 0.7):
                    print("inside")
                    joint=[jointNum,results.pose_landmarks.landmark[jointNum].x * image_width,
                                                   results.pose_landmarks.landmark[jointNum].y * image_height,
                                                   results.pose_landmarks.landmark[jointNum].z * image_width]

                    jointsFrame.append(joint)
                #all the options
                jointsFrameAll.append([jointNum, results.pose_landmarks.landmark[jointNum].visibility,
                                    results.pose_landmarks.landmark[jointNum].x * image_width,
                                        results.pose_landmarks.landmark[jointNum].y * image_height,
                                        results.pose_landmarks.landmark[jointNum].z * image_width])
            print("fefsdff")
            print(jointsFrame)
            list_joints.append(jointsFrame)
            list_joints_all.append(jointsFrameAll)
            key = cv.waitKey(1)
            if key == ord('q'):
                wf_joints(folder_name, name+".xlsx", list_joints, False)
                wf_joints(folder_name, name + "_All.xlsx", list_joints_all, True)
                cap.release()
                break

        cap.release()

if __name__ == '__main__':
    live_pose()

