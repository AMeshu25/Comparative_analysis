import pandas as pd
import os
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np

#----------------------------all ZED files null values
# path = 'ZED/'
# filesnames = os.listdir(path)
# ZED_2mm_files =[]
# ZED_4mm_files =[]
# temp4 =[]
# temp2 =[]
# # devide the files to 2mm and 4mm
# for file in filesnames:
#     if file[-11] == '2':
#         ZED_2mm_files.append(file)
#     if file[-11]=='4':
#         ZED_4mm_files.append(file)
# None_count = 0
# mone =0         #just for me to know when finished
# for file in ZED_2mm_files:
#     print(mone)
#     df = pd.read_excel(path+file)
#     None_count+=df.isna().sum().sum()
#     mone+=1
# print('Total amount of nulls in 2mm is = ', None_count)
# mone =0
# for file in ZED_4mm_files:
#     # print(mone)
#     df = pd.read_excel('ZED/'+file)
#     None_count+=df.isna().sum().sum()
#     mone+=1
# print('Total amount of nulls in 4mm is = ', None_count)
#there is no null values at the ZED camera at all

#-----------------------------------VICON null values---------------------------
joints = ['LFHD','RFHD','LBHD','RBHD','C7','T10','CLAV','STRN','RBAK','LSHO','LUPA','LELB','LFRM','LWRA','LWRB','LFIN',
           'RSHO','RUPA','RELB','RFRM','RWRA','RWRB','RFIN','LASI','RASI','LPSI','RPSI','LTHI','LKNE','LTIB','LANK','LHEE','LTOE','RTHI','RKNE','RTIB','RANK','RHEE','RTOE']
coordinates =['x','y','z']
VICON_headers =[]
VICON_headers.append('Frame')
VICON_headers.append('Sub_Frame')
for joint in joints:
    for cor in coordinates:
        VICON_headers.append(joint+cor)
path = 'SHIFTED/'
# filesnames = os.listdir(path)
# None_count =0
# mone =0
# for file in ['3_VICON_s2.xlsx']: #filesnames:
#     if file =='16_VICON_s5.xlsx':   #there mising columns?!
#         df = pd.read_excel(path+file)
#     else:
#         df = pd.read_excel(path+file, names = headers)
#     temp_count = df.isna().sum().sum() -2
#     None_count+=temp_count
#     mone+=1
#     col_null =df.columns[df.isna().any()].tolist()
#     # print(mone,'/',len(filesnames))
#     print(mone,'. '+file[0:-5] + ' Number of frames with None =',temp_count/3, ' | null values are at =', col_null[2:])   #the first 2 columns has null and its not relevant
# print('Total amount of frames with nulls values in VICON is = ', None_count/3)

#--------------deleting NONE values from 15_s1 and 2_s1 ------------------------

# df_drop_none = pd.read_excel(path+'15_VICON _s1.xlsx')
# df_drop_none=df_drop_none.dropna()
# df_drop_none.to_excel(path+'15_VICON _s1.xlsx')
# print(df_drop_none.isna().sum().sum())
# df_drop_none = pd.read_excel(path+'2_VICON_s1.xlsx')
# df_drop_none=df_drop_none.dropna()
# df_drop_none.to_excel(path+'2_VICON_s1.xlsx')
# print(df_drop_none.isna().sum().sum())

joints = list(range(1,24))        #18 is left ankle
joints.remove(10)   #those joints are not in the file
joints.remove(16)
joints.remove(20)
NUITRACK_headers =['Frame']
for joint in joints:
    for cor in coordinates:
        NUITRACK_headers.append(str(joint)+cor)

joints = list(range(34))
ZED_headers =['Frame']
ZED_Y_coor =[]
for joint in joints:
    for cor in coordinates:
        if cor =='y':
            ZED_Y_coor.append(str(joint)+cor)
        ZED_headers.append(str(joint)+cor)
# df_ZED = pd.read_excel('SHIFTED/11_ZED4mm_s1.xlsx')

