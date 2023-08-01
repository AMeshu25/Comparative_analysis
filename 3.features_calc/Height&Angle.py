import pandas as pd
import os
import math
from math import isnan
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
        df = pd.read_excel('SHIFTED/'+file,names=VICON_headers,skiprows=2)
        return df,'RANKx','LANKx',0
    if file[-13:-8] == 'track':
        df = pd.read_excel('SHIFTED/' + file)
        return df,'23z', '19z',3
    if file[-14:-8] == 'ZED4mm':
        df = pd.read_excel('SHIFTED/' + file)
        return df, '24z','20z',2
    if file[-14:-8] == 'ZED2mm':
        df = pd.read_excel('SHIFTED/' + file)
        return df, '24z','20z',1
    if file[-12:-8] == 'Pipe':
        df = pd.read_excel('SHIFTED/' + file)
        return df,'Right ankle_z', 'Left ankle_z',4
    print('!@!@!@!!@!@!@!@!@!PROBLEM IN ',file)
    return [],0,'',''

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

def max_step_height(df,right_ankle, left_ankle):
    df['step_height'] = abs(df[right_ankle]-df[left_ankle])
    temp = df['step_height'].dropna()
    return max(temp)

def get_triangle(knee_x,knee_y,hip_x1,hip_y1,hip_x2,hip_y2,):
    a = math.sqrt((knee_x-hip_x1)**2+(knee_y-hip_y1)**2)
    b = math.sqrt((hip_x2-hip_x1)**2+(hip_y2-hip_y1)**2)
    c = math.sqrt((knee_x-hip_x2)**2+(knee_y-hip_y2)**2)
    return a,b,c

def angle_calculator(a,b,c): #return the gamma angle by the law of cosines
    ans = c**2-a**2-b**2
    ans = ans/(2*a*b)
    return math.degrees(math.acos(ans))

def max_legs_angle(right_knee_x,right_knee_y,left_knee_x,left_knee_y,rasi_x,rasi_y,lasi_x,lasi_y):
    all_angles_ls = []
    for i in range(len(right_knee_x)):
        left_calc = [left_knee_x.loc[i],left_knee_y.loc[i],lasi_x.loc[i],lasi_y.loc[i],rasi_x.loc[i],rasi_y.loc[i]]
        right_calc = [right_knee_x.loc[i],right_knee_y.loc[i],rasi_x.loc[i],rasi_y.loc[i],lasi_x.loc[i],lasi_y.loc[i]]
        a,b,c = get_triangle(left_calc[0],left_calc[1],left_calc[2],left_calc[3],left_calc[4],left_calc[5])
        left_angle = angle_calculator(a,b,c)
        a, b, c = get_triangle(right_calc[0],right_calc[1],right_calc[2],right_calc[3],right_calc[4],right_calc[5])
        right_angle = angle_calculator(a,b,c)
        all_angles_ls.append(right_angle+left_angle-180)
    all_angles_ls = [x for x in all_angles_ls if isnan(x) == False]
    return max(all_angles_ls)
def get_df_angle_camera(file):
    if file[-13:-8] == 'VICON':
        df = pd.read_excel('SHIFTED/'+file,names=VICON_headers,skiprows=2)
        return df,'RKNEy','RKNEz','RASIy','RASIz','LASIy','LASIz','LKNEy','LKNEz',0
    if file[-13:-8] == 'track':
        df = pd.read_excel('SHIFTED/' + file)
        return df,'22x','22y','21x','21y','17x','17y','18x','18y',3
    if file[-14:-8] == 'ZED4mm':
        df = pd.read_excel('SHIFTED/' + file)
        return df,'23x','23y','22x','22y','18x','18y','19x','19y',2
    if file[-14:-8] == 'ZED2mm':
        df = pd.read_excel('SHIFTED/' + file)
        return df,'23x','23y','22x','22y','18x','18y','19x','19y',1
    if file[-12:-8] == 'Pipe':
        df = pd.read_excel('SHIFTED/' + file)
        return df,'Right knee_x','Right knee_y','Right hip_x','Right hip_y','Left hip_x','Left hip_y','Left knee_x','Left knee_y',4
    print('!@!@!@!!@!@!@!@!@!PROBLEM IN ',file)
    return [],0,'',''

