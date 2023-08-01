import pandas as pd
import numpy as np
import os
from matplotlib import pyplot as plt



def merge_by_exp(ZED_lst, VICON_lst, NUITRACK_lst, MEDIA_lst):  #return a dic that key = experimet, value = list of files name
    file_by_exp = {}
    for exp in VICON_lst:
        temp_ZED =0
        for ZED_exp in ZED_lst:
            if exp[0:2]== ZED_exp[0:2] and exp[-6]== ZED_exp[-6]:
                temp_ZED= ZED_exp
                break
        temp_NUITRACK=0
        for NUITRACK_exp in NUITRACK_lst:
            if exp[0:2] == NUITRACK_exp[0:2] and exp[-6] == NUITRACK_exp[-6]:
                temp_NUITRACK=NUITRACK_exp
                break
        temp_MEDIA=0
        for MEDIA_exp in MEDIA_lst:
            if exp[0:2] == MEDIA_exp[0:2] and exp[-6] == MEDIA_exp[-6]:
                temp_MEDIA=MEDIA_exp
                break
        ans =[]
        ans.append(exp)
        if temp_ZED!= 0:
            ans.append(temp_ZED)
        if temp_NUITRACK!=0:
            ans.append(temp_NUITRACK)
        if temp_MEDIA!=0:
            ans.append(temp_MEDIA)
        file_by_exp[exp[0:2]+'_s'+exp[-6]] = ans
    return file_by_exp
def get_df_camera(file):    #gets directory and return df and param
    if file[-13:-8] == 'VICON':
        df = pd.read_excel('SHIFTED/' + file, names=VICON_headers,skiprows=2)
        return df, 'LSHOy', 'RSHOy', 0
    if file[-13:-8] == 'track':
        df = pd.read_excel('SHIFTED/' + file, names=NUITRACK_headers)
        return df, '6x', '12x', 3
    if file[-14:-8] == 'ZED4mm':
        df = pd.read_excel('SHIFTED/' + file)
        return df, '5x', '12x', 2
    if file[-14:-8] == 'ZED2mm':
        df = pd.read_excel('SHIFTED/' + file)
        return df, '5x', '12x', 1
    if file[-12:-8] == 'Pipe':
        df = pd.read_excel('SHIFTED/' + file)
        return df, 'Left shoulder_x', 'Right shoulder_x', 4
    print('!@!@!@!!@!@!@!@!@!PROBLEM IN ', file)
    return [],0,'',''
ZED_path = 'ZED/'
ZED_filesnames = os.listdir(ZED_path)
VICON_path = 'VICON/'
VICON_filesnames = os.listdir(VICON_path)
NUITRACK_path = 'NUITRACK/'
NUITRACK_filesnames = os.listdir(NUITRACK_path)
MEDIA_path = 'MEDIA/'
MEDIA_filesnames = os.listdir(MEDIA_path)
exp_by_s_dic = merge_by_exp(ZED_filesnames,VICON_filesnames,NUITRACK_filesnames,MEDIA_filesnames)

joints = ['LFHD','RFHD','LBHD','RBHD','C7','T10','CLAV','STRN','RBAK','LSHO','LUPA','LELB','LFRM','LWRA','LWRB','LFIN',
           'RSHO','RUPA','RELB','RFRM','RWRA','RWRB','RFIN','LASI','RASI','LPSI','RPSI','LTHI','LKNE','LTIB','LANK','LHEE','LTOE','RTHI','RKNE','RTIB','RANK','RHEE','RTOE']
coordinates =['x','y','z']
VICON_headers =[]
VICON_headers.append('Frame')
VICON_headers.append('Sub_Frame')
for joint in joints:
    for cor in coordinates:
        VICON_headers.append(joint+cor)
joints = list(range(1,24))        #18 is left ankle
joints.remove(10)   #those joints are not in the file
joints.remove(16)
joints.remove(20)
NUITRACK_headers =['Frame']
for joint in joints:
    for cor in coordinates:
        NUITRACK_headers.append(str(joint)+cor)

#-------------Fixing Z coordinate for ZED and NUITRACK -------------




# df_manual = pd.read_excel('manual_count_steps.xlsx')
#------------------------------ Turning count NEW FEATURE -------------------

def turning_count(left,right):      #gets left and right vector and calculate the turning
    front_looking =True     #the experiment allways start looking to the cameras
                            #meaning right<left
    left_temp = left.dropna()
    right_temp = right.dropna()
    # print(right_temp)
    left_ls = left_temp.values
    right_ls = right_temp.values
    # print(right_ls)
    # print(left_ls)
    turning_mone =0
    range_count = 0
    len_run = min(len(left_ls),len(right_ls))
    for i in range(len_run):
        if front_looking and right_ls[i]>left_ls[i]:
            turning_mone+=1
            # range_count=1
            front_looking=False
        # elif not front_looking and right_ls[i]>left_ls[i]:
        #     range_count += 1
        # if range_count==5:
        #     turning_mone+=1
        if not front_looking and right_ls[i]<left_ls[i]:
            # print('Did IT')
            turning_mone += 1
            # range_count = 1
            front_looking=True
        # elif front_looking and right_ls[i]<left_ls[i]:
        #     range_count+=1
    return turning_mone


