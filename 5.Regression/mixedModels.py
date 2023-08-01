import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt


def getPvalue(res):     #return the p-value part from string results
    index1 = res.index('p-value=')
    index2 = res[index1:].index(',')
    index2=index1+index2
    index1 +=8
    return res[index1:index2]

def get_feature_exp(feature,df):        #return dataFrame with the exp number
    df_res=pd.DataFrame()
    for camera in ['1','2','3','4']:
        df_res = pd.concat([df_res,df_1[df_1['Body_width'+camera] != 0][[feature+'0',feature+camera,'exps_num']]])
    return df_res


# making a list of all features name
features = ['Body_width','Max_delta_X','Max_delta_Y','Max_Z','Min_Z','Max_legs_angle','Max_step_height','Max_step_length','Max_velocity','Max_acceleration','Min_leg_angle','steps_count_ankle_diff','steps_count_derivative','Turn_count_ankles','Turn_count_hips','Turn_count_shoulders']
headers =[]
for j in range(len(features)):
    for i in ['0','1','2','3','4']:
        headers.append(features[j]+i)
df_1 = pd.read_excel('allFeatures.xlsx',skiprows=1,index_col=0)
df_1 = df_1.dropna(axis=1)
df_1.columns = headers
exps = list(df_1.T.columns)
for i in range(len(exps)):
    if exps[i][1]=='_':
        exps[i] = exps[i][:-4]
    else:
        exps[i] = exps[i][:-3]
df_1['exps_num'] = exps
get_feature_exp('Turn_count_shoulders',df_1).to_csv('Test.csv')
# 'steps_count_ankle_diff','steps_count_derivative','Turn_count_ankles','Turn_count_hips','Turn_count_shoulders'

ls_Pvalues=[]
dic_res = {}
df_res = pd.DataFrame()
for i in range(0,len(headers),5):
    break
    #---------------ZED2mm
    temp = df_1[df_1[headers[i+1]]!=0][[headers[i],headers[i+1],'exps_num']]    #For ZED2mm features
    md = smf.mixedlm(headers[i]+'~'+headers[i+1], data=temp,groups=temp["exps_num"])
    mdf = md.fit()
    LRresult1 = (mdf.summary().tables[1])
    dic_res[headers[i+1]] = LRresult1
    waldtest = mdf.wald_test(r_matrix=headers[i+1]+" = 1")
    zed2_wald = getPvalue(waldtest.summary())
    #R2 results
    var_resid = mdf.scale
    var_random_effect = float(mdf.cov_re.iloc[0])
    var_fixed_effect = mdf.predict(temp).var()
    total_var = var_fixed_effect + var_random_effect + var_resid
    marginal_r2 = var_fixed_effect / total_var
    conditional_r2 = (var_fixed_effect + var_random_effect) / total_var
    r2_zed2mm = [marginal_r2,conditional_r2,'first=marginal, second=condotional']
    LRresult1['R2'] = r2_zed2mm

    # ---------------ZED4mm
    temp = df_1[df_1[headers[i + 2]] != 0][[headers[i], headers[i + 2], 'exps_num']]  # For ZED4mm features
    md = smf.mixedlm(headers[i] + '~' + headers[i + 2], data=temp, groups=temp["exps_num"])
    mdf = md.fit()
    LRresult2 = (mdf.summary().tables[1])
    dic_res[headers[i + 2]] = LRresult2
    waldtest = mdf.wald_test(r_matrix=headers[i+2]+" = 1")
    zed4_wald = getPvalue(waldtest.summary())
    # R2 results
    var_resid = mdf.scale
    var_random_effect = float(mdf.cov_re.iloc[0])
    var_fixed_effect = mdf.predict(temp).var()
    total_var = var_fixed_effect + var_random_effect + var_resid
    marginal_r2 = var_fixed_effect / total_var
    conditional_r2 = (var_fixed_effect + var_random_effect) / total_var
    r2_zed4mm = [marginal_r2, conditional_r2,'first=marginal, second=condotional']
    LRresult2['R2'] = r2_zed4mm

    # ---------------NUITRACK
    temp = df_1[df_1[headers[i + 3]] != 0][[headers[i], headers[i + 3], 'exps_num']]  # For Nuitrack features
    md = smf.mixedlm(headers[i] + '~' + headers[i + 3], data=temp, groups=temp["exps_num"])
    mdf = md.fit()
    LRresult3 = (mdf.summary().tables[1])
    dic_res[headers[i + 3]] = LRresult3
    waldtest = mdf.wald_test(r_matrix=headers[i+3]+" = 1")
    nuitrack_wald = getPvalue(waldtest.summary())
    # R2 results
    var_resid = mdf.scale
    var_random_effect = float(mdf.cov_re.iloc[0])
    var_fixed_effect = mdf.predict(temp).var()
    total_var = var_fixed_effect + var_random_effect + var_resid
    marginal_r2 = var_fixed_effect / total_var
    conditional_r2 = (var_fixed_effect + var_random_effect) / total_var
    r2_nuitrack = [marginal_r2, conditional_r2,'first=marginal, second=condotional']
    LRresult3['R2'] = r2_nuitrack

    # ---------------MEDIA
    temp = df_1[df_1[headers[i + 4]] != 0][[headers[i], headers[i + 4], 'exps_num']]  # For MEDIA features
    md = smf.mixedlm(headers[i] + '~' + headers[i + 4], data=temp, groups=temp["exps_num"])
    mdf = md.fit()
    LRresult4 = (mdf.summary().tables[1])
    dic_res[headers[i + 4]] = LRresult4
    # df_res = pd.concat([df_res,LRresult1,LRresult2,LRresult3,LRresult4])
    waldtest = mdf.wald_test(r_matrix=headers[i+4]+" = 1")
    media_wald = getPvalue(waldtest.summary())
    # R2 results
    var_resid = mdf.scale
    var_random_effect = float(mdf.cov_re.iloc[0])
    var_fixed_effect = mdf.predict(temp).var()
    total_var = var_fixed_effect + var_random_effect + var_resid
    marginal_r2 = var_fixed_effect / total_var
    conditional_r2 = (var_fixed_effect + var_random_effect) / total_var
    r2_media = [marginal_r2, conditional_r2,'first=marginal, second=condotional']
    LRresult4['R2'] = r2_media
    df_res = pd.concat([df_res, LRresult1, LRresult2, LRresult3, LRresult4])
    ls_Pvalues.append([features[int(i/5)],zed2_wald,zed4_wald,nuitrack_wald,media_wald])
    ls_Pvalues.append([features[int(i/5)]+'-marginal_r2',r2_zed2mm[0],r2_zed4mm[0],r2_nuitrack[0],r2_media[0]])
    ls_Pvalues.append([features[int(i/5)]+'-conditional_r2',r2_zed2mm[1],r2_zed4mm[1],r2_nuitrack[1],r2_media[1]])



