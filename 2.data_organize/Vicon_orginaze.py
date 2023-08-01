import pandas as pd
from matplotlib import pyplot as plt
import os

joints = ['LFHD','RFHD','LBHD','RBHD','C7','T10','CLAV','STRN','RBAK','LSHO','LUPA','LELB','LFRM','LWRA','LWRB','LFIN',
           'RSHO','RUPA','RELB','RFRM','RWRA','RWRB','RFIN','LASI','RASI','LPSI','RPSI','LTHI','LKNE','LTIB','LANK','LHEE','LTOE','RTHI','RKNE','RTIB','RANK','RHEE','RTOE']
coordinates =['x','y','z']
VICON_headers =[]
VICON_headers.append('Frame')
VICON_headers.append('Sub_Frame')
for joint in joints:
    for cor in coordinates:
        VICON_headers.append(joint+cor)
df_2 = pd.read_excel('VICON_NEW/9_VICON_s3.xlsx',names=VICON_headers,skiprows=2)
df_11 = pd.read_excel('VICON/15_VICON_s1.xlsx',names=VICON_headers,skiprows=2)

df_2['RUPAy'].plot(c='r')
df_11['RUPAy'].plot(c='m')
plt.title('Right Hip Y')
plt.legend(['8 exp','15 exp'])
plt.show()

df_2['RUPAx'].plot(c='r')
df_11['RUPAx'].plot(c='m')
plt.title('Right Hip X')
plt.legend(['8 exp','15 exp'])
plt.show()


# joints = ['LFHD','RFHD','LBHD','RBHD','C7','T10','CLAV','STRN','RBAK','LSHO','LUPA','LELB','LFRM','LWRA','LWRB','LFIN',
#            'RSHO','RUPA','RELB','RFRM','RWRA','RWRB','RFIN','LASI','RASI','LPSI','RPSI','LTHI','LKNE','LTIB','LANK','LHEE','LTOE','RTHI','RKNE','RTIB','RANK','RHEE','RTOE']
# coordinates =['y','x','z']
# VICON_headers1 =[]
# VICON_headers1.append('Frame')
# VICON_headers1.append('Sub_Frame')
# for joint in joints:
#     for cor in coordinates:
#         VICON_headers1.append(joint+cor)
# VICON_path = 'orginaze_VICON/'
# VICON_filesnames = os.listdir(VICON_path)
# x_headers = [x for x in VICON_headers if x[-1]=='x']
# mone =1
# for file in VICON_filesnames:
#     print(mone,'. started with->',file)
#     df = pd.read_excel(VICON_path+file,names=VICON_headers1)
#     df = df[VICON_headers]      #reorganize the X and Y coordinates
#     for x_cor in x_headers:     #mul by -1 every X coordinate
#         vector = df[x_cor].values
#         for i in range(2,len(vector)):
#             vector[i]=-1*float(vector[i])
#         df[x_cor] = vector
#     df.to_excel('VICON_NEW/'+file,header=True,index=False)
#     mone+=1