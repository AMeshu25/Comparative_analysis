import pandas as pd
import os
from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error

def Steps_Count(right_z, left_z,param):   #gets two lists of z coordinates of two joints
    count = 0
    plus_minus =[]
    plus_minus_counter =1
    steps_count=2
    max_len = max(len(right_z.values),len(left_z.values))
    for i in range(max_len):
    # for right,left in right_z.values,left_z.values:
        right = right_z.values[i]
        left = left_z.values[i]
        if right == None:   #if there is no value take the last one
            right = last_right
        if left == None:
            left = last_left
        if right < left:
            plus_minus.append('+')
        else:
            plus_minus.append('-')
        last_right = right          #save the last value for none cells
        last_left = left
    last_symbol = plus_minus[0]
    for v in plus_minus[1:]:
        if last_symbol==v:
            plus_minus_counter+=1
        else:
            last_symbol = v
            plus_minus_counter=1
        if plus_minus_counter==param:
            steps_count+=1
    return steps_count

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

#-------------------- Headers ---------
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

print(exp_by_s_dic)

#--------------------------- Steps count initialize param
# param =[]
# value =[]
# manual_count =[]
#--------param by one exp
#------------------ZED4mm param grid search
# exp_dir_lst = exp_by_s_dic['12_s2']     #manual steps count is around 55
# df = pd.read_excel('SHIFTED/'+exp_dir_lst[1])
# print('-----------ZED 4mm grid search for steps count param----------')
# for i in range(5,40): #the joints in ZED are 20 and 24
#     param.append(i)
#     count = Steps_Count(df['24z'],df['20z'],i)
#     value.append(count)
#     manual_count.append(55)
#     print('the parameter value=',i,' Steps count=',count)
# plt.plot(param, value)
# plt.plot(param, manual_count)
# plt.legend(['System', 'Manual'],loc='upper center',bbox_to_anchor=(1.2, 1),fontsize=12)
# plt.xlabel("Parameter - frames threshold")
# plt.ylabel("Steps count")
# plt.title('ZED 4mm param grid search')
# plt.savefig('ZED4mm_param_GridSearch.png',bbox_inches='tight')
# plt.show()
# #------------------VICON param grid search
# param =[]
# value =[]
# manual_count =[]
# df = pd.read_excel('SHIFTED/'+exp_dir_lst[0],names=VICON_headers)
# print('-----------VICON grid search for steps count param----------')

# for exp in exp_by_s_dic:

