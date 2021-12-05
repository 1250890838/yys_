from mycode import cap
import numpy
import cv2.cv2 as cv
import tkinter as tk
import win32gui,win32api
from win32con import *
from mycode.settings import *
from mycode import app
import aircv as ac
import time
def judge_juexing_type(juexing):
    #判断要打的觉醒类型，返回相应图片
    type=juexing.get()
    if type=="火":
        type=jx_backh
    elif type=="水":
        type=jx_backs
    elif type=="风":
        type=jx_backf
    else:
        type=jx_backl
    return type
def judge_team(chose_siji,chose_dashou):
    siji = chose_siji.get()
    dashou = chose_dashou.get()
    if siji == "晴明" and dashou == "晴明":
        backgroundtwo = zd_backqq
        backgroundone = zd_backq
    elif siji == "晴明" and dashou == "神乐":
        backgroundtwo = zd_backqs
        backgroundone = zd_backq
    elif siji == "神乐" and dashou == "晴明":
        backgroundtwo = zd_backsq
        backgroundone = zd_backs
    elif siji == "神乐" and dashou == "神乐":
        backgroundtwo = zd_backss
        backgroundone = zd_backs
    else:
        content.insert(tk.END, "没有选择合适的角色!")
        return NOSUIT
    return (backgroundone,backgroundtwo)
def fetch_image_and_convert():
    src = cap.fetch_image()
    src = cv.cvtColor(numpy.asarray(src), cv.COLOR_RGB2BGR)
    return src
def recognize_state(state,content):
    if state == NOTFOUND:  # 阴阳师窗口没找到,退出线程
        content.insert(tk.END, "没有识别到阴阳师窗口\n")
        return YERROR
    elif state == INCON:  # 没有把界面拖到单人觉醒的界面,退出线程
        content.insert(tk.END, "没有识别到单人觉醒的界面\n")
        return YERROR
    else:
        content.insert(tk.END, "已识别到了单人觉醒界面\n")
        return 0
def left_click(hwnd,pos,deletion=True):
    x, y = pos['result']
    if deletion:
        lparam = win32api.MAKELONG(int(x-10), int(y-30))
    else:
        lparam = win32api.MAKELONG(int(x), int(y))
    win32gui.PostMessage(hwnd, WM_LBUTTONDOWN, None, lparam);
    win32gui.PostMessage(hwnd, WM_LBUTTONUP, None, lparam);
def left_click_xy(hwnd,x,y,deletion=True):
    if deletion:
        lparam = win32api.MAKELONG(int(x - 10), int(y - 30))
    else:
        lparam = win32api.MAKELONG(int(x), int(y))
    win32gui.PostMessage(hwnd, WM_LBUTTONDOWN, None, lparam);
    win32gui.PostMessage(hwnd, WM_LBUTTONUP, None, lparam);
def LCLICK_UNTIL(hwnd,type,pos):
    while True:  # 无限单击至单人觉醒界面出现
        src = cap.fetch_image()
        if int(cap.howdiffer(cap.pHash(src), cap.pHash(type))) <= 5:
            break
        left_click(hwnd, pos, False)
def WAIT_UNTIL(background):
    while True:
        src = cap.fetch_image()
        if  int(cap.howdiffer(cap.pHash(src), cap.pHash(background)))<= 4:
            src = cv.cvtColor(numpy.asarray(src), cv.COLOR_RGB2BGR)
            return src
        else:
            pass
def WAIT_SEARCH(search):
    while True:
        src = fetch_image_and_convert()
        search_pos = ac.find_template(src,search, 0.5)
        if search_pos == None:
            continue
        else:
            return search_pos
def LCLICK_UNTIL_TWO(hwnd,pos,backgroundone,backgroundtwo):
    while True:
        src = cap.fetch_image()
        if int(cap.howdiffer(cap.pHash(src), cap.pHash(backgroundone))) <= 5 \
                or int(cap.howdiffer(cap.pHash(src), cap.pHash(backgroundtwo))) <= 5:
            return
        left_click(hwnd,pos,False)
def WAIT_UNTIL_TWO(backgroundone,backgroundtwo):
    while True:
        src = cap.fetch_image()
        if int(cap.howdiffer(cap.pHash(src), cap.pHash(backgroundone))) <= 5 \
                or int(cap.howdiffer(cap.pHash(src), cap.pHash(backgroundtwo))) <= 5:
            return