# df_VICON = pd.read_excel('VICON/11_VICON_s2.xlsx',names=VICON_headers,skiprows=2)
# df_MEDIA = pd.read_excel('SHIFTED/11_MediaPipe_S3.xlsx')
# df1 = df.loc[:, df.columns != col]
# df_frame = df_MEDIA['Key Point Number->']
# df_MEDIA = df_MEDIA.loc[:,df_MEDIA.columns!='Key Point Number->']
# df_MEDIA['Key Point Number->']=df_frame
# df_NUITRACK = pd.read_excel('SHIFTED/11_Nuitrack_S2.xlsx')
# print(df_NUITRACK)
# df_VICON['RSHOx'].plot(c='g')
# plt.title('VICON right shoulder Z 11 s1')
# plt.show()
# df_MEDIA['Left ankle_x'].plot(c='r')
# plt.title('MEDIA left ankle X')
# plt.show()
# df_NUITRACK['12z'].plot(c='lightpink')
# df_ZED['11z'].plot(c='r')
# df_VICON['RSHOx'].plot(c='g')
# plt.ylim([0,500])
# df_MEDIA['Left shoulder_z'].plot(c='orange')
# plt.title('MEDIA Left shoulder Z 11 s3')
# plt.xlabel('Frame')
# plt.ylabel('Z')
# plt.show()
# df_ZED['11x'].plot(c='r')
# df_VICON['RSHOy'].plot(c='g')
# df_NUITRACK['12x'].plot(c='lightpink')
# df_MEDIA['Left shoulder_x'].plot(c='orange')
# plt.title('MEDIA Left shoulder X 11 s3')
# plt.xlabel('Frame')
# plt.ylabel('X')
# plt.show()
# df_ZED['11y'].plot(c='r')
# df_VICON['RSHOz'].plot(c='g')
# df_NUITRACK['12y'].plot(c='lightpink')
# df_MEDIA['Left shoulder_y'].plot(c='orange')
# plt.title('MEDIA Left shoulder Y 11 s3')
# plt.xlabel('Frame')
# plt.ylabel('Y')
# plt.show()

#
# y_coor = df_VICON.filter(regex='y').iloc[0].T
# x_coor = df_VICON.filter(regex='x').iloc[0].T
# z_coor = df_VICON.filter(regex='z').iloc[0].T

# y_coor = df_VICON.loc[0,['y' in i[-1:] for i in df_VICON.columns]].T
# x_coor = df_VICON.loc[0,['x' in i[-1:] for i in df_VICON.columns]].T
# z_coor = df_VICON.loc[0,['z' in i[-1:] for i in df_VICON.columns]].T
# plt.scatter(y_coor,z_coor)      #VICON
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.xlim([0,700])
# plt.ylim([-200,800])
# plt.show()

# y_coor = df_MEDIA.loc[81,['y' in i[-1:] for i in df_MEDIA.columns]].T
# x_coor = df_MEDIA.loc[81,['x' in i[-1:] for i in df_MEDIA.columns]].T
# z_coor = df_MEDIA.loc[81,['z' in i[-1:] for i in df_MEDIA.columns]].T
# plt.scatter(x_coor,y_coor)
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.title('MEDIA NEW scale (mul by 5) vs VICON')
# df_MEDIA = pd.read_excel('SHIFTED/11_MediaPipe_S3.xlsx')
# y_coor = df_MEDIA.loc[81,['y' in i[-1:] for i in df_MEDIA.columns]].T
# x_coor = df_MEDIA.loc[81,['x' in i[-1:] for i in df_MEDIA.columns]].T
# z_coor = df_MEDIA.loc[81,['z' in i[-1:] for i in df_MEDIA.columns]].T
# plt.scatter(x_coor,y_coor,color='lightpink')
# plt.show()

# df_VICON.plot(kind='line',x='Frame', y ='LANKz',title='VICON left ankle - Y',)
# plt.xlabel('Frame')
# plt.ylabel('Y')
# plt.show()
# df_VICON.plot(kind='line',x='Frame', y ='LANKx',title='VICON left ankle - Z',)
# plt.xlabel('Frame')
# plt.ylabel('Z')
# plt.show()
# df_VICON.plot(kind='line',x='Frame', y ='LANKy',title='VICON left ankle - X',)
# plt.xlabel('Frame')
# plt.ylabel('X')
# plt.show()

#---------------------ZED plots ----------------
joints = list(range(34))
ZED_headers =['Frame']
ZED_Y_coor =[]
for joint in joints:
    for cor in coordinates:
        if cor =='y':
            ZED_Y_coor.append(str(joint)+cor)
        ZED_headers.append(str(joint)+cor)