# for i in range(5,100,2):
#     param.append(i)
#     count = Steps_Count(df['RANKz'], df['LANKz'],i)
#     value.append(count)
#     manual_count.append(44)     #when 11 s1 is 55, to 12 s2 is 44
#     print('the parameter value=', i, ' Steps count=', count)
# plt.plot(param, value)
# plt.plot(param, manual_count)
# plt.legend(['System', 'Manual'],loc='upper center',bbox_to_anchor=(1.2, 1),fontsize=12)
# plt.xlabel("Parameter - frames threshold")
# plt.ylabel("Steps count")
# plt.title('VICON param grid search')
# plt.savefig('VICON_param_GridSearch.png',bbox_inches='tight')
# plt.show()
# #------------------ZED2mm param grid search
# param =[]
# value =[]
# manual_count =[]
# exp_dir_lst = exp_by_s_dic['11_s5']     #manual steps count is around 51
# df = pd.read_excel('SHIFTED/'+exp_dir_lst[1])
# print('-----------ZED 2mm grid search for steps count param----------')
# for i in range(5,40): #the joints in ZED are 20 and 24
#     param.append(i)
#     count = Steps_Count(df['24z'],df['20z'], i)
#     value.append(count)
#     manual_count.append(51)
#     print('the parameter value=',i,' Steps count=',count)
# plt.plot(param, value)
# plt.plot(param, manual_count)
# plt.legend(['System', 'Manual'],loc='upper center',bbox_to_anchor=(1.2, 1),fontsize=12)
# plt.xlabel("Parameter - frames threshold")
# plt.ylabel("Steps count")
# plt.title('ZED 2mm param grid search')
# plt.savefig('ZED2mm_param_GridSearch.png',bbox_inches='tight')
# plt.show()
# #------------------MEDIA param grid search
# param =[]
# value =[]
# manual_count =[]
# exp_dir_lst = exp_by_s_dic['11_s3']     #manual steps count is around 57
# df = pd.read_excel('SHIFTED/'+exp_dir_lst[1])
# print('-----------MEADIA grid search for steps count param----------')
# for i in range(5,40):
#     param.append(i)
#     count = Steps_Count(df['Right ankle_z'], df['Left ankle_z'], i)
#     value.append(count)
#     manual_count.append(57)
#     print('the parameter value=', i, ' Steps count=', count)
# plt.plot(param, value)
# plt.plot(param, manual_count)
# plt.legend(['System', 'Manual'],loc='upper center',bbox_to_anchor=(1.2, 1),fontsize=12)
# plt.xlabel("Parameter - frames threshold")
# plt.ylabel("Steps count")
# plt.title('MEDIA PIPE param grid search')
# plt.savefig('MEDIAPIPE_param_GridSearch.png',bbox_inches='tight')
# plt.show()
# #------------------Nuitrack param grid search
# param =[]
# value =[]
# manual_count =[]
# exp_dir_lst = exp_by_s_dic['11_s2']     #manual steps count is around 54
# df = pd.read_excel('SHIFTED/'+exp_dir_lst[2],names=NUITRACK_headers)
# print('-----------NUITRACK grid search for steps count param----------')
# for i in range(2,40):
#     param.append(i)
#     count = Steps_Count(df['23z'], df['19z'], i)
#     value.append(count)
#     manual_count.append(54)
#     print('the parameter value=', i, ' Steps count=', count)
# plt.plot(param, value, label="System")
# plt.plot(param, manual_count,label="Manual")
# plt.legend(['System', 'Manual'],loc='upper center',bbox_to_anchor=(1.2, 1),fontsize=12)
# plt.xlabel("Parameter - frames threshold")
# plt.ylabel("Steps count")
# plt.title('NUITRACK param grid search')
# plt.savefig('NUITRACK_param_GridSearch.png',bbox_inches='tight')
# plt.show()

#---------------After initialazing the threshold per each camera
#initioal param are:

#final opt param
# ZED4mm_param = 6
# ZED2mm_param = 11
# VICON_param = 66
# NUITRACK_param = 2  #not enough frames -> check it
# MEDIA_param = 7
#---------------------------------param by all exp

df_manual = pd.read_excel('manual_count_steps.xlsx')
manual_dic ={}
exps = df_manual['exp'].values
counts =df_manual['count'].values
for i in range(len(df_manual['count'].values)):
    manual_dic[exps[i]] = counts[i]
#----------VICON
# param = []
# error =[]
# mone =1
# zeros1 = []
# for key in exp_by_s_dic:
#     print(mone,'. Began with-> ',exp_by_s_dic[key][0])
#     df = pd.read_excel('SHIFTED/'+exp_by_s_dic[key][0], names=VICON_headers)
#     for i in range(20,80,5):
#         param.append(i)
#         count = Steps_Count(df['RANKx'], df['LANKx'],i)
#         error_exp = manual_dic[key] - count
#         error.append(error_exp)
#         zeros1.append(0)
#     mone+=1
#     # if mone == 4:
#     #     break
#
# mean_error_param = []
# zeros =[]
# for i in range(20,80,5):
#     mean_error_param.append(0)
#     zeros.append(0)
# mean_param = list(range(20,80,5))
# for i in range(len(error)):
#     mean_error_param[i%len(mean_error_param)]+=error[i]/80
# plt.scatter(param,error)
# plt.scatter(param,zeros1, c='m', marker='_')
# plt.xlabel("Parameter - frames threshold")
# plt.ylabel("Error (manual - vicon)")
# plt.title('VICON param grid search')
# plt.show()
# plt.scatter(mean_param,mean_error_param)
# plt.scatter(mean_param,zeros, c='m', marker='_')
# plt.xlabel("Parameter - frames threshold")
# plt.ylabel("Mean Error (manual - vicon)")
# plt.title('VICON param grid search')
# # plt.savefig('VICON_param_GridSearch.png',bbox_inches='tight')
# plt.show()