def if_exist_lclick(hwnd,search,degree):
    try:
        src=fetch_image_and_convert()
        pos=ac.find_template(src,search,degree)
    except:
        return
    if pos==None:
        return
    else:
        left_click(hwnd,pos)
def juexing_one(hwnd,content,chose_siji,strict):
    frequency = 0  # 统计刷副本次数
    content.insert(tk.END, "已选择单人觉醒\n")
    type = judge_juexing_type(chose_siji)  # 选择麒麟类型
    state = app.jxmatch(content, type)  # 觉醒图片匹配
    state = recognize_state(state, content)
    if state == YERROR:
        return
    while (frequency!=strict):  # 开始刷
        src = fetch_image_and_convert()
        pos = ac.find_template(src, jx_bg, 0.5)  # 识别挑战按钮
        if pos == None:
            continue
        confirm_left_click(hwnd,pos,type)
        while True:
            src = fetch_image_and_convert()
            pos = ac.find_template(src, play_over)  # 识别结束按钮
            if pos != None:
                LCLICK_UNTIL(hwnd,type,pos) #不断进行这个函数直到第二个参数type出现
                break
        frequency += 1
        content.insert(tk.END, "第" + str(frequency) + "次\n")
        if app.ifstop: #检测是否按下了停止键
            content.insert(tk.END, "已停止\n")
            return
def juexing_two(hwnd,content,chose_siji,chose_dashou,strict):
    frequency=0
    content.insert(tk.END, "已选择组队觉醒\n")
    ret=judge_team(chose_siji, chose_dashou)
    if ret==NOSUIT:
        return
    backgroundone=ret[0]
    backgroundtwo=ret[1]
    first = True
    state = app.jxsmatch(content)
    state=recognize_state(state,content)
    if state == YERROR:
        return
    while frequency!=strict:
        src=WAIT_UNTIL(backgroundtwo)
        pos = ac.find_template(src,zd_bg)
        if pos==None:
            continue
        confirm_left_click(hwnd,pos,backgroundtwo)
        while True:
            src = fetch_image_and_convert()
            pos_over = ac.find_template(src, play_over, 0.5)
            if pos_over != None:
                pos_over['result']=(50,150)
                if first != True:
                    LCLICK_UNTIL_TWO(hwnd,pos_over,backgroundone, backgroundtwo)
                else: #第一次
                    while True:
                        src=fetch_image_and_convert()
                        pos = ac.find_template(src, zd_first, 0.6)
                        yes = int(cap.howdiffer(cap.pHash(src), cap.pHash(backgroundone))) <= 5 \
                                or int(cap.howdiffer(cap.pHash(src), cap.pHash(backgroundtwo))) <= 5
                        if pos == None and yes == False:
                            left_click(hwnd,pos_over,False)
                        elif pos:
                            x,y=pos["result"]
                            pos["result"]=(x-100,y-60)
                            left_click(hwnd,pos)
                            pos["result"]=(x,y)
                            left_click(hwnd,pos)
                            first = False
                            break
                        else:
                            first = False
                            break
                break
        frequency += 1
        content.insert(tk.END, "第" + str(frequency) + "次\n")
        if app.ifstop:  # 检测是否按下了停止键
            content.insert(tk.END, "已停止\n")
            return
def yuhun_one(hwnd,content,strict):
    frequency = 0  # 统计刷副本次数
    content.insert(tk.END, "已选择单人御魂\n")
    state = app.jxmatch(content,yh_back)  # 御魂图片匹配
    state = recognize_state(state, content)
    if state == YERROR:
        return
    while (frequency!=strict):  # 开始刷
        src = fetch_image_and_convert()
        pos = ac.find_template(src, yh_begin, 0.5)  # 识别挑战按钮
        if pos == None:
            continue
        confirm_left_click(hwnd,pos,yh_back)
        while True:
            src = fetch_image_and_convert()
            pos = ac.find_template(src, play_over)  # 识别结束按钮
            if pos != None:
                LCLICK_UNTIL(hwnd,yh_back, pos)  # 不断进行这个函数直到第二个参数type出现
                break
        frequency += 1
        content.insert(tk.END, "第" + str(frequency) + "次\n")
        if app.ifstop:  # 检测是否按下了停止键
            content.insert(tk.END, "已停止\n")
            return