# df_ZED = pd.read_excel('ZED/9_ZED4mm_s2.xlsx',names=ZED_headers)
# y_coor = df_NUITRACK.filter(regex='y').iloc[0].T
# x_coor = df_NUITRACK.filter(regex='x').iloc[0].T
# z_coor = df_NUITRACK.filter(regex='z').iloc[0].T
# plt.scatter(x_coor,y_coor)
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.show()
# df_ZED.plot(kind='line',x='Frame', y ='20z',title='ZED4mm left ankle - Z',color='red')
# plt.xlabel('Frame')
# plt.ylabel('Z')
# plt.show()
# df_ZED.plot(kind='line',x='Frame', y ='20x',title='ZED4mm left ankle - X',color='red')
# plt.xlabel('Frame')
# plt.ylabel('X')
# plt.show()
# df_ZED.plot(kind='line',x='Frame', y ='20y',title='ZED4mm  left ankle - Y',color='red')
# plt.xlabel('Frame')
# plt.ylabel('Y')
# plt.show()

#-----------------NUITRACK plots----------------
joints = list(range(1,24))        #18 is left ankle
joints.remove(10)   #those joints are not in the file
joints.remove(16)
joints.remove(20)
NUITRACK_headers =['Frame']
for joint in joints:
    for cor in coordinates:
        NUITRACK_headers.append(str(joint)+cor)
# df = pd.read_excel(path+'9_nuitrack_S2.xlsx')
# df_NUITRACK.plot(kind='scatter',x='Frame', y ='18z',title='NUITRACK left ankle - Z',color='grey')
# plt.xlabel('Frame')
# plt.ylabel('Z')
# plt.show()
# df.plot(kind='scatter',x='Frame', y ='18x',title='NUITRACK left ankle - X',color='grey')
# plt.xlabel('Frame')
# plt.ylabel('X')
# plt.show()
# df.plot(kind='scatter',x='Frame', y ='18y',title='NUITRACK left ankle - Y',color='grey')
# plt.xlabel('Frame')
# plt.ylabel('Y')
# plt.show()

#-----------------NUITRACK plots----------------

# df.plot(x='Frame', y ='18z',title='9 NUITRACK s2 Ankle Z',color='grey')
# plt.show()
# df.plot(x='Frame', y ='18x',title='9 NUITRACK s2 Ankle X',color='grey')
# plt.show()
# df.plot(x='Frame', y ='18y',title='9 NUITRACK s2 Ankle Y',color='grey')
# plt.show()

#----------------- Orginaze by each experiment ---------
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

def change_coordinates(listdir,is_zed): #gets list of files name and boolean variable, True = ZED camera, False = MEDIA PIPE
    factor = -1       #10
    path ='MEDIA/'
    mone =1
    if is_zed:
        # factor=1000
        path='ZED/'
    for file in listdir:
        df = pd.read_excel(path+file)
        df_new = df.loc[:, df.columns != 'Key Point Number->']
        df_new=df_new[ZED_Y_coor]*-1
        # df_new.insert(0,'Key Point Number->',df['Frame'])
        print(df)
        # df_new.to_excel(path+file,index=False)
        print(mone,'finished with ', file)
        mone+=1
        break


ZED_path = 'ZED/'
ZED_filesnames = os.listdir(ZED_path)
VICON_path = 'VICON/'
VICON_filesnames = os.listdir(VICON_path)
NUITRACK_path = 'NUITRACK/'
NUITRACK_filesnames = os.listdir(NUITRACK_path)
MEDIA_path = 'MEDIA/'
MEDIA_filesnames = os.listdir(MEDIA_path)
exp_by_s_dic = merge_by_exp(ZED_filesnames,VICON_filesnames,NUITRACK_filesnames,MEDIA_filesnames)
#exp_by_s_dic is a dictionary where key=paticipant+experiment number, value=list of files name
print(exp_by_s_dic)

#since zed is in meters and MEDIA PIPE is in Cmeters we change them to mm by the function
#runs only once!!!!
# change_coordinates(ZED_filesnames, True)
# change_coordinates(MEDIA_filesnames, False)
MEDIA_Y_coor = ['Nose_y','Right eye inner_y','Right eye_y','Right eye outer_y','Left eye inner_y','Left eye_y','Left eye outer_y','Right ear_y'
    ,'Left ear_y','mouth right_y','mouth left_y','Right shoulder_y','Left shoulder_y','Right elbow_y','Left elbow_y','Right wrist_y'
    ,'Left wrist_y','Right pinkey knuckle #1_y','Left pinkey knuckle #1_y','Right index knuckle #1_y','Left index knuckle #1_y'
    ,'Right thumb knuckle #2_y','Left thumb knuckle #2_y','Right hip_y','Left hip_y','Right knee_y','Left knee_y','Right ankle_y'
    ,'Left ankle_y','Right heel_y','Left heel_y','Right foot index_y','Left foot index_y']