df_old_count = pd.read_excel('Total_steps.xlsx')    #save the exp by the camera

#----------ZED 4mm
def get_ZED4mm_dir(ls):
    for file in ls:
        if file[-14:-8] == 'ZED4mm':
            return file

# ZED4mm_exps_ls = df_old_count[df_old_count[2]>0]['exp'].values  #returns a list of all exp for specific camera
# param = []
# error =[]
# mone =1
zeros1 =[]
# for key in ZED4mm_exps_ls:
#     rev_file = get_ZED4mm_dir(exp_by_s_dic[key])
#     print(mone,'. Began with-> ',rev_file)
#     df = pd.read_excel('SHIFTED/'+rev_file)
#     for i in range(2,40):
#         param.append(i)
#         count = Steps_Count(df['24z'],df['20z'],i)
#         error_exp = manual_dic[key] - count
#         error.append(error_exp)
#         zeros1.append(0)
#     mone+=1
#     # if mone == 4:
#     #     break
# mean_error_param = []
# zeros = []
# for i in range(2,40):
#     mean_error_param.append(0)
#     zeros.append(0)
# mean_param = list(range(2,40))
# for i in range(len(error)):
#     mean_error_param[i%len(mean_error_param)]+=error[i]/24
# plt.scatter(param,error, c='red')
# plt.scatter(param,zeros1, c='m', marker='_')
# plt.xlabel("Parameter - frames threshold")
# plt.ylabel("Error (manual - ZED4mm)")
# plt.title('ZED4mm param grid search')
# plt.show()
# plt.scatter(mean_param,mean_error_param, c='red')
# plt.scatter(mean_param,zeros, c='m', marker='_')
# plt.xlabel("Parameter - frames threshold")
# plt.ylabel("Mean Error (manual - ZED4mm)")
# plt.title('ZED4mm param grid search')
# plt.savefig('ZED4mm_param_GridSearch.png',bbox_inches='tight')
# plt.show()



#----------ZED 2mm
# ZED4mm_exps_ls = df_old_count[df_old_count[2]>0]['exp'].values
def get_ZED2mm_dir(ls):
    for file in ls:
        if file[-14:-8] == 'ZED2mm':
            return file

# ZED2mm_exps_ls = df_old_count[df_old_count[1]>0]['exp'].values  #returns a list of all exp for specific camera
# param = []
# error =[]
# zeros =[]
# mone =1
# for key in ZED2mm_exps_ls:
#     rev_file = get_ZED2mm_dir(exp_by_s_dic[key])
#     print(mone,'. Began with-> ',rev_file)
#     df = pd.read_excel('SHIFTED/'+rev_file)
#     for i in range(2,40):
#         param.append(i)
#         count = Steps_Count(df['24z'],df['20z'],i)
#         error_exp = manual_dic[key] - count
#         error.append(error_exp)
#         zeros1.append(0)
#     zeros.append(0)
#     mone+=1
    # if mone == 4:
    #     break
# mean_error_param = []
# for i in range(2,40):
#     mean_error_param.append(0)
# mean_param = list(range(2,40))
# for i in range(len(error)):
#     mean_error_param[i%len(mean_error_param)]+=error[i]/24
# plt.scatter(param,error, c='red')
# plt.scatter(param,zeros1, c='m', marker='_')
# plt.xlabel("Parameter - frames threshold")
# plt.ylabel("Error (manual - ZED2mm)")
# plt.title('ZED2mm param grid search')
# plt.show()
# plt.scatter(mean_param,mean_error_param, c='red')
# plt.scatter(mean_param,zeros, c='m', marker='_')
# plt.xlabel("Parameter - frames threshold")
# plt.ylabel("Mean Error (manual - ZED2mm)")
# plt.title('ZED2mm param grid search')
# plt.savefig('VICON_param_GridSearch.png',bbox_inches='tight')
# plt.show()
#
# #----------NUITRACK
# NUITRACK_exps_ls = df_old_count[df_old_count[3]>0]['exp'].values
def get_NUITRACK_dir(ls):
    for file in ls:
        if file[-13:-8] == 'track':
            return file
