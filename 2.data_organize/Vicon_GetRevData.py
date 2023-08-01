import os
import pandas as pd
import csv

#here you right the folder that contains all the csv files
path = 'VICON_Data_old/'
firstSpace = True
filesnames = os.listdir(path)
mone =1
# all variable is the upper bound if want to run less than all but dont care who first
all = len(filesnames)
for file in filesnames:
    data = []
    name=file[:-3]
    # write the exact rout to folder
    # ---------need to be chage to more modular form
    with open('D:\\project_analyze\\Camera_Comperisson\\VICON_Data_old\\'+file, newline='',encoding='utf-8') as file:
        print('started with: ',name)
        reader = csv.reader(file)
        counter =0
        for row in reader:
            if len(row) == 0:
                if (firstSpace):
                    firstSpace = False
            if firstSpace == False:
                data.append(row)
            counter+=1
        firstSpace = True
        print('rows number= ',counter)

    res = pd.DataFrame(data[3:])
    res.to_excel('NEW/'+name+'xlsx',header=False, index=False)
    print('finished ',round(100*mone/all),'%| files left =',all-mone,'| name=',name)
    mone+=1