def swap_ZED_MEDIA(listdir, is_zed):
    path = 'NUITRACK/'
    mone = 1
    coor = NUITRACK_headers
    if is_zed:
        # factor=1000
        path = 'ZED/'
        coor=ZED_Y_coor
    for file in listdir:
        # if file not in ['10_ZED2mm_s1.xlsx','10_ZED2mm_s4.xlsx','10_ZED4mm_s5.xlsx']:
        df = pd.read_excel(path + file)
        # print(df)
        ls_coor = df[coor].values
        df[coor] = df[coor].apply(lambda z: z * -1)
        # df_frame = df['Key Point Number->']
        # df.loc[:,df.columns!='Key Point Number->'] = df.loc[:,df.columns!='Key Point Number->']*5
        # df['Key Point Number->']=df_frame
        df.to_excel(path+file,index=False)
        print(mone, 'finished with ', file)
        mone += 1

# swap_ZED_MEDIA(ZED_filesnames,True)
# swap_ZED_MEDIA(NUITRACK_filesnames,False)
#----------shifting------

def get_df_by_Camera(path,camera):  #get path and camera type -> create dataframe with the headers
    if camera=='ZED4mm' or camera=='ZED2mm':
        df = pd.read_excel('ZED/'+path)
    if camera=='Nuitrack':
        df = pd.read_excel('NUITRACK/'+path)
    if camera=='MediaPipe':
        df = pd.read_excel('MEDIA/'+path)
    return df

def Shift_Data(df, vector):
    col_number = len(df.columns)
    x_coor_4_all = list(range(1, col_number,3))
    y_coor_4_all = list(range(2, col_number,3))
    z_coor_4_all = list(range(3, col_number,3))
    df.iloc[:, x_coor_4_all]= df.iloc[:, x_coor_4_all] +vector[0]
    df.iloc[:, y_coor_4_all]= df.iloc[:, y_coor_4_all] +vector[1]
    df.iloc[:, z_coor_4_all]= df.iloc[:, z_coor_4_all] +vector[2]
    return df

def get_df_MEDIA(path,camera):  #get path and camera type -> create dataframe with the headers
    df =[]
    if camera=='MediaPipe':
        df = pd.read_excel('MEDIA/'+path)
    return df

def Shift_MEDIA_Data(df, vector):       #Ours mistake -> the media coordinates are the same as ZED&Nuitrack
    col_number = len(df.columns)
    x_coor_4_all = list(range(1, col_number,3))
    y_coor_4_all = list(range(2, col_number,3))
    z_coor_4_all = list(range(3, col_number,3))
    df.iloc[:, x_coor_4_all]= df.iloc[:, x_coor_4_all] +vector[0]
    df.iloc[:, y_coor_4_all]= df.iloc[:, y_coor_4_all] +vector[2]
    df.iloc[:, z_coor_4_all]= df.iloc[:, z_coor_4_all] +vector[1]
    return df

def shifting_media(exp_by_s_dic):
    mone =1
    for key in exp_by_s_dic: #runs over each experiment
        participant_num = key[0:-3]
        vicon_path = exp_by_s_dic[key][0]
        for file in exp_by_s_dic[key][1:]:  #runs over each file
            if participant_num[1]=='_': #technical issue to get the camera type (wont work with participant num > 99
                camera_type= file[2:-8]
            else:
                camera_type = file[3:-8]
            df_camera = get_df_MEDIA(file,camera_type)
            if len(df_camera)==0:
                continue
            df_vicon = pd.read_excel('VICON/' + vicon_path, names=VICON_headers, skiprows=2)
            shift_Vector = get_shifting_Vector(df_vicon,df_camera,camera_type)  #return a vector as list [x,y,z] to shift
            df_shifted = Shift_Data(df_camera,shift_Vector)
            df_shifted.to_excel('SHIFTED/'+file,index=False)
            print(mone,'. ',file)
            mone+=1