def min_squat_angle(ankle_y,ankle_z,knee_y,knee_z, hip_y, hip_z):
    all_angles_ls = []
    for i in range(len(ankle_y)):
        a, b,c = get_triangle(ankle_y.loc[i],ankle_z.loc[i],knee_y.loc[i],knee_z.loc[i],hip_y.loc[i],hip_z.loc[i])
        angle = angle_calculator(a,b,c)
        all_angles_ls.append(angle)
    all_angles_ls = [x for x in all_angles_ls if isnan(x) == False]
    return min(all_angles_ls)

def get_df_leg_angle_camera(file):
    if file[-13:-8] == 'VICON':
        df = pd.read_excel('SHIFTED/'+file,names=VICON_headers,skiprows=2)
        return df,'RANKz','RANKx','RKNEz','RKNEx','RASIz','RASIx',0
    if file[-13:-8] == 'track':
        df = pd.read_excel('SHIFTED/' + file)
        return df,'23y','23z','22y','22z','21y','21z',3
    if file[-14:-8] == 'ZED4mm':
        df = pd.read_excel('SHIFTED/' + file)
        return df,'24y','24z','23y','23z','22y','22z',2
    if file[-14:-8] == 'ZED2mm':
        df = pd.read_excel('SHIFTED/' + file)
        return df,'24y','24z','23y','23z','22y','22z',1
    if file[-12:-8] == 'Pipe':
        df = pd.read_excel('SHIFTED/' + file)
        return df,'Right ankle_y','Right ankle_z','Right knee_y','Right knee_z','Right hip_y','Right hip_z',4
    print('!@!@!@!!@!@!@!@!@!PROBLEM IN ',file)
    return [],'','','','','',''

# -----------------MIN LEG ANGLE calculations----------------

# angle_dic = {}
# mone = 1
# for exp in exp_by_s_dic:
#     angle_lst_count = [0, 0, 0, 0, 0]
#     for file in exp_by_s_dic[exp]:
#         print(mone, '. started with->', file)
#         df, right_ankle_y,right_ankle_z,right_knee_y,right_knee_z,rasi_y,rasi_z, i = get_df_leg_angle_camera(file)
#         angle = min_squat_angle(df[right_ankle_y],df[right_ankle_z],df[right_knee_y],df[right_knee_z],df[rasi_y],df[rasi_z])
#         angle_lst_count[i] += angle*1000    #because values are small
#         angle_dic[exp] = angle_lst_count
#     mone += 1
#     # if mone == 2:
#     #     break
# df_angle = pd.DataFrame(data=angle_dic)
# print(df_angle.T)
# df_angle.T.to_excel('MIN_leg_angle.xlsx')
# -----------------MAX ANGLE calculations----------------

# angle_dic = {}
# mone = 1
# for exp in exp_by_s_dic:
#     angle_lst_count = [0, 0, 0, 0, 0]
#     for file in exp_by_s_dic[exp]:
#         print(mone, '. started with->', file)
#         df, right_knee_x,right_knee_y,rasi_x,rasi_y,lasi_x,lasi_y,left_knee_x,left_knee_y, i = get_df_angle_camera(file)
#         angle = max_legs_angle(df[right_knee_x],df[right_knee_y],df[rasi_x],df[rasi_y],df[lasi_x],df[lasi_y],df[left_knee_x],df[left_knee_y])
#         angle_lst_count[i] += angle
#         angle_dic[exp] = angle_lst_count
#     mone += 1
#     # if mone == 3:
#     #     break
# df_angle = pd.DataFrame(data=angle_dic)
# print(df_angle.T)
# df_angle.T.to_excel('Max_legs_angle.xlsx')

#-----------------MAX STEP HEIGHT&LENGTH calculations----------------
# max_dic ={}
# mone =1
# for exp in exp_by_s_dic:
#     max_lst_count=[0,0,0,0,0]
#     for file in exp_by_s_dic[exp]:
#         print(mone,'. started with->',file)
#         df,right_ankle,left_ankle,i = get_df_camera(file)
#         maxi = max_step_height(df,right_ankle,left_ankle)
#         max_lst_count[i]+=maxi
#     max_dic[exp] = max_lst_count
#     mone+=1
#     # if mone == 17:
#     #     break
# df_max = pd.DataFrame(data=max_dic)
# print(df_max.T)
# df_max.T.to_excel('Max_step_length.xlsx')
# df_min.T.to_excel('Min_dist.xlsx')


