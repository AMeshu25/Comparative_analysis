########################################################################
#
# Copyright (c) 2022, STEREOLABS.
#
# All rights reserved.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
########################################################################

import pyzed.sl as sl
import keyboard
import cv2
import numpy as np
import pandas as pd
import xlsxwriter
import msvcrt

def main():
    # Create a Camera object
    zed = sl.Camera()

    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD720  # Use HD720 video mode
    init_params.depth_mode = sl.DEPTH_MODE.PERFORMANCE
    init_params.coordinate_units = sl.UNIT.METER
    init_params.sdk_verbose = True
    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        exit(1)

    obj_param = sl.ObjectDetectionParameters()
    # Different model can be chosen, optimizing the runtime or the accuracy
    obj_param.detection_model = sl.DETECTION_MODEL.HUMAN_BODY_FAST
    obj_param.enable_tracking = True
    obj_param.image_sync = True
    obj_param.enable_mask_output = False
    # Optimize the person joints position, requires more computations
    obj_param.enable_body_fitting = True
    obj_param.body_format = sl.BODY_FORMAT.POSE_34

    camera_infos = zed.get_camera_information()
    if obj_param.enable_tracking:
        positional_tracking_param = sl.PositionalTrackingParameters()
        # positional_tracking_param.set_as_static = True
        positional_tracking_param.set_floor_as_origin = True
        zed.enable_positional_tracking(positional_tracking_param)

    print("Object Detection: Loading Module...")

    err = zed.enable_object_detection(obj_param)
    if err != sl.ERROR_CODE.SUCCESS:
        print(repr(err))
        zed.close()
        exit(1)

    objects = sl.Objects()
    obj_runtime_param = sl.ObjectDetectionRuntimeParameters()
    # For outdoor scene or long range, the confidence should be lowered to avoid missing detections (~20-30)
    # For indoor scene or closer range, a higher confidence limits the risk of false positives and increase the precision (~50+)
    obj_runtime_param.detection_confidence_threshold = 50
    ls_frames =[]
    frame_num=0
    while zed.grab() == sl.ERROR_CODE.SUCCESS:
        err = zed.retrieve_objects(objects, obj_runtime_param)
        if objects.is_new:
            obj_array = objects.object_list
            print(str(len(obj_array)) + " Person(s) detected\n")
            if len(obj_array) > 0:
                first_object = obj_array[0]
                print("First Person attributes:")
                print(" Confidence (" + str(int(first_object.confidence)) + "/100)")
                if obj_param.enable_tracking:
                    print(" Tracking ID: " + str(int(first_object.id)) + " tracking state: " + repr(
                        first_object.tracking_state) + " / " + repr(first_object.action_state))
                position = first_object.position
                velocity = first_object.velocity
                dimensions = first_object.dimensions
                print(" 3D position: [{0},{1},{2}]\n Velocity: [{3},{4},{5}]\n 3D dimentions: [{6},{7},{8}]".format(
                    position[0], position[1], position[2], velocity[0], velocity[1], velocity[2], dimensions[0],
                    dimensions[1], dimensions[2]))
                if first_object.mask.is_init():
                    print(" 2D mask available")

                print(" Keypoint 2D ")
                keypoint_2d = first_object.keypoint_2d
                for it in keypoint_2d:
                    print("    " + str(it))
                print("\n Keypoint 3D ")
                keypoint = first_object.keypoint
                for it in keypoint:
                    print("    " + str(it))
                ls_frames.append(keypoint)
                frame_num=frame_num+1
                if keyboard.is_pressed('q'):
                    break
    print('--------------------------------------------------------------------------------------------')
    # Close the camera
    zed.close()

    workbook = xlsxwriter.Workbook('Amir.xlsx')
    worksheet = workbook.add_worksheet()
    row_num =2
    col_num =1
    frame_num=0
    worksheet.write(2,0,'x')
    worksheet.write(3,0,'y')
    worksheet.write(4,0,'z')
    worksheet.write(1, col_num - 1, 'Key Point Number')
    for i in ls_frames: #run over each skeleton frame
        worksheet.write(0, col_num-1, 'Frame Number')
        worksheet.write(0,col_num,frame_num)
        key_num=0
        for keypoint in i:   #run over x, y and z for each skeleton point
            worksheet.write(1,col_num,key_num)
            worksheet.write(row_num,col_num,keypoint[0])
            worksheet.write(row_num+1, col_num, keypoint[1])
            worksheet.write(row_num+2, col_num, keypoint[2])
            col_num= col_num+1
            key_num=key_num+1
        frame_num=frame_num+1
    workbook.close()

    # with xlsxwriter.Workbook('frames.xlsx') as workbook:
    #     worksheet = workbook.add_worksheet()
    #     for row_num,data in enumerate(ls_frames):
    #         worksheet.write_row(row_num,0,data)
    # pd.Series(ls_frames)
    # ls_frames.to_excel('frames.xlsx')
    # df = pd.DataFrame(ls_frames).T
    # df.to_csv('frames.csv')




if __name__ == "__main__":
    main()