# steps_count_dic ={}
# mone =1
# for exp in exp_by_s_dic:
#     temp_lst_count=[0,0,0,0,0]
#     for file in exp_by_s_dic[exp]:
#         print(mone,'. started with->',file)
#         df,left,right,i = get_df_camera(file)
#         steps_count = turning_count(df[left],df[right])
#         if steps_count==0:
#             temp_lst_count[i]=-1
#         else:
#             temp_lst_count[i]=steps_count
#     steps_count_dic[exp] = temp_lst_count
#     mone+=1
#     # if mone==6:
#     #     break
# df = pd.DataFrame(data=steps_count_dic)
# print(df.T)
# df.T.to_excel('Turning_Count.xlsx')

#-----------------RMSE calculations steps count 2
from sklearn.metrics import mean_squared_error
#--------RMSE vs VICON
# ['orchid','lightskyblue', 'lightgreen', 'lightpink', 'lightyellow']
#  [''Vicon', 'ZED2mm', 'ZED4mm', 'MediaPipe', 'Nuitrack']
df = pd.read_excel('Turning_Count.xlsx')
df_ZED2mm = df[df[1]!=0][[0,1]]
rms_ZED2mm = mean_squared_error(df_ZED2mm[0], df_ZED2mm[1], squared=False)
df_ZED4mm = df[df[2]!=0][[0,2]]
rms_ZED4mm = mean_squared_error(df_ZED4mm[0], df_ZED4mm[2], squared=False)
df_NUITRACK = df[df[3]!=0][[0,3]]
df_NUITRACK[3] = df_NUITRACK[3].replace([-1],0)
# if len(df_NUITRACK[3])!=0:
rms_NUITRACK = mean_squared_error(df_NUITRACK[0], df_NUITRACK[3], squared=False)

df_MEDIA = df[df[4]!=0][[0,4]]
rms_MEDIA = mean_squared_error(df_MEDIA[0], df_MEDIA[4], squared=False)
RMSE = [rms_ZED2mm,rms_ZED4mm,rms_MEDIA,rms_NUITRACK]
cameras =['ZED2mm', 'ZED4mm', 'MediaPipe', 'Nuitrack']
col =['lightskyblue', 'lightgreen', 'lightpink', 'lightyellow']
bars = plt.bar(cameras,RMSE,color = col)
plt.title('RMSE of each camera vs the VICON')
plt.ylabel('RMSE')
for bar in bars:
    yval=round(bar.get_height(),3)
    plt.text(bar.get_x(),yval,yval)

plt.show()
#
# #--------RMSE vs manual
# df_res = pd.read_excel('manual_count_steps.xlsx')
# df = pd.read_excel('Turning_Count.xlsx')
# df['manual'] = 2
# rms_VICON = mean_squared_error(df['manual'], df[0], squared=False)
# df_ZED2mm = df[df[1]!=0]
# rms_ZED2mm = mean_squared_error(df_ZED2mm['manual'], df_ZED2mm[1], squared=False)
# df_ZED4mm = df[df[2]!=0]
# rms_ZED4mm = mean_squared_error(df_ZED4mm['manual'], df_ZED4mm[2], squared=False)
# df_NUITRACK = df[df[3]!=0]
# df_NUITRACK[3] = df_NUITRACK[3].replace([-1],0)
# if len(df_NUITRACK[3])!=0:
#     rms_NUITRACK = mean_squared_error(df_NUITRACK['manual'], df_NUITRACK[3], squared=False)
# else:
#     rms_NUITRACK=100
# df_MEDIA = df[df[4]!=0]
# rms_MEDIA = mean_squared_error(df_MEDIA['manual'], df_MEDIA[4], squared=False)
# RMSE = [rms_VICON,rms_ZED2mm,rms_ZED4mm,rms_MEDIA,rms_NUITRACK]
# cameras =['Vicon', 'ZED2mm', 'ZED4mm', 'MediaPipe', 'Nuitrack']
# col =['orchid','lightskyblue', 'lightgreen', 'lightpink', 'lightyellow']
# bars = plt.bar(cameras,RMSE,color = col)
# plt.title('RMSE of each camera vs the MANUAL')
# plt.ylabel('RMSE')
# for bar in bars:
#     yval=round(bar.get_height(),3)
#     plt.text(bar.get_x(),yval,yval)
#
# plt.show()