import time
import numpy as np
import cv2.cv2
import cv2.cv2 as cv
import numpy
import win32gui, win32ui, win32con, win32api
from PIL import ImageGrab
from mycode.settings import  *
def howdiffer(a,b,n=64):
    differ=0
    #cl1=[ c1 for c1 in a]
    #cl2=[ c2 for c2 in b]
    tl=zip(a,b)
    for c1,c2 in tl:
        if c1!=c2:
            differ+=1
        else:
            pass
    return str(differ)
def get_window_pos(name): #返回坐标值及句柄
    handle = win32gui.FindWindow(0, name)
    # 获取窗口句柄
    if handle == 0:
        raise Exception("没找到阴阳师窗口")
    else:
        # 返回坐标值和handle
        return win32gui.GetWindowRect(handle), handle
def get_window_pos_clear(name): #返回窗口句柄
    handle = win32gui.FindWindow(0, name)
    if handle == 0:
        raise Exception("没找到阴阳师窗口")
    return handle
def fetch_image():
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
            return grab_image
        except:
            pass

def aHash(img):
    try:
        gray = cv.cvtColor(img, cv2.COLOR_BGR2GRAY)
    except:
        image = cv.cvtColor(numpy.asarray(img), cv.COLOR_RGB2BGR)
        gray = cv.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv.resize(gray, (8,8))
    s = 0
    hash_str = ''
    for i in range(8):
        for j in range(8):
            s = s+gray[i, j]
    avg = s/64
    for i in range(8):
        for j in range(8):
            if gray[i, j] > avg:
                hash_str = hash_str+'1'
            else:
                hash_str = hash_str+'0'
    return hash_str


def pHash(img):
    # 感知哈希算法
    # 缩放32*32
    try:
        gray = cv.cvtColor(img, cv2.COLOR_BGR2GRAY)
    except:
        image = cv.cvtColor(numpy.asarray(img), cv.COLOR_RGB2BGR)
        gray = cv.cvtColor(image, cv2.COLOR_BGR2GRAY)

    img = cv2.resize(gray, (32, 32))  # , interpolation=cv2.INTER_CUBIC
    # 将灰度图转为浮点型，再进行dct变换
    dct = cv2.dct(np.float32(gray))
    # opencv实现的掩码操作
    dct_roi = dct[0:8, 0:8]

    hash = []
    avreage = np.mean(dct_roi)
    for i in range(dct_roi.shape[0]):
        for j in range(dct_roi.shape[1]):
            if dct_roi[i, j] > avreage:
                hash.append(1)
            else:
                hash.append(0)
    return hash


