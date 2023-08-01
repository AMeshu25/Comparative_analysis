import xlsxwriter
import datetime
import Settings as s
from Joint import joint
# from openpyxl import Workbook


def create_workbook(worksheet_name):
    #current_time = datetime.datetime.now()
    # worksheet_name = str(current_time.day) + "." + str(current_time.month) + " " + str(current_time.hour) + "." + \
    #                  str(current_time.minute) + "." + str(current_time.second) + ".xlsx"
    folder_path = s.excel_path
    s.excel_workbook = xlsxwriter.Workbook(folder_path + "/" + worksheet_name)
    s.ex_list = []


def wf_joints(sheetName, list_joints):
    '''
    Writing joints data for an exercise in Excel file in two versions
    :param ex_name:
    :param list_joints:
    :return:
    '''
    jointsNumber = {"1": 1, "2": 4, "3":7, "4":10, "5":13, "6":16, "7":19, "8":22, "9":25,
                    "11":28, "12":31, "13":34, "14":37, "15":40,
                    "17":43, "18":46, "19":49,
                    "21":52, "22":55, "23":58}
    current_time = datetime.datetime.now()
    name = sheetName + str(current_time.minute) + str(current_time.second)
    s.worksheet = s.excel_workbook.add_worksheet(name)
    s.worksheet.write(0, 0, 'Key Point Number->')
    for x, y in jointsNumber.items():
        s.worksheet.write(0, y, x)
    frame_number = 1
    row = 1
    for l in range(1, len(list_joints)): #specific frame
        if list_joints[l]==None:
            frame_number += 1
            continue
        s.worksheet.write(row, 0, frame_number)
        firstJoint=1
        for j in list_joints[l]:  # data inside the frame - same row all the joints in the frame
            print(j.__str__())
            if type(j) == joint:
                j_ar = j.joint_to_array()
                jointNum=j_ar[0]
                if (firstJoint==1):
                    jointNum = j_ar[0][-1]
                if (jointNum==1):
                    print("4444444")
                col=jointsNumber.get(jointNum)
                for i in range(1, len(j_ar)):
                    s.worksheet.write(row, col, str(j_ar[i]))
                    col += 1
                firstJoint +=1
        # for j in list_joints[l]: #data inside the frame - same row all the joints in the frame
        #     if type(j) == joint:
        #         j_ar = j.joint_to_array()
        #         jointNum=j_ar.type()
        #         for i in range(1, len(j_ar)):
        #             s.worksheet.write(row, col, str(j_ar[i]))
        #             col += 1

            # else:
            #     print("inelse")
            #     print(j)
            #     print(type(j))
            #     s.worksheet.write(row, frame_number, j)
            #     row += 1

        frame_number += 1
        row += 1


#write to execl file exercises names and the successful repetition number
def wf_exercise():
    row = 1
    col = 0
    s.worksheet = s.excel_workbook.add_worksheet("success")
    for ex in s.ex_list:
        s.worksheet.write(row, col, ex[0])
        s.worksheet.write(row, col+1, ex[1])
        row += 1

def close_workbook():
    s.excel_workbook.close()

if __name__ == "__main__":
    s.excel_path = R'C:\Users\TEMP.NAAMA\PycharmProjects\Nuitrack\excel_folder/'
    create_workbook("Naama.xlsx")
    join = [[12, 496.793, 98.652, 927.991],
    [6, 457.266, 80.806, 757.736],
    [12, 496.610, 91.162, 930.897]]
    wf_joints("m",join)

    wf_exercise()
    close_workbook()