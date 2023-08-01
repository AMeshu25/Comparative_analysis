import pandas as pd
from sklearn.metrics import mean_squared_error
from matplotlib import pyplot as plt
import os

def get_Score(rmse):    #Simple grading
    sort_ls = list(rmse)
    sort_ls.sort()
    res = [0,0,0,0]
    for i in range(len(sort_ls)):
        for j in range(len(sort_ls)):
            if sort_ls[i]==rmse[j]:
                res[j]=i
                break
    return res

def get_K_last_Score(rmse,k):   #last k in simple grading NOT USED
    sort_ls = list(rmse)
    sort_ls.sort()
    res = [0,0,0,0]
    k = len(rmse)-k
    for i in range(k,len(sort_ls)):
        for j in range(len(sort_ls)):
            if sort_ls[i]==rmse[j]:
                res[j]+=i-k
                break
    return res

def get_weighted_Score(rmse):       #Normalized grading.
    maxi = max(rmse)
    mini = min(rmse)
    delta = maxi-mini
    res = [0,0,0,0]
    for i in range(len(rmse)):
       if rmse[i] == maxi:
           res[i] = 1
       elif rmse[i]== mini:
           res[i]=0
       else:
           res[i] = round((rmse[i]-mini)/delta,3)
    return res

dir_files = os.listdir()        #get relevent files to compute RMSE
ls_res = []
for file in dir_files:
    if len(file)>4and file[-4:]=='xlsx':
        ls_res.append(file)
        # print(file[-4:])
ls_res = ls_res[:-2]
# ls_res.pop(1)
ls_res.remove('Turning_Count.xlsx')
ls_res.remove('first90subject11.xlsx')
ls_res.remove('RMSEFeatures_amir.xlsx')
ls_res.remove('allFeatures.xlsx')
ls_res.remove('manual_count_steps.xlsx')
print(ls_res)
print(len(ls_res))


#--------------standard deviation bar plots----------------
# for file in ['Turning_Count.xlsx']:#ls_res:
#     df = pd.read_excel(file)
#     stdev_ZED2mm = df[df[1]!=0][1].std()
#     stdev_ZED4mm = df[df[2]!=0][2].std()
#     stdev_NUITRACK = df[df[3]!=0][3].std()
#     stdev_MEDIA = df[df[4]!=0][4].std()
#     score =[stdev_ZED2mm,stdev_ZED4mm,stdev_MEDIA,stdev_NUITRACK]
#     cameras = ['ZED2mm', 'ZED4mm', 'MediaPipe', 'Nuitrack']
#     col = ['lightskyblue', 'lightgreen', 'lightpink', 'lightyellow']
#     bars = plt.bar(cameras, score, color=col)
#     plt.title(file[:-5]+' feature - Standard Deviation')
#     plt.ylabel('grade')
#     for bar in bars:
#         yval = round(bar.get_height(), 3)
#         plt.text(bar.get_x(), yval, yval)
#     plt.show()


#---------Calculating the RMSE
weights = [0.019,0.0754,0.0377,0.1132,0.0377,0.0754,0.0754,0.0754,0.0755,0.1132,0.0377,0.1132,0.1132,0.019,0.019]
score = [0,0,0,0]       #score 0-ZED2mm, 1-ZED4mm, 2-Nuitrack, 3-MEDIA
mone =0
# print(ls_res)
dic = {}
dic['Feature'] = ['ZED2mm', 'ZED4mm', 'MediaPipe', 'Nuitrack']
for file in ls_res:
    df = pd.read_excel(file)
    df_ZED2mm = df[df[1]!=0][[0,1]]
    rms_ZED2mm = mean_squared_error(df_ZED2mm[0], df_ZED2mm[1], squared=False)
    df_ZED4mm = df[df[2]!=0][[0,2]]
    rms_ZED4mm = mean_squared_error(df_ZED4mm[0], df_ZED4mm[2], squared=False)
    df_NUITRACK = df[df[3]!=0][[0,3]]
    rms_NUITRACK = mean_squared_error(df_NUITRACK[0], df_NUITRACK[3], squared=False)
    df_MEDIA = df[df[4]!=0][[0,4]]
    rms_MEDIA = mean_squared_error(df_MEDIA[0], df_MEDIA[4], squared=False)
    RMSE = [rms_ZED2mm,rms_ZED4mm,rms_MEDIA,rms_NUITRACK]
    dic[file] = RMSE
    temp = get_weighted_Score(RMSE)
    # temp = get_Score(RMSE)
    for i in range(len(score)):
        score[i]+=temp[i]*weights[mone]
    mone+=1
cameras =['ZED2mm', 'ZED4mm', 'MediaPipe', 'Nuitrack']
col =['lightskyblue', 'lightgreen', 'lightpink', 'lightyellow']
bars = plt.bar(cameras,score,color = col)
plt.title('RMSE Score Results - Relative normalization with weights')
plt.ylabel('RMSE')
for bar in bars:
    yval=round(bar.get_height(),3)
    plt.text(bar.get_x(),yval,yval)

plt.show()
# df_all = pd.DataFrame(data=dic)
# df_all.T.to_excel('RMSEFeatures_amir.xlsx')
