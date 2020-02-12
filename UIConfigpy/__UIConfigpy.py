from tkinter import *
# import pandas as pd
# import numpy as np
from time import sleep
# from PIL import Image, ImageTk
# from tkinter import filedialog
import os
# import shutil
# from xlsxwriter.workbook import Workbook
# from xlsxwriter.worksheet import Worksheet

root = Tk()
root.title('GAC_EDR_Check_Tool')
root.geometry('350x350')

canvas = Canvas(root,
                width=500,  # 指定Canvas组件的宽度
                height=600,  # 指定Canvas组件的高度
                bg='white')  # 指定Canvas组件的背景色
# im = Tkinter.PhotoImage(file='img.gif')     # 使用PhotoImage打开图片
image = Image.open("Config.PNG")
im = ImageTk.PhotoImage(image)

canvas.create_image(160, 100, image=im)  # 使用create_image将图片添加到Canvas组件中
canvas.create_text(280, 117,  # 使用create_text方法在坐标（302，77）处绘制文字
                   text='For GAC EDR Test'  # 所绘制文字的内容
                   , fill='Blue')  # 所绘制文字的颜色为灰色
canvas.create_text(270, 190,  # 使用create_text方法在坐标（302，77）处绘制文字
                   text='Veoneer'  # 所绘制文字的内容
                   , fill='White', font=18)  # 所绘制文字的颜色为灰色


def open_files_xlsx():
    files_info = filedialog.askopenfilenames(title='Select EDR Result.xlsx',
                                             filetypes=[("EDR_Actual_Result", "*.xlsx")],
                                             initialdir="c:/project/GAC_A39/EDR_Test_logs")
    save_data = str(files_info)
    f = open('1_EDR_Checklist_want.txt', 'w+')
    f.writelines(save_data)
    f.close()
    output = save_data.strip('(')
    output = output.strip(')')
    output = output.split(',')
    print('You have selected_' + str(len(output)) + "_files to the EDR checklist")


def open_files_txt():
    files_info = filedialog.askopenfilenames(title='Select EDR txt files', filetypes=[("Related_txt_Files", "*.txt")],
                                             initialdir="c:/project/GAC_A39/EDR_Test_logs")
    save_data = str(files_info)
    f = open('2_Related_txtlist.txt', 'w+')
    f.writelines(save_data)
    f.close()
    output = save_data.strip('(')
    output = output.strip(')')
    output = output.split(',')
    print('You have selected_' + str(len(output)) + "_related txt files for EDR check ")


def check_selected_files():
    sleep(1)
    f = open('1_EDR_Checklist_want.txt', 'r', True)
    xlsx_file_list = f.read()
    f.close()
    g = open('2_Related_txtlist.txt', 'r', True)
    txt_file_list = g.read()
    g.close()
    xlsx_file_list = xlsx_file_list.strip('(')
    xlsx_file_list = xlsx_file_list.strip(')')
    xlsx_file_list = xlsx_file_list.split(',')
    final_check_list = []
    if os.path.exists('3_Final_check_list.txt'):
        os.remove('3_Final_check_list.txt')
    if os.path.exists('1_EDR_Checklist_want.txt'):
        os.remove('1_EDR_Checklist_want.txt')
    if os.path.exists('2_Related_txtlist.txt'):
        os.remove('2_Related_txtlist.txt')
    sleep(1)
    for i in range(len(xlsx_file_list)):
        check_name = xlsx_file_list[i][:-18]
        # print(check_name)
        # result = check_name in txt_file_list
        if check_name in txt_file_list and check_name != '':
            final_check_list.append(xlsx_file_list[i] + ',')
        else:
            print(xlsx_file_list[i] + "_don't find match txt file, It has been deleted from EDR checklist")
    f = open('3_Final_check_list.txt', 'w+')
    f.writelines(final_check_list)
    f.close()
    print("Final checklist has been updated, You can do the ST4 now")


def output_edr_result():
    f = open('3_Final_check_list.txt', 'r', True)
    final_check_list = f.read()
    f.close()
    final_check_list = final_check_list.split(',')
    print('Start to handle.....please wait.....The color of ST4 button will return to Orange when finished ')
    for i in range(len(final_check_list) - 1):
        final_check_list[i] = final_check_list[i].strip()
        final_check_list[i] = final_check_list[i].strip("'")
        print(final_check_list[i])
        if final_check_list[i] != "":
            check_edr_result(final_check_list[i])
    # if os.path.exists('3_Final_check_list.txt'):
    #     os.remove('3_Final_check_list.txt')
    if os.path.exists('1_EDR_Checklist_want.txt'):
        os.remove('1_EDR_Checklist_want.txt')
    if os.path.exists('2_Related_txtlist.txt'):
        os.remove('2_Related_txtlist.txt')
    sleep(1)
    print('All the files in the checklist task has been finished~~~')