# param = []
# error =[]
# zeros=[]
# mone =1
# for key in NUITRACK_exps_ls:
#     rev_file = get_NUITRACK_dir(exp_by_s_dic[key])
#     print(mone,'. Began with-> ',rev_file)
#     df = pd.read_excel('SHIFTED/'+rev_file)
#     for i in range(2,40):
#         param.append(i)
#         count = Steps_Count(df['23z'],df['19z'],i)+30  #'23z', '19z'
#         error_exp = manual_dic[key] - count
#         error.append(error_exp)
#         zeros1.append(0)
#     mone+=1
#     # if mone == 4:
#     #     break
# mean_error_param = []
# for i in range(2,40):
#     mean_error_param.append(0)
#     zeros.append(0)
# mean_param = list(range(2,40))
# for i in range(len(error)):
#     mean_error_param[i%len(mean_error_param)]+=error[i]/24
# plt.scatter(param,error, c='grey')
# plt.scatter(param,zeros1, c='m', marker='_')
# plt.xlabel("Parameter - frames threshold")
# plt.ylabel("Error (manual - NUITRACK)")
# plt.title('NUITRACK param grid search with factor of 30')
# plt.show()
# plt.scatter(mean_param,mean_error_param, c='grey')
# plt.scatter(mean_param,zeros, c='m', marker='_')
# plt.xlabel("Parameter - frames threshold")
# plt.ylabel("Mean Error (manual - NUITRACK)")
# plt.title('NUITRACK param grid search')
# plt.savefig('NUITRACK_param_GridSearch.png',bbox_inches='tight')
# plt.show()


#----------MEDIA PIPE
# zeros1 =[]
# MEDIA_exps_ls = df_old_count[df_old_count[4]>0]['exp'].values
# def get_MEDIA_dir(ls):
#     for file in ls:
#         if file[-12:-8] == 'Pipe':
#             return file
# param = []
# error =[]
# mone =1
# for key in MEDIA_exps_ls:
#     rev_file = get_MEDIA_dir(exp_by_s_dic[key])
#     print(mone,'. Began with-> ',rev_file)
#     df = pd.read_excel('SHIFTED/'+rev_file)
#     for i in range(2,40):
#         param.append(i)
#         count = Steps_Count(df['Right ankle_y'],df['Left ankle_y'],i)  #'Right ankle_z', 'Left ankle_z'
#         error_exp = manual_dic[key] - count
#         error.append(error_exp)
#         zeros1.append(0)
#     mone+=1
    # if mone == 4:
    #     break
# mean_error_param = []
# zeros =[]
# for i in range(2,40):
#     mean_error_param.append(0)
#     zeros.append(0)
# mean_param = list(range(2,40))
# for i in range(len(error)):
#     mean_error_param[i%len(mean_error_param)]+=error[i]/24
# plt.scatter(param,error, c='green')
# plt.scatter(param,zeros1, c='m', marker='_')
# plt.xlabel("Parameter - frames threshold")
# plt.ylabel("Error (manual - MEDIA)")
# plt.title('MEDIA param grid search')
# plt.show()
# plt.scatter(mean_param,mean_error_param, c='green')
# plt.scatter(mean_param,zeros, c='m', marker='_')
# plt.xlabel("Parameter - frames threshold")
# plt.ylabel("Mean Error (manual - MEDIA)")
# plt.title('MEDIA param grid search')
# plt.savefig('MEDIA_param_GridSearch.png',bbox_inches='tight')
# plt.show()