def yyh_one(hwnd,content,strict):
    frequency = 0  # 统计刷副本次数
    content.insert(tk.END, "已选择单人御魂\n")
    state = app.jxmatch(content, yyh_back) #御魂图片匹配
    state = recognize_state(state, content)
    if state == YERROR:
        return
    while (frequency!=strict):  # 开始刷
        src = fetch_image_and_convert()
        pos = ac.find_template(src,yyh_bg, 0.5)  # 识别挑战按钮
        if pos == None:
            continue
        confirm_left_click(hwnd,pos,yyh_back)
        while True:
            src = fetch_image_and_convert()
            pos = ac.find_template(src, play_over)  # 识别结束按钮
            if pos != None:
                LCLICK_UNTIL(hwnd,yyh_back,pos)  # 不断进行这个函数直到第二个参数type出现
                break
        frequency += 1
        content.insert(tk.END, "第" + str(frequency) + "次\n")
        if app.ifstop:  # 检测是否按下了停止键
            content.insert(tk.END, "已停止\n")
            return
def zd_dashou(hwnd,content,chose_siji,chose_dashou,strict):
    frequency = 0
    content.insert(tk.END, "已选择组队模式（打手）\n")
    ret = judge_team(chose_siji, chose_dashou)
    if ret == NOSUIT:
        return
    backgroundone = ret[0]
    backgroundtwo = ret[1]
    first = True
    state = app.jxsmatch(content)
    state = recognize_state(state, content)
    if state == YERROR:
        return
    hwnd = cap.get_window_pos_clear("阴阳师-网易游戏")
    pos=WAIT_SEARCH(play_over)
    pos["result"]=(50,150)
    while True:
        src=fetch_image_and_convert()
        left_click(hwnd,pos,False)
        auto_pos = ac.find_template(src, zd_auto, 0.8)
        con_pos = ac.find_template(src, zd_confirm, 0.8)
        if auto_pos or con_pos:
            break
    if auto_pos:
        left_click(hwnd,auto_pos)
        yes_pos=WAIT_SEARCH(zd_first)
        left_click(hwnd,yes_pos)
        WAIT_UNTIL_TWO(backgroundone,backgroundtwo)
        while frequency!=strict:
            src=fetch_image_and_convert()
            pos = ac.find_template(src, play_over, 0.5)
            if pos == None:
                continue
            else:
                LCLICK_UNTIL_TWO(hwnd,pos,backgroundone,backgroundtwo)
                frequency += 1
                content.insert(tk.END, "第" + str(frequency) + "次\n")
    elif con_pos:
        left_click(hwnd,con_pos)
        while frequency!=strict:
            WAIT_UNTIL_TWO(backgroundone, backgroundtwo)
            over_pos=WAIT_SEARCH(play_over)
            while True:
                src = fetch_image_and_convert()
                over_pos["result"]=(50,150)
                left_click(hwnd,over_pos)
                auto_pos = ac.find_template(src, zd_auto, 0.8)
                con_pos = ac.find_template(src, zd_confirm, 0.8)
                if not (auto_pos or con_pos):
                    continue
                if auto_pos:
                    left_click(hwnd, auto_pos)
                    yes_pos = WAIT_SEARCH(zd_first)
                    left_click(hwnd, yes_pos)
                    WAIT_UNTIL_TWO(backgroundone, backgroundtwo)
                    while frequency!=strict:
                        src = fetch_image_and_convert()
                        pos = ac.find_template(src, play_over, 0.5)
                        if pos == None:
                            continue
                        else:
                            LCLICK_UNTIL_TWO(hwnd, pos, backgroundone, backgroundtwo)
                            frequency += 1
                            content.insert(tk.END, "第" + str(frequency) + "次\n")
                    return
                elif con_pos:
                    left_click(hwnd,con_pos)
                    break
            frequency += 1
            content.insert(tk.END, "第" + str(frequency) + "次\n")


def confirm_left_click(hwnd,pos,background):
    while True:
        left_click(hwnd, pos)  # 左键单击参数(挑战按钮)位置
        src = fetch_image_and_convert()
        if int(cap.howdiffer(cap.pHash(background), cap.pHash(src))) >= 10:
            return