def check_edr_result(path):
    edr_info_path = path[:-17] + '.txt'
    f2 = open(edr_info_path, 'r', True, 'utf-8')
    edr_info = []
    while True:
        want_data = f2.readline()
        if not want_data:
            break
        edr_info.append(want_data)
    # print(edr_info)
    total_len = len(edr_info)
    # print(total_len)

    pulse_define = edr_info[total_len - 3]
    # print(crash_curves)
    # print(pulse_define)
    f2.close()

    important_information = pd.read_csv(edr_info_path)

    # confirm event start time , deploy loop and continue time
    case_start_time = {}
    case_deploy = {}
    case_continue_time = {}
    for i in range(total_len - 3):
        txt_useful_info = edr_info[i][8:]
        # print(txt_useful_info)
        txt_event_no = txt_useful_info.split(",")[0]
        txt_start_time = txt_useful_info.split(",")[1]
        case_start_time[txt_event_no] = txt_start_time
        next_start_time = edr_info[i + 1][8:]
        next_start_time = next_start_time.split(",")[1]
        if next_start_time[0] != '"':
            during_time = int(next_start_time) - int(txt_start_time)
        else:
            during_time = 300
        # print(during_time)
        # print(next_start_time)
        txt_deploy_loop = txt_useful_info.split('"')[1]
        txt_deploy_loop = txt_deploy_loop.split(",")
        expect_deploy_no = []
        # print(txt_deploy_loop)
        for j in range(len(txt_deploy_loop)):
            deploy_status = txt_deploy_loop[j]
            if deploy_status == '1':
                expect_deploy_no.append(j)
        # print(expect_deploy_no)
        case_deploy[txt_event_no] = expect_deploy_no
        case_continue_time[txt_event_no] = during_time
        # print(case_deploy)
    # print(case_start_time)
    # print(case_continue_time)

    # confirm crash curves file
    crash_curves = edr_info[total_len - 2]
    crash_curves = crash_curves.split('=')
    crash_curves = crash_curves[1].split(',')
    ctx_file = crash_curves[0].strip(' ').strip('[').strip('"')
    ctx_file = 'C:/Project/GAC_A39/ARIA_Configuration/P50/Crash_Data/SC2-1S/' + ctx_file
    cty_file = crash_curves[1].strip(' ').strip('[').strip('"')
    cty_file = 'C:/Project/GAC_A39/ARIA_Configuration/P50/Crash_Data/SC2-1S/' + cty_file
    frsuL_file = crash_curves[2].strip(' ').strip('[').strip('"')
    frsuL_file = 'C:/Project/GAC_A39/ARIA_Configuration/P50/Crash_Data/SC2-1S/' + frsuL_file
    frsuR_file = crash_curves[3].strip(' ').strip('[').strip('"')
    frsuR_file = 'C:/Project/GAC_A39/ARIA_Configuration/P50/Crash_Data/SC2-1S/' + frsuR_file
    srsuL_file = crash_curves[4].strip(' ').strip('[').strip('"')
    srsuL_file = 'C:/Project/GAC_A39/ARIA_Configuration/P50/Crash_Data/SC2-1S/' + srsuL_file
    srsuR_file = crash_curves[5].strip(' ').strip('[').strip('"').strip(';').strip('"').strip(']').strip('"')
    srsuR_file = 'C:/Project/GAC_A39/ARIA_Configuration/P50/Crash_Data/SC2-1S/' + srsuR_file
    # print(srsuL_file)
    # print(ctx_file+'|'+cty_file+'|'+frsuL_file+'|'+frsuR_file+'|'+srsuL_file+'|'+srsuR_file)
    a = open(ctx_file, 'r', True, 'utf-8')
    ctx_value = a.readlines()
    a.close()
    b = open(cty_file, 'r', True, 'utf-8')
    cty_value = b.readlines()
    b.close()
    c = open(frsuL_file, 'r', True, 'utf-8')
    frsuL_value = c.readlines()
    c.close()
    d = open(frsuR_file, 'r', True, 'utf-8')
    frsuR_value = d.readlines()
    d.close()
    e = open(srsuL_file, 'r', True, 'utf-8')
    srsuL_value = e.readlines()
    e.close()
    g = open(srsuR_file, 'r', True, 'utf-8')
    srsuR_value = g.readlines()
    g.close()
    # add 0 , let all the data have the same length
    ctx_len = len(ctx_value)
    cty_len = len(cty_value)
    frsuL_len = len(frsuL_value)
    frsuR_len = len(frsuR_value)
    srsuL_len = len(srsuL_value)
    srsuR_len = len(srsuR_value)
    max_len = max(ctx_len, cty_len, frsuL_len, frsuR_len, srsuL_len, srsuR_len)
    if ctx_len < max_len:
        for ctx in range(max_len - ctx_len):
            ctx_value.append('0')
    if cty_len < max_len:
        for cty in range(max_len - cty_len):
            cty_value.append('0')
    if frsuL_len < max_len:
        for frsu1 in range(max_len - frsuL_len):
            frsuL_value.append('0')
    if frsuR_len < max_len:
        for frsur in range(max_len - frsuR_len):
            frsuR_value.append('0')
    if srsuL_len < max_len:
        for srsul in range(max_len - srsuL_len):
            srsuL_value.append('0')
    if srsuR_len < max_len:
        for srsur in range(max_len - srsuR_len):
            srsuR_value.append('0')

    want_column = 'PARAMETER NAME'
    actual_result = 'READ VALUE'

    global_data = pd.read_excel(path, 'Gloabl Data')
    global_data = pd.DataFrame(global_data, columns=['PARAMETER NAME', 'READ VALUE', 'Expect', 'Judge'])

    buffer_number = 0
    # confirm EDR1 Event
    edr1_event = global_data[global_data[want_column] == 'RstEdr_GlobalEventInfo.au32LifeTimeEventNb._0_']
    edr1_event_index = edr1_event.index.tolist()
    edr1_event_index = edr1_event_index[0]
    edr1_event_no = edr1_event.loc[[edr1_event_index], [actual_result]]
    edr1_event_no = np.array(edr1_event_no)
    edr1_event_no = edr1_event_no.tolist()
    edr1_event_no = edr1_event_no[0][0]
    edr1_event_no = int(edr1_event_no, 16)
    if edr1_event_no != 0:
        buffer_number = buffer_number + 1
        edr1_start_time = case_start_time[str(edr1_event_no)]
        edr1_deploy_loop = case_deploy[str(edr1_event_no)]
        edr1_continue_time = case_continue_time[str(edr1_event_no)]
        # print(edr1_continue_time)
        time_between_1 = 65535
        if edr1_event_no != 1:
            last_event_time = case_start_time[str(edr1_event_no - 1)]
            if int(edr1_start_time) - int(last_event_time) < 5000:
                time_between_1 = int(edr1_start_time) - int(last_event_time)
                time_between_1 = int(time_between_1) * 2

        if edr1_continue_time >= 300:
            edr1_continue_time = 300
        # print(edr1_start_time+'|'+str(edr1_deploy_loop)+'|'+str(edr1_continue_time))

        # confirm EDR1 Type
        edr1_ctx = []
        edr1_cty = []
        edr1_frsul = []
        edr1_frsur = []
        edr1_srsul = []
        edr1_srsur = []
        expect_ac_x_1 = []
        expect_ac_y_1 = []
        expect_ac_frsul_1 = []
        expect_ac_frsur_1 = []
        expect_ac_srsul_1 = []
        expect_ac_srsur_1 = []

        for i in range(300 * 2):
            edr1_ctx.append((ctx_value[(int(edr1_start_time) * 2 + i)].strip('\n').strip(' ')))
            edr1_cty.append((cty_value[(int(edr1_start_time) * 2 + i)].strip('\n').strip(' ')))
            edr1_frsul.append((frsuL_value[(int(edr1_start_time) * 2 + i)].strip('\n').strip(' ')))
            edr1_frsur.append((frsuR_value[(int(edr1_start_time) * 2 + i)].strip('\n').strip(' ')))
            edr1_srsul.append((srsuL_value[(int(edr1_start_time) * 2 + i)].strip('\n').strip(' ')))
            edr1_srsur.append((srsuR_value[(int(edr1_start_time) * 2 + i)].strip('\n').strip(' ')))
        if int(edr1_ctx[0]) >= 100 and (int(edr1_frsul[0]) >= 100 or int(edr1_frsur[0]) >= 100):
            edr1_crash_type = 258
            edr1_algo_type = 2
            # print(len(edr1_ctx))
            for i in range(300 * 2):
                expect_ac_x_1.append(int(edr1_ctx[i]) * (-4))
                expect_ac_y_1.append(int(edr1_cty[i]) * (-4))
                expect_ac_frsul_1.append(int(edr1_frsul[i]) * (-64))
                expect_ac_frsur_1.append(int(edr1_frsur[i]) * (-64))
                expect_ac_srsul_1.append(int(edr1_srsul[i]) * (-32))
                expect_ac_srsur_1.append(int(edr1_srsur[i]) * (-32))
            # print(expect_ac_x_1)
            # print(expect_ac_y_1)
            # print(expect_ac_frsul_1)
            # print(expect_ac_frsur_1)
            # print(expect_ac_srsul_1)
            # print(expect_ac_srsur_1)

        elif int(edr1_ctx[0]) <= -150 and (int(edr1_frsul[0]) <= -150 or int(edr1_frsur[0]) <= -150):
            edr1_crash_type = 2064
            edr1_algo_type = 32
            for i in range(300 * 2):
                expect_ac_x_1.append(int(edr1_ctx[i]) * (-4))
                expect_ac_y_1.append(int(edr1_cty[i]) * (-4))
                expect_ac_frsul_1.append(int(edr1_frsul[i]) * (-64))
                expect_ac_frsur_1.append(int(edr1_frsur[i]) * (-64))
                expect_ac_srsul_1.append(int(edr1_srsul[i]) * (-32))
                expect_ac_srsur_1.append(int(edr1_srsur[i]) * (-32))

        elif int(edr1_cty[0]) <= -100 and int(edr1_srsul[0]) >= 100:
            edr1_crash_type = 516
            edr1_algo_type = 4
            for i in range(300 * 2):
                expect_ac_x_1.append(int(edr1_ctx[i]) * (-4))
                expect_ac_y_1.append(int(edr1_cty[i]) * 4)
                expect_ac_frsul_1.append(int(edr1_frsul[i]) * (-64))
                expect_ac_frsur_1.append(int(edr1_frsur[i]) * (-64))
                expect_ac_srsul_1.append(int(edr1_srsul[i]) * (-32))
                expect_ac_srsur_1.append(int(edr1_srsur[i]) * 32)

        elif int(edr1_cty[0]) >= 100 and int(edr1_srsur[0]) >= 100:
            edr1_crash_type = 1032
            edr1_algo_type = 8
            for i in range(300 * 2):
                expect_ac_x_1.append(int(edr1_ctx[i]) * 4)
                expect_ac_y_1.append(int(edr1_cty[i]) * 4)
                expect_ac_frsul_1.append(int(edr1_frsul[i]) * 64)
                expect_ac_frsur_1.append(int(edr1_frsur[i]) * 64)
                expect_ac_srsul_1.append(int(edr1_srsul[i]) * (-32))
                expect_ac_srsur_1.append(int(edr1_srsur[i]) * 32)
        else:
            edr1_crash_type = 0
            edr1_algo_type = 0
            if int(edr1_ctx[0]) > 0 and (int(edr1_frsul[0]) > 0 or int(edr1_frsur[0]) > 0):
                for i in range(300 * 2):
                    expect_ac_x_1.append(int(edr1_ctx[i]) * (-4))
                    expect_ac_y_1.append(int(edr1_cty[i]) * (-4))
                    expect_ac_frsul_1.append(int(edr1_frsul[i]) * (-64))
                    expect_ac_frsur_1.append(int(edr1_frsur[i]) * (-64))
                    expect_ac_srsul_1.append(int(edr1_srsul[i]) * (-32))
                    expect_ac_srsur_1.append(int(edr1_srsur[i]) * (-32))

            elif int(edr1_ctx[0]) < 0 and (int(edr1_frsul[0]) < 0 or int(edr1_frsur[0]) < 0):
                for i in range(300 * 2):
                    expect_ac_x_1.append(int(edr1_ctx[i]) * (-4))
                    expect_ac_y_1.append(int(edr1_cty[i]) * (-4))
                    expect_ac_frsul_1.append(int(edr1_frsul[i]) * (-64))
                    expect_ac_frsur_1.append(int(edr1_frsur[i]) * (-64))
                    expect_ac_srsul_1.append(int(edr1_srsul[i]) * (-32))
                    expect_ac_srsur_1.append(int(edr1_srsur[i]) * (-32))

            elif int(edr1_cty[0]) < 0 and int(edr1_srsul[0]) > 0:
                for i in range(300 * 2):
                    expect_ac_x_1.append(int(edr1_ctx[i]) * (-4))
                    expect_ac_y_1.append(int(edr1_cty[i]) * 4)
                    expect_ac_frsul_1.append(int(edr1_frsul[i]) * (-64))
                    expect_ac_frsur_1.append(int(edr1_frsur[i]) * (-64))
                    expect_ac_srsul_1.append(int(edr1_srsul[i]) * (-32))
                    expect_ac_srsur_1.append(int(edr1_srsur[i]) * 32)

            elif int(edr1_cty[0]) > 0 and int(edr1_srsur[0]) > 0:
                for i in range(300 * 2):
                    expect_ac_x_1.append(int(edr1_ctx[i]) * (-4))
                    expect_ac_y_1.append(int(edr1_cty[i]) * 4)
                    expect_ac_frsul_1.append(int(edr1_frsul[i]) * (-64))
                    expect_ac_frsur_1.append(int(edr1_frsur[i]) * (-64))
                    expect_ac_srsul_1.append(int(edr1_srsul[i]) * (-32))
                    expect_ac_srsur_1.append(int(edr1_srsur[i]) * 32)

            else:
                for i in range(300 * 2):
                    expect_ac_x_1.append(int(edr1_ctx[i]) * 4)
                    expect_ac_y_1.append(int(edr1_cty[i]) * (-4))
                    expect_ac_frsul_1.append(int(edr1_frsul[i]) * 64)
                    expect_ac_frsur_1.append(int(edr1_frsur[i]) * 64)
                    expect_ac_srsul_1.append(int(edr1_srsul[i]) * (-32))
                    expect_ac_srsur_1.append(int(edr1_srsur[i]) * 32)

        max_ctx_1 = max(expect_ac_x_1)
        min_ctx_1 = min(expect_ac_x_1)
        if abs(max_ctx_1) >= abs(min_ctx_1):
            max_ctx_ac_1 = max_ctx_1
        else:
            max_ctx_ac_1 = min_ctx_1
        max_cty_1 = max(expect_ac_y_1)
        min_cty_1 = min(expect_ac_y_1)
        if abs(max_cty_1) >= abs(min_cty_1):
            max_cty_ac_1 = max_cty_1
        else:
            max_cty_ac_1 = min_cty_1
        max_ctx_time_1 = expect_ac_x_1.index(max_ctx_ac_1)
        max_cty_time_1 = expect_ac_y_1.index(max_cty_ac_1)
        # edr1 algo start time
        expect_front_algo_1 = 32766
        expect_sidel_algo_1 = 32766
        expect_sider_algo_1 = 32766
        expect_rear_algo_1 = 32766
        if int(edr1_ctx[0]) > 50:
            expect_front_algo_1 = 0
        if int(edr1_cty[0]) < -50:
            expect_sidel_algo_1 = 0
        if int(edr1_cty[0]) > 50:
            expect_sider_algo_1 = 0
        if int(edr1_ctx[0]) < -50:
            expect_rear_algo_1 = 0
        # edr1 deploy loop
        loop0_decision_1 = loop0_status_1 = 0
        loop1_decision_1 = loop1_status_1 = 0
        loop2_decision_1 = loop2_status_1 = 0
        loop3_decision_1 = loop3_status_1 = 0
        loop4_decision_1 = loop4_status_1 = 0
        loop5_decision_1 = loop5_status_1 = 0
        loop6_decision_1 = loop6_status_1 = 0
        loop7_decision_1 = loop7_status_1 = 0
        loop8_decision_1 = loop8_status_1 = 0
        loop9_decision_1 = loop9_status_1 = 0
        loop10_decision_1 = loop10_status_1 = 0
        loop11_decision_1 = loop11_status_1 = 0
        deploy_request_1 = 0
        crash_priority_1 = 1
        for l in edr1_deploy_loop:
            if l == 0:
                loop0_decision_1 = loop0_status_1 = 134
                deploy_request_1 = 1
                crash_priority_1 = 192
            elif l == 1:
                loop1_decision_1 = loop1_status_1 = 134
                deploy_request_1 = 1
                crash_priority_1 = 192
            elif l == 2:
                loop2_decision_1 = loop2_status_1 = 134
                deploy_request_1 = 1
                crash_priority_1 = 192
            elif l == 3:
                loop3_decision_1 = loop3_status_1 = 134
                deploy_request_1 = 1
                crash_priority_1 = 192
            elif l == 4:
                loop4_decision_1 = loop4_status_1 = 134
                deploy_request_1 = 1
                if crash_priority_1 != 192:
                    crash_priority_1 = 144
            elif l == 5:
                loop5_decision_1 = loop5_status_1 = 134
                deploy_request_1 = 1
                crash_priority_1 = 192
            elif l == 6:
                loop6_decision_1 = loop6_status_1 = 134
                deploy_request_1 = 1
                crash_priority_1 = 192
            elif l == 7:
                loop7_decision_1 = loop7_status_1 = 134
                deploy_request_1 = 1
                if crash_priority_1 != 192:
                    crash_priority_1 = 144
            elif l == 8:
                loop8_decision_1 = loop8_status_1 = 134
                deploy_request_1 = 1
                if crash_priority_1 != 192:
                    crash_priority_1 = 144
            elif l == 9:
                loop9_decision_1 = loop9_status_1 = 134
                deploy_request_1 = 1
                if crash_priority_1 != 192:
                    crash_priority_1 = 144
            elif l == 10:
                loop10_decision_1 = loop10_status_1 = 134
                deploy_request_1 = 1
                if crash_priority_1 != 192:
                    crash_priority_1 = 144
            elif l == 11:
                loop11_decision_1 = loop11_status_1 = 134
                deploy_request_1 = 1
                if crash_priority_1 != 192:
                    crash_priority_1 = 144
            # special for gac
        if edr1_crash_type == 2064:
            loop0_status_1 = 0
            loop1_status_1 = 0
            loop2_status_1 = 0
            loop3_status_1 = 0
            loop4_status_1 = 0
            loop5_status_1 = 0
            loop6_status_1 = 0
            loop7_status_1 = 0
            loop8_status_1 = 0
            loop9_status_1 = 0
            loop10_status_1 = 0
            loop11_status_1 = 0
            deploy_request_1 = 0
            crash_priority_1 = 4

        # edr1 algo end time
        algo_end_time_1 = 0
        for i in range(edr1_continue_time * 2):
            # print(abs(int(edr1_ctx[i])))
            if (abs(int(edr1_ctx[i])) < 50) and (abs(int(edr1_cty[i])) < 50) and (abs(int(edr1_frsul[i])) < 50) and (
                    abs(int(edr1_frsur[i])) < 50) and (abs(int(edr1_srsul[i])) < 50) and (abs(int(edr1_srsur[i])) < 50):
                algo_end_time_1 = algo_end_time_1 + 1
            else:
                algo_end_time_1 = 0
            if algo_end_time_1 > 80:
                algo_end_time_1 = int(i)
                break

    # confirm EDR2 Event
    edr2_event = global_data[global_data[want_column] == 'RstEdr_GlobalEventInfo.au32LifeTimeEventNb._1_']
    edr2_event_index = edr2_event.index.tolist()
    edr2_event_index = edr2_event_index[0]
    edr2_event_no = edr2_event.loc[[edr2_event_index], [actual_result]]
    edr2_event_no = np.array(edr2_event_no)
    edr2_event_no = edr2_event_no.tolist()
    edr2_event_no = edr2_event_no[0][0]
    edr2_event_no = int(edr2_event_no, 16)
    if edr2_event_no != 0:
        buffer_number = buffer_number + 1
        edr2_start_time = case_start_time[str(edr2_event_no)]
        edr2_deploy_loop = case_deploy[str(edr2_event_no)]
        edr2_continue_time = case_continue_time[str(edr2_event_no)]
        time_between_2 = 65535
        if edr2_event_no != 1:
            last_event_time_2 = case_start_time[str(edr2_event_no - 1)]
            if int(edr2_start_time) - int(last_event_time_2) < 5000:
                time_between_2 = int(edr2_start_time) - int(last_event_time_2)
                time_between_2 = int(time_between_2) * 2
        if edr2_continue_time >= 300:
            edr2_continue_time = 300
        # print(edr2_start_time+'|'+str(edr2_deploy_loop)+'|'+str(edr2_continue_time))

        # confirm EDR2 Type
        edr2_ctx = []
        edr2_cty = []
        edr2_frsul = []
        edr2_frsur = []
        edr2_srsul = []
        edr2_srsur = []
        expect_ac_x_2 = []
        expect_ac_y_2 = []
        expect_ac_frsul_2 = []
        expect_ac_frsur_2 = []
        expect_ac_srsul_2 = []
        expect_ac_srsur_2 = []

        for i in range(300 * 2):
            edr2_ctx.append((ctx_value[(int(edr2_start_time) * 2 + i)].strip('\n').strip(' ')))
            edr2_cty.append((cty_value[(int(edr2_start_time) * 2 + i)].strip('\n').strip(' ')))
            edr2_frsul.append((frsuL_value[(int(edr2_start_time) * 2 + i)].strip('\n').strip(' ')))
            edr2_frsur.append((frsuR_value[(int(edr2_start_time) * 2 + i)].strip('\n').strip(' ')))
            edr2_srsul.append((srsuL_value[(int(edr2_start_time) * 2 + i)].strip('\n').strip(' ')))
            edr2_srsur.append((srsuR_value[(int(edr2_start_time) * 2 + i)].strip('\n').strip(' ')))


        if int(edr2_ctx[0]) >= 100 and (int(edr2_frsul[0]) >= 100 or int(edr2_frsur[0]) >= 100):
            edr2_crash_type = 258
            edr2_algo_type = 2
            # print(len(edr2_ctx))
            for i in range(300 * 2):
                expect_ac_x_2.append(int(edr2_ctx[i]) * (-4))
                expect_ac_y_2.append(int(edr2_cty[i]) * (-4))
                expect_ac_frsul_2.append(int(edr2_frsul[i]) * (-64))
                expect_ac_frsur_2.append(int(edr2_frsur[i]) * (-64))
                expect_ac_srsul_2.append(int(edr2_srsul[i]) * (-32))
                expect_ac_srsur_2.append(int(edr2_srsur[i]) * (-32))
            # print(expect_ac_x_2)
            # print(expect_ac_y_2)
            # print(expect_ac_frsul_2)
            # print(expect_ac_frsur_2)
            # print(expect_ac_srsul_2)
            # print(expect_ac_srsur_2)

        elif int(edr2_ctx[0]) <= -150 and (int(edr2_frsul[0]) <= -150 or int(edr2_frsur[0]) <= -150):
            edr2_crash_type = 2064
            edr2_algo_type = 32
            for i in range(300 * 2):
                expect_ac_x_2.append(int(edr2_ctx[i]) * (-4))
                expect_ac_y_2.append(int(edr2_cty[i]) * (-4))
                expect_ac_frsul_2.append(int(edr2_frsul[i]) * (-64))
                expect_ac_frsur_2.append(int(edr2_frsur[i]) * (-64))
                expect_ac_srsul_2.append(int(edr2_srsul[i]) * (-32))
                expect_ac_srsur_2.append(int(edr2_srsur[i]) * (-32))

        elif int(edr2_cty[0]) <= -100 and int(edr2_srsul[0]) >= 100:
            edr2_crash_type = 516
            edr2_algo_type = 4
            for i in range(300 * 2):
                expect_ac_x_2.append(int(edr2_ctx[i]) * (-4))
                expect_ac_y_2.append(int(edr2_cty[i]) * 4)
                expect_ac_frsul_2.append(int(edr2_frsul[i]) * (-64))
                expect_ac_frsur_2.append(int(edr2_frsur[i]) * (-64))
                expect_ac_srsul_2.append(int(edr2_srsul[i]) * (-32))
                expect_ac_srsur_2.append(int(edr2_srsur[i]) * 32)

        elif int(edr2_cty[0]) >= 100 and int(edr2_srsur[0]) >= 100:
            edr2_crash_type = 1032
            edr2_algo_type = 8
            for i in range(300 * 2):
                expect_ac_x_2.append(int(edr2_ctx[i]) * 4)
                expect_ac_y_2.append(int(edr2_cty[i]) * 4)
                expect_ac_frsul_2.append(int(edr2_frsul[i]) * 64)
                expect_ac_frsur_2.append(int(edr2_frsur[i]) * 64)
                expect_ac_srsul_2.append(int(edr2_srsul[i]) * (-32))
                expect_ac_srsur_2.append(int(edr2_srsur[i]) * 32)
        else:
            edr2_crash_type = 0
            edr2_algo_type = 0
            if int(edr2_ctx[0]) > 0 and (int(edr2_frsul[0]) > 0 or int(edr2_frsur[0]) > 0):
                for i in range(300 * 2):
                    expect_ac_x_2.append(int(edr2_ctx[i]) * (-4))
                    expect_ac_y_2.append(int(edr2_cty[i]) * (-4))
                    expect_ac_frsul_2.append(int(edr2_frsul[i]) * (-64))
                    expect_ac_frsur_2.append(int(edr2_frsur[i]) * (-64))
                    expect_ac_srsul_2.append(int(edr2_srsul[i]) * (-32))
                    expect_ac_srsur_2.append(int(edr2_srsur[i]) * (-32))

            elif int(edr2_ctx[0]) < 0 and (int(edr2_frsul[0]) < 0 or int(edr2_frsur[0]) < 0):
                for i in range(300 * 2):
                    expect_ac_x_2.append(int(edr2_ctx[i]) * (-4))
                    expect_ac_y_2.append(int(edr2_cty[i]) * (-4))
                    expect_ac_frsul_2.append(int(edr2_frsul[i]) * (-64))
                    expect_ac_frsur_2.append(int(edr2_frsur[i]) * (-64))
                    expect_ac_srsul_2.append(int(edr2_srsul[i]) * (-32))
                    expect_ac_srsur_2.append(int(edr2_srsur[i]) * (-32))

            elif int(edr2_cty[0]) < 0 and int(edr2_srsul[0]) > 0:
                for i in range(300 * 2):
                    expect_ac_x_2.append(int(edr2_ctx[i]) * (-4))
                    expect_ac_y_2.append(int(edr2_cty[i]) * 4)
                    expect_ac_frsul_2.append(int(edr2_frsul[i]) * (-64))
                    expect_ac_frsur_2.append(int(edr2_frsur[i]) * (-64))
                    expect_ac_srsul_2.append(int(edr2_srsul[i]) * (-32))
                    expect_ac_srsur_2.append(int(edr2_srsur[i]) * 32)

            elif int(edr2_cty[0]) > 0 and int(edr2_srsur[0]) > 0:
                for i in range(300 * 2):
                    expect_ac_x_2.append(int(edr2_ctx[i]) * (-4))
                    expect_ac_y_2.append(int(edr2_cty[i]) * 4)
                    expect_ac_frsul_2.append(int(edr2_frsul[i]) * (-64))
                    expect_ac_frsur_2.append(int(edr2_frsur[i]) * (-64))
                    expect_ac_srsul_2.append(int(edr2_srsul[i]) * (-32))
                    expect_ac_srsur_2.append(int(edr2_srsur[i]) * 32)

            else:
                for i in range(300 * 2):
                    expect_ac_x_2.append(int(edr2_ctx[i]) * 4)
                    expect_ac_y_2.append(int(edr2_cty[i]) * (-4))
                    expect_ac_frsul_2.append(int(edr2_frsul[i]) * 64)
                    expect_ac_frsur_2.append(int(edr2_frsur[i]) * 64)
                    expect_ac_srsul_2.append(int(edr2_srsul[i]) * (-32))
                    expect_ac_srsur_2.append(int(edr2_srsur[i]) * 32)
        # print(edr2_crash_type)
        max_ctx_2 = max(expect_ac_x_2)
        min_ctx_2 = min(expect_ac_x_2)
        if abs(max_ctx_2) >= abs(min_ctx_2):
            max_ctx_ac_2 = max_ctx_2
        else:
            max_ctx_ac_2 = min_ctx_2
        max_cty_2 = max(expect_ac_y_2)
        min_cty_2 = min(expect_ac_y_2)
        if abs(max_cty_2) >= abs(min_cty_2):
            max_cty_ac_2 = max_cty_2
        else:
            max_cty_ac_2 = min_cty_2
        max_ctx_time_2 = expect_ac_x_2.index(max_ctx_ac_2)
        max_cty_time_2 = expect_ac_y_2.index(max_cty_ac_2)
        # edr2 algo start time
        expect_front_algo_2 = 32766
        expect_sidel_algo_2 = 32766
        expect_sider_algo_2 = 32766
        expect_rear_algo_2 = 32766
        if int(edr2_ctx[0]) > 50:
            expect_front_algo_2 = 0
        if int(edr2_cty[0]) < -50:
            expect_sidel_algo_2 = 0
        if int(edr2_cty[0]) > 50:
            expect_sider_algo_2 = 0
        if int(edr2_ctx[0]) < -50:
            expect_rear_algo_2 = 0
        # edr2 deploy loop
        loop0_decision_2 = loop0_status_2 = 0
        loop1_decision_2 = loop1_status_2 = 0
        loop2_decision_2 = loop2_status_2 = 0
        loop3_decision_2 = loop3_status_2 = 0
        loop4_decision_2 = loop4_status_2 = 0
        loop5_decision_2 = loop5_status_2 = 0
        loop6_decision_2 = loop6_status_2 = 0
        loop7_decision_2 = loop7_status_2 = 0
        loop8_decision_2 = loop8_status_2 = 0
        loop9_decision_2 = loop9_status_2 = 0
        loop10_decision_2 = loop10_status_2 = 0
        loop11_decision_2 = loop11_status_2 = 0
        deploy_request_2 = 0
        crash_priority_2 = 1
        for l in edr2_deploy_loop:
            if l == 0:
                loop0_decision_2 = loop0_status_2 = 134
                deploy_request_2 = 1
                crash_priority_2 = 192
            elif l == 1:
                loop1_decision_2 = loop1_status_2 = 134
                deploy_request_2 = 1
                crash_priority_2 = 192
            elif l == 2:
                loop2_decision_2 = loop2_status_2 = 134
                deploy_request_2 = 1
                crash_priority_2 = 192
            elif l == 3:
                loop3_decision_2 = loop3_status_2 = 134
                deploy_request_2 = 1
                crash_priority_2 = 192
            elif l == 4:
                loop4_decision_2 = loop4_status_2 = 134
                deploy_request_2 = 1
                if crash_priority_2 != 192:
                    crash_priority_2 = 144
            elif l == 5:
                loop5_decision_2 = loop5_status_2 = 134
                deploy_request_2 = 1
                crash_priority_2 = 192
            elif l == 6:
                loop6_decision_2 = loop6_status_2 = 134
                deploy_request_2 = 1
                crash_priority_2 = 192
            elif l == 7:
                loop7_decision_2 = loop7_status_2 = 134
                deploy_request_2 = 1
                if crash_priority_2 != 192:
                    crash_priority_2 = 144
            elif l == 8:
                loop8_decision_2 = loop8_status_2 = 134
                deploy_request_2 = 1
                if crash_priority_2 != 192:
                    crash_priority_2 = 144
            elif l == 9:
                loop9_decision_2 = loop9_status_2 = 134
                deploy_request_2 = 1
                if crash_priority_2 != 192:
                    crash_priority_2 = 144
            elif l == 10:
                loop10_decision_2 = loop10_status_2 = 134
                deploy_request_2 = 1
                if crash_priority_2 != 192:
                    crash_priority_2 = 144
            elif l == 11:
                loop11_decision_2 = loop11_status_2 = 134
                deploy_request_2 = 1
                if crash_priority_2 != 192:
                    crash_priority_2 = 144
        if edr2_crash_type == 2064:
            loop0_status_2 = 0
            loop1_status_2 = 0
            loop2_status_2 = 0
            loop3_status_2 = 0
            loop4_status_2 = 0
            loop5_status_2 = 0
            loop6_status_2 = 0
            loop7_status_2 = 0
            loop8_status_2 = 0
            loop9_status_2 = 0
            loop10_status_2 = 0
            loop11_status_2 = 0
            deploy_request_2 = 0
            crash_priority_2 = 4
        # edr2 algo end time
        algo_end_time_2 = 0
        for i in range(edr2_continue_time * 2):
            # print(abs(int(edr2_ctx[i])))
            if (abs(int(edr2_ctx[i])) < 50) and (abs(int(edr2_cty[i])) < 50) and (abs(int(edr2_frsul[i])) < 50) and (
                    abs(int(edr2_frsur[i])) < 50) and (abs(int(edr2_srsul[i])) < 50) and (abs(int(edr2_srsur[i])) < 50):
                algo_end_time_2 = algo_end_time_2 + 1
            else:
                algo_end_time_2 = 0
            if algo_end_time_2 > 80:
                algo_end_time_2 = int(i)
                break

    # confirm EDR3 Event
    edr3_event = global_data[global_data[want_column] == 'RstEdr_GlobalEventInfo.au32LifeTimeEventNb._2_']
    edr3_event_index = edr3_event.index.tolist()
    edr3_event_index = edr3_event_index[0]
    edr3_event_no = edr3_event.loc[[edr3_event_index], [actual_result]]
    edr3_event_no = np.array(edr3_event_no)
    edr3_event_no = edr3_event_no.tolist()
    edr3_event_no = edr3_event_no[0][0]
    edr3_event_no = int(edr3_event_no, 16)
    if edr3_event_no != 0:
        buffer_number = buffer_number + 1
        edr3_start_time = case_start_time[str(edr3_event_no)]
        edr3_deploy_loop = case_deploy[str(edr3_event_no)]
        edr3_continue_time = case_continue_time[str(edr3_event_no)]
        time_between_3 = 65535
        if edr3_event_no != 1:
            last_event_time_3 = case_start_time[str(edr3_event_no - 1)]
            if int(edr3_start_time) - int(last_event_time_3) < 5000:
                time_between_3 = int(edr3_start_time) - int(last_event_time_3)
                time_between_3 = (time_between_3) * 2

        if edr3_continue_time >= 300:
            edr3_continue_time = 300
        # print(edr3_start_time+'|'+str(edr3_deploy_loop)+'|'+str(edr3_continue_time))

        # confirm EDR3 Type
        edr3_ctx = []
        edr3_cty = []
        edr3_frsul = []
        edr3_frsur = []
        edr3_srsul = []
        edr3_srsur = []
        expect_ac_x_3 = []
        expect_ac_y_3 = []
        expect_ac_frsul_3 = []
        expect_ac_frsur_3 = []
        expect_ac_srsul_3 = []
        expect_ac_srsur_3 = []

        for i in range(300 * 2):
            edr3_ctx.append((ctx_value[(int(edr3_start_time) * 2 + i)].strip('\n').strip(' ')))
            edr3_cty.append((cty_value[(int(edr3_start_time) * 2 + i)].strip('\n').strip(' ')))
            edr3_frsul.append((frsuL_value[(int(edr3_start_time) * 2 + i)].strip('\n').strip(' ')))
            edr3_frsur.append((frsuR_value[(int(edr3_start_time) * 2 + i)].strip('\n').strip(' ')))
            edr3_srsul.append((srsuL_value[(int(edr3_start_time) * 2 + i)].strip('\n').strip(' ')))
            edr3_srsur.append((srsuR_value[(int(edr3_start_time) * 2 + i)].strip('\n').strip(' ')))
        if int(edr3_ctx[0]) >= 100 and (int(edr3_frsul[0]) >= 100 or int(edr3_frsur[0]) >= 100):
            edr3_crash_type = 258
            edr3_algo_type = 2
            # print(len(edr3_ctx))
            for i in range(300 * 2):
                expect_ac_x_3.append(int(edr3_ctx[i]) * (-4))
                expect_ac_y_3.append(int(edr3_cty[i]) * (-4))
                expect_ac_frsul_3.append(int(edr3_frsul[i]) * (-64))
                expect_ac_frsur_3.append(int(edr3_frsur[i]) * (-64))
                expect_ac_srsul_3.append(int(edr3_srsul[i]) * (-32))
                expect_ac_srsur_3.append(int(edr3_srsur[i]) * (-32))
            # print(expect_ac_x_3)
            # print(expect_ac_y_3)
            # print(expect_ac_frsul_3)
            # print(expect_ac_frsur_3)
            # print(expect_ac_srsul_3)
            # print(expect_ac_srsur_3)

        elif int(edr3_ctx[0]) <= -150 and (int(edr3_frsul[0]) <= -150 or int(edr3_frsur[0]) <= -150):
            edr3_crash_type = 2064
            edr3_algo_type = 32
            for i in range(300 * 2):
                expect_ac_x_3.append(int(edr3_ctx[i]) * (-4))
                expect_ac_y_3.append(int(edr3_cty[i]) * (-4))
                expect_ac_frsul_3.append(int(edr3_frsul[i]) * (-64))
                expect_ac_frsur_3.append(int(edr3_frsur[i]) * (-64))
                expect_ac_srsul_3.append(int(edr3_srsul[i]) * (-32))
                expect_ac_srsur_3.append(int(edr3_srsur[i]) * (-32))

        elif int(edr3_cty[0]) <= -100 and int(edr3_srsul[0]) >= 100:
            edr3_crash_type = 516
            edr3_algo_type = 4
            for i in range(300 * 2):
                expect_ac_x_3.append(int(edr3_ctx[i]) * (-4))
                expect_ac_y_3.append(int(edr3_cty[i]) * 4)
                expect_ac_frsul_3.append(int(edr3_frsul[i]) * (-64))
                expect_ac_frsur_3.append(int(edr3_frsur[i]) * (-64))
                expect_ac_srsul_3.append(int(edr3_srsul[i]) * (-32))
                expect_ac_srsur_3.append(int(edr3_srsur[i]) * 32)

        elif int(edr3_cty[0]) >= 100 and int(edr3_srsur[0]) >= 100:
            edr3_crash_type = 1032
            edr3_algo_type = 8
            for i in range(300 * 2):
                expect_ac_x_3.append(int(edr3_ctx[i]) * 4)
                expect_ac_y_3.append(int(edr3_cty[i]) * 4)
                expect_ac_frsul_3.append(int(edr3_frsul[i]) * 64)
                expect_ac_frsur_3.append(int(edr3_frsur[i]) * 64)
                expect_ac_srsul_3.append(int(edr3_srsul[i]) * (-32))
                expect_ac_srsur_3.append(int(edr3_srsur[i]) * 32)
        else:
            edr3_crash_type = 0
            edr3_algo_type = 0
            if int(edr3_ctx[0]) > 0 and (int(edr3_frsul[0]) > 0 or int(edr3_frsur[0]) > 0):
                for i in range(300 * 2):
                    expect_ac_x_3.append(int(edr3_ctx[i]) * (-4))
                    expect_ac_y_3.append(int(edr3_cty[i]) * (-4))
                    expect_ac_frsul_3.append(int(edr3_frsul[i]) * (-64))
                    expect_ac_frsur_3.append(int(edr3_frsur[i]) * (-64))
                    expect_ac_srsul_3.append(int(edr3_srsul[i]) * (-32))
                    expect_ac_srsur_3.append(int(edr3_srsur[i]) * (-32))

            elif int(edr3_ctx[0]) < 0 and (int(edr3_frsul[0]) < 0 or int(edr3_frsur[0]) < 0):
                for i in range(300 * 2):
                    expect_ac_x_3.append(int(edr3_ctx[i]) * (-4))
                    expect_ac_y_3.append(int(edr3_cty[i]) * (-4))
                    expect_ac_frsul_3.append(int(edr3_frsul[i]) * (-64))
                    expect_ac_frsur_3.append(int(edr3_frsur[i]) * (-64))
                    expect_ac_srsul_3.append(int(edr3_srsul[i]) * (-32))
                    expect_ac_srsur_3.append(int(edr3_srsur[i]) * (-32))

            elif int(edr3_cty[0]) < 0 and int(edr3_srsul[0]) > 0:
                for i in range(300 * 2):
                    expect_ac_x_3.append(int(edr3_ctx[i]) * (-4))
                    expect_ac_y_3.append(int(edr3_cty[i]) * 4)
                    expect_ac_frsul_3.append(int(edr3_frsul[i]) * (-64))
                    expect_ac_frsur_3.append(int(edr3_frsur[i]) * (-64))
                    expect_ac_srsul_3.append(int(edr3_srsul[i]) * (-32))
                    expect_ac_srsur_3.append(int(edr3_srsur[i]) * 32)

            elif int(edr3_cty[0]) > 0 and int(edr3_srsur[0]) > 0:
                for i in range(300 * 2):
                    expect_ac_x_3.append(int(edr3_ctx[i]) * (-4))
                    expect_ac_y_3.append(int(edr3_cty[i]) * 4)
                    expect_ac_frsul_3.append(int(edr3_frsul[i]) * (-64))
                    expect_ac_frsur_3.append(int(edr3_frsur[i]) * (-64))
                    expect_ac_srsul_3.append(int(edr3_srsul[i]) * (-32))
                    expect_ac_srsur_3.append(int(edr3_srsur[i]) * 32)

            else:
                for i in range(300 * 2):
                    expect_ac_x_3.append(int(edr3_ctx[i]) * 4)
                    expect_ac_y_3.append(int(edr3_cty[i]) * (-4))
                    expect_ac_frsul_3.append(int(edr3_frsul[i]) * 64)
                    expect_ac_frsur_3.append(int(edr3_frsur[i]) * 64)
                    expect_ac_srsul_3.append(int(edr3_srsul[i]) * (-32))
                    expect_ac_srsur_3.append(int(edr3_srsur[i]) * 32)
        # print(edr3_algo_type)
        max_ctx_3 = max(expect_ac_x_3)
        min_ctx_3 = min(expect_ac_x_3)
        if abs(max_ctx_3) >= abs(min_ctx_3):
            max_ctx_ac_3 = max_ctx_3
        else:
            max_ctx_ac_3 = min_ctx_3
        max_cty_3 = max(expect_ac_y_3)
        min_cty_3 = min(expect_ac_y_3)
        if abs(max_cty_3) >= abs(min_cty_3):
            max_cty_ac_3 = max_cty_3
        else:
            max_cty_ac_3 = min_cty_3
        max_ctx_time_3 = expect_ac_x_3.index(max_ctx_ac_3)
        max_cty_time_3 = expect_ac_y_3.index(max_cty_ac_3)

        # edr3 algo start time
        expect_front_algo_3 = 32766
        expect_sidel_algo_3 = 32766
        expect_sider_algo_3 = 32766
        expect_rear_algo_3 = 32766
        if int(edr3_ctx[0]) > 50:
            expect_front_algo_3 = 0
        if int(edr3_cty[0]) < -50:
            expect_sidel_algo_3 = 0
        if int(edr3_cty[0]) > 50:
            expect_sider_algo_3 = 0
        if int(edr3_ctx[0]) < -50:
            expect_rear_algo_3 = 0

        # edr3 deploy loop
        loop0_decision_3 = loop0_status_3 = 0
        loop1_decision_3 = loop1_status_3 = 0
        loop2_decision_3 = loop2_status_3 = 0
        loop3_decision_3 = loop3_status_3 = 0
        loop4_decision_3 = loop4_status_3 = 0
        loop5_decision_3 = loop5_status_3 = 0
        loop6_decision_3 = loop6_status_3 = 0
        loop7_decision_3 = loop7_status_3 = 0
        loop8_decision_3 = loop8_status_3 = 0
        loop9_decision_3 = loop9_status_3 = 0
        loop10_decision_3 = loop10_status_3 = 0
        loop11_decision_3 = loop11_status_3 = 0
        deploy_request_3 = 0
        crash_priority_3 = 1
        for l in edr3_deploy_loop:
            if l == 0:
                loop0_decision_3 = loop0_status_3 = 134
                deploy_request_3 = 1
                crash_priority_3 = 192
            elif l == 1:
                loop1_decision_3 = loop1_status_3 = 134
                deploy_request_3 = 1
                crash_priority_3 = 192
            elif l == 2:
                loop2_decision_3 = loop2_status_3 = 134
                deploy_request_3 = 1
                crash_priority_3 = 192
            elif l == 3:
                loop3_decision_3 = loop3_status_3 = 134
                deploy_request_3 = 1
                crash_priority_3 = 192
            elif l == 4:
                loop4_decision_3 = loop4_status_3 = 134
                deploy_request_3 = 1
                if crash_priority_3 != 192:
                    crash_priority_3 = 144
            elif l == 5:
                loop5_decision_3 = loop5_status_3 = 134
                deploy_request_3 = 1
                crash_priority_3 = 192
            elif l == 6:
                loop6_decision_3 = loop6_status_3 = 134
                deploy_request_3 = 1
                crash_priority_3 = 192
            elif l == 7:
                loop7_decision_3 = loop7_status_3 = 134
                deploy_request_3 = 1
                if crash_priority_3 != 192:
                    crash_priority_3 = 144
            elif l == 8:
                loop8_decision_3 = loop8_status_3 = 134
                deploy_request_3 = 1
                if crash_priority_3 != 192:
                    crash_priority_3 = 144
            elif l == 9:
                loop9_decision_3 = loop9_status_3 = 134
                deploy_request_3 = 1
                if crash_priority_3 != 192:
                    crash_priority_3 = 144
            elif l == 10:
                loop10_decision_3 = loop10_status_3 = 134
                deploy_request_3 = 1
                if crash_priority_3 != 192:
                    crash_priority_3 = 144
            elif l == 11:
                loop11_decision_3 = loop11_status_3 = 134
                deploy_request_3 = 1
                if crash_priority_3 != 192:
                    crash_priority_3 = 144

        if edr3_crash_type == 2064:
            loop0_status_3 = 0
            loop1_status_3 = 0
            loop2_status_3 = 0
            loop3_status_3 = 0
            loop4_status_3 = 0
            loop5_status_3 = 0
            loop6_status_3 = 0
            loop7_status_3 = 0
            loop8_status_3 = 0
            loop9_status_3 = 0
            loop10_status_3 = 0
            loop11_status_3 = 0
            deploy_request_3 = 0
            crash_priority_3 = 4

        # edr3 algo end time
        algo_end_time_3 = 0
        for i in range(edr3_continue_time * 2):
            # print(abs(int(edr3_ctx[i])))
            if (abs(int(edr3_ctx[i])) < 50) and (abs(int(edr3_cty[i])) < 50) and (abs(int(edr3_frsul[i])) < 50) and (
                    abs(int(edr3_frsur[i])) < 50) and (abs(int(edr3_srsul[i])) < 50) and (abs(int(edr3_srsur[i])) < 50):
                algo_end_time_3 = algo_end_time_3 + 1
            else:
                algo_end_time_3 = 0
            if algo_end_time_3 > 80:
                algo_end_time_3 = int(i)
                break

    filename = path.split('/')
    save_name = filename[4]
    Check_result_path = "C://Project/GAC_A39/EDR_Test_logs/EDR_Check_Result/"
    Result_Analyze = Check_result_path + save_name
    Result_writer = pd.ExcelWriter(Result_Analyze)

    # save global data
    global_data.to_excel(Result_writer, 'global_data')

    for k in range(buffer_number):
        # print(k)
        current_edr = ('EDR' + str(k + 1)).strip()
        print("checking_" + current_edr)
        Acct_data = pd.read_excel(path, current_edr)
        Acct_data = pd.DataFrame(Acct_data, columns=['PARAMETER NAME', 'READ VALUE', 'Expect', 'Judge'])
        desired_width = 5000
        pd.set_option('display.width', desired_width)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        pd.set_option('max_colwidth', 200)

        # algo end time from nvm
        algo_end_nvm = 'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u16AlgoEndTime'
        algo_end_nvm = Acct_data[Acct_data[want_column] == algo_end_nvm]
        algo_end_index_1 = algo_end_nvm.index.tolist()
        algo_end_index_1 = algo_end_index_1[0]
        algo_end_nvm = algo_end_nvm.loc[[algo_end_index_1], [actual_result]]
        algo_end_nvm = np.array(algo_end_nvm)
        algo_end_nvm = algo_end_nvm.tolist()
        algo_end_nvm = algo_end_nvm[0][0]
        algo_end_nvm = int(algo_end_nvm, 16)
        algo_end_expect = 0
        # print(algo_end_nvm)
        table_end = algo_end_nvm + 80
        if table_end >= 620:
            table_end = 620
        dv_end = algo_end_nvm + 80
        if dv_end >= 520:
            dv_end = 520
        max_dv_end = algo_end_nvm + 60
        if max_dv_end >= 600:
            max_dv_end = 600
        if abs((locals()['algo_end_time_' + str(k + 1)]) - algo_end_nvm) <= 4:
            algo_end_expect = algo_end_nvm

        # caculate dv
        offset_time_10ms = 'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.u8EDROffsetTime10ms'
        offset_time_10ms = Acct_data[Acct_data[want_column] == offset_time_10ms]
        offset_time_index = offset_time_10ms.index.tolist()
        offset_time_index = offset_time_index[0]
        offset_time_10ms = offset_time_10ms.loc[[offset_time_index], [actual_result]]
        offset_time_10ms = np.array(offset_time_10ms)
        offset_time_10ms = offset_time_10ms.tolist()
        offset_time_10ms = offset_time_10ms[0][0]
        offset_time_10ms = int(offset_time_10ms, 16)
        dv_offset = offset_time_10ms + 1

        actual_ctx_max_dv = 'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._6_.s16Data'
        actual_ctx_max_dv = Acct_data[Acct_data[want_column] == actual_ctx_max_dv]
        ctx_max_dv_index = actual_ctx_max_dv.index.tolist()
        ctx_max_dv_index = ctx_max_dv_index[0]
        actual_ctx_max_dv = actual_ctx_max_dv.loc[[ctx_max_dv_index], [actual_result]]
        actual_ctx_max_dv = np.array(actual_ctx_max_dv)
        actual_ctx_max_dv = actual_ctx_max_dv.tolist()
        actual_ctx_max_dv = actual_ctx_max_dv[0][0]
        actual_ctx_max_dv = int(actual_ctx_max_dv, 16)
        if actual_ctx_max_dv > 32767:
            actual_ctx_max_dv = actual_ctx_max_dv - 65535

        actual_cty_max_dv = 'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._6_.s16Data'
        actual_cty_max_dv = Acct_data[Acct_data[want_column] == actual_cty_max_dv]
        cty_max_dv_index = actual_cty_max_dv.index.tolist()
        cty_max_dv_index = cty_max_dv_index[0]
        actual_cty_max_dv = actual_cty_max_dv.loc[[cty_max_dv_index], [actual_result]]
        actual_cty_max_dv = np.array(actual_cty_max_dv)
        actual_cty_max_dv = actual_cty_max_dv.tolist()
        actual_cty_max_dv = actual_cty_max_dv[0][0]
        actual_cty_max_dv = int(actual_cty_max_dv, 16)
        if actual_cty_max_dv > 32767:
            actual_cty_max_dv = actual_cty_max_dv - 65535

        ctx_dv = []
        cty_dv = []
        ctx_data = locals()['expect_ac_x_' + str(k + 1)]
        cty_data = locals()['expect_ac_y_' + str(k + 1)]
        expect_x_t0 = int(ctx_data[0] * dv_offset / 32)
        expect_y_t0 = int(cty_data[0] * dv_offset / 32)
        ctx_dv.append(expect_x_t0)
        cty_dv.append(expect_y_t0)
        dv_continue = int((algo_end_expect / 2 - 40) / 10)
        dv_keep = dv_continue + 8
        max_ctx_dv = 0
        max_cty_dv = 0
        dv_x_other = int(ctx_data[0] * 100 / 32)
        dv_y_other = int(cty_data[0] * 100 / 32)
        if abs(int(ctx_data[0] * 1 / 32)) <= abs(abs(dv_x_other) - abs(actual_ctx_max_dv)) <= abs(
                int(ctx_data[0] * 2 / 32)):
            max_ctx_dv = int(ctx_data[0] * 99)
            before_t0_x = int(ctx_data[0] * 1)
        elif abs(int(ctx_data[0] * 2 / 32)) <= abs(abs(dv_x_other) - abs(actual_ctx_max_dv)) <= abs(
                int(ctx_data[0] * 3 / 32)):
            max_ctx_dv = int(ctx_data[0] * 98)
            before_t0_x = int(ctx_data[0] * 2)
        elif abs(int(ctx_data[0] * 3 / 32)) <= abs(abs(dv_x_other) - abs(actual_ctx_max_dv)) <= abs(
                int(ctx_data[0] * 4 / 32)):
            max_ctx_dv = int(ctx_data[0] * 97)
            before_t0_x = int(ctx_data[0] * 3)
        else:
            max_ctx_dv = int(ctx_data[0] * 100)
            before_t0_x = 0

        if abs(int(cty_data[0] * 1 / 32)) <= abs(abs(dv_y_other) - abs(actual_cty_max_dv)) <= abs(
                int(cty_data[0] * 2 / 32)):
            max_cty_dv = int(cty_data[0] * 99)
            before_t0_y = int(cty_data[0] * 1)
        elif abs(int(cty_data[0] * 2 / 32)) <= abs(abs(dv_y_other) - abs(actual_cty_max_dv)) <= abs(
                int(cty_data[0] * 3 / 32)):
            max_cty_dv = int(cty_data[0] * 98)
            before_t0_y = int(cty_data[0] * 2)
        elif abs(int(cty_data[0] * 3 / 32)) <= abs(abs(dv_y_other) - abs(actual_cty_max_dv)) <= abs(
                int(cty_data[0] * 4 / 32)):
            max_cty_dv = int(cty_data[0] * 97)
            before_t0_y = int(cty_data[0] * 3)
        else:
            max_cty_dv = int(cty_data[0] * 100)
            before_t0_y = 0

        max_resultant_dv = max_ctx_dv ** 2 + max_cty_dv ** 2
        # print(max_resultant_dv)

        if dv_continue <= 25:
            for i in range(dv_continue - 1):
                dv_x_current = int(ctx_data[i + 10] * (dv_offset + (20 * (i + 1))) / 32)
                dv_y_current = int(cty_data[i + 10] * (dv_offset + (20 * (i + 1))) / 32)
                ctx_dv.append(dv_x_current)
                cty_dv.append(dv_y_current)
            for j in range(dv_keep - dv_continue):
                ctx_dv.append(dv_x_other)
                cty_dv.append(dv_y_other)
            for h in range(26 - dv_keep):
                ctx_dv.append(0)
                cty_dv.append(0)

        # max dv time
        ctx_dv_max_time = 'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.u16TimeMaxDeltaVLgt'
        ctx_dv_max_time = Acct_data[Acct_data[want_column] == ctx_dv_max_time]
        ctx_dv_max_index = ctx_dv_max_time.index.tolist()
        ctx_dv_max_index = ctx_dv_max_index[0]
        ctx_dv_max_time = ctx_dv_max_time.loc[[ctx_dv_max_index], [actual_result]]
        ctx_dv_max_time = np.array(ctx_dv_max_time)
        ctx_dv_max_time = ctx_dv_max_time.tolist()
        ctx_dv_max_time = ctx_dv_max_time[0][0]
        ctx_dv_max_time = int(ctx_dv_max_time, 16)

        cty_dv_max_time = 'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.u16TimeMaxDeltaVLat'
        cty_dv_max_time = Acct_data[Acct_data[want_column] == cty_dv_max_time]
        cty_dv_max_index = cty_dv_max_time.index.tolist()
        cty_dv_max_index = cty_dv_max_index[0]
        cty_dv_max_time = cty_dv_max_time.loc[[cty_dv_max_index], [actual_result]]
        cty_dv_max_time = np.array(cty_dv_max_time)
        cty_dv_max_time = cty_dv_max_time.tolist()
        cty_dv_max_time = cty_dv_max_time[0][0]
        cty_dv_max_time = int(cty_dv_max_time, 16)

        if ctx_dv_max_time >= cty_dv_max_time:
            max_resultant_time = ctx_dv_max_time
        else:
            max_resultant_time = cty_dv_max_time

        my_check_list_always_0 = [
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.s32IgnDownload',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u32Latitude',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u32Longitude',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._3_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._4_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._5_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._6_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._7_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._8_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._9_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._10_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._11_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._12_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._13_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._14_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._15_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._16_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._17_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._18_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._19_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._20_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._21_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._22_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._23_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._24_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._25_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._26_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._27_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._28_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._29_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._30_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._31_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._32_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._33_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._34_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._35_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._36_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._37_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._38_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._39_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._40_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._41_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._42_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._43_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._44_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._45_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._46_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._47_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._48_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._49_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.aVehRollRate._50_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u8PADIState',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._3_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._4_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._5_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._6_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._7_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._8_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._9_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._10_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._11_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._12_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._13_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._14_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._15_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._16_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._17_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._18_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._19_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._20_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._21_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._22_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._23_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._24_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._25_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._26_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._27_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._28_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._29_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._30_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._31_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._32_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._33_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._34_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._35_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._36_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._37_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._38_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._39_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._40_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._41_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._42_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._43_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._44_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._45_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._46_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._47_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._48_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._49_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._50_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._51_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._52_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._53_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._54_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._55_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._56_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._57_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._58_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._59_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._60_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._61_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._62_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._63_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._64_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._65_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._66_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._67_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._68_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._69_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._70_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._71_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._72_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._73_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._74_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._75_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._76_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._77_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._78_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._79_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._80_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._81_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._82_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._83_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._84_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._85_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._86_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._87_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._88_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._89_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._90_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._91_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._92_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._93_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._94_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._95_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._96_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._97_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._98_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._99_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._100_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._101_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._102_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._103_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._104_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._105_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._106_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._107_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._108_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._109_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._110_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._111_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._112_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._113_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._114_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._115_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._116_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._117_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._118_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._119_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._120_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._121_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._122_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._123_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._124_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._125_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._126_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._127_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._128_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._129_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._130_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._131_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._132_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._133_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._134_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._135_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._136_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._137_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._138_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._139_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._140_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._141_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._142_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._143_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._144_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._145_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._146_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._147_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._148_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._149_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._150_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._151_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._152_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._153_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._154_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._155_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._156_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._157_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._158_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._159_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._160_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._161_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._162_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._163_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._164_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._165_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._166_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._167_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._168_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._169_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._170_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._171_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._172_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._173_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._174_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._175_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._176_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._177_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._178_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._179_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._180_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._181_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._182_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._183_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._184_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._185_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._186_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._187_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._188_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._189_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._190_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._191_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._192_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._193_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._194_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._195_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._196_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._197_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._198_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._199_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._200_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._201_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._202_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._203_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._204_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._205_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._206_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._207_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._208_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._209_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._210_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._211_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._212_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._213_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._214_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._215_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._216_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._217_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._218_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._219_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._220_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._221_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._222_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._223_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._224_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._225_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._226_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._227_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._228_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._229_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._230_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._231_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._232_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._233_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._234_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._235_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._236_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._237_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._238_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._239_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._240_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._241_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._242_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._243_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._244_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._245_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._246_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._247_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._248_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._249_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelVetRecordDataElement.aAccelVet._250_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._3_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._4_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._5_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._6_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._7_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._8_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._9_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._10_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._11_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._12_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._13_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._14_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._15_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._16_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._17_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._18_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._19_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._20_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._21_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._22_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._23_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._24_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._25_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._26_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._27_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._28_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._29_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._30_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._31_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._32_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._33_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._34_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._35_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._36_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._37_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._38_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._39_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._40_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._41_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._42_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._43_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._44_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._45_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._46_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._47_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._48_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._49_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._50_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._51_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._52_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._53_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._54_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._55_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._56_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._57_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._58_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._59_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._60_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._61_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._62_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._63_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._64_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._65_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._66_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._67_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._68_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._69_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._70_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._71_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._72_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._73_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._74_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._75_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._76_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._77_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._78_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._79_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._4_._80_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._3_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._4_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._5_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._6_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._7_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._8_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._9_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._10_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._11_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._12_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._13_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._14_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._15_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._16_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._17_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._18_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._19_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._20_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._21_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._22_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._23_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._24_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._25_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._26_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._27_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._28_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._29_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._30_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._31_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._32_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._33_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._34_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._35_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._36_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._37_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._38_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._39_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._40_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._41_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._42_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._43_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._44_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._45_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._46_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._47_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._48_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._49_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._50_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._51_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._52_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._53_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._54_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._55_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._56_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._57_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._58_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._59_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._60_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._61_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._62_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._63_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._64_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._65_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._66_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._67_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._68_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._69_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._70_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._71_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._72_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._73_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._74_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._75_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._76_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._77_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._78_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._79_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._5_._80_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._3_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._4_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._5_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._6_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._7_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._8_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._9_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._10_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._11_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._12_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._13_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._14_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._15_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._16_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._17_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._18_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._19_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._20_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._21_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._22_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._23_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._24_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._25_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._26_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._27_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._28_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._29_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._30_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._31_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._32_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._33_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._34_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._35_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._36_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._37_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._38_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._39_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelVet._40_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._4_._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._4_._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._4_._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._4_._3_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._4_._4_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._4_._5_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._4_._6_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._4_._7_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._4_._8_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._4_._9_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._4_._10_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._4_._11_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._4_._12_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._4_._13_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._4_._14_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._4_._15_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._4_._16_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._4_._17_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._4_._18_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._4_._19_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._4_._20_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._5_._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._5_._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._5_._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._5_._3_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._5_._4_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._5_._5_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._5_._6_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._5_._7_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._5_._8_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._5_._9_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._5_._10_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._5_._11_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._5_._12_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._5_._13_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._5_._14_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._5_._15_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._5_._16_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._5_._17_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._5_._18_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._5_._19_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._5_._20_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aVehRollRate._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aVehRollRate._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aVehRollRate._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aVehRollRate._3_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aVehRollRate._4_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aVehRollRate._5_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aVehRollRate._6_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aVehRollRate._7_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aVehRollRate._8_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aVehRollRate._9_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aVehRollRate._10_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aBrakeOverrideState._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aBrakeOverrideState._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aBrakeOverrideState._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aBrakeOverrideState._3_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aBrakeOverrideState._4_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aBrakeOverrideState._5_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aBrakeOverrideState._6_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aBrakeOverrideState._7_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aBrakeOverrideState._8_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aBrakeOverrideState._9_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aBrakeOverrideState._10_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehRollAgl._0_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehRollAgl._0_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehRollAgl._1_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehRollAgl._1_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehRollAgl._2_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehRollAgl._2_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehRollAgl._3_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehRollAgl._3_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehRollAgl._4_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehRollAgl._4_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehRollAgl._5_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehRollAgl._5_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehRollAgl._6_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehRollAgl._6_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehRollAgl._7_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehRollAgl._7_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehRollAgl._8_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehRollAgl._8_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehRollAgl._9_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehRollAgl._9_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehRollAgl._10_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehRollAgl._10_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._0_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._1_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._2_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._3_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._4_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._5_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._6_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._7_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._8_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._9_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._10_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._11_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._12_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._13_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._14_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._15_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._16_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._17_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._18_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._19_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._20_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._21_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._22_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._23_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._24_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._25_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._0_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._1_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._2_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._3_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._4_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._5_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._6_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._7_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._8_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._9_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._10_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._11_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._12_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._13_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._14_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._15_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._16_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._17_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._18_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._19_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._20_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._21_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._22_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._23_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._24_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._25_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.DeployConfirmation.DeployConfirmationRawData._12_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.DeployConfirmation.DeployConfirmationRawData._13_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.DeployConfirmation.DeployConfirmationRawData._14_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.DeployConfirmation.DeployConfirmationRawData._15_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.DeployConfirmation.DeployConfirmationRawData._16_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.DeployConfirmation.DeployConfirmationRawData._17_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.DeployConfirmation.DeployConfirmationRawData._18_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.DeployConfirmation.DeployConfirmationRawData._19_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.DeployConfirmation.DeployConfirmationRawData._20_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.DeployConfirmation.DeployConfirmationRawData._21_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.DeployConfirmation.DeployConfirmationRawData._22_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.DeployConfirmation.DeployConfirmationRawData._23_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.DeployConfirmation.DeployConfirmationRawData._24_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.DeployConfirmation.DeployConfirmationRawData._25_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.DeployConfirmation.DeployConfirmationRawData._26_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.DeployConfirmation.DeployConfirmationRawData._27_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.DeployConfirmation.DeployConfirmationRawData._28_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.DeployConfirmation.DeployConfirmationRawData._29_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.DeployConfirmation.DeployConfirmationRawData._30_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.DeployConfirmation.DeployConfirmationRawData._31_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.RollOverDisableSwitchLatched',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._0_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._0_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._1_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._1_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._2_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._2_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._3_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._3_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._4_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._4_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._5_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._5_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._6_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._6_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._7_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._7_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._8_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._8_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._9_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._9_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._10_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._10_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._11_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._11_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._12_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._12_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._13_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._13_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._14_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._14_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._15_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._15_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._16_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._16_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._17_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._17_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._18_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._18_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._19_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._19_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._20_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._20_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._21_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._21_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._22_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._22_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._23_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._23_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._24_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._24_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._25_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._25_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._26_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._26_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._27_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._27_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._28_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._28_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._29_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._29_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._30_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._30_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._31_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._31_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._32_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._32_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._33_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._33_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._34_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._34_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._35_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._35_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._36_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._36_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._37_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._37_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._38_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._38_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._39_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._39_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._40_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._40_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._41_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._41_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._42_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._42_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._43_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._43_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._44_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._44_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._45_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._45_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._46_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._46_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._47_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._47_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._48_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._48_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._49_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._49_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._50_.s16Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aVehRollAgl._50_.u8InvalidityCnt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.s32AdjustRollAngle'
        ]

        my_check_list_default_0 = [
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u32Odometer',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.VehSpdLgtAtTimeZero.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u8EventHour',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u8EventMinute',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u8TirePressureWarningState',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aStabilityCrl._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aStabilityCrl._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aStabilityCrl._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aStabilityCrl._3_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aStabilityCrl._4_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aStabilityCrl._5_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aStabilityCrl._6_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aStabilityCrl._7_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aStabilityCrl._8_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aStabilityCrl._9_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aStabilityCrl._10_',

            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aTractionControlState._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aTractionControlState._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aTractionControlState._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aTractionControlState._3_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aTractionControlState._4_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aTractionControlState._5_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aTractionControlState._6_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aTractionControlState._7_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aTractionControlState._8_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aTractionControlState._9_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aTractionControlState._10_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAbsCtrlActv._0_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAbsCtrlActv._1_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAbsCtrlActv._2_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAbsCtrlActv._3_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAbsCtrlActv._4_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAbsCtrlActv._5_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAbsCtrlActv._6_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAbsCtrlActv._7_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAbsCtrlActv._8_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAbsCtrlActv._9_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAbsCtrlActv._10_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aCurrentGearPosition._0_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aCurrentGearPosition._1_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aCurrentGearPosition._2_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aCurrentGearPosition._3_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aCurrentGearPosition._4_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aCurrentGearPosition._5_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aCurrentGearPosition._6_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aCurrentGearPosition._7_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aCurrentGearPosition._8_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aCurrentGearPosition._9_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aCurrentGearPosition._10_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aDirectionIndicatorState._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aDirectionIndicatorState._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aDirectionIndicatorState._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aDirectionIndicatorState._3_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aDirectionIndicatorState._4_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aDirectionIndicatorState._5_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aDirectionIndicatorState._6_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aDirectionIndicatorState._7_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aDirectionIndicatorState._8_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aDirectionIndicatorState._9_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aDirectionIndicatorState._10_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aEngThrtRate._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aEngThrtRate._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aEngThrtRate._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aEngThrtRate._3_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aEngThrtRate._4_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aEngThrtRate._5_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aEngThrtRate._6_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aEngThrtRate._7_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aEngThrtRate._8_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aEngThrtRate._9_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aEngThrtRate._10_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aBrkPelRat._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aBrkPelRat._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aBrkPelRat._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aBrkPelRat._3_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aBrkPelRat._4_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aBrkPelRat._5_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aBrkPelRat._6_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aBrkPelRat._7_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aBrkPelRat._8_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aBrkPelRat._9_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aBrkPelRat._10_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aHeadlightsstate._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aHeadlightsstate._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aHeadlightsstate._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aHeadlightsstate._3_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aHeadlightsstate._4_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aHeadlightsstate._5_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aHeadlightsstate._6_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aHeadlightsstate._7_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aHeadlightsstate._8_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aHeadlightsstate._9_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aHeadlightsstate._10_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehSpdLgt._0_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehSpdLgt._1_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehSpdLgt._2_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehSpdLgt._3_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehSpdLgt._4_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehSpdLgt._5_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehSpdLgt._6_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehSpdLgt._7_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehSpdLgt._8_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehSpdLgt._9_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehSpdLgt._10_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aEngN._0_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aEngN._1_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aEngN._2_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aEngN._3_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aEngN._4_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aEngN._5_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aEngN._6_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aEngN._7_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aEngN._8_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aEngN._9_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aEngN._10_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAccrPedlRat._0_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAccrPedlRat._0_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAccrPedlRat._1_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAccrPedlRat._1_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAccrPedlRat._2_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAccrPedlRat._2_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAccrPedlRat._3_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAccrPedlRat._3_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAccrPedlRat._4_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAccrPedlRat._4_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAccrPedlRat._5_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAccrPedlRat._5_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAccrPedlRat._6_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAccrPedlRat._6_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAccrPedlRat._7_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAccrPedlRat._7_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAccrPedlRat._8_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAccrPedlRat._8_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAccrPedlRat._9_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAccrPedlRat._9_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAccrPedlRat._10_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAccrPedlRat._10_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.BltLockStateDriver',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.BltLockStateFPsngr',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.CuttoffSwitchFPsngr',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.BeltLockStAtRowFirstMidLatched',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.BeltLockStAtRowSecLeftLatched',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.BeltLockStAtRowSecRightLatched',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.BeltLockStAtRowSecMidLatched',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.EncodedActFlts.au32EncodedActFlts._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.EncodedActFlts.au32EncodedActFlts._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.EncodedActFlts.au32EncodedActFlts._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.EncodedActFlts.au32EncodedActFlts._3_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.EncodedActFlts.au32EncodedActFlts._4_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.EncodedActFlts.au32EncodedActFlts._5_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.EncodedActFlts.au32EncodedActFlts._6_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.EncodedActFlts.au32EncodedActFlts._7_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.EncodedActFlts.au32EncodedActFlts._8_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.EncodedActFlts.au32EncodedActFlts._9_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.EncodedActFlts.au32EncodedActFlts._10_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.EncodedActFlts.au32EncodedActFlts._11_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.EncodedActFlts.au32EncodedActFlts._12_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.EncodedActFlts.au32EncodedActFlts._13_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.EncodedActFlts.au32EncodedActFlts._14_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.EncodedActFlts.au32EncodedActFlts._15_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.EncodedActFlts.au32EncodedActFlts._16_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.EncodedActFlts.au32EncodedActFlts._17_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.EncodedActFlts.au32EncodedActFlts._18_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.EncodedActFlts.au32EncodedActFlts._19_'
        ]

        my_check_list_default_1 = [
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.VehSpdLgtAtTimeZero.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.BrkPedValAtTimeZero.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.BrkPedValAtTimeZero.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u8IgnCycleKeyOn',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u8EventMonth',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u8EventDate',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u8EventSecond',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u8BrakeAlarmStatus',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAEBState._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAEBState._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAEBState._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAEBState._3_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAEBState._4_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAEBState._5_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAEBState._6_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAEBState._7_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAEBState._8_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAEBState._9_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAEBState._10_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aPinionSteerAg._0_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aPinionSteerAg._1_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aPinionSteerAg._2_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aPinionSteerAg._3_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aPinionSteerAg._4_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aPinionSteerAg._5_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aPinionSteerAg._6_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aPinionSteerAg._7_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aPinionSteerAg._8_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aPinionSteerAg._9_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aPinionSteerAg._10_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAbsCtrlActv._0_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAbsCtrlActv._1_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAbsCtrlActv._2_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAbsCtrlActv._3_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAbsCtrlActv._4_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAbsCtrlActv._5_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAbsCtrlActv._6_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAbsCtrlActv._7_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAbsCtrlActv._8_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAbsCtrlActv._9_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aAbsCtrlActv._10_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehSpdLgt._0_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehSpdLgt._1_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehSpdLgt._2_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehSpdLgt._3_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehSpdLgt._4_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehSpdLgt._5_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehSpdLgt._6_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehSpdLgt._7_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehSpdLgt._8_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehSpdLgt._9_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aVehSpdLgt._10_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aBrkPedVal._0_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aBrkPedVal._0_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aBrkPedVal._1_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aBrkPedVal._1_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aBrkPedVal._2_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aBrkPedVal._2_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aBrkPedVal._3_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aBrkPedVal._3_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aBrkPedVal._4_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aBrkPedVal._4_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aBrkPedVal._5_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aBrkPedVal._5_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aBrkPedVal._6_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aBrkPedVal._6_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aBrkPedVal._7_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aBrkPedVal._7_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aBrkPedVal._8_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aBrkPedVal._8_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aBrkPedVal._9_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aBrkPedVal._9_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aBrkPedVal._10_.Data',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aBrkPedVal._10_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aEngN._0_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aEngN._1_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aEngN._2_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aEngN._3_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aEngN._4_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aEngN._5_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aEngN._6_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aEngN._7_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aEngN._8_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aEngN._9_.Qf',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aEngN._10_.Qf']

        my_check_list_default_2 = [
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aACCState._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aACCState._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aACCState._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aACCState._3_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aACCState._4_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aACCState._5_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aACCState._6_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aACCState._7_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aACCState._8_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aACCState._9_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aACCState._10_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aCruiseControlState._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aCruiseControlState._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aCruiseControlState._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aCruiseControlState._3_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aCruiseControlState._4_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aCruiseControlState._5_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aCruiseControlState._6_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aCruiseControlState._7_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aCruiseControlState._8_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aCruiseControlState._9_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aCruiseControlState._10_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aLaneDepartureSystemState._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aLaneDepartureSystemState._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aLaneDepartureSystemState._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aLaneDepartureSystemState._3_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aLaneDepartureSystemState._4_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aLaneDepartureSystemState._5_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aLaneDepartureSystemState._6_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aLaneDepartureSystemState._7_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aLaneDepartureSystemState._8_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aLaneDepartureSystemState._9_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aLaneDepartureSystemState._10_']

        my_check_list_default_3 = [
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.SeatTrackPosDrvr',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.SeatTrackPosFPsngr',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.BeltLockStAtRowThrdLeftLatched',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.BeltLockStAtRowThrdRightLatched',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.BeltLockStAtRowThrdMidLatched']

        my_check_list_default_FFFF = [
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoDeployTab._12_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoDeployTab._13_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoDeployTab._14_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoDeployTab._15_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoDeployTab._16_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoDeployTab._17_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoDeployTab._18_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoDeployTab._19_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoDeployTab._20_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoDeployTab._21_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoDeployTab._22_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoDeployTab._23_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoDeployTab._24_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoDeployTab._25_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoDeployTab._26_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoDeployTab._27_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoDeployTab._28_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoDeployTab._29_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoDeployTab._30_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoDeployTab._31_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoSendCmdTab._12_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoSendCmdTab._13_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoSendCmdTab._14_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoSendCmdTab._15_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoSendCmdTab._16_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoSendCmdTab._17_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoSendCmdTab._18_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoSendCmdTab._19_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoSendCmdTab._20_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoSendCmdTab._21_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoSendCmdTab._22_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoSendCmdTab._23_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoSendCmdTab._24_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoSendCmdTab._25_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoSendCmdTab._26_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoSendCmdTab._27_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoSendCmdTab._28_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoSendCmdTab._29_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoSendCmdTab._30_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoSendCmdTab._31_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.u16TimetoER']

        my_check_list_default_7FFE = [
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u16DelayFromEDR_T0._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u16DelayFromEDR_T0._4_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u16DelayFromEDR_T0._6_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u16DelayFromEDR_T0._7_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u16DelayFromEDR_T0._8_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u16DelayFromEDR_T0._9_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u16DelayFromEDR_T0._10_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u16DelayFromEDR_T0._11_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u16DelayFromEDR_T0._12_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u16DelayFromEDR_T0._13_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u16DelayFromEDR_T0._14_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u16DelayFromEDR_T0._15_']

        my_check_list_NA = [
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_TimeWhenInternalConfirmationMet',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_VehicleSpeed',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_TimeWhenFrsuIsFaulty',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_TimeToSeverity._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_TimeToSeverity._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_TimeToSeverity._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_CrashMgrActvTmrAtWkup',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_CrashMgrActvTmrAtRst',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_ThresholdClassAtWakeUp',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_UnconfEventCountAtWakeUp',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_XyOutputLatched',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_AngleClassLevel._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_AngleClassLevel._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_AngleClassLevel._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_EvanCr1ClassLevel._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_EvanCr1ClassLevel._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_EvanCr1ClassLevel._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_EvanCr2ClassLevel._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_EvanCr2ClassLevel._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_EvanCr2ClassLevel._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_XpecClassLevel._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_XpecClassLevel._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_XpecClassLevel._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_CentXDvClassLevel._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_CentXDvClassLevel._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_CentXDvClassLevel._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_CentXAccClassLevel._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_CentXAccClassLevel._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_CentXAccClassLevel._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_NocClassLevel._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_NocClassLevel._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_NocClassLevel._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_TocClassLevel._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_TocClassLevel._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_TocClassLevel._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_FrsuDvClassLevel._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_FrsuDvClassLevel._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_FrsuDvClassLevel._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_FrsuAccClassLevel._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_FrsuAccClassLevel._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_FrsuAccClassLevel._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_LpSpCrashLevel._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_LpSpCrashLevel._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_LpSpCrashLevel._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_LpMpCrashLevel._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_LpMpCrashLevel._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_LpMpCrashLevel._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_LpSeverity._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_LpSeverity._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_LpSeverity._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_CraftCrashLevel._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_CraftCrashLevel._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_CraftCrashLevel._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_HpSpPassengerCrashLevel._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_HpSpPassengerCrashLevel._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_HpSpPassengerCrashLevel._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_HpSpDriverCrashLevel._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_HpSpDriverCrashLevel._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_HpSpDriverCrashLevel._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_HpMpPassengerXAccLevel._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_HpMpPassengerXAccLevel._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_HpMpPassengerXAccLevel._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_HpMpDriverXAccLevel._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_HpMpDriverXAccLevel._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_HpMpDriverXAccLevel._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_HpMpPassengerFdvLevel._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_HpMpPassengerFdvLevel._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_HpMpPassengerFdvLevel._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_HpMpDriverFdvLevel._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_HpMpDriverFdvLevel._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_HpMpDriverFdvLevel._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_FinalSeverity',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_VrLevelBySp',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgInternalData.FrntInternalData.OpsFrntAlg_VrLevelByMp',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.SideLeftInternalData.OpsSideAlg_AlgorithmTime',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.SideLeftInternalData.OpsSideAlg_SeverityWord',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.SideLeftInternalData.OpsSideAlg_CrashMgrActvTmrAtWkup',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.SideLeftInternalData.OpsSideAlg_CrashMgrActvTmrAtRst',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgInternalData.SideLeftInternalData.OpsSideAlg_LveValue',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.SideLeftInternalData.OpsSideAlg_ConfirmationLatches',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.SideLeftInternalData.OpsSideAlg_ConfirmationTime',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.SideLeftInternalData.OpsSideAlg_SensorFaultAtDecision',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.SideLeftInternalData.OpsSideAlg_CvAccIndex._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.SideLeftInternalData.OpsSideAlg_CvAccIndex._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.SideLeftInternalData.OpsSideAlg_CvAccIndex._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.SideLeftInternalData.OpsSideAlg_CvAccIndex._3_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.SideLeftInternalData.OpsSideAlg_CvAccIndex._4_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgInternalData.SideLeftInternalData.OpsSideAlg_NvCvMet',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.SideLeftInternalData.OpsSideAlg_UnconfEventCountAtWakeUp',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.SideLeftInternalData.OpsSideAlg_XyLatchedLevel',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.SideRightInternalData.OpsSideAlg_AlgorithmTime',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.SideRightInternalData.OpsSideAlg_SeverityWord',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.SideRightInternalData.OpsSideAlg_CrashMgrActvTmrAtWkup',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.SideRightInternalData.OpsSideAlg_CrashMgrActvTmrAtRst',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgInternalData.SideRightInternalData.OpsSideAlg_LveValue',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.SideRightInternalData.OpsSideAlg_ConfirmationLatches',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.SideRightInternalData.OpsSideAlg_ConfirmationTime',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.SideRightInternalData.OpsSideAlg_SensorFaultAtDecision',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.SideRightInternalData.OpsSideAlg_CvAccIndex._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.SideRightInternalData.OpsSideAlg_CvAccIndex._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.SideRightInternalData.OpsSideAlg_CvAccIndex._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.SideRightInternalData.OpsSideAlg_CvAccIndex._3_',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.SideRightInternalData.OpsSideAlg_CvAccIndex._4_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgInternalData.SideRightInternalData.OpsSideAlg_NvCvMet',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.SideRightInternalData.OpsSideAlg_UnconfEventCountAtWakeUp',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.SideRightInternalData.OpsSideAlg_XyLatchedLevel',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.RearInternalData.OpsReAlg_CrashMgrActvTmrAtWkup',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.RearInternalData.OpsReAlg_CrashMgrActvTmrAtRst',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgInternalData.RearInternalData.u8ConfAlgoTime',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.RearInternalData.OpsReAlg_UnconfEventCountAtWakeUp',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgInternalData.RearInternalData.u8BackupSwitchTime',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgInternalData.RearInternalData.u8CxDvLevel',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgInternalData.RearInternalData.u8CxAccLevel',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgInternalData.RearInternalData.u8DecisionMetTime',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgInternalData.RearInternalData.s8XyOutputAtDecision',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgInternalData.RollInternalData.s32MaxRollAngle',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgInternalData.RollInternalData.u32InvalidInputAtDecision',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgInternalData.RollInternalData.u32RolDecisionTime',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgInternalData.RollInternalData.u32RolConfirmationTime',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.RollInternalData.OpsRollAlg_CrashMgrActvTmrAtWkup',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.RollInternalData.OpsRollAlg_CrashMgrActvTmrAtRst',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgInternalData.RollInternalData.s16FveUsedByAlgo',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgInternalData.RollInternalData.s16LveUsedByAlgo',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.RollInternalData.u8LeftRolDecisionPathAtDecision',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.RollInternalData.u8RightRolDecisionPathAtDecision',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgInternalData.RollInternalData.u8RollRateLevelAtDecision',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.RollInternalData.u8RollAngleLevelAtDecision',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgInternalData.RollInternalData.u8LowGYLevelAtDecision',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgInternalData.RollInternalData.u8LowgYDvLevelAtDecision',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgInternalData.RollInternalData.u8LowGZLevelAtDecision',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgInternalData.RollInternalData.u8LowgZDvLevelAtDecision',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.RollInternalData.OpsRollAlg_UnconfEventCountAtWakeUp',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgInternalData.RollInternalData.s8XyStateAtDecision',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AlgInternalData.RollInternalData.u8RollConfSensorAtDeployTime',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_VehDynInErrTime._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_VehDynInErrTime._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_VehDynInErrTime._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_VehDynInErrTime._3_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_VehDynInErrTime._4_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_VehDynInErrTime._5_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_VehDynInErrTime._6_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_VehDynInErrTime._7_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_OPSSensorErrTime._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_OPSSensorErrTime._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_OPSSensorErrTime._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_OPSSensorErrTime._3_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_OPSSensorErrTime._4_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_OPSSensorErrTime._5_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_OPSSensorErrTime._6_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_OPSSensorErrTime._7_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_OPSSensorErrTime._8_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_OPSSensorErrTime._9_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_OPSSensorErrTime._10_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_OPSSensorErrTime._11_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_OPSSensorErrTime._12_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_OPSSensorErrTime._13_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_OPSSensorErrTime._14_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_OPSSensorErrTime._15_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_OPSSensorErrTime._16_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_OPSSensorErrTime._17_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_OPSSensorErrTime._18_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_OPSSensorErrTime._19_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_OPSSensorErrTime._20_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_OPSSensorErrTime._21_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_OPSSensorErrTime._22_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_OPSSensorErrTime._23_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_OPSSensorErrTime._24_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_OPSSensorErrTime._25_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_OPSSensorErrTime._26_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_OPSSensorErrTime._27_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_OPSSensorErrTime._28_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_OPSSensorErrTime._29_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_OPSFsrEventTime',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_OPSRollEventTime',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgCommonInternalData.OpsCshMgr_OPSPedEventTime']

        my_check_list_No_Need = [
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.u8IndexAdditionaldata5sTo0sXPerSec',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.u8NbOfSamplesFilledAdditionaldata5SecTo0SecYPerSec',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.u16EDROffsetTime200ms',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.u16EDROffsetTime250ms',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.u16EDROffsetTime500ms',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.u16EDROffsetTime1s',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.u8EDROffsetTime1ms',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.u8EDROffsetTime10ms',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.u8EDROffsetTime100ms']

        my_check_list_Special_Chk = [
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u32AirbagWarnLampOnTime',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u32AirbagWarnLampOnCycle',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.u16TimeMaxDeltaVLgt',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.u16TimeMaxDeltaVLat',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.u8IndexAccXmsTo0msYPerSec',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.u8IndexRsuXmsTo0msYPerSec',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.u8AddiIndex5sTo0sxPerSec',
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.u8IndexAcc1sTo0sXPerSec',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.s8Index1sTo0s10PerSec',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.u8Index5sTo0sxPerSec',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.u32LifeOperatingTimer',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.u32ResetCycleTimer',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.u32IgnCycleCrash',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.u8Index0sTo250msTyp100PerSec',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.s32AdjustXDV',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.s32AdjustYDV'
        ]

        my_check_list_different_value = {
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u16RsuStatusT0': 2560,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u8EventYear': 13,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u8IndexAcc0msToXmsYPerSec': 251,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u8IndexRsu0msToXmsYPerSec': 81,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u8Index0msToXmsYPerSec': 51,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aVehYawRate._0_': 2991,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aVehYawRate._1_': 2991,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aVehYawRate._2_': 2991,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aVehYawRate._3_': 2991,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aVehYawRate._4_': 2991,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aVehYawRate._5_': 2991,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aVehYawRate._6_': 2991,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aVehYawRate._7_': 2991,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aVehYawRate._8_': 2991,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aVehYawRate._9_': 2991,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aVehYawRate._10_': 2991,
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aCurrentGearPosition._0_.Data': 254,
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aCurrentGearPosition._1_.Data': 254,
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aCurrentGearPosition._2_.Data': 254,
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aCurrentGearPosition._3_.Data': 254,
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aCurrentGearPosition._4_.Data': 254,
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aCurrentGearPosition._5_.Data': 254,
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aCurrentGearPosition._6_.Data': 254,
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aCurrentGearPosition._7_.Data': 254,
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aCurrentGearPosition._8_.Data': 254,
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aCurrentGearPosition._9_.Data': 254,
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aCurrentGearPosition._10_.Data': 254,
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aParkingBrakeState._0_': 254,
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aParkingBrakeState._1_': 254,
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aParkingBrakeState._2_': 254,
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aParkingBrakeState._3_': 254,
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aParkingBrakeState._4_': 254,
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aParkingBrakeState._5_': 254,
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aParkingBrakeState._6_': 254,
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aParkingBrakeState._7_': 254,
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aParkingBrakeState._8_': 254,
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aParkingBrakeState._9_': 254,
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.aParkingBrakeState._10_': 254,
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.u8AddiNbOfSamplesFilled5sTo0sxPerSec': 11,
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.u8NbOfSamplesFilledAcc1SecTo0SecYPerSec': 11,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.s8NbOfSamplesFilled1sTo0s10PerSec': 11,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.u8NbOfSamplesFilled5sTo0sxPerSec': 11,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aPinionSteerAg._0_.Data': 156,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aPinionSteerAg._1_.Data': 156,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aPinionSteerAg._2_.Data': 156,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aPinionSteerAg._3_.Data': 156,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aPinionSteerAg._4_.Data': 156,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aPinionSteerAg._5_.Data': 156,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aPinionSteerAg._6_.Data': 156,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aPinionSteerAg._7_.Data': 156,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aPinionSteerAg._8_.Data': 156,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aPinionSteerAg._9_.Data': 156,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.aPinionSteerAg._10_.Data': 156,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.OccptSizeFPsngr': 7,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.u8CompletionStatus': 19,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.s8Index0sTo5s10PerSec': 51,
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.u8NbOfSamplesFilledAccXmsTo0msYPerSec': 41,
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.PreEventData.PreEventAdditionalData.u8NbOfSamplesFilledRsuXmsTo0msYPerSec': 21,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._0_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._1_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._2_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._3_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._4_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._5_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._6_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._7_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._8_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._9_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._10_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._11_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._12_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._13_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._14_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._15_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._16_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._17_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._18_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._19_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._20_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._21_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._22_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._23_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._24_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._25_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._26_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._27_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._28_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._29_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._30_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._31_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._32_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._33_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._34_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._35_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._36_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._37_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._38_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._39_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLgt._40_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._0_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._1_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._2_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._3_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._4_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._5_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._6_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._7_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._8_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._9_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._10_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._11_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._12_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._13_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._14_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._15_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._16_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._17_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._18_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._19_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._20_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._21_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._22_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._23_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._24_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._25_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._26_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._27_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._28_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._29_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._30_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._31_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._32_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._33_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._34_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._35_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._36_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._37_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._38_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._39_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aAccelLat._40_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._0_._0_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._0_._1_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._0_._2_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._0_._3_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._0_._4_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._0_._5_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._0_._6_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._0_._7_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._0_._8_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._0_._9_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._0_._10_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._0_._11_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._0_._12_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._0_._13_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._0_._14_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._0_._15_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._0_._16_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._0_._17_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._0_._18_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._0_._19_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._0_._20_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._1_._0_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._1_._1_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._1_._2_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._1_._3_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._1_._4_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._1_._5_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._1_._6_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._1_._7_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._1_._8_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._1_._9_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._1_._10_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._1_._11_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._1_._12_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._1_._13_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._1_._14_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._1_._15_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._1_._16_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._1_._17_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._1_._18_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._1_._19_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._1_._20_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._2_._0_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._2_._1_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._2_._2_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._2_._3_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._2_._4_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._2_._5_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._2_._6_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._2_._7_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._2_._8_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._2_._9_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._2_._10_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._2_._11_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._2_._12_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._2_._13_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._2_._14_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._2_._15_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._2_._16_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._2_._17_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._2_._18_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._2_._19_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._2_._20_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._3_._0_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._3_._1_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._3_._2_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._3_._3_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._3_._4_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._3_._5_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._3_._6_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._3_._7_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._3_._8_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._3_._9_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._3_._10_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._3_._11_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._3_._12_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._3_._13_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._3_._14_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._3_._15_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._3_._16_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._3_._17_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._3_._18_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._3_._19_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aRsuData._3_._20_': 0,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.u16TableTwoCompleteDelay': 10200,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.u16TableOneCompleteDelay': table_end,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.u16DeltaVCaptureCompleteDelay': dv_end,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.u16MaxDeltaVCaptureCompleteDelay': max_dv_end,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u16AlgoEndTime': algo_end_expect
        }

        my_check_list_CapVoltage_range = [
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aCapVoltage._0_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aCapVoltage._1_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aCapVoltage._2_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aCapVoltage._3_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aCapVoltage._4_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aCapVoltage._5_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aCapVoltage._6_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aCapVoltage._7_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aCapVoltage._8_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aCapVoltage._9_',
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.PreEventData.PreEventAdditionalData.aCapVoltage._10_']

        my_check_list_Voltage_range = ['RstEdr_EventDataCaptureBuffer._' + str(k) + '_.BattVolt']

        my_check_list_important_value = {
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u16CrashOutput': locals()[
                'edr' + str(k + 1) + '_crash_type'],
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AdditionalRecordDataElement.u16TimeMaxresultantDeltaV': max_resultant_time,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.FrntAirbagWarnLampSts': 1,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.u8MultiEventNumber': 1,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgInternalDataCapturedStatus': locals()[
                'edr' + str(k + 1) + '_algo_type'],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AlgInternalDataCaptureRequest': locals()[
                'edr' + str(k + 1) + '_algo_type'],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u16DelayFromEDR_T0._1_':
                locals()[
                    'expect_front_algo_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u16DelayFromEDR_T0._2_':
                locals()[
                    'expect_sidel_algo_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u16DelayFromEDR_T0._3_':
                locals()[
                    'expect_sider_algo_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u16DelayFromEDR_T0._5_':
                locals()[
                    'expect_rear_algo_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.bDeployConfirmationCaptureRequested': locals()[
                'deploy_request_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.u8DataAreaPriority': locals()[
                'crash_priority_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.u32LifeTimeEventNb': locals()[
                'edr' + str(k + 1) + '_event_no']
        }

        my_check_list_ac_dv = {
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._0_':
                locals()['expect_ac_x_' + str(k + 1)][0],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._1_':
                locals()['expect_ac_x_' + str(k + 1)][2],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._2_':
                locals()['expect_ac_x_' + str(k + 1)][4],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._3_':
                locals()['expect_ac_x_' + str(k + 1)][6],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._4_':
                locals()['expect_ac_x_' + str(k + 1)][8],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._5_':
                locals()['expect_ac_x_' + str(k + 1)][10],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._6_':
                locals()['expect_ac_x_' + str(k + 1)][12],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._7_':
                locals()['expect_ac_x_' + str(k + 1)][14],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._8_':
                locals()['expect_ac_x_' + str(k + 1)][16],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._9_':
                locals()['expect_ac_x_' + str(k + 1)][18],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._10_':
                locals()['expect_ac_x_' + str(k + 1)][20],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._11_':
                locals()['expect_ac_x_' + str(k + 1)][22],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._12_':
                locals()['expect_ac_x_' + str(k + 1)][24],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._13_':
                locals()['expect_ac_x_' + str(k + 1)][26],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._14_':
                locals()['expect_ac_x_' + str(k + 1)][28],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._15_':
                locals()['expect_ac_x_' + str(k + 1)][30],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._16_':
                locals()['expect_ac_x_' + str(k + 1)][32],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._17_':
                locals()['expect_ac_x_' + str(k + 1)][34],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._18_':
                locals()['expect_ac_x_' + str(k + 1)][36],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._19_':
                locals()['expect_ac_x_' + str(k + 1)][38],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._20_':
                locals()['expect_ac_x_' + str(k + 1)][40],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._21_':
                locals()['expect_ac_x_' + str(k + 1)][42],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._22_':
                locals()['expect_ac_x_' + str(k + 1)][44],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._23_':
                locals()['expect_ac_x_' + str(k + 1)][46],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._24_':
                locals()['expect_ac_x_' + str(k + 1)][48],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._25_':
                locals()['expect_ac_x_' + str(k + 1)][50],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._26_':
                locals()['expect_ac_x_' + str(k + 1)][52],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._27_':
                locals()['expect_ac_x_' + str(k + 1)][54],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._28_':
                locals()['expect_ac_x_' + str(k + 1)][56],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._29_':
                locals()['expect_ac_x_' + str(k + 1)][58],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._30_':
                locals()['expect_ac_x_' + str(k + 1)][60],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._31_':
                locals()['expect_ac_x_' + str(k + 1)][62],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._32_':
                locals()['expect_ac_x_' + str(k + 1)][64],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._33_':
                locals()['expect_ac_x_' + str(k + 1)][66],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._34_':
                locals()['expect_ac_x_' + str(k + 1)][68],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._35_':
                locals()['expect_ac_x_' + str(k + 1)][70],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._36_':
                locals()['expect_ac_x_' + str(k + 1)][72],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._37_':
                locals()['expect_ac_x_' + str(k + 1)][74],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._38_':
                locals()['expect_ac_x_' + str(k + 1)][76],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._39_':
                locals()['expect_ac_x_' + str(k + 1)][78],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._40_':
                locals()['expect_ac_x_' + str(k + 1)][80],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._41_':
                locals()['expect_ac_x_' + str(k + 1)][82],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._42_':
                locals()['expect_ac_x_' + str(k + 1)][84],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._43_':
                locals()['expect_ac_x_' + str(k + 1)][86],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._44_':
                locals()['expect_ac_x_' + str(k + 1)][88],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._45_':
                locals()['expect_ac_x_' + str(k + 1)][90],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._46_':
                locals()['expect_ac_x_' + str(k + 1)][92],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._47_':
                locals()['expect_ac_x_' + str(k + 1)][94],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._48_':
                locals()['expect_ac_x_' + str(k + 1)][96],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._49_':
                locals()['expect_ac_x_' + str(k + 1)][98],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._50_':
                locals()['expect_ac_x_' + str(k + 1)][100],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._51_':
                locals()['expect_ac_x_' + str(k + 1)][102],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._52_':
                locals()['expect_ac_x_' + str(k + 1)][104],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._53_':
                locals()['expect_ac_x_' + str(k + 1)][106],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._54_':
                locals()['expect_ac_x_' + str(k + 1)][108],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._55_':
                locals()['expect_ac_x_' + str(k + 1)][110],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._56_':
                locals()['expect_ac_x_' + str(k + 1)][112],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._57_':
                locals()['expect_ac_x_' + str(k + 1)][114],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._58_':
                locals()['expect_ac_x_' + str(k + 1)][116],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._59_':
                locals()['expect_ac_x_' + str(k + 1)][118],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._60_':
                locals()['expect_ac_x_' + str(k + 1)][120],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._61_':
                locals()['expect_ac_x_' + str(k + 1)][122],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._62_':
                locals()['expect_ac_x_' + str(k + 1)][124],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._63_':
                locals()['expect_ac_x_' + str(k + 1)][126],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._64_':
                locals()['expect_ac_x_' + str(k + 1)][128],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._65_':
                locals()['expect_ac_x_' + str(k + 1)][130],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._66_':
                locals()['expect_ac_x_' + str(k + 1)][132],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._67_':
                locals()['expect_ac_x_' + str(k + 1)][134],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._68_':
                locals()['expect_ac_x_' + str(k + 1)][136],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._69_':
                locals()['expect_ac_x_' + str(k + 1)][138],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._70_':
                locals()['expect_ac_x_' + str(k + 1)][140],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._71_':
                locals()['expect_ac_x_' + str(k + 1)][142],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._72_':
                locals()['expect_ac_x_' + str(k + 1)][144],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._73_':
                locals()['expect_ac_x_' + str(k + 1)][146],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._74_':
                locals()['expect_ac_x_' + str(k + 1)][148],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._75_':
                locals()['expect_ac_x_' + str(k + 1)][150],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._76_':
                locals()['expect_ac_x_' + str(k + 1)][152],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._77_':
                locals()['expect_ac_x_' + str(k + 1)][154],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._78_':
                locals()['expect_ac_x_' + str(k + 1)][156],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._79_':
                locals()['expect_ac_x_' + str(k + 1)][158],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._80_':
                locals()['expect_ac_x_' + str(k + 1)][160],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._81_':
                locals()['expect_ac_x_' + str(k + 1)][162],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._82_':
                locals()['expect_ac_x_' + str(k + 1)][164],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._83_':
                locals()['expect_ac_x_' + str(k + 1)][166],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._84_':
                locals()['expect_ac_x_' + str(k + 1)][168],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._85_':
                locals()['expect_ac_x_' + str(k + 1)][170],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._86_':
                locals()['expect_ac_x_' + str(k + 1)][172],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._87_':
                locals()['expect_ac_x_' + str(k + 1)][174],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._88_':
                locals()['expect_ac_x_' + str(k + 1)][176],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._89_':
                locals()['expect_ac_x_' + str(k + 1)][178],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._90_':
                locals()['expect_ac_x_' + str(k + 1)][180],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._91_':
                locals()['expect_ac_x_' + str(k + 1)][182],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._92_':
                locals()['expect_ac_x_' + str(k + 1)][184],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._93_':
                locals()['expect_ac_x_' + str(k + 1)][186],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._94_':
                locals()['expect_ac_x_' + str(k + 1)][188],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._95_':
                locals()['expect_ac_x_' + str(k + 1)][190],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._96_':
                locals()['expect_ac_x_' + str(k + 1)][192],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._97_':
                locals()['expect_ac_x_' + str(k + 1)][194],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._98_':
                locals()['expect_ac_x_' + str(k + 1)][196],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._99_':
                locals()['expect_ac_x_' + str(k + 1)][198],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._100_':
                locals()['expect_ac_x_' + str(k + 1)][200],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._101_':
                locals()['expect_ac_x_' + str(k + 1)][202],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._102_':
                locals()['expect_ac_x_' + str(k + 1)][204],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._103_':
                locals()['expect_ac_x_' + str(k + 1)][206],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._104_':
                locals()['expect_ac_x_' + str(k + 1)][208],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._105_':
                locals()['expect_ac_x_' + str(k + 1)][210],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._106_':
                locals()['expect_ac_x_' + str(k + 1)][212],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._107_':
                locals()['expect_ac_x_' + str(k + 1)][214],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._108_':
                locals()['expect_ac_x_' + str(k + 1)][216],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._109_':
                locals()['expect_ac_x_' + str(k + 1)][218],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._110_':
                locals()['expect_ac_x_' + str(k + 1)][220],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._111_':
                locals()['expect_ac_x_' + str(k + 1)][222],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._112_':
                locals()['expect_ac_x_' + str(k + 1)][224],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._113_':
                locals()['expect_ac_x_' + str(k + 1)][226],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._114_':
                locals()['expect_ac_x_' + str(k + 1)][228],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._115_':
                locals()['expect_ac_x_' + str(k + 1)][230],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._116_':
                locals()['expect_ac_x_' + str(k + 1)][232],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._117_':
                locals()['expect_ac_x_' + str(k + 1)][234],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._118_':
                locals()['expect_ac_x_' + str(k + 1)][236],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._119_':
                locals()['expect_ac_x_' + str(k + 1)][238],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._120_':
                locals()['expect_ac_x_' + str(k + 1)][240],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._121_':
                locals()['expect_ac_x_' + str(k + 1)][242],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._122_':
                locals()['expect_ac_x_' + str(k + 1)][244],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._123_':
                locals()['expect_ac_x_' + str(k + 1)][246],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._124_':
                locals()['expect_ac_x_' + str(k + 1)][248],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._125_':
                locals()['expect_ac_x_' + str(k + 1)][250],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._126_':
                locals()['expect_ac_x_' + str(k + 1)][252],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._127_':
                locals()['expect_ac_x_' + str(k + 1)][254],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._128_':
                locals()['expect_ac_x_' + str(k + 1)][256],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._129_':
                locals()['expect_ac_x_' + str(k + 1)][258],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._130_':
                locals()['expect_ac_x_' + str(k + 1)][260],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._131_':
                locals()['expect_ac_x_' + str(k + 1)][262],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._132_':
                locals()['expect_ac_x_' + str(k + 1)][264],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._133_':
                locals()['expect_ac_x_' + str(k + 1)][266],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._134_':
                locals()['expect_ac_x_' + str(k + 1)][268],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._135_':
                locals()['expect_ac_x_' + str(k + 1)][270],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._136_':
                locals()['expect_ac_x_' + str(k + 1)][272],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._137_':
                locals()['expect_ac_x_' + str(k + 1)][274],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._138_':
                locals()['expect_ac_x_' + str(k + 1)][276],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._139_':
                locals()['expect_ac_x_' + str(k + 1)][278],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._140_':
                locals()['expect_ac_x_' + str(k + 1)][280],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._141_':
                locals()['expect_ac_x_' + str(k + 1)][282],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._142_':
                locals()['expect_ac_x_' + str(k + 1)][284],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._143_':
                locals()['expect_ac_x_' + str(k + 1)][286],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._144_':
                locals()['expect_ac_x_' + str(k + 1)][288],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._145_':
                locals()['expect_ac_x_' + str(k + 1)][290],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._146_':
                locals()['expect_ac_x_' + str(k + 1)][292],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._147_':
                locals()['expect_ac_x_' + str(k + 1)][294],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._148_':
                locals()['expect_ac_x_' + str(k + 1)][296],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._149_':
                locals()['expect_ac_x_' + str(k + 1)][298],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._150_':
                locals()['expect_ac_x_' + str(k + 1)][300],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._151_':
                locals()['expect_ac_x_' + str(k + 1)][302],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._152_':
                locals()['expect_ac_x_' + str(k + 1)][304],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._153_':
                locals()['expect_ac_x_' + str(k + 1)][306],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._154_':
                locals()['expect_ac_x_' + str(k + 1)][308],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._155_':
                locals()['expect_ac_x_' + str(k + 1)][310],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._156_':
                locals()['expect_ac_x_' + str(k + 1)][312],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._157_':
                locals()['expect_ac_x_' + str(k + 1)][314],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._158_':
                locals()['expect_ac_x_' + str(k + 1)][316],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._159_':
                locals()['expect_ac_x_' + str(k + 1)][318],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._160_':
                locals()['expect_ac_x_' + str(k + 1)][320],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._161_':
                locals()['expect_ac_x_' + str(k + 1)][322],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._162_':
                locals()['expect_ac_x_' + str(k + 1)][324],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._163_':
                locals()['expect_ac_x_' + str(k + 1)][326],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._164_':
                locals()['expect_ac_x_' + str(k + 1)][328],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._165_':
                locals()['expect_ac_x_' + str(k + 1)][330],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._166_':
                locals()['expect_ac_x_' + str(k + 1)][332],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._167_':
                locals()['expect_ac_x_' + str(k + 1)][334],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._168_':
                locals()['expect_ac_x_' + str(k + 1)][336],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._169_':
                locals()['expect_ac_x_' + str(k + 1)][338],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._170_':
                locals()['expect_ac_x_' + str(k + 1)][340],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._171_':
                locals()['expect_ac_x_' + str(k + 1)][342],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._172_':
                locals()['expect_ac_x_' + str(k + 1)][344],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._173_':
                locals()['expect_ac_x_' + str(k + 1)][346],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._174_':
                locals()['expect_ac_x_' + str(k + 1)][348],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._175_':
                locals()['expect_ac_x_' + str(k + 1)][350],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._176_':
                locals()['expect_ac_x_' + str(k + 1)][352],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._177_':
                locals()['expect_ac_x_' + str(k + 1)][354],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._178_':
                locals()['expect_ac_x_' + str(k + 1)][356],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._179_':
                locals()['expect_ac_x_' + str(k + 1)][358],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._180_':
                locals()['expect_ac_x_' + str(k + 1)][360],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._181_':
                locals()['expect_ac_x_' + str(k + 1)][362],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._182_':
                locals()['expect_ac_x_' + str(k + 1)][364],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._183_':
                locals()['expect_ac_x_' + str(k + 1)][366],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._184_':
                locals()['expect_ac_x_' + str(k + 1)][368],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._185_':
                locals()['expect_ac_x_' + str(k + 1)][370],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._186_':
                locals()['expect_ac_x_' + str(k + 1)][372],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._187_':
                locals()['expect_ac_x_' + str(k + 1)][374],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._188_':
                locals()['expect_ac_x_' + str(k + 1)][376],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._189_':
                locals()['expect_ac_x_' + str(k + 1)][378],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._190_':
                locals()['expect_ac_x_' + str(k + 1)][380],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._191_':
                locals()['expect_ac_x_' + str(k + 1)][382],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._192_':
                locals()['expect_ac_x_' + str(k + 1)][384],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._193_':
                locals()['expect_ac_x_' + str(k + 1)][386],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._194_':
                locals()['expect_ac_x_' + str(k + 1)][388],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._195_':
                locals()['expect_ac_x_' + str(k + 1)][390],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._196_':
                locals()['expect_ac_x_' + str(k + 1)][392],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._197_':
                locals()['expect_ac_x_' + str(k + 1)][394],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._198_':
                locals()['expect_ac_x_' + str(k + 1)][396],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._199_':
                locals()['expect_ac_x_' + str(k + 1)][398],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._200_':
                locals()['expect_ac_x_' + str(k + 1)][400],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._201_':
                locals()['expect_ac_x_' + str(k + 1)][402],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._202_':
                locals()['expect_ac_x_' + str(k + 1)][404],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._203_':
                locals()['expect_ac_x_' + str(k + 1)][406],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._204_':
                locals()['expect_ac_x_' + str(k + 1)][408],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._205_':
                locals()['expect_ac_x_' + str(k + 1)][410],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._206_':
                locals()['expect_ac_x_' + str(k + 1)][412],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._207_':
                locals()['expect_ac_x_' + str(k + 1)][414],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._208_':
                locals()['expect_ac_x_' + str(k + 1)][416],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._209_':
                locals()['expect_ac_x_' + str(k + 1)][418],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._210_':
                locals()['expect_ac_x_' + str(k + 1)][420],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._211_':
                locals()['expect_ac_x_' + str(k + 1)][422],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._212_':
                locals()['expect_ac_x_' + str(k + 1)][424],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._213_':
                locals()['expect_ac_x_' + str(k + 1)][426],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._214_':
                locals()['expect_ac_x_' + str(k + 1)][428],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._215_':
                locals()['expect_ac_x_' + str(k + 1)][430],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._216_':
                locals()['expect_ac_x_' + str(k + 1)][432],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._217_':
                locals()['expect_ac_x_' + str(k + 1)][434],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._218_':
                locals()['expect_ac_x_' + str(k + 1)][436],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._219_':
                locals()['expect_ac_x_' + str(k + 1)][438],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._220_':
                locals()['expect_ac_x_' + str(k + 1)][440],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._221_':
                locals()['expect_ac_x_' + str(k + 1)][442],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._222_':
                locals()['expect_ac_x_' + str(k + 1)][444],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._223_':
                locals()['expect_ac_x_' + str(k + 1)][446],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._224_':
                locals()['expect_ac_x_' + str(k + 1)][448],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._225_':
                locals()['expect_ac_x_' + str(k + 1)][450],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._226_':
                locals()['expect_ac_x_' + str(k + 1)][452],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._227_':
                locals()['expect_ac_x_' + str(k + 1)][454],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._228_':
                locals()['expect_ac_x_' + str(k + 1)][456],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._229_':
                locals()['expect_ac_x_' + str(k + 1)][458],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._230_':
                locals()['expect_ac_x_' + str(k + 1)][460],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._231_':
                locals()['expect_ac_x_' + str(k + 1)][462],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._232_':
                locals()['expect_ac_x_' + str(k + 1)][464],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._233_':
                locals()['expect_ac_x_' + str(k + 1)][466],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._234_':
                locals()['expect_ac_x_' + str(k + 1)][468],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._235_':
                locals()['expect_ac_x_' + str(k + 1)][470],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._236_':
                locals()['expect_ac_x_' + str(k + 1)][472],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._237_':
                locals()['expect_ac_x_' + str(k + 1)][474],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._238_':
                locals()['expect_ac_x_' + str(k + 1)][476],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._239_':
                locals()['expect_ac_x_' + str(k + 1)][478],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._240_':
                locals()['expect_ac_x_' + str(k + 1)][480],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._241_':
                locals()['expect_ac_x_' + str(k + 1)][482],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._242_':
                locals()['expect_ac_x_' + str(k + 1)][484],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._243_':
                locals()['expect_ac_x_' + str(k + 1)][486],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._244_':
                locals()['expect_ac_x_' + str(k + 1)][488],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._245_':
                locals()['expect_ac_x_' + str(k + 1)][490],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._246_':
                locals()['expect_ac_x_' + str(k + 1)][492],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._247_':
                locals()['expect_ac_x_' + str(k + 1)][494],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._248_':
                locals()['expect_ac_x_' + str(k + 1)][496],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._249_':
                locals()['expect_ac_x_' + str(k + 1)][498],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLgtRecordDataElement.aAccelLgt._250_':
                locals()['expect_ac_x_' + str(k + 1)][500],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._0_':
                locals()['expect_ac_y_' + str(k + 1)][0],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._1_':
                locals()['expect_ac_y_' + str(k + 1)][2],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._2_':
                locals()['expect_ac_y_' + str(k + 1)][4],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._3_':
                locals()['expect_ac_y_' + str(k + 1)][6],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._4_':
                locals()['expect_ac_y_' + str(k + 1)][8],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._5_':
                locals()['expect_ac_y_' + str(k + 1)][10],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._6_':
                locals()['expect_ac_y_' + str(k + 1)][12],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._7_':
                locals()['expect_ac_y_' + str(k + 1)][14],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._8_':
                locals()['expect_ac_y_' + str(k + 1)][16],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._9_':
                locals()['expect_ac_y_' + str(k + 1)][18],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._10_':
                locals()['expect_ac_y_' + str(k + 1)][20],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._11_':
                locals()['expect_ac_y_' + str(k + 1)][22],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._12_':
                locals()['expect_ac_y_' + str(k + 1)][24],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._13_':
                locals()['expect_ac_y_' + str(k + 1)][26],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._14_':
                locals()['expect_ac_y_' + str(k + 1)][28],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._15_':
                locals()['expect_ac_y_' + str(k + 1)][30],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._16_':
                locals()['expect_ac_y_' + str(k + 1)][32],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._17_':
                locals()['expect_ac_y_' + str(k + 1)][34],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._18_':
                locals()['expect_ac_y_' + str(k + 1)][36],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._19_':
                locals()['expect_ac_y_' + str(k + 1)][38],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._20_':
                locals()['expect_ac_y_' + str(k + 1)][40],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._21_':
                locals()['expect_ac_y_' + str(k + 1)][42],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._22_':
                locals()['expect_ac_y_' + str(k + 1)][44],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._23_':
                locals()['expect_ac_y_' + str(k + 1)][46],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._24_':
                locals()['expect_ac_y_' + str(k + 1)][48],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._25_':
                locals()['expect_ac_y_' + str(k + 1)][50],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._26_':
                locals()['expect_ac_y_' + str(k + 1)][52],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._27_':
                locals()['expect_ac_y_' + str(k + 1)][54],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._28_':
                locals()['expect_ac_y_' + str(k + 1)][56],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._29_':
                locals()['expect_ac_y_' + str(k + 1)][58],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._30_':
                locals()['expect_ac_y_' + str(k + 1)][60],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._31_':
                locals()['expect_ac_y_' + str(k + 1)][62],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._32_':
                locals()['expect_ac_y_' + str(k + 1)][64],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._33_':
                locals()['expect_ac_y_' + str(k + 1)][66],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._34_':
                locals()['expect_ac_y_' + str(k + 1)][68],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._35_':
                locals()['expect_ac_y_' + str(k + 1)][70],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._36_':
                locals()['expect_ac_y_' + str(k + 1)][72],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._37_':
                locals()['expect_ac_y_' + str(k + 1)][74],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._38_':
                locals()['expect_ac_y_' + str(k + 1)][76],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._39_':
                locals()['expect_ac_y_' + str(k + 1)][78],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._40_':
                locals()['expect_ac_y_' + str(k + 1)][80],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._41_':
                locals()['expect_ac_y_' + str(k + 1)][82],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._42_':
                locals()['expect_ac_y_' + str(k + 1)][84],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._43_':
                locals()['expect_ac_y_' + str(k + 1)][86],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._44_':
                locals()['expect_ac_y_' + str(k + 1)][88],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._45_':
                locals()['expect_ac_y_' + str(k + 1)][90],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._46_':
                locals()['expect_ac_y_' + str(k + 1)][92],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._47_':
                locals()['expect_ac_y_' + str(k + 1)][94],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._48_':
                locals()['expect_ac_y_' + str(k + 1)][96],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._49_':
                locals()['expect_ac_y_' + str(k + 1)][98],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._50_':
                locals()['expect_ac_y_' + str(k + 1)][100],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._51_':
                locals()['expect_ac_y_' + str(k + 1)][102],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._52_':
                locals()['expect_ac_y_' + str(k + 1)][104],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._53_':
                locals()['expect_ac_y_' + str(k + 1)][106],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._54_':
                locals()['expect_ac_y_' + str(k + 1)][108],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._55_':
                locals()['expect_ac_y_' + str(k + 1)][110],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._56_':
                locals()['expect_ac_y_' + str(k + 1)][112],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._57_':
                locals()['expect_ac_y_' + str(k + 1)][114],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._58_':
                locals()['expect_ac_y_' + str(k + 1)][116],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._59_':
                locals()['expect_ac_y_' + str(k + 1)][118],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._60_':
                locals()['expect_ac_y_' + str(k + 1)][120],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._61_':
                locals()['expect_ac_y_' + str(k + 1)][122],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._62_':
                locals()['expect_ac_y_' + str(k + 1)][124],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._63_':
                locals()['expect_ac_y_' + str(k + 1)][126],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._64_':
                locals()['expect_ac_y_' + str(k + 1)][128],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._65_':
                locals()['expect_ac_y_' + str(k + 1)][130],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._66_':
                locals()['expect_ac_y_' + str(k + 1)][132],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._67_':
                locals()['expect_ac_y_' + str(k + 1)][134],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._68_':
                locals()['expect_ac_y_' + str(k + 1)][136],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._69_':
                locals()['expect_ac_y_' + str(k + 1)][138],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._70_':
                locals()['expect_ac_y_' + str(k + 1)][140],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._71_':
                locals()['expect_ac_y_' + str(k + 1)][142],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._72_':
                locals()['expect_ac_y_' + str(k + 1)][144],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._73_':
                locals()['expect_ac_y_' + str(k + 1)][146],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._74_':
                locals()['expect_ac_y_' + str(k + 1)][148],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._75_':
                locals()['expect_ac_y_' + str(k + 1)][150],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._76_':
                locals()['expect_ac_y_' + str(k + 1)][152],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._77_':
                locals()['expect_ac_y_' + str(k + 1)][154],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._78_':
                locals()['expect_ac_y_' + str(k + 1)][156],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._79_':
                locals()['expect_ac_y_' + str(k + 1)][158],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._80_':
                locals()['expect_ac_y_' + str(k + 1)][160],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._81_':
                locals()['expect_ac_y_' + str(k + 1)][162],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._82_':
                locals()['expect_ac_y_' + str(k + 1)][164],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._83_':
                locals()['expect_ac_y_' + str(k + 1)][166],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._84_':
                locals()['expect_ac_y_' + str(k + 1)][168],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._85_':
                locals()['expect_ac_y_' + str(k + 1)][170],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._86_':
                locals()['expect_ac_y_' + str(k + 1)][172],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._87_':
                locals()['expect_ac_y_' + str(k + 1)][174],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._88_':
                locals()['expect_ac_y_' + str(k + 1)][176],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._89_':
                locals()['expect_ac_y_' + str(k + 1)][178],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._90_':
                locals()['expect_ac_y_' + str(k + 1)][180],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._91_':
                locals()['expect_ac_y_' + str(k + 1)][182],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._92_':
                locals()['expect_ac_y_' + str(k + 1)][184],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._93_':
                locals()['expect_ac_y_' + str(k + 1)][186],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._94_':
                locals()['expect_ac_y_' + str(k + 1)][188],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._95_':
                locals()['expect_ac_y_' + str(k + 1)][190],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._96_':
                locals()['expect_ac_y_' + str(k + 1)][192],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._97_':
                locals()['expect_ac_y_' + str(k + 1)][194],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._98_':
                locals()['expect_ac_y_' + str(k + 1)][196],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._99_':
                locals()['expect_ac_y_' + str(k + 1)][198],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._100_':
                locals()['expect_ac_y_' + str(k + 1)][200],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._101_':
                locals()['expect_ac_y_' + str(k + 1)][202],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._102_':
                locals()['expect_ac_y_' + str(k + 1)][204],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._103_':
                locals()['expect_ac_y_' + str(k + 1)][206],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._104_':
                locals()['expect_ac_y_' + str(k + 1)][208],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._105_':
                locals()['expect_ac_y_' + str(k + 1)][210],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._106_':
                locals()['expect_ac_y_' + str(k + 1)][212],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._107_':
                locals()['expect_ac_y_' + str(k + 1)][214],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._108_':
                locals()['expect_ac_y_' + str(k + 1)][216],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._109_':
                locals()['expect_ac_y_' + str(k + 1)][218],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._110_':
                locals()['expect_ac_y_' + str(k + 1)][220],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._111_':
                locals()['expect_ac_y_' + str(k + 1)][222],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._112_':
                locals()['expect_ac_y_' + str(k + 1)][224],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._113_':
                locals()['expect_ac_y_' + str(k + 1)][226],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._114_':
                locals()['expect_ac_y_' + str(k + 1)][228],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._115_':
                locals()['expect_ac_y_' + str(k + 1)][230],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._116_':
                locals()['expect_ac_y_' + str(k + 1)][232],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._117_':
                locals()['expect_ac_y_' + str(k + 1)][234],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._118_':
                locals()['expect_ac_y_' + str(k + 1)][236],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._119_':
                locals()['expect_ac_y_' + str(k + 1)][238],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._120_':
                locals()['expect_ac_y_' + str(k + 1)][240],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._121_':
                locals()['expect_ac_y_' + str(k + 1)][242],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._122_':
                locals()['expect_ac_y_' + str(k + 1)][244],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._123_':
                locals()['expect_ac_y_' + str(k + 1)][246],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._124_':
                locals()['expect_ac_y_' + str(k + 1)][248],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._125_':
                locals()['expect_ac_y_' + str(k + 1)][250],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._126_':
                locals()['expect_ac_y_' + str(k + 1)][252],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._127_':
                locals()['expect_ac_y_' + str(k + 1)][254],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._128_':
                locals()['expect_ac_y_' + str(k + 1)][256],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._129_':
                locals()['expect_ac_y_' + str(k + 1)][258],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._130_':
                locals()['expect_ac_y_' + str(k + 1)][260],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._131_':
                locals()['expect_ac_y_' + str(k + 1)][262],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._132_':
                locals()['expect_ac_y_' + str(k + 1)][264],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._133_':
                locals()['expect_ac_y_' + str(k + 1)][266],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._134_':
                locals()['expect_ac_y_' + str(k + 1)][268],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._135_':
                locals()['expect_ac_y_' + str(k + 1)][270],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._136_':
                locals()['expect_ac_y_' + str(k + 1)][272],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._137_':
                locals()['expect_ac_y_' + str(k + 1)][274],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._138_':
                locals()['expect_ac_y_' + str(k + 1)][276],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._139_':
                locals()['expect_ac_y_' + str(k + 1)][278],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._140_':
                locals()['expect_ac_y_' + str(k + 1)][280],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._141_':
                locals()['expect_ac_y_' + str(k + 1)][282],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._142_':
                locals()['expect_ac_y_' + str(k + 1)][284],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._143_':
                locals()['expect_ac_y_' + str(k + 1)][286],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._144_':
                locals()['expect_ac_y_' + str(k + 1)][288],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._145_':
                locals()['expect_ac_y_' + str(k + 1)][290],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._146_':
                locals()['expect_ac_y_' + str(k + 1)][292],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._147_':
                locals()['expect_ac_y_' + str(k + 1)][294],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._148_':
                locals()['expect_ac_y_' + str(k + 1)][296],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._149_':
                locals()['expect_ac_y_' + str(k + 1)][298],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._150_':
                locals()['expect_ac_y_' + str(k + 1)][300],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._151_':
                locals()['expect_ac_y_' + str(k + 1)][302],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._152_':
                locals()['expect_ac_y_' + str(k + 1)][304],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._153_':
                locals()['expect_ac_y_' + str(k + 1)][306],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._154_':
                locals()['expect_ac_y_' + str(k + 1)][308],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._155_':
                locals()['expect_ac_y_' + str(k + 1)][310],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._156_':
                locals()['expect_ac_y_' + str(k + 1)][312],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._157_':
                locals()['expect_ac_y_' + str(k + 1)][314],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._158_':
                locals()['expect_ac_y_' + str(k + 1)][316],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._159_':
                locals()['expect_ac_y_' + str(k + 1)][318],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._160_':
                locals()['expect_ac_y_' + str(k + 1)][320],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._161_':
                locals()['expect_ac_y_' + str(k + 1)][322],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._162_':
                locals()['expect_ac_y_' + str(k + 1)][324],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._163_':
                locals()['expect_ac_y_' + str(k + 1)][326],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._164_':
                locals()['expect_ac_y_' + str(k + 1)][328],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._165_':
                locals()['expect_ac_y_' + str(k + 1)][330],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._166_':
                locals()['expect_ac_y_' + str(k + 1)][332],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._167_':
                locals()['expect_ac_y_' + str(k + 1)][334],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._168_':
                locals()['expect_ac_y_' + str(k + 1)][336],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._169_':
                locals()['expect_ac_y_' + str(k + 1)][338],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._170_':
                locals()['expect_ac_y_' + str(k + 1)][340],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._171_':
                locals()['expect_ac_y_' + str(k + 1)][342],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._172_':
                locals()['expect_ac_y_' + str(k + 1)][344],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._173_':
                locals()['expect_ac_y_' + str(k + 1)][346],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._174_':
                locals()['expect_ac_y_' + str(k + 1)][348],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._175_':
                locals()['expect_ac_y_' + str(k + 1)][350],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._176_':
                locals()['expect_ac_y_' + str(k + 1)][352],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._177_':
                locals()['expect_ac_y_' + str(k + 1)][354],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._178_':
                locals()['expect_ac_y_' + str(k + 1)][356],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._179_':
                locals()['expect_ac_y_' + str(k + 1)][358],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._180_':
                locals()['expect_ac_y_' + str(k + 1)][360],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._181_':
                locals()['expect_ac_y_' + str(k + 1)][362],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._182_':
                locals()['expect_ac_y_' + str(k + 1)][364],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._183_':
                locals()['expect_ac_y_' + str(k + 1)][366],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._184_':
                locals()['expect_ac_y_' + str(k + 1)][368],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._185_':
                locals()['expect_ac_y_' + str(k + 1)][370],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._186_':
                locals()['expect_ac_y_' + str(k + 1)][372],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._187_':
                locals()['expect_ac_y_' + str(k + 1)][374],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._188_':
                locals()['expect_ac_y_' + str(k + 1)][376],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._189_':
                locals()['expect_ac_y_' + str(k + 1)][378],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._190_':
                locals()['expect_ac_y_' + str(k + 1)][380],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._191_':
                locals()['expect_ac_y_' + str(k + 1)][382],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._192_':
                locals()['expect_ac_y_' + str(k + 1)][384],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._193_':
                locals()['expect_ac_y_' + str(k + 1)][386],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._194_':
                locals()['expect_ac_y_' + str(k + 1)][388],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._195_':
                locals()['expect_ac_y_' + str(k + 1)][390],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._196_':
                locals()['expect_ac_y_' + str(k + 1)][392],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._197_':
                locals()['expect_ac_y_' + str(k + 1)][394],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._198_':
                locals()['expect_ac_y_' + str(k + 1)][396],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._199_':
                locals()['expect_ac_y_' + str(k + 1)][398],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._200_':
                locals()['expect_ac_y_' + str(k + 1)][400],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._201_':
                locals()['expect_ac_y_' + str(k + 1)][402],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._202_':
                locals()['expect_ac_y_' + str(k + 1)][404],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._203_':
                locals()['expect_ac_y_' + str(k + 1)][406],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._204_':
                locals()['expect_ac_y_' + str(k + 1)][408],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._205_':
                locals()['expect_ac_y_' + str(k + 1)][410],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._206_':
                locals()['expect_ac_y_' + str(k + 1)][412],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._207_':
                locals()['expect_ac_y_' + str(k + 1)][414],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._208_':
                locals()['expect_ac_y_' + str(k + 1)][416],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._209_':
                locals()['expect_ac_y_' + str(k + 1)][418],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._210_':
                locals()['expect_ac_y_' + str(k + 1)][420],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._211_':
                locals()['expect_ac_y_' + str(k + 1)][422],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._212_':
                locals()['expect_ac_y_' + str(k + 1)][424],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._213_':
                locals()['expect_ac_y_' + str(k + 1)][426],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._214_':
                locals()['expect_ac_y_' + str(k + 1)][428],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._215_':
                locals()['expect_ac_y_' + str(k + 1)][430],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._216_':
                locals()['expect_ac_y_' + str(k + 1)][432],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._217_':
                locals()['expect_ac_y_' + str(k + 1)][434],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._218_':
                locals()['expect_ac_y_' + str(k + 1)][436],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._219_':
                locals()['expect_ac_y_' + str(k + 1)][438],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._220_':
                locals()['expect_ac_y_' + str(k + 1)][440],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._221_':
                locals()['expect_ac_y_' + str(k + 1)][442],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._222_':
                locals()['expect_ac_y_' + str(k + 1)][444],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._223_':
                locals()['expect_ac_y_' + str(k + 1)][446],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._224_':
                locals()['expect_ac_y_' + str(k + 1)][448],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._225_':
                locals()['expect_ac_y_' + str(k + 1)][450],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._226_':
                locals()['expect_ac_y_' + str(k + 1)][452],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._227_':
                locals()['expect_ac_y_' + str(k + 1)][454],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._228_':
                locals()['expect_ac_y_' + str(k + 1)][456],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._229_':
                locals()['expect_ac_y_' + str(k + 1)][458],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._230_':
                locals()['expect_ac_y_' + str(k + 1)][460],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._231_':
                locals()['expect_ac_y_' + str(k + 1)][462],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._232_':
                locals()['expect_ac_y_' + str(k + 1)][464],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._233_':
                locals()['expect_ac_y_' + str(k + 1)][466],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._234_':
                locals()['expect_ac_y_' + str(k + 1)][468],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._235_':
                locals()['expect_ac_y_' + str(k + 1)][470],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._236_':
                locals()['expect_ac_y_' + str(k + 1)][472],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._237_':
                locals()['expect_ac_y_' + str(k + 1)][474],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._238_':
                locals()['expect_ac_y_' + str(k + 1)][476],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._239_':
                locals()['expect_ac_y_' + str(k + 1)][478],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._240_':
                locals()['expect_ac_y_' + str(k + 1)][480],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._241_':
                locals()['expect_ac_y_' + str(k + 1)][482],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._242_':
                locals()['expect_ac_y_' + str(k + 1)][484],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._243_':
                locals()['expect_ac_y_' + str(k + 1)][486],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._244_':
                locals()['expect_ac_y_' + str(k + 1)][488],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._245_':
                locals()['expect_ac_y_' + str(k + 1)][490],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._246_':
                locals()['expect_ac_y_' + str(k + 1)][492],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._247_':
                locals()['expect_ac_y_' + str(k + 1)][494],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._248_':
                locals()['expect_ac_y_' + str(k + 1)][496],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._249_':
                locals()['expect_ac_y_' + str(k + 1)][498],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalAccelLatRecordDataElement.aAccelLat._250_':
                locals()['expect_ac_y_' + str(k + 1)][500],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.s16MaxAccelLgt':
                locals()['max_ctx_ac_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.s16MaxAccelLat':
                locals()['max_cty_ac_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u16TimeMaxAccelLgt':
                locals()['max_ctx_time_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.u16TimeMaxAccelLat':
                locals()['max_cty_time_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.DeployConfirmation.DeployConfirmationRawData._0_': locals()[
                'loop0_status_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.DeployConfirmation.DeployConfirmationRawData._1_': locals()[
                'loop1_status_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.DeployConfirmation.DeployConfirmationRawData._2_': locals()[
                'loop2_status_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.DeployConfirmation.DeployConfirmationRawData._3_': locals()[
                'loop3_status_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.DeployConfirmation.DeployConfirmationRawData._4_': locals()[
                'loop4_status_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.DeployConfirmation.DeployConfirmationRawData._5_': locals()[
                'loop5_status_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.DeployConfirmation.DeployConfirmationRawData._6_': locals()[
                'loop6_status_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.DeployConfirmation.DeployConfirmationRawData._7_': locals()[
                'loop7_status_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.DeployConfirmation.DeployConfirmationRawData._8_': locals()[
                'loop8_status_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.DeployConfirmation.DeployConfirmationRawData._9_': locals()[
                'loop9_status_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.DeployConfirmation.DeployConfirmationRawData._10_':
                locals()[
                    'loop10_status_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.DeployConfirmation.DeployConfirmationRawData._11_':
                locals()[
                    'loop11_status_' + str(k + 1)]

        }

        my_check_list_250ms_dv = {
            'RstEdr_EventDataCaptureBuffer._' + str(
                k) + '_.AdditionalRecordDataElement.u64MaxResultantDeltaV': max_resultant_dv,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._0_.s16Data': ctx_dv[0],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._1_.s16Data': ctx_dv[1],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._2_.s16Data': ctx_dv[2],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._3_.s16Data': ctx_dv[3],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._4_.s16Data': ctx_dv[4],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._5_.s16Data': ctx_dv[5],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._6_.s16Data': ctx_dv[6],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._7_.s16Data': ctx_dv[7],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._8_.s16Data': ctx_dv[8],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._9_.s16Data': ctx_dv[9],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._10_.s16Data': ctx_dv[10],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._11_.s16Data': ctx_dv[11],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._12_.s16Data': ctx_dv[12],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._13_.s16Data': ctx_dv[13],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._14_.s16Data': ctx_dv[14],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._15_.s16Data': ctx_dv[15],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._16_.s16Data': ctx_dv[16],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._17_.s16Data': ctx_dv[17],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._18_.s16Data': ctx_dv[18],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._19_.s16Data': ctx_dv[19],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._20_.s16Data': ctx_dv[20],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._21_.s16Data': ctx_dv[21],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._22_.s16Data': ctx_dv[22],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._23_.s16Data': ctx_dv[23],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._24_.s16Data': ctx_dv[24],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLgt._25_.s16Data': ctx_dv[25],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._0_.s16Data': cty_dv[0],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._1_.s16Data': cty_dv[1],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._2_.s16Data': cty_dv[2],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._3_.s16Data': cty_dv[3],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._4_.s16Data': cty_dv[4],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._5_.s16Data': cty_dv[5],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._6_.s16Data': cty_dv[6],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._7_.s16Data': cty_dv[7],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._8_.s16Data': cty_dv[8],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._9_.s16Data': cty_dv[9],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._10_.s16Data': cty_dv[10],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._11_.s16Data': cty_dv[11],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._12_.s16Data': cty_dv[12],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._13_.s16Data': cty_dv[13],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._14_.s16Data': cty_dv[14],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._15_.s16Data': cty_dv[15],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._16_.s16Data': cty_dv[16],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._17_.s16Data': cty_dv[17],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._18_.s16Data': cty_dv[18],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._19_.s16Data': cty_dv[19],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._20_.s16Data': cty_dv[20],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._21_.s16Data': cty_dv[21],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._22_.s16Data': cty_dv[22],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._23_.s16Data': cty_dv[23],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._24_.s16Data': cty_dv[24],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.aDeltaVLat._25_.s16Data': cty_dv[25]
        }

        my_check_list_8_byte_dv = {
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.LgtComponentDV': max_ctx_dv,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRecordDataElement.LatComponentDV': max_cty_dv,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.s32MaxDeltaVLgt': max_ctx_dv,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.s32MaxDeltaVLat': max_cty_dv
        }

        my_check_list_rsu = {
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._0_':
                locals()['expect_ac_frsul_' + str(k + 1)][0],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._1_':
                locals()['expect_ac_frsul_' + str(k + 1)][2],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._2_':
                locals()['expect_ac_frsul_' + str(k + 1)][4],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._3_':
                locals()['expect_ac_frsul_' + str(k + 1)][6],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._4_':
                locals()['expect_ac_frsul_' + str(k + 1)][8],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._5_':
                locals()['expect_ac_frsul_' + str(k + 1)][10],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._6_':
                locals()['expect_ac_frsul_' + str(k + 1)][12],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._7_':
                locals()['expect_ac_frsul_' + str(k + 1)][14],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._8_':
                locals()['expect_ac_frsul_' + str(k + 1)][16],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._9_':
                locals()['expect_ac_frsul_' + str(k + 1)][18],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._10_':
                locals()['expect_ac_frsul_' + str(k + 1)][20],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._11_':
                locals()['expect_ac_frsul_' + str(k + 1)][22],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._12_':
                locals()['expect_ac_frsul_' + str(k + 1)][24],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._13_':
                locals()['expect_ac_frsul_' + str(k + 1)][26],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._14_':
                locals()['expect_ac_frsul_' + str(k + 1)][28],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._15_':
                locals()['expect_ac_frsul_' + str(k + 1)][30],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._16_':
                locals()['expect_ac_frsul_' + str(k + 1)][32],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._17_':
                locals()['expect_ac_frsul_' + str(k + 1)][34],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._18_':
                locals()['expect_ac_frsul_' + str(k + 1)][36],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._19_':
                locals()['expect_ac_frsul_' + str(k + 1)][38],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._20_':
                locals()['expect_ac_frsul_' + str(k + 1)][40],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._21_':
                locals()['expect_ac_frsul_' + str(k + 1)][42],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._22_':
                locals()['expect_ac_frsul_' + str(k + 1)][44],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._23_':
                locals()['expect_ac_frsul_' + str(k + 1)][46],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._24_':
                locals()['expect_ac_frsul_' + str(k + 1)][48],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._25_':
                locals()['expect_ac_frsul_' + str(k + 1)][50],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._26_':
                locals()['expect_ac_frsul_' + str(k + 1)][52],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._27_':
                locals()['expect_ac_frsul_' + str(k + 1)][54],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._28_':
                locals()['expect_ac_frsul_' + str(k + 1)][56],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._29_':
                locals()['expect_ac_frsul_' + str(k + 1)][58],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._30_':
                locals()['expect_ac_frsul_' + str(k + 1)][60],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._31_':
                locals()['expect_ac_frsul_' + str(k + 1)][62],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._32_':
                locals()['expect_ac_frsul_' + str(k + 1)][64],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._33_':
                locals()['expect_ac_frsul_' + str(k + 1)][66],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._34_':
                locals()['expect_ac_frsul_' + str(k + 1)][68],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._35_':
                locals()['expect_ac_frsul_' + str(k + 1)][70],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._36_':
                locals()['expect_ac_frsul_' + str(k + 1)][72],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._37_':
                locals()['expect_ac_frsul_' + str(k + 1)][74],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._38_':
                locals()['expect_ac_frsul_' + str(k + 1)][76],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._39_':
                locals()['expect_ac_frsul_' + str(k + 1)][78],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._40_':
                locals()['expect_ac_frsul_' + str(k + 1)][80],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._41_':
                locals()['expect_ac_frsul_' + str(k + 1)][82],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._42_':
                locals()['expect_ac_frsul_' + str(k + 1)][84],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._43_':
                locals()['expect_ac_frsul_' + str(k + 1)][86],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._44_':
                locals()['expect_ac_frsul_' + str(k + 1)][88],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._45_':
                locals()['expect_ac_frsul_' + str(k + 1)][90],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._46_':
                locals()['expect_ac_frsul_' + str(k + 1)][92],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._47_':
                locals()['expect_ac_frsul_' + str(k + 1)][94],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._48_':
                locals()['expect_ac_frsul_' + str(k + 1)][96],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._49_':
                locals()['expect_ac_frsul_' + str(k + 1)][98],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._50_':
                locals()['expect_ac_frsul_' + str(k + 1)][100],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._51_':
                locals()['expect_ac_frsul_' + str(k + 1)][102],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._52_':
                locals()['expect_ac_frsul_' + str(k + 1)][104],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._53_':
                locals()['expect_ac_frsul_' + str(k + 1)][106],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._54_':
                locals()['expect_ac_frsul_' + str(k + 1)][108],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._55_':
                locals()['expect_ac_frsul_' + str(k + 1)][110],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._56_':
                locals()['expect_ac_frsul_' + str(k + 1)][112],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._57_':
                locals()['expect_ac_frsul_' + str(k + 1)][114],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._58_':
                locals()['expect_ac_frsul_' + str(k + 1)][116],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._59_':
                locals()['expect_ac_frsul_' + str(k + 1)][118],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._60_':
                locals()['expect_ac_frsul_' + str(k + 1)][120],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._61_':
                locals()['expect_ac_frsul_' + str(k + 1)][122],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._62_':
                locals()['expect_ac_frsul_' + str(k + 1)][124],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._63_':
                locals()['expect_ac_frsul_' + str(k + 1)][126],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._64_':
                locals()['expect_ac_frsul_' + str(k + 1)][128],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._65_':
                locals()['expect_ac_frsul_' + str(k + 1)][130],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._66_':
                locals()['expect_ac_frsul_' + str(k + 1)][132],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._67_':
                locals()['expect_ac_frsul_' + str(k + 1)][134],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._68_':
                locals()['expect_ac_frsul_' + str(k + 1)][136],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._69_':
                locals()['expect_ac_frsul_' + str(k + 1)][138],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._70_':
                locals()['expect_ac_frsul_' + str(k + 1)][140],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._71_':
                locals()['expect_ac_frsul_' + str(k + 1)][142],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._72_':
                locals()['expect_ac_frsul_' + str(k + 1)][144],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._73_':
                locals()['expect_ac_frsul_' + str(k + 1)][146],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._74_':
                locals()['expect_ac_frsul_' + str(k + 1)][148],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._75_':
                locals()['expect_ac_frsul_' + str(k + 1)][150],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._76_':
                locals()['expect_ac_frsul_' + str(k + 1)][152],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._77_':
                locals()['expect_ac_frsul_' + str(k + 1)][154],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._78_':
                locals()['expect_ac_frsul_' + str(k + 1)][156],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._79_':
                locals()['expect_ac_frsul_' + str(k + 1)][158],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._0_._80_':
                locals()['expect_ac_frsul_' + str(k + 1)][160],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._0_':
                locals()['expect_ac_frsur_' + str(k + 1)][0],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._1_':
                locals()['expect_ac_frsur_' + str(k + 1)][2],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._2_':
                locals()['expect_ac_frsur_' + str(k + 1)][4],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._3_':
                locals()['expect_ac_frsur_' + str(k + 1)][6],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._4_':
                locals()['expect_ac_frsur_' + str(k + 1)][8],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._5_':
                locals()['expect_ac_frsur_' + str(k + 1)][10],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._6_':
                locals()['expect_ac_frsur_' + str(k + 1)][12],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._7_':
                locals()['expect_ac_frsur_' + str(k + 1)][14],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._8_':
                locals()['expect_ac_frsur_' + str(k + 1)][16],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._9_':
                locals()['expect_ac_frsur_' + str(k + 1)][18],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._10_':
                locals()['expect_ac_frsur_' + str(k + 1)][20],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._11_':
                locals()['expect_ac_frsur_' + str(k + 1)][22],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._12_':
                locals()['expect_ac_frsur_' + str(k + 1)][24],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._13_':
                locals()['expect_ac_frsur_' + str(k + 1)][26],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._14_':
                locals()['expect_ac_frsur_' + str(k + 1)][28],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._15_':
                locals()['expect_ac_frsur_' + str(k + 1)][30],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._16_':
                locals()['expect_ac_frsur_' + str(k + 1)][32],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._17_':
                locals()['expect_ac_frsur_' + str(k + 1)][34],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._18_':
                locals()['expect_ac_frsur_' + str(k + 1)][36],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._19_':
                locals()['expect_ac_frsur_' + str(k + 1)][38],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._20_':
                locals()['expect_ac_frsur_' + str(k + 1)][40],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._21_':
                locals()['expect_ac_frsur_' + str(k + 1)][42],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._22_':
                locals()['expect_ac_frsur_' + str(k + 1)][44],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._23_':
                locals()['expect_ac_frsur_' + str(k + 1)][46],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._24_':
                locals()['expect_ac_frsur_' + str(k + 1)][48],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._25_':
                locals()['expect_ac_frsur_' + str(k + 1)][50],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._26_':
                locals()['expect_ac_frsur_' + str(k + 1)][52],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._27_':
                locals()['expect_ac_frsur_' + str(k + 1)][54],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._28_':
                locals()['expect_ac_frsur_' + str(k + 1)][56],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._29_':
                locals()['expect_ac_frsur_' + str(k + 1)][58],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._30_':
                locals()['expect_ac_frsur_' + str(k + 1)][60],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._31_':
                locals()['expect_ac_frsur_' + str(k + 1)][62],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._32_':
                locals()['expect_ac_frsur_' + str(k + 1)][64],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._33_':
                locals()['expect_ac_frsur_' + str(k + 1)][66],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._34_':
                locals()['expect_ac_frsur_' + str(k + 1)][68],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._35_':
                locals()['expect_ac_frsur_' + str(k + 1)][70],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._36_':
                locals()['expect_ac_frsur_' + str(k + 1)][72],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._37_':
                locals()['expect_ac_frsur_' + str(k + 1)][74],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._38_':
                locals()['expect_ac_frsur_' + str(k + 1)][76],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._39_':
                locals()['expect_ac_frsur_' + str(k + 1)][78],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._40_':
                locals()['expect_ac_frsur_' + str(k + 1)][80],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._41_':
                locals()['expect_ac_frsur_' + str(k + 1)][82],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._42_':
                locals()['expect_ac_frsur_' + str(k + 1)][84],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._43_':
                locals()['expect_ac_frsur_' + str(k + 1)][86],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._44_':
                locals()['expect_ac_frsur_' + str(k + 1)][88],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._45_':
                locals()['expect_ac_frsur_' + str(k + 1)][90],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._46_':
                locals()['expect_ac_frsur_' + str(k + 1)][92],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._47_':
                locals()['expect_ac_frsur_' + str(k + 1)][94],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._48_':
                locals()['expect_ac_frsur_' + str(k + 1)][96],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._49_':
                locals()['expect_ac_frsur_' + str(k + 1)][98],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._50_':
                locals()['expect_ac_frsur_' + str(k + 1)][100],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._51_':
                locals()['expect_ac_frsur_' + str(k + 1)][102],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._52_':
                locals()['expect_ac_frsur_' + str(k + 1)][104],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._53_':
                locals()['expect_ac_frsur_' + str(k + 1)][106],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._54_':
                locals()['expect_ac_frsur_' + str(k + 1)][108],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._55_':
                locals()['expect_ac_frsur_' + str(k + 1)][110],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._56_':
                locals()['expect_ac_frsur_' + str(k + 1)][112],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._57_':
                locals()['expect_ac_frsur_' + str(k + 1)][114],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._58_':
                locals()['expect_ac_frsur_' + str(k + 1)][116],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._59_':
                locals()['expect_ac_frsur_' + str(k + 1)][118],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._60_':
                locals()['expect_ac_frsur_' + str(k + 1)][120],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._61_':
                locals()['expect_ac_frsur_' + str(k + 1)][122],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._62_':
                locals()['expect_ac_frsur_' + str(k + 1)][124],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._63_':
                locals()['expect_ac_frsur_' + str(k + 1)][126],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._64_':
                locals()['expect_ac_frsur_' + str(k + 1)][128],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._65_':
                locals()['expect_ac_frsur_' + str(k + 1)][130],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._66_':
                locals()['expect_ac_frsur_' + str(k + 1)][132],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._67_':
                locals()['expect_ac_frsur_' + str(k + 1)][134],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._68_':
                locals()['expect_ac_frsur_' + str(k + 1)][136],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._69_':
                locals()['expect_ac_frsur_' + str(k + 1)][138],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._70_':
                locals()['expect_ac_frsur_' + str(k + 1)][140],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._71_':
                locals()['expect_ac_frsur_' + str(k + 1)][142],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._72_':
                locals()['expect_ac_frsur_' + str(k + 1)][144],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._73_':
                locals()['expect_ac_frsur_' + str(k + 1)][146],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._74_':
                locals()['expect_ac_frsur_' + str(k + 1)][148],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._75_':
                locals()['expect_ac_frsur_' + str(k + 1)][150],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._76_':
                locals()['expect_ac_frsur_' + str(k + 1)][152],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._77_':
                locals()['expect_ac_frsur_' + str(k + 1)][154],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._78_':
                locals()['expect_ac_frsur_' + str(k + 1)][156],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._79_':
                locals()['expect_ac_frsur_' + str(k + 1)][158],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._1_._80_':
                locals()['expect_ac_frsur_' + str(k + 1)][160],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._0_':
                locals()['expect_ac_srsul_' + str(k + 1)][0],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._1_':
                locals()['expect_ac_srsul_' + str(k + 1)][2],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._2_':
                locals()['expect_ac_srsul_' + str(k + 1)][4],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._3_':
                locals()['expect_ac_srsul_' + str(k + 1)][6],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._4_':
                locals()['expect_ac_srsul_' + str(k + 1)][8],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._5_':
                locals()['expect_ac_srsul_' + str(k + 1)][10],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._6_':
                locals()['expect_ac_srsul_' + str(k + 1)][12],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._7_':
                locals()['expect_ac_srsul_' + str(k + 1)][14],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._8_':
                locals()['expect_ac_srsul_' + str(k + 1)][16],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._9_':
                locals()['expect_ac_srsul_' + str(k + 1)][18],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._10_':
                locals()['expect_ac_srsul_' + str(k + 1)][20],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._11_':
                locals()['expect_ac_srsul_' + str(k + 1)][22],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._12_':
                locals()['expect_ac_srsul_' + str(k + 1)][24],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._13_':
                locals()['expect_ac_srsul_' + str(k + 1)][26],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._14_':
                locals()['expect_ac_srsul_' + str(k + 1)][28],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._15_':
                locals()['expect_ac_srsul_' + str(k + 1)][30],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._16_':
                locals()['expect_ac_srsul_' + str(k + 1)][32],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._17_':
                locals()['expect_ac_srsul_' + str(k + 1)][34],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._18_':
                locals()['expect_ac_srsul_' + str(k + 1)][36],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._19_':
                locals()['expect_ac_srsul_' + str(k + 1)][38],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._20_':
                locals()['expect_ac_srsul_' + str(k + 1)][40],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._21_':
                locals()['expect_ac_srsul_' + str(k + 1)][42],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._22_':
                locals()['expect_ac_srsul_' + str(k + 1)][44],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._23_':
                locals()['expect_ac_srsul_' + str(k + 1)][46],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._24_':
                locals()['expect_ac_srsul_' + str(k + 1)][48],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._25_':
                locals()['expect_ac_srsul_' + str(k + 1)][50],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._26_':
                locals()['expect_ac_srsul_' + str(k + 1)][52],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._27_':
                locals()['expect_ac_srsul_' + str(k + 1)][54],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._28_':
                locals()['expect_ac_srsul_' + str(k + 1)][56],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._29_':
                locals()['expect_ac_srsul_' + str(k + 1)][58],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._30_':
                locals()['expect_ac_srsul_' + str(k + 1)][60],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._31_':
                locals()['expect_ac_srsul_' + str(k + 1)][62],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._32_':
                locals()['expect_ac_srsul_' + str(k + 1)][64],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._33_':
                locals()['expect_ac_srsul_' + str(k + 1)][66],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._34_':
                locals()['expect_ac_srsul_' + str(k + 1)][68],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._35_':
                locals()['expect_ac_srsul_' + str(k + 1)][70],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._36_':
                locals()['expect_ac_srsul_' + str(k + 1)][72],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._37_':
                locals()['expect_ac_srsul_' + str(k + 1)][74],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._38_':
                locals()['expect_ac_srsul_' + str(k + 1)][76],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._39_':
                locals()['expect_ac_srsul_' + str(k + 1)][78],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._40_':
                locals()['expect_ac_srsul_' + str(k + 1)][80],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._41_':
                locals()['expect_ac_srsul_' + str(k + 1)][82],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._42_':
                locals()['expect_ac_srsul_' + str(k + 1)][84],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._43_':
                locals()['expect_ac_srsul_' + str(k + 1)][86],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._44_':
                locals()['expect_ac_srsul_' + str(k + 1)][88],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._45_':
                locals()['expect_ac_srsul_' + str(k + 1)][90],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._46_':
                locals()['expect_ac_srsul_' + str(k + 1)][92],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._47_':
                locals()['expect_ac_srsul_' + str(k + 1)][94],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._48_':
                locals()['expect_ac_srsul_' + str(k + 1)][96],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._49_':
                locals()['expect_ac_srsul_' + str(k + 1)][98],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._50_':
                locals()['expect_ac_srsul_' + str(k + 1)][100],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._51_':
                locals()['expect_ac_srsul_' + str(k + 1)][102],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._52_':
                locals()['expect_ac_srsul_' + str(k + 1)][104],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._53_':
                locals()['expect_ac_srsul_' + str(k + 1)][106],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._54_':
                locals()['expect_ac_srsul_' + str(k + 1)][108],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._55_':
                locals()['expect_ac_srsul_' + str(k + 1)][110],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._56_':
                locals()['expect_ac_srsul_' + str(k + 1)][112],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._57_':
                locals()['expect_ac_srsul_' + str(k + 1)][114],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._58_':
                locals()['expect_ac_srsul_' + str(k + 1)][116],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._59_':
                locals()['expect_ac_srsul_' + str(k + 1)][118],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._60_':
                locals()['expect_ac_srsul_' + str(k + 1)][120],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._61_':
                locals()['expect_ac_srsul_' + str(k + 1)][122],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._62_':
                locals()['expect_ac_srsul_' + str(k + 1)][124],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._63_':
                locals()['expect_ac_srsul_' + str(k + 1)][126],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._64_':
                locals()['expect_ac_srsul_' + str(k + 1)][128],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._65_':
                locals()['expect_ac_srsul_' + str(k + 1)][130],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._66_':
                locals()['expect_ac_srsul_' + str(k + 1)][132],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._67_':
                locals()['expect_ac_srsul_' + str(k + 1)][134],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._68_':
                locals()['expect_ac_srsul_' + str(k + 1)][136],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._69_':
                locals()['expect_ac_srsul_' + str(k + 1)][138],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._70_':
                locals()['expect_ac_srsul_' + str(k + 1)][140],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._71_':
                locals()['expect_ac_srsul_' + str(k + 1)][142],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._72_':
                locals()['expect_ac_srsul_' + str(k + 1)][144],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._73_':
                locals()['expect_ac_srsul_' + str(k + 1)][146],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._74_':
                locals()['expect_ac_srsul_' + str(k + 1)][148],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._75_':
                locals()['expect_ac_srsul_' + str(k + 1)][150],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._76_':
                locals()['expect_ac_srsul_' + str(k + 1)][152],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._77_':
                locals()['expect_ac_srsul_' + str(k + 1)][154],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._78_':
                locals()['expect_ac_srsul_' + str(k + 1)][156],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._79_':
                locals()['expect_ac_srsul_' + str(k + 1)][158],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._2_._80_':
                locals()['expect_ac_srsul_' + str(k + 1)][160],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._0_':
                locals()['expect_ac_srsur_' + str(k + 1)][0],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._1_':
                locals()['expect_ac_srsur_' + str(k + 1)][2],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._2_':
                locals()['expect_ac_srsur_' + str(k + 1)][4],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._3_':
                locals()['expect_ac_srsur_' + str(k + 1)][6],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._4_':
                locals()['expect_ac_srsur_' + str(k + 1)][8],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._5_':
                locals()['expect_ac_srsur_' + str(k + 1)][10],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._6_':
                locals()['expect_ac_srsur_' + str(k + 1)][12],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._7_':
                locals()['expect_ac_srsur_' + str(k + 1)][14],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._8_':
                locals()['expect_ac_srsur_' + str(k + 1)][16],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._9_':
                locals()['expect_ac_srsur_' + str(k + 1)][18],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._10_':
                locals()['expect_ac_srsur_' + str(k + 1)][20],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._11_':
                locals()['expect_ac_srsur_' + str(k + 1)][22],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._12_':
                locals()['expect_ac_srsur_' + str(k + 1)][24],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._13_':
                locals()['expect_ac_srsur_' + str(k + 1)][26],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._14_':
                locals()['expect_ac_srsur_' + str(k + 1)][28],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._15_':
                locals()['expect_ac_srsur_' + str(k + 1)][30],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._16_':
                locals()['expect_ac_srsur_' + str(k + 1)][32],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._17_':
                locals()['expect_ac_srsur_' + str(k + 1)][34],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._18_':
                locals()['expect_ac_srsur_' + str(k + 1)][36],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._19_':
                locals()['expect_ac_srsur_' + str(k + 1)][38],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._20_':
                locals()['expect_ac_srsur_' + str(k + 1)][40],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._21_':
                locals()['expect_ac_srsur_' + str(k + 1)][42],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._22_':
                locals()['expect_ac_srsur_' + str(k + 1)][44],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._23_':
                locals()['expect_ac_srsur_' + str(k + 1)][46],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._24_':
                locals()['expect_ac_srsur_' + str(k + 1)][48],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._25_':
                locals()['expect_ac_srsur_' + str(k + 1)][50],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._26_':
                locals()['expect_ac_srsur_' + str(k + 1)][52],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._27_':
                locals()['expect_ac_srsur_' + str(k + 1)][54],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._28_':
                locals()['expect_ac_srsur_' + str(k + 1)][56],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._29_':
                locals()['expect_ac_srsur_' + str(k + 1)][58],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._30_':
                locals()['expect_ac_srsur_' + str(k + 1)][60],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._31_':
                locals()['expect_ac_srsur_' + str(k + 1)][62],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._32_':
                locals()['expect_ac_srsur_' + str(k + 1)][64],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._33_':
                locals()['expect_ac_srsur_' + str(k + 1)][66],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._34_':
                locals()['expect_ac_srsur_' + str(k + 1)][68],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._35_':
                locals()['expect_ac_srsur_' + str(k + 1)][70],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._36_':
                locals()['expect_ac_srsur_' + str(k + 1)][72],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._37_':
                locals()['expect_ac_srsur_' + str(k + 1)][74],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._38_':
                locals()['expect_ac_srsur_' + str(k + 1)][76],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._39_':
                locals()['expect_ac_srsur_' + str(k + 1)][78],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._40_':
                locals()['expect_ac_srsur_' + str(k + 1)][80],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._41_':
                locals()['expect_ac_srsur_' + str(k + 1)][82],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._42_':
                locals()['expect_ac_srsur_' + str(k + 1)][84],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._43_':
                locals()['expect_ac_srsur_' + str(k + 1)][86],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._44_':
                locals()['expect_ac_srsur_' + str(k + 1)][88],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._45_':
                locals()['expect_ac_srsur_' + str(k + 1)][90],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._46_':
                locals()['expect_ac_srsur_' + str(k + 1)][92],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._47_':
                locals()['expect_ac_srsur_' + str(k + 1)][94],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._48_':
                locals()['expect_ac_srsur_' + str(k + 1)][96],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._49_':
                locals()['expect_ac_srsur_' + str(k + 1)][98],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._50_':
                locals()['expect_ac_srsur_' + str(k + 1)][100],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._51_':
                locals()['expect_ac_srsur_' + str(k + 1)][102],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._52_':
                locals()['expect_ac_srsur_' + str(k + 1)][104],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._53_':
                locals()['expect_ac_srsur_' + str(k + 1)][106],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._54_':
                locals()['expect_ac_srsur_' + str(k + 1)][108],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._55_':
                locals()['expect_ac_srsur_' + str(k + 1)][110],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._56_':
                locals()['expect_ac_srsur_' + str(k + 1)][112],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._57_':
                locals()['expect_ac_srsur_' + str(k + 1)][114],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._58_':
                locals()['expect_ac_srsur_' + str(k + 1)][116],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._59_':
                locals()['expect_ac_srsur_' + str(k + 1)][118],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._60_':
                locals()['expect_ac_srsur_' + str(k + 1)][120],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._61_':
                locals()['expect_ac_srsur_' + str(k + 1)][122],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._62_':
                locals()['expect_ac_srsur_' + str(k + 1)][124],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._63_':
                locals()['expect_ac_srsur_' + str(k + 1)][126],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._64_':
                locals()['expect_ac_srsur_' + str(k + 1)][128],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._65_':
                locals()['expect_ac_srsur_' + str(k + 1)][130],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._66_':
                locals()['expect_ac_srsur_' + str(k + 1)][132],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._67_':
                locals()['expect_ac_srsur_' + str(k + 1)][134],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._68_':
                locals()['expect_ac_srsur_' + str(k + 1)][136],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._69_':
                locals()['expect_ac_srsur_' + str(k + 1)][138],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._70_':
                locals()['expect_ac_srsur_' + str(k + 1)][140],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._71_':
                locals()['expect_ac_srsur_' + str(k + 1)][142],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._72_':
                locals()['expect_ac_srsur_' + str(k + 1)][144],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._73_':
                locals()['expect_ac_srsur_' + str(k + 1)][146],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._74_':
                locals()['expect_ac_srsur_' + str(k + 1)][148],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._75_':
                locals()['expect_ac_srsur_' + str(k + 1)][150],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._76_':
                locals()['expect_ac_srsur_' + str(k + 1)][152],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._77_':
                locals()['expect_ac_srsur_' + str(k + 1)][154],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._78_':
                locals()['expect_ac_srsur_' + str(k + 1)][156],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._79_':
                locals()['expect_ac_srsur_' + str(k + 1)][158],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.AdditionalRsuSmplRecordDataElement.aRsuData._3_._80_':
                locals()['expect_ac_srsur_' + str(k + 1)][160]

        }

        my_check_list_deploy_decision = {
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoSendCmdTab._0_':
                locals()['loop0_decision_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoSendCmdTab._1_':
                locals()['loop1_decision_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoSendCmdTab._2_':
                locals()['loop2_decision_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoSendCmdTab._3_':
                locals()['loop3_decision_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoSendCmdTab._4_':
                locals()['loop4_decision_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoSendCmdTab._5_':
                locals()['loop5_decision_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoSendCmdTab._6_':
                locals()['loop6_decision_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoSendCmdTab._7_':
                locals()['loop7_decision_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoSendCmdTab._8_':
                locals()['loop8_decision_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoSendCmdTab._9_':
                locals()['loop9_decision_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoSendCmdTab._10_':
                locals()['loop10_decision_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoSendCmdTab._11_':
                locals()['loop11_decision_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoDeployTab._0_':
                locals()['loop0_decision_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoDeployTab._1_':
                locals()['loop1_decision_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoDeployTab._2_':
                locals()['loop2_decision_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoDeployTab._3_':
                locals()['loop3_decision_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoDeployTab._4_':
                locals()['loop4_decision_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoDeployTab._5_':
                locals()['loop5_decision_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoDeployTab._6_':
                locals()['loop6_decision_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoDeployTab._7_':
                locals()['loop7_decision_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoDeployTab._8_':
                locals()['loop8_decision_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoDeployTab._9_':
                locals()['loop9_decision_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoDeployTab._10_':
                locals()['loop10_decision_' + str(k + 1)],
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.au16TimetoDeployTab._11_':
                locals()['loop11_decision_' + str(k + 1)]
        }

        my_check_list_tolerance = {
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.u16ElapsedTimeFromTime0': 10200,
            'RstEdr_EventDataCaptureBuffer._' + str(k) + '_.u16TimeBtwEvents': locals()['time_between_' + str(k + 1)]
        }

        for element in my_check_list_always_0:
            want_element = element
            a = want_element = Acct_data[Acct_data[want_column] == want_element]
            row_index = a.index.tolist()
            row_index = row_index[0]
            # print(want_element)
            # print(row_index)
            want_element = want_element.loc[[row_index], [actual_result]]
            want_element = np.array(want_element)
            want_element = want_element.tolist()
            b = want_element = want_element[0][0]
            want_element = int(want_element, 16)

            if want_element == 0:
                Acct_data.loc[[row_index], ['Expect']] = b
                Acct_data.loc[[row_index], ['Judge']] = 'Pass'
            else:
                Acct_data.loc[[row_index], ['Expect']] = 'value=0'
                Acct_data.loc[[row_index], ['Judge']] = 'Fail'

        for element in my_check_list_default_0:
            want_element = element
            a = want_element = Acct_data[Acct_data[want_column] == want_element]
            row_index = a.index.tolist()
            row_index = row_index[0]
            # print(want_element)
            # print(row_index)
            want_element = want_element.loc[[row_index], [actual_result]]
            want_element = np.array(want_element)
            want_element = want_element.tolist()
            b = want_element = want_element[0][0]
            want_element = int(want_element, 16)

            if want_element == 0:
                Acct_data.loc[[row_index], ['Expect']] = b
                Acct_data.loc[[row_index], ['Judge']] = 'Pass'
            else:
                Acct_data.loc[[row_index], ['Expect']] = 'Default=0'
                Acct_data.loc[[row_index], ['Judge']] = 'Please CHK'

        for element in my_check_list_default_1:
            want_element = element
            a = want_element = Acct_data[Acct_data[want_column] == want_element]
            row_index = a.index.tolist()
            row_index = row_index[0]
            # print(want_element)
            # print(row_index)
            want_element = want_element.loc[[row_index], [actual_result]]
            want_element = np.array(want_element)
            want_element = want_element.tolist()
            b = want_element = want_element[0][0]
            want_element = int(want_element, 16)

            if want_element == 1:
                Acct_data.loc[[row_index], ['Expect']] = b
                Acct_data.loc[[row_index], ['Judge']] = 'Pass'
            else:
                Acct_data.loc[[row_index], ['Expect']] = 'Default=1'
                Acct_data.loc[[row_index], ['Judge']] = 'Please CHK'

        for element in my_check_list_default_2:
            want_element = element
            a = want_element = Acct_data[Acct_data[want_column] == want_element]
            row_index = a.index.tolist()
            row_index = row_index[0]
            # print(want_element)
            # print(row_index)
            want_element = want_element.loc[[row_index], [actual_result]]
            want_element = np.array(want_element)
            want_element = want_element.tolist()
            b = want_element = want_element[0][0]
            want_element = int(want_element, 16)

            if want_element == 2:
                Acct_data.loc[[row_index], ['Expect']] = b
                Acct_data.loc[[row_index], ['Judge']] = 'Pass'
            else:
                Acct_data.loc[[row_index], ['Expect']] = 'Default=2'
                Acct_data.loc[[row_index], ['Judge']] = 'Please CHK'

        for element in my_check_list_default_3:
            want_element = element
            a = want_element = Acct_data[Acct_data[want_column] == want_element]
            row_index = a.index.tolist()
            row_index = row_index[0]
            # print(want_element)
            # print(row_index)
            want_element = want_element.loc[[row_index], [actual_result]]
            want_element = np.array(want_element)
            want_element = want_element.tolist()
            b = want_element = want_element[0][0]
            want_element = int(want_element, 16)

            if want_element == 3:
                Acct_data.loc[[row_index], ['Expect']] = b
                Acct_data.loc[[row_index], ['Judge']] = 'Pass'
            else:
                Acct_data.loc[[row_index], ['Expect']] = 'Default=3'
                Acct_data.loc[[row_index], ['Judge']] = 'Please CHK'

        for element in my_check_list_default_FFFF:
            want_element = element
            a = want_element = Acct_data[Acct_data[want_column] == want_element]
            row_index = a.index.tolist()
            row_index = row_index[0]
            # print(want_element)
            # print(row_index)
            want_element = want_element.loc[[row_index], [actual_result]]
            want_element = np.array(want_element)
            want_element = want_element.tolist()
            b = want_element = want_element[0][0]
            want_element = int(want_element, 16)

            if want_element == 65535:
                Acct_data.loc[[row_index], ['Expect']] = b
                Acct_data.loc[[row_index], ['Judge']] = 'Pass'
            else:
                Acct_data.loc[[row_index], ['Expect']] = '0xFFFF'
                Acct_data.loc[[row_index], ['Judge']] = 'Fail'

        for element in my_check_list_default_7FFE:
            want_element = element
            a = want_element = Acct_data[Acct_data[want_column] == want_element]
            row_index = a.index.tolist()
            row_index = row_index[0]
            # print(want_element)
            # print(row_index)
            want_element = want_element.loc[[row_index], [actual_result]]
            want_element = np.array(want_element)
            want_element = want_element.tolist()
            b = want_element = want_element[0][0]
            want_element = int(want_element, 16)

            if want_element == 32766:
                Acct_data.loc[[row_index], ['Expect']] = b
                Acct_data.loc[[row_index], ['Judge']] = 'Pass'
            else:
                Acct_data.loc[[row_index], ['Expect']] = 'Default=0x7FFE'
                Acct_data.loc[[row_index], ['Judge']] = 'Please CHK'

        for element in my_check_list_NA:
            want_element = element
            a = want_element = Acct_data[Acct_data[want_column] == want_element]
            row_index = a.index.tolist()
            row_index = row_index[0]
            Acct_data.loc[[row_index], ['Expect']] = 'Chk_by_Alg'
            Acct_data.loc[[row_index], ['Judge']] = 'NA'

        for element in my_check_list_No_Need:
            want_element = element
            a = want_element = Acct_data[Acct_data[want_column] == want_element]
            row_index = a.index.tolist()
            row_index = row_index[0]
            Acct_data.loc[[row_index], ['Expect']] = 'SW_Integration'
            Acct_data.loc[[row_index], ['Judge']] = 'NA'

        for element in my_check_list_Special_Chk:
            want_element = element
            a = want_element = Acct_data[Acct_data[want_column] == want_element]
            row_index = a.index.tolist()
            row_index = row_index[0]
            Acct_data.loc[[row_index], ['Expect']] = 'Unknown'
            Acct_data.loc[[row_index], ['Judge']] = 'Special_Case_CHK'

        for element, value in my_check_list_different_value.items():
            want_element = element
            a = want_element = Acct_data[Acct_data[want_column] == want_element]
            row_index = a.index.tolist()
            row_index = row_index[0]
            # print(want_element)
            # print(row_index)
            want_element = want_element.loc[[row_index], [actual_result]]
            want_element = np.array(want_element)
            want_element = want_element.tolist()
            b = want_element = want_element[0][0]
            want_element = int(want_element, 16)

            if want_element == value:
                Acct_data.loc[[row_index], ['Expect']] = b
                Acct_data.loc[[row_index], ['Judge']] = 'Pass'
            else:
                Acct_data.loc[[row_index], ['Expect']] = hex(value)
                Acct_data.loc[[row_index], ['Judge']] = 'Fail'

        for element in my_check_list_CapVoltage_range:
            want_element = element
            a = want_element = Acct_data[Acct_data[want_column] == want_element]
            row_index = a.index.tolist()
            row_index = row_index[0]
            # print(want_element)
            # print(row_index)
            want_element = want_element.loc[[row_index], [actual_result]]
            want_element = np.array(want_element)
            want_element = want_element.tolist()
            b = want_element = want_element[0][0]
            want_element = int(want_element, 16)
            want_element = (want_element / 1023) * 40
            if (want_element >= 29.5) and (want_element <= 36.8):
                Acct_data.loc[[row_index], ['Expect']] = '0x02F2-0x03AD'
                Acct_data.loc[[row_index], ['Judge']] = 'Pass'
            else:
                Acct_data.loc[[row_index], ['Expect']] = '0x02F2-0x03AD'
                Acct_data.loc[[row_index], ['Judge']] = 'Fail'

        for element in my_check_list_Voltage_range:
            want_element = element
            a = want_element = Acct_data[Acct_data[want_column] == want_element]
            row_index = a.index.tolist()
            row_index = row_index[0]
            # print(want_element)
            # print(row_index)
            want_element = want_element.loc[[row_index], [actual_result]]
            want_element = np.array(want_element)
            want_element = want_element.tolist()
            b = want_element = want_element[0][0]
            want_element = int(want_element, 16)
            want_element = (want_element / 1023) * 25
            if (want_element >= 11.5) and (want_element <= 13):
                Acct_data.loc[[row_index], ['Expect']] = '0x01D6-0x0213'
                Acct_data.loc[[row_index], ['Judge']] = 'Pass'
            else:
                Acct_data.loc[[row_index], ['Expect']] = '0x01D6-0x0213'
                Acct_data.loc[[row_index], ['Judge']] = 'Fail'

        for element, value in my_check_list_important_value.items():
            want_element = element
            a = want_element = Acct_data[Acct_data[want_column] == want_element]
            row_index = a.index.tolist()
            row_index = row_index[0]
            # print(want_element)
            # print(row_index)
            want_element = want_element.loc[[row_index], [actual_result]]
            want_element = np.array(want_element)
            want_element = want_element.tolist()
            b = want_element = want_element[0][0]
            want_element = int(want_element, 16)

            if want_element == value:
                Acct_data.loc[[row_index], ['Expect']] = b
                Acct_data.loc[[row_index], ['Judge']] = 'Pass'
            else:
                Acct_data.loc[[row_index], ['Expect']] = hex(value)
                Acct_data.loc[[row_index], ['Judge']] = 'Fail'

        for element, value in my_check_list_ac_dv.items():
            want_element = element
            a = want_element = Acct_data[Acct_data[want_column] == want_element]
            row_index = a.index.tolist()
            row_index = row_index[0]
            # print(want_element)
            # print(row_index)
            want_element = want_element.loc[[row_index], [actual_result]]
            want_element = np.array(want_element)
            want_element = want_element.tolist()
            b = want_element = want_element[0][0]
            want_element = int(want_element, 16)
            if value < 0:
                want_element = want_element - 65536
            # print(want_element)
            # print(value)

            if want_element - value <= 3:
                # print(want_element - value)
                Acct_data.loc[[row_index], ['Expect']] = b
                Acct_data.loc[[row_index], ['Judge']] = 'Pass'
            else:
                Acct_data.loc[[row_index], ['Expect']] = hex(value)
                Acct_data.loc[[row_index], ['Judge']] = 'Fail'

        for element, value in my_check_list_250ms_dv.items():
            want_element = element
            a = want_element = Acct_data[Acct_data[want_column] == want_element]
            row_index = a.index.tolist()
            row_index = row_index[0]
            want_element = want_element.loc[[row_index], [actual_result]]
            want_element = np.array(want_element)
            want_element = want_element.tolist()
            b = want_element = want_element[0][0]
            want_element = int(want_element, 16)
            if value < 0:
                want_element = want_element - 65536
            # print(want_element)
            # print(value)
            if abs(want_element - value) <= 5:
                # print(want_element - value)
                Acct_data.loc[[row_index], ['Expect']] = b
                Acct_data.loc[[row_index], ['Judge']] = 'Pass'
            else:
                Acct_data.loc[[row_index], ['Expect']] = hex(value)
                Acct_data.loc[[row_index], ['Judge']] = 'Fail'

        for element, value in my_check_list_8_byte_dv.items():
            want_element = element
            a = want_element = Acct_data[Acct_data[want_column] == want_element]
            row_index = a.index.tolist()
            row_index = row_index[0]
            want_element = want_element.loc[[row_index], [actual_result]]
            want_element = np.array(want_element)
            want_element = want_element.tolist()
            b = want_element = want_element[0][0]
            want_element = int(want_element, 16)
            if value < 0:
                want_element = want_element - 4294967295
            # print(want_element)
            # print(value)
            if abs(want_element - value) <= 5:
                # print(want_element - value)
                Acct_data.loc[[row_index], ['Expect']] = b
                Acct_data.loc[[row_index], ['Judge']] = 'Pass'
            else:
                Acct_data.loc[[row_index], ['Expect']] = hex(value)
                Acct_data.loc[[row_index], ['Judge']] = 'Fail'

        for element, value in my_check_list_rsu.items():
            want_element = element
            a = want_element = Acct_data[Acct_data[want_column] == want_element]
            row_index = a.index.tolist()
            row_index = row_index[0]
            # print(want_element)
            # print(row_index)
            want_element = want_element.loc[[row_index], [actual_result]]
            want_element = np.array(want_element)
            want_element = want_element.tolist()
            b = want_element = want_element[0][0]
            want_element = int(want_element, 16)
            if value < 0:
                want_element = want_element - 65536
            # print(want_element)
            # print(value)

            if want_element - value <= 3:
                # print(want_element - value)
                Acct_data.loc[[row_index], ['Expect']] = b
                Acct_data.loc[[row_index], ['Judge']] = 'Pass'
            else:
                Acct_data.loc[[row_index], ['Expect']] = hex(value)
                Acct_data.loc[[row_index], ['Judge']] = 'Fail'

        for element, value in my_check_list_deploy_decision.items():
            want_element = element
            a = want_element = Acct_data[Acct_data[want_column] == want_element]
            row_index = a.index.tolist()
            row_index = row_index[0]
            # print(want_element)
            # print(row_index)
            want_element = want_element.loc[[row_index], [actual_result]]
            want_element = np.array(want_element)
            want_element = want_element.tolist()
            b = want_element = want_element[0][0]
            want_element = int(want_element, 16)
            if (want_element == 65535 and value == 0) or (want_element != 65535 and value != 0):
                # print(want_element - value)
                Acct_data.loc[[row_index], ['Expect']] = b
                Acct_data.loc[[row_index], ['Judge']] = 'Pass'
            else:
                Acct_data.loc[[row_index], ['Expect']] = hex(value)
                Acct_data.loc[[row_index], ['Judge']] = 'Fail'

        for element, value in my_check_list_tolerance.items():
            want_element = element
            a = want_element = Acct_data[Acct_data[want_column] == want_element]
            row_index = a.index.tolist()
            row_index = row_index[0]
            want_element = want_element.loc[[row_index], [actual_result]]
            want_element = np.array(want_element)
            want_element = want_element.tolist()
            b = want_element = want_element[0][0]
            want_element = int(want_element, 16)

            if abs(want_element - value) <= 10:
                # print(want_element - value)
                Acct_data.loc[[row_index], ['Expect']] = b
                Acct_data.loc[[row_index], ['Judge']] = 'Pass'
            else:
                Acct_data.loc[[row_index], ['Expect']] = hex(value)
                Acct_data.loc[[row_index], ['Judge']] = 'Fail'
        # print(Acct_data)
        # filename = path.split('/')
        # save_name = filename[4]
        # Check_result_path = "C://Project/GAC_A39/EDR_Test_logs/EDR_Check_Result/"
        # Result_Analyze = Check_result_path + save_name
        # Result_writer = pd.ExcelWriter(Result_Analyze)
        Acct_data.to_excel(Result_writer, current_edr)
        workbook1 = Result_writer.book
        worksheets = Result_writer.sheets
        worksheet1 = worksheets[current_edr]
        format1 = workbook1.add_format(
            {'bg_color': '#FFC7CE', 'font_color': '#9C0006', 'bold': True, 'align': 'left', 'valign': 'top',
             'text_wrap': True})
        worksheet1.set_column("B:B", 100)
        worksheet1.set_column("C:D", 36)
        worksheet1.set_column("E:E", 36, cell_format=format1)

    sleep(1)
    important_information.to_excel(Result_writer, 'useful_info', index=False)
    Result_writer.save()
    sleep(2)
    finished_case = 'C:\\Project\\GAC_A39\\EDR_Test_logs\\__check_finished\\'
    current_case = path
    check_exisit = finished_case + current_case.split('/')[4]
    check_exisit_2 = finished_case + edr_info_path.split('/')[4]
    if os.path.exists(check_exisit):
        os.remove(check_exisit)
    # if os.path.exists(check_exisit_2):
    #     os.remove(check_exisit_2)
    shutil.move(current_case, finished_case)
    # shutil.move(edr_info_path, finished_case)
    print('***' + save_name + '_has been created ok in your PC, You can see the result now!!!***')


button_1 = Button(root, text='ST1: Select EDR_result.xlsx', background='#ffffc0', command=open_files_xlsx, font=14)
button_2 = Button(root, text='ST2：Select txt files', background='#fff1c0', command=open_files_txt, font=14)
button_3 = Button(root, text='ST3： Check ST1&ST2 ', background='Yellow', command=check_selected_files, font=14)
button_4 = Button(root, text='ST4： Output Result ', background='#ff9800', command=output_edr_result, font=14)
button_1.pack(side=TOP, fill=BOTH, expand=YES)
button_2.pack(side=TOP, fill=BOTH, expand=YES)
button_3.pack(side=TOP, fill=BOTH, expand=YES)
button_4.pack(side=TOP, fill=BOTH, expand=YES)
root.resizable(width=FALSE, height=FALSE)
canvas.pack()
root.geometry('+1100+200')
root.mainloop()