def get_df_camera(file):    #gets directory and return df and param
    ZED4mm_param = 8       #was 9
    ZED2mm_param = 9
    VICON_param = 35
    NUITRACK_param = 2  # not enough frames -> check it
    MEDIA_param = 7
    if file[-13:-8] == 'VICON':
        df = pd.read_excel('SHIFTED/'+file,names=VICON_headers)
        return df,VICON_param,'RANKx','LANKx',0
    if file[-13:-8] == 'track':
        df = pd.read_excel('SHIFTED/' + file, names=NUITRACK_headers)
        return df, NUITRACK_param,'23z', '19z',3
    if file[-14:-8] == 'ZED4mm':
        df = pd.read_excel('SHIFTED/' + file)
        return df, ZED4mm_param,'24z','20z',2
    if file[-14:-8] == 'ZED2mm':
        df = pd.read_excel('SHIFTED/' + file)
        return df, ZED2mm_param,'24z','20z',1
    if file[-12:-8] == 'Pipe':
        df = pd.read_excel('SHIFTED/' + file)
        return df,MEDIA_param,'Right ankle_z', 'Left ankle_z',4
    print('!@!@!@!!@!@!@!@!@!PROBLEM IN ',file)
    return [],0,'',''
# --------------------graphs ---------
# ls_files = exp_by_s_dic['11_s3']
# Vicon_df = pd.read_excel('SHIFTED/'+ls_files[0],names=VICON_headers,skiprows=2)
# ZED2mm_df = pd.read_excel('SHIFTED/'+ls_files[1])
# MEDIA_df = pd.read_excel('SHIFTED/'+ls_files[1])
# ZED2mm_df['Frame'] = ZED2mm_df.iloc[0]
# Vicon_df.plot(x='Frame', y ='LSHOy',title='VICON X',color='orchid')
# plt.show()
# ZED2mm_df.plot(x='Frame', y ='5x',title='ZED X',color='silver')
# plt.show()
# MEDIA_df.plot(x='Key Point Number->', y ='Left shoulder_x',title='MEDIA PIPE X',color='lightpink')
# plt.xlabel('Frame')
# plt.show()
#
# Vicon_df.plot(x='Frame', y ='LSHOx',title='VICON Z',color='orchid')
# plt.show()
# ZED2mm_df = ZED2mm_df['19z']*-1
# ZED2mm_df.plot(x='Frame', y ='5z',title='ZED Z',color='silver')
# plt.show()
# MEDIA_df.plot(x='Key Point Number->', y ='Left shoulder_z',title='MEDIA PIPE Z ',color='lightpink')
# plt.xlabel('Frame')
# plt.show()
#
# Vicon_df.plot(x='Frame', y ='LSHOz',title='VICON Y',color='orchid')
# plt.show()
# ZED2mm_df.plot(x='Frame', y ='5y',title='ZED Y',color='silver')
# plt.show()
# MEDIA_df.plot(x='Key Point Number->', y ='Left shoulder_y',title='MEDIA PIPE Y ',color='lightpink')
# plt.xlabel('Frame')
# plt.show()

# ls_files = exp_by_s_dic['9__s2']
# NUITRACK_df = pd.read_excel('SHIFTED/'+ls_files[2])
# NUITRACK_df.plot(x='Frame', y ='18x',title='9 NUITRACK s2 left ankle X - Shifted',color='grey')
# plt.show()
# NUITRACK_df.plot(x='Frame', y ='18y',title='9 NUITRACK s2 left ankle Y - Shifted',color='grey')
# plt.show()
# NUITRACK_df.plot(x='Frame', y ='18z',title='9 NUITRACK s2 left ankle Z - Shifted',color='grey')
# plt.show()


#Run the steps counter function over all the data and then save first to dictionary then to xlsx file
# steps_count_dic ={}
# mone =1
# for exp in exp_by_s_dic:
#     temp_lst_count=[0,0,0,0,0]
#     for file in exp_by_s_dic[exp]:
#         print(mone,'. started with->',file)
#         df,param,right,left,i = get_df_camera(file)
#         steps_count = Steps_Count(df[right],df[left],param)
#         temp_lst_count[i]=steps_count
#     steps_count_dic[exp] = temp_lst_count
#     mone+=1
# df = pd.DataFrame(data=steps_count_dic)
# print(df.T)
# df.T.to_excel('Total_steps.xlsx')
#--------RMSE vs VICON
# df = pd.read_excel('Total_steps.xlsx')
# df_ZED2mm = df[df[1]!=0][[0,1]]
# rms_ZED2mm = mean_squared_error(df_ZED2mm[0], df_ZED2mm[1], squared=False)
# df_ZED4mm = df[df[2]!=0][[0,2]]
# rms_ZED4mm = mean_squared_error(df_ZED4mm[0], df_ZED4mm[2], squared=False)
# df_NUITRACK = df[df[3]!=0][[0,3]]
# rms_NUITRACK = mean_squared_error(df_NUITRACK[0], df_NUITRACK[3], squared=False)
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

