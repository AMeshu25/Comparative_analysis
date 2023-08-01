import pandas as pd
import os
import math
from math import isnan
import statistics
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
        df = pd.read_excel('SHIFTED/' + file, names=VICON_headers, skiprows=2)
        return df, 'RASIy', 'RASIz', 'LASIy', 'LASIz', 0
    if file[-13:-8] == 'track':
        df = pd.read_excel('SHIFTED/' + file)
        return df, '21x', '21y', '17x', '17y', 3
    if file[-14:-8] == 'ZED4mm':
        df = pd.read_excel('SHIFTED/' + file)
        return df, '22x', '22y', '18x', '18y', 2
    if file[-14:-8] == 'ZED2mm':
        df = pd.read_excel('SHIFTED/' + file)
        return df, '22x', '22y', '18x', '18y', 1
    if file[-12:-8] == 'Pipe':
        df = pd.read_excel('SHIFTED/' + file)
        return df, 'Right hip_x', 'Right hip_y', 'Left hip_x', 'Left hip_y', 4
    print('!@!@!@!!@!@!@!@!@!PROBLEM IN ', file)
    return [], '', '', '', '', '', ''

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
ZED_path = 'ZED/'
ZED_filesnames = os.listdir(ZED_path)
VICON_path = 'VICON/'
VICON_filesnames = os.listdir(VICON_path)
NUITRACK_path = 'NUITRACK/'
NUITRACK_filesnames = os.listdir(NUITRACK_path)
MEDIA_path = 'MEDIA/'
MEDIA_filesnames = os.listdir(MEDIA_path)
exp_by_s_dic = merge_by_exp(ZED_filesnames,VICON_filesnames,NUITRACK_filesnames,MEDIA_filesnames)

def max_Z(vector):
    vector = vector.dropna()
    ls_coor = vector.values
    maxi = ls_coor[0]
    for val in ls_coor[1:]:
        if val>maxi:
            maxi = val
    return maxi

def min_Z(vector):
    vector = vector.dropna()
    ls_coor = vector.values
    mini = ls_coor[0]
    for val in ls_coor[1:]:
        if val<mini:
            mini = val
    return mini

def get_vetor_len(hip_x1,hip_y1,hip_x2,hip_y2):
    a = math.sqrt((hip_x2-hip_x1)**2+(hip_y2-hip_y1)**2)
    return a

def average_body_len(rasi_x,rasi_y,lasi_x,lasi_y):
    width_lst = []
    for i in range(len(rasi_x)):
        length = get_vetor_len(rasi_x.iloc[i],rasi_y.iloc[i],lasi_x.iloc[i], lasi_y.iloc[i])
        width_lst.append(length)
        width_lst = [x for x in width_lst if isnan(x) == False]
        avg = statistics.mean(width_lst)
        return avg


# avg_dic ={}
# mone =1
# for exp in exp_by_s_dic:
#     avg_lst_width=[0,0,0,0,0]
#     for file in exp_by_s_dic[exp]:
#         print(mone,'. started with->',file)
#         df,right_hip_x,right_hip_y,left_hip_x,left_hip_y,i = get_df_camera(file)
#         avg = average_body_len(df[right_hip_x],df[right_hip_y],df[left_hip_x],df[left_hip_y])
#         avg_lst_width[i]+=avg
#     avg_dic[exp] = avg_lst_width
#     mone+=1
#     # if mone == 3:
#     #     break
# df_avg = pd.DataFrame(data=avg_dic)
# print(df_avg.T)
# df_avg.T.to_excel('Avg_Body_length.xlsx')

#-----------------------RMSE AVG BODY LENGTH ----------
from sklearn.metrics import mean_squared_error
#--------RMSE vs VICON
# ['orchid','lightskyblue', 'lightgreen', 'lightpink', 'lightyellow']
#  [''Vicon', 'ZED2mm', 'ZED4mm', 'MediaPipe', 'Nuitrack']
df = pd.read_excel('Avg_Body_length.xlsx')
df_ZED2mm = df[df[1]!=0][[0,1]]
rms_ZED2mm = mean_squared_error(df_ZED2mm[0], df_ZED2mm[1], squared=False)
df_ZED4mm = df[df[2]!=0][[0,2]]
rms_ZED4mm = mean_squared_error(df_ZED4mm[0], df_ZED4mm[2], squared=False)
df_NUITRACK = df[df[3]!=0][[0,3]]
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

df_ZED2mm[1].plot(c='r')
df_ZED2mm[0].plot(c='m')
plt.show()
df_ZED4mm[2].plot(c='r')
df_ZED4mm[0].plot(c='m')
plt.show()
df_NUITRACK[3].plot(c='r')
df_NUITRACK[0].plot(c='m')
plt.show()
df_MEDIA[4].plot(c='r')
df_MEDIA[0].plot(c='m')
plt.show()