def shifting(exp_by_s_dic):
    mone =1
    for key in exp_by_s_dic: #runs over each experiment
        participant_num = key[0:-3]
        vicon_path = exp_by_s_dic[key][0]
        df_vicon = pd.read_excel('VICON/'+vicon_path,names=VICON_headers, skiprows=2)
        for file in exp_by_s_dic[key][1:]:  #runs over each file
            if participant_num[1]=='_': #technical issue to get the camera type (wont work with participant num > 99
                camera_type= file[2:-8]
            else:
                camera_type = file[3:-8]
            df_camera = get_df_by_Camera(file,camera_type)
            shift_Vector = get_shifting_Vector(df_vicon,df_camera,camera_type)  #return a vector as list [x,y,z] to shift
            df_shifted = Shift_Data(df_camera,shift_Vector)
            df_shifted.to_excel('SHIFTED/'+file,index=False)
            print(mone,'. ',file)
        mone+=1
        # if mone ==4:
        #     break

#return the shifted vector
def get_shifting_Vector(df_vicon,df_camera,camera_type):
    flag = False
    if camera_type == 'ZED4mm' or camera_type == 'ZED2mm':
        VICON_joint = 'CLAV'
        other_joint = '3'
    if camera_type == 'Nuitrack':
        # isVICON=True
        VICON_joint = 'CLAV'
        other_joint = '2'
    if camera_type == 'MediaPipe':
        flag = True
        VICON_joint = 'CLAV'
        other_joint = 'Right shoulder_'
        second_joint = 'Left shoulder_'
    # print(VICON_joint,' ',other_joint)
    #using the ZED and REALSENSE coordinates: x<->z, y<->x, z<->y (VICON<->other)
    if not flag:
        delta_x = float(df_vicon.iloc[0][VICON_joint+'y']) - float(df_camera.iloc[0][other_joint+'x'])        #shifted the coordinates to z->x->y
        delta_y = float(df_vicon.iloc[0][VICON_joint + 'z']) - float(df_camera.iloc[0][other_joint + 'y'])
        delta_z = float(df_vicon.iloc[0][VICON_joint+'x']) - float(df_camera.iloc[0][other_joint+'z'])
    else:
        delta_x = float(df_vicon.iloc[0][VICON_joint + 'y']) - float(df_camera.iloc[0][other_joint + 'x']+df_camera.iloc[0][second_joint+'x'])/2
        delta_y = float(df_vicon.iloc[0][VICON_joint + 'z']) - float(df_camera.iloc[0][other_joint + 'y']+df_camera.iloc[0][second_joint+'y'])/2
        delta_z = float(df_vicon.iloc[0][VICON_joint + 'x']) - float(df_camera.iloc[0][other_joint + 'z']+df_camera.iloc[0][second_joint+'z'])/2

    # print(delta_x,', ',delta_y,', ',delta_z)
    return [delta_x,delta_y,delta_z]




#--------------because i'm a fool and had to fix the data, do not run those fun again
def correct_data_ZED(): #need to change frame scala and delete one col
    ZED_path = 'ZED/'
    ZED_filesnames = os.listdir(ZED_path)
    for file in ZED_filesnames:
        df = pd.read_excel(ZED_path+file)
        df = df.iloc[:,1:]
        df.set_axis(ZED_headers, axis=1, inplace=True)
        df.Frame = df.Frame/1000
        df.to_excel(ZED_path+file, index=False)
        print(file)

def correct_data_MEDIA(): #need to change frame scala and delete one col
    MEDIA_path = 'MEDIA/'
    MEDIA_filesnames = os.listdir(MEDIA_path)
    for file in MEDIA_filesnames:
        df = pd.read_excel(MEDIA_path+file)
        df = df.iloc[:,1:]
        df['Key Point Number->'] = df['Key Point Number->']/10
        df.to_excel(MEDIA_path+file, index=False)
        print(file)

# correct_data_MEDIA()
# correct_data_ZED()


# dic ={'2__s2':['2_VICON_s2.xlsx', '2_Nuitrack_S2.xlsx']}
# shifting(dic)
shifting(exp_by_s_dic)      #does the magic of shifting
# shifting_media(exp_by_s_dic)



#----------------- KS test ---------------
#test for participant 9 session 2 ZED 4mm vs VICON

# print('begin test')
# print('Left ankle z coordinate test =',stats.ks_2samp(df_ZED['20z'],df_VICON['LANKz']))
# print('Left ankle x coordinate test =',stats.ks_2samp(df_ZED['20x'],df_VICON['LANKx']))
# print('Left ankle y coordinate test =',stats.ks_2samp(df_ZED['20y'],df_VICON['LANKy']))

def KS_2_sampled(data1,joint1, data2, joint2):
    return stats.ks_2samp(data1[joint1],data2[joint2])


