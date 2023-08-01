import pandas as pd
import numpy as np
import os
from matplotlib import pyplot as plt
from scipy.signal import butter, filtfilt

def derivative(vector): #calculates the derivative of X vector by delta X where delta t is allways 1
    temp=vector.dropna()
    # print(vector.isna().sum())
    vector_ls = temp.values
    derivative_ls=[]
    for i in range(len(vector_ls)-1):
        derivative_ls.append(vector_ls[i+1]-vector_ls[i])
    df_derivative = pd.DataFrame(derivative_ls,columns=['der'])
    return df_derivative

def mean_filtering(mean_size,vector):
    vector_ls = vector.values
    for i in range(len(vector_ls)-mean_size):
        new_value = vector_ls[i]
        for j in range(i+1,i+mean_size):
            new_value +=vector_ls[j]
        new_value = new_value/mean_size
        vector_ls[i] = new_value
    df_filtered = pd.DataFrame(vector_ls,columns=['der'])
    return df_filtered

def butter_filter(vector,cutoff,fps):
    filter_order =2
    y,x = butter(filter_order,cutoff/(fps/2))
    right = filtfilt(y,x,vector)
    df = pd.DataFrame(right,columns=['z'])
    return df
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
def steps_count_derivative(vector,butter_param,fps,zero_param):     #
    # if butter_param!=2.9:
    #     vector = butter_filter(vector, butter_param, fps)
    df_der = derivative(vector)
    df_der[abs(df_der['der']) < zero_param] = 0
    der_ls = df_der['der'].values
    on_move = False
    steps_counter = 0
    for der in der_ls:
        if der !=0 and not on_move:
            on_move=True
            steps_counter+=1
        if der==0 and on_move:
            on_move=False
    # print('Count is = ', steps_counter)
    return steps_counter*2
def get_df_camera(file):    #gets directory and return df and param
    ZED4mm_param = 90
    ZED2mm_param = 80
    VICON_param = 7
    NUITRACK_param = 3
    MEDIA_param = 210
    if file[-13:-8] == 'VICON':
        df = pd.read_excel('SHIFTED/'+file,names=VICON_headers,skiprows=2)
        return df,'RANKx',120,VICON_param,0
    if file[-13:-8] == 'track':
        df = pd.read_excel('SHIFTED/' + file, names=NUITRACK_headers)
        return df,'23z',30, NUITRACK_param,3
    if file[-14:-8] == 'ZED4mm':
        df = pd.read_excel('SHIFTED/' + file)
        return df,'24z',30, ZED4mm_param,2
    if file[-14:-8] == 'ZED2mm':
        df = pd.read_excel('SHIFTED/' + file)
        return df,'24z',30, ZED2mm_param,1
    if file[-12:-8] == 'Pipe':
        df = pd.read_excel('SHIFTED/' + file)
        return df,'Right ankle_z',30,MEDIA_param,4
    print('!@!@!@!!@!@!@!@!@!PROBLEM IN ',file)
    return [],0,'',''

def get_exp_name(file):
    exp_num = file[:2] + file[-8]
    print(exp_num)

ZED_path = 'ZED/'
ZED_filesnames = os.listdir(ZED_path)
VICON_path = 'VICON/'
VICON_filesnames = os.listdir(VICON_path)
NUITRACK_path = 'NUITRACK/'
NUITRACK_filesnames = os.listdir(NUITRACK_path)
MEDIA_path = 'MEDIA/'
MEDIA_filesnames = os.listdir(MEDIA_path)
exp_by_s_dic = merge_by_exp(ZED_filesnames,VICON_filesnames,NUITRACK_filesnames,MEDIA_filesnames)
print(exp_by_s_dic)

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


# df_ZED = pd.read_excel('SHIFTED/3_VICON_s1.xlsx',names=VICON_headers,skiprows=2)
#-------------filtering
# print(butter_filter(df_ZED['24z'],10,30))
# df_manual = pd.read_excel('manual_count_steps.xlsx')
# res_count = []
# real_error =[]
# ls_count = df_manual['count'].values
# ls_exp = df_manual['exp'].values
# dic_manual = {}
# for i in range(len(ls_count)):
#     dic_manual[ls_exp[i]] = ls_count[i]
# print(dic_manual)
# #             #ZED2mm param = 56 | ZED4mm param = 71 | MEDIA = 210 | NUITRACK = 2.9 | VICON = 2.2
# parameters = np.arange(70,90,0.2)
# df = pd.read_excel('Total_steps_2.xlsx')
# df_ZED2mm = df[df[1]!=0]['exp']
# error =[]
# zeros1=[]
# mone =1
# parameter_plot =[]
# for key in df_ZED2mm.values: #exp_by_s_dic:
#     for file in exp_by_s_dic[key][1:2]:
#         print(mone,'. Began with-> ',file)
#         df_NUITRACK = pd.read_excel('SHIFTED/'+file)
#         for param in parameters:
#             # param.append(i)
#             count_steps = steps_count_derivative(df_NUITRACK['24z'],2.9,30,param)
#             error_exp = dic_manual[key]-count_steps
#             error.append(error_exp)
#             zeros1.append(0)
#             parameter_plot.append(param)
#         mone+=1
# # print(error)
# plt.scatter(parameter_plot,error, color='blue')
# plt.scatter(parameter_plot,zeros1, color='salmon')
#
# plt.title('GridSearch the range for velocity 0')
# plt.show()

#----------------------------Create result table ------------------

steps_count_dic ={}
mone =1
for exp in exp_by_s_dic:
    temp_lst_count=[0,0,0,0,0]
    for file in exp_by_s_dic[exp]:
        print(mone,'. started with->',file)
        df,ankle,fps,zero_param,i = get_df_camera(file)
        steps_count = steps_count_derivative(df[ankle],10,fps,zero_param)
        temp_lst_count[i]=steps_count
    steps_count_dic[exp] = temp_lst_count
    mone+=1
    # if mone==5:
    #     break
df = pd.DataFrame(data=steps_count_dic)
print(df.T)
df.T.to_excel('Total_steps_2.xlsx')


#-----------------RMSE calculations steps count 2
from sklearn.metrics import mean_squared_error
#--------RMSE vs VICON
df = pd.read_excel('Total_steps_2.xlsx')
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

# ['orchid','lightskyblue', 'lightgreen', 'lightpink', 'lightyellow']
#  [''Vicon', 'ZED2mm', 'ZED4mm', 'MediaPipe', 'Nuitrack']
#--------RMSE vs manual
# df_res = pd.read_excel('manual_count_steps.xlsx')
# df = pd.read_excel('Total_steps_2.xlsx')
# df['manual'] = df_res['count']
# rms_VICON = mean_squared_error(df['manual'], df[0], squared=False)
# df_ZED2mm = df[df[1]!=0]
# rms_ZED2mm = mean_squared_error(df_ZED2mm['manual'], df_ZED2mm[1], squared=False)
# df_ZED4mm = df[df[2]!=0]
# rms_ZED4mm = mean_squared_error(df_ZED4mm['manual'], df_ZED4mm[2], squared=False)
# df_NUITRACK = df[df[3]!=0]
# rms_NUITRACK = mean_squared_error(df_NUITRACK['manual'], df_NUITRACK[3], squared=False)
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