# ['orchid','lightskyblue', 'lightgreen', 'lightpink', 'lightyellow']
#  [''Vicon', 'ZED2mm', 'ZED4mm', 'MediaPipe', 'Nuitrack']
# --------RMSE vs manual
df_res = pd.read_excel('manual_count_steps.xlsx')
df = pd.read_excel('Total_steps.xlsx')
df['manual'] = df_res['count']
rms_VICON = mean_squared_error(df['manual'], df[0], squared=False)
df_ZED2mm = df[df[1]!=0]
rms_ZED2mm = mean_squared_error(df_ZED2mm['manual'], df_ZED2mm[1], squared=False)
df_ZED4mm = df[df[2]!=0]
rms_ZED4mm = mean_squared_error(df_ZED4mm['manual'], df_ZED4mm[2], squared=False)
df_NUITRACK = df[df[3]!=0]
rms_NUITRACK = mean_squared_error(df_NUITRACK['manual'], df_NUITRACK[3], squared=False)
df_MEDIA = df[df[4]!=0]
rms_MEDIA = mean_squared_error(df_MEDIA['manual'], df_MEDIA[4], squared=False)
RMSE = [rms_VICON,rms_ZED2mm,rms_ZED4mm,rms_MEDIA,rms_NUITRACK]
cameras =['Vicon', 'ZED2mm', 'ZED4mm', 'MediaPipe', 'Nuitrack']
col =['orchid','lightskyblue', 'lightgreen', 'lightpink', 'lightyellow']
bars = plt.bar(cameras,RMSE,color = col)
plt.title('RMSE of each camera vs the MANUAL')
plt.ylabel('RMSE')
for bar in bars:
    yval=round(bar.get_height(),3)
    plt.text(bar.get_x(),yval,yval)

plt.show()


def get_X_Y_coor(coor,is_VICON):
    X =[]
    Y=[]
    y_start=1
    x_start=0
    factor = 1
    if is_VICON:
        y_start =2      #OMGGG y its workingggg????
        x_start =1  #its should be x=0,y=1,z=2 but it is x=1,y=2,z=0
        factor =1
    for i in range(x_start,len(coor),3):
        X.append(coor[i])
    for i in range(y_start,len(coor),3):
        Y.append(factor*coor[i])
    return X,Y
#--------------------- shifting graphs----------
    #Vicon=0 | ZED2mm=1 | ZED4mm=2 | Nuitrack=3 | MeadiPipe=4
# ls_files = exp_by_s_dic['11_s5']
# df = pd.read_excel('SHIFTED/'+ls_files[0],names=VICON_headers,skiprows=2)
# coor = df.iloc[370].values
# #first two cells are irelevant
# X_VICON, Y_VICON = get_X_Y_coor(coor[2:],True)
# df = pd.read_excel('ZED/'+ls_files[1])
# coor = df.iloc[76].values
# X_ZED4mm, Y_ZED4mm = get_X_Y_coor(coor[1:],False)
# df = pd.read_excel('SHIFTED/'+ls_files[1])
# coor = df.iloc[76].values
# X_ZED4mm_SHIFTED, Y_ZED4mm_SHIFTED = get_X_Y_coor(coor[1:],False)
# plt.scatter(X_VICON,Y_VICON)
# plt.scatter(X_ZED4mm,Y_ZED4mm,c='red')
# plt.xlabel("X coordinate")
# plt.ylabel("Y coordinate")
# # plt.xlim([-400,800])
# # plt.ylim(-1200,2000)
# plt.title('VICON vs ZED2mm')
# plt.scatter(X_ZED4mm_SHIFTED,Y_ZED4mm_SHIFTED,c='lightpink')
# plt.show()


