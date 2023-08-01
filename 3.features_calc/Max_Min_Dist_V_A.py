import pandas as pd
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
        df = pd.read_excel('SHIFTED/'+file,names=VICON_headers,skiprows=2)
        return df,'RANKx',0
    if file[-13:-8] == 'track':
        df = pd.read_excel('SHIFTED/' + file)
        return df,'23z',3
    if file[-14:-8] == 'ZED4mm':
        df = pd.read_excel('SHIFTED/' + file)
        return df,'24z',2
    if file[-14:-8] == 'ZED2mm':
        df = pd.read_excel('SHIFTED/' + file)
        return df,'24z',1
    if file[-12:-8] == 'Pipe':
        df = pd.read_excel('SHIFTED/' + file)
        return df,'Right ankle_z',4
    print('!@!@!@!!@!@!@!@!@!PROBLEM IN ',file)
    return [],0,''

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

# max_dic ={}
# min_dic={}
# mone =1
# for exp in exp_by_s_dic:
#     max_lst_count=[0,0,0,0,0]
#     min_lst_count=[0,0,0,0,0]
#     for file in exp_by_s_dic[exp]:
#         print(mone,'. started with->',file)
#         df,joint,i = get_df_camera(file)
#         maxi = max_Z(df[joint])
#         mini = min_Z(df[joint])
#         max_lst_count[i]+=maxi
#         min_lst_count[i]+=mini
#     max_dic[exp] = max_lst_count
#     min_dic[exp] = min_lst_count
#     mone+=1
#     # if mone == 15:
#     #     break
# df_max = pd.DataFrame(data=max_dic)
# df_min = pd.DataFrame(data=min_dic)
# df_max.T.to_excel('Max_dist.xlsx')
# df_min.T.to_excel('Min_dist.xlsx')


#-----------------------RMSE MAX ----------
from sklearn.metrics import mean_squared_error
#--------RMSE vs VICON
# ['orchid','lightskyblue', 'lightgreen', 'lightpink', 'lightyellow']
#  [''Vicon', 'ZED2mm', 'ZED4mm', 'MediaPipe', 'Nuitrack']
df = pd.read_excel('Max_dist.xlsx')
# df = df[df[0]>500]
df_ZED2mm = df[df[1]!=0][[0,1]]
rms_ZED2mm = mean_squared_error(df_ZED2mm[0], df_ZED2mm[1], squared=False)
df_ZED4mm = df[df[2]!=0][[0,2]]
rms_ZED4mm = mean_squared_error(df_ZED4mm[0], df_ZED4mm[2], squared=False)
df_NUITRACK = df[df[3]!=0][[0,3]]
print(df_ZED4mm)
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

#-----------------------RMSE MIN ----------
from sklearn.metrics import mean_squared_error
#--------RMSE vs VICON
# ['orchid','lightskyblue', 'lightgreen', 'lightpink', 'lightyellow']
#  [''Vicon', 'ZED2mm', 'ZED4mm', 'MediaPipe', 'Nuitrack']
df = pd.read_excel('Min_dist.xlsx')
# df = df[df[0]<-500]
df_ZED2mm = df[df[1]!=0][[0,1]]
rms_ZED2mm = mean_squared_error(df_ZED2mm[0], df_ZED2mm[1], squared=False)
df_ZED4mm = df[df[2]!=0][[0,2]]
rms_ZED4mm = mean_squared_error(df_ZED4mm[0], df_ZED4mm[2], squared=False)
df_NUITRACK = df[df[3]!=0][[0,3]]
print(df_ZED4mm)
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