#-----------------------RMSE MAX STEP HEIGHT ----------
from sklearn.metrics import mean_squared_error
#--------RMSE vs VICON
# ['orchid','lightskyblue', 'lightgreen', 'lightpink', 'lightyellow']
#  [''Vicon', 'ZED2mm', 'ZED4mm', 'MediaPipe', 'Nuitrack']
# df = pd.read_excel('Max_legs_angle.xlsx')
# df_ZED2mm = df[df[1]!=0][[0,1]]
# rms_ZED2mm = mean_squared_error(df_ZED2mm[0], df_ZED2mm[1], squared=False)
# df_ZED4mm = df[df[2]!=0][[0,2]]
# rms_ZED4mm = mean_squared_error(df_ZED4mm[0], df_ZED4mm[2], squared=False)
# df_NUITRACK = df[df[3]!=0][[0,3]]
# rms_NUITRACK = mean_squared_error(df_NUITRACK[0], df_NUITRACK[3], squared=False)
#
# df_MEDIA = df[df[4]!=0][[0,4]]
# rms_MEDIA = mean_squared_error(df_MEDIA[0], df_MEDIA[4], squared=False)
# RMSE = [rms_ZED2mm,rms_ZED4mm,rms_MEDIA,rms_NUITRACK]
# cameras =['ZED2mm', 'ZED4mm', 'MediaPipe', 'Nuitrack']
# col =['lightskyblue', 'lightgreen', 'lightpink', 'lightyellow']
# bars = plt.bar(cameras,RMSE,color = col)
# plt.title('RMSE of each camera vs the VICON')
# plt.ylabel('RMSE')
# for bar in bars:
#     yval=round(bar.get_height(),3)
#     plt.text(bar.get_x(),yval,yval)
#
# plt.show()

#-----------------------RMSE MAM STEP LENGTH ----------
#--------RMSE vs VICON
# ['orchid','lightskyblue', 'lightgreen', 'lightpink', 'lightyellow']
#  [''Vicon', 'ZED2mm', 'ZED4mm', 'MediaPipe', 'Nuitrack']
# df = pd.read_excel('Max_step_length.xlsx')
# df_ZED2mm = df[df[1]!=0][[0,1]]
# rms_ZED2mm = mean_squared_error(df_ZED2mm[0], df_ZED2mm[1], squared=False)
# df_ZED4mm = df[df[2]!=0][[0,2]]
# rms_ZED4mm = mean_squared_error(df_ZED4mm[0], df_ZED4mm[2], squared=False)
# df_NUITRACK = df[df[3]!=0][[0,3]]
# rms_NUITRACK = mean_squared_error(df_NUITRACK[0], df_NUITRACK[3], squared=False)
#
# df_MEDIA = df[df[4]!=0][[0,4]]
# rms_MEDIA = mean_squared_error(df_MEDIA[0], df_MEDIA[4], squared=False)
# RMSE = [rms_ZED2mm,rms_ZED4mm,rms_MEDIA,rms_NUITRACK]
# cameras =['ZED2mm', 'ZED4mm', 'MediaPipe', 'Nuitrack']
# col =['lightskyblue', 'lightgreen', 'lightpink', 'lightyellow']
# bars = plt.bar(cameras,RMSE,color = col)
# plt.title('RMSE of each camera vs the VICON')
# plt.ylabel('RMSE')
# for bar in bars:
#     yval=round(bar.get_height(),3)
#     plt.text(bar.get_x(),yval,yval)
#
# plt.show()

#-----------------------RMSE MAM LEGS ANGLE ----------
#--------RMSE vs VICON
# ['orchid','lightskyblue', 'lightgreen', 'lightpink', 'lightyellow']
#  [''Vicon', 'ZED2mm', 'ZED4mm', 'MediaPipe', 'Nuitrack']
df = pd.read_excel('MAX_legs_angle.xlsx')
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