df_Pvalues = pd.DataFrame(data=ls_Pvalues,columns=['Feature','ZED2mm','ZED4mm','Nuitrack','MediaPipe'])
# df_Pvalues.to_csv('WaldTest_Pvalues1.csv',index=False)
# df_res.to_csv('Regression1.csv')


#----------------------- GRAPHS

# counter = 0
# camera = ['ZED2mm','ZED4mm','Nuitrack','Media']
# camera_index =0
# dic_org = {}
# ls_coef = df_res['Coef.'].values
# for i in range(0,len(ls_coef),3):
#     dic_org[features[counter]+camera[camera_index]]=[ls_coef[i],ls_coef[i+1]]
#     camera_index+=1
#     if camera_index>3:
#         camera_index=0
#         counter+=1
#
# df_org_data =pd.DataFrame.from_dict(dic_org)
# filter_col = [col for col in df_org_data if col.endswith('ZED2mm')]
# zed2= df_org_data[filter_col].T
# filter_col = [col for col in df_org_data if col.endswith('ZED4mm')]
# zed4= df_org_data[filter_col].T
# filter_col = [col for col in df_org_data if col.endswith('Nuitrack')]
# nuitrack= df_org_data[filter_col].T
# filter_col = [col for col in df_org_data if col.endswith('Media')]
# media= df_org_data[filter_col].T

# zed2[1].astype(float).plot(kind='density')
# plt.title('ZED2mm beta1 density plot')
# plt.show()
# zed2[0].astype(float).plot(kind='density')
# plt.title('ZED2mm beta0 density plot')
# plt.show()
# zed4[1].astype(float).plot(kind='density')
# plt.title('ZED4mm beta1 density plot')
# plt.show()
# zed4[0].astype(float).plot(kind='density')
# plt.title('ZED4mm beta0 density plot')
# plt.show()
# nuitrack[1].astype(float).plot(kind='density')
# plt.title('Nuitrack beta1 density plot')
# plt.show()
# nuitrack[0].astype(float).plot(kind='density')
# plt.title('Nuitrack beta0 density plot')
# plt.show()
# media[1].astype(float).plot(kind='density')
# plt.title('MediaPipe beta1 density plot')
# plt.show()
# media[0].astype(float).plot(kind='density')
# plt.title('MediaPipe beta0 density plot')
# plt.show()
# df_org_data = df_org_data.T
# df_org_data.columns = ['beta0','beta1']
# df_org_data.to_csv('Org_mixedModels.csv')


