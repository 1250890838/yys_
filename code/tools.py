from mycode import cap
import numpy
import cv2.cv2 as cv
import tkinter as tk
import win32gui,win32api,win32con
from win32con import *
from mycode.settings import *
from mycode import app
import aircv as ac
from PIL import ImageGrab
import time

def fetch_image():
    '''
    截图并返回图的数组
    '''
    try:
        (x1, y1, x2, y2), handle = get_window_pos(yys_name)
    except:
        return NOTFOUND
    while True:
        try:
        # 发送还原最小化窗口的信息
            win32gui.SendMessage(handle, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
        # 设为高亮
            win32gui.SetForegroundWindow(handle)
        # 截图
            grab_image = ImageGrab.grab((x1, y1, x2, y2))
            src = cv.cvtColor(numpy.asarray(grab_image), cv.COLOR_RGB2BGR)
            return src
        except:
            pass

def pHash(img):
    '''
    感知哈希算法
    '''
    try:
        gray = cv.cvtColor(img, cv2.COLOR_BGR2GRAY)
    except:
        image = cv.cvtColor(numpy.asarray(img), cv.COLOR_RGB2BGR)
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    img = cv.resize(gray, (32, 32))
    # 将灰度图转为浮点型，再进行dct变换
    dct = cv.dct(numpy.float32(gray))
    # opencv实现的掩码操作
    dct_roi = dct[0:8, 0:8]

    hash = []
    avreage = numpy.mean(dct_roi)
    for i in range(dct_roi.shape[0]):
        for j in range(dct_roi.shape[1]):
            if dct_roi[i, j] > avreage:
                hash.append(1)
            else:
                hash.append(0)
    return hash
def howdiffer(img1,img2,n=64):
    """
        通过掉用phash比较两张图片相似度，返回值越小差别越小
    """
    num1=pHash(img1)
    num2=pHash(img2)
    differ=0
    tl=zip(num1,num2)
    for c1,c2 in tl:
        if c1!=c2:
            differ+=1
        else:
            pass
    return int(differ)
def get_window_pos(name):
    '''
        返回坐标值及句柄
    '''
    handle = win32gui.FindWindow(0, name)
    if handle == 0:
        raise Exception("没找到阴阳师窗口")
    else:
        return win32gui.GetWindowRect(handle), handle
def get_hwnd(name): #返回窗口句柄
    handle = win32gui.FindWindow(0, name)
    if handle == 0:
        raise Exception("没找到阴阳师窗口")
    return handle
def judge_juexing_type(juexing):
    '''
        判断要打的觉醒类型，返回相应图片
    '''
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
    """

    :param chose_siji: 司机
    :param chose_dashou: 打手
    :return: 元组(图片，图片)
    """
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
def recognize_state(state,content):
    if state == NOTFOUND:
        content.insert(tk.END, "没有识别到阴阳师窗口\n")
        return YERROR
    elif state == INCON:
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
    while True:  # 无限单击至界面出现
        src = fetch_image()
        if howdiffer(src,type) <= 5:
            break
        left_click(hwnd, pos, False)
def WAIT_UNTIL(background):
    while True:
        src = fetch_image()
        if  howdiffer(src,background)<= 5:
            return src
        else:
            pass
def WAIT_SEARCH(search):
    while True:
        src = fetch_image()
        search_pos = ac.find_template(src,search, 0.5)
        if search_pos == None:
            continue
        else:
            return search_pos
def LCLICK_UNTIL_TWO(hwnd,pos,backgroundone,backgroundtwo):
    while True:
        src = fetch_image()
        if howdiffer(src,backgroundone) <= 5 \
                or howdiffer(src,backgroundtwo) <= 5:
            return
        left_click(hwnd,pos,False)
def WAIT_UNTIL_TWO(backgroundone,backgroundtwo):
    while True:
        src = fetch_image()
        if howdiffer(src,backgroundone) <= 5 \
                or howdiffer(src,backgroundtwo) <= 5:
            return
def if_exist_lclick(hwnd,search,degree):
    try:
        src=fetch_image()
        pos=ac.find_template(src,search,degree)
    except:
        return
    if pos==None:
        return
    else:
        left_click(hwnd,pos)
def confirm_left_click(hwnd,pos,background):
    while True:
        left_click(hwnd, pos)  # 左键单击参数(挑战按钮)位置
        src = fetch_image()
        if howdiffer(background, src) >= 10:
            return
def match(content,img1):
    img=fetch_image()
    if(howdiffer(img,img1)<=10):
        return 0
    else:
        content.insert(tk.END,"单人觉醒启动失败\n")
        return INCON

