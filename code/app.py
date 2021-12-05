import tkinter as tk
from functools import partial
import cv2.cv2 as cv
import numpy
import time
import threading
import aircv as ac
from mycode.settings import *
from mycode import tools
from tkinter.font import Font
from tkinter import ttk
from mycode.zuduisiji import zudui_siji
from mycode.juexingone import juexing_one
from mycode.yuhunone import yuhun_one
from mycode.yeyuanhuo import yyh_one
from mycode.zuduidashou import zudui_dashou
class Application(tk.Tk):
    def __init__(self,title, master=None):
        tk.Tk.__init__(self,master)
        self.geometry("500x300")
        self.resizable(width=False,height=False)
        myFont = Font(family="Times New Roman", size=12)
        self.state = tk.Text(self,width=30,height=15)
        self.state.configure(font=myFont)
        self.state.pack(side=tk.LEFT,padx=10,pady=10)
        self.father_fr=tk.Frame(self)
        self.father_fr.pack()
        self.fr=tk.Frame(self.father_fr)
        self.fr.pack()
        self.ofr=tk.Frame(self.father_fr)
        self.ofr.pack()
        choose1 = ('单人觉醒', '组队觉醒/御魂/魂土(司机)','组队觉醒/御魂/魂土(打手)','单人御魂1~10','业原火')
        self.cmb1 = ttk.Combobox(self.fr,state='readonly',value=choose1,width=15)
        self.cmb1.grid(row=0, column=0,columnspan=1)
        self.cmb1.set(choose1[0])
        self.cmb2 = ttk.Combobox(self.fr, state='readonly',width=5,value=ql_type)
        self.cmb2.grid(row=1, column=0, columnspan=1)
        self.cmb2.set(ql_type[0])
        self.cmb3 = ttk.Combobox(self.fr, state='readonly',width=5)
        self.cmb3.grid(row=1, column=1, columnspan=1)
        self.cmb1.bind("<<ComboboxSelected>>",lambda event:change_relation(self.cmb1,self.cmb2,self.cmb3))
        self.entry=ttk.Entry(self.fr,width=5)
        self.entry.grid(row=2,column=2)
        self.button=tk.Button(self.fr,text="开刷",bg="yellow",command=partial(launch,self.state,self.cmb1,self.cmb2,self.cmb3,self.entry),pady=10,height=1)
        self.button.grid(row=2,column=0,padx=5)
        self.butst=tk.Button(self.fr,text="测试",command=testi,pady=10,height=1)
        self.butst.grid(row=2,column=1,padx=5)
        MODES=[
                ("接受", "yes"),
                ("拒绝", "no"),
        ]
        v = tk.StringVar()
        for text, mode in MODES:
            b = tk.Radiobutton(self.ofr, text=text,
                            variable=v, value=mode,command=partial(selection,v))
            b.pack(anchor="w")

def launch(content,choose1,choose2,choose3,frequency): #启动线程，开刷
    jxthread=Jxthread(content,choose1,choose2,choose3,frequency)
    jxthread.setDaemon(True)
    jxthread.start()
    invatethread=InvateThread()
    invatethread.setDaemon(True)
    invatethread.start()

class Jxthread(threading.Thread): #主线程，调用play函数
    def __init__(self,content,chose1,chose2,chose3,frequency):
        self.content=content
        self.chose1=chose1
        self.chose2=chose2
        self.chose3=chose3
        self.frequency=frequency
        threading.Thread.__init__(self)
    def run(self):
        play(self.content,self.chose1,self.chose2,self.chose3,self.frequency)

def play(content,chose_mode,chose_siji,chose_dashou,frequency): #
    global main_thread_exist
    frequency=int(frequency.get())
    hwnd = tools.get_hwnd(yys_name)
    if hwnd==None:
        content.insert(tk.END,"没有找到阴阳师窗口\n")
        main_thread_exist=False
    if(chose_mode.get()=="单人觉醒"):
        juexing_one(hwnd,content,chose_siji,frequency)
    elif chose_mode.get()=="组队觉醒/御魂/魂土(司机)":
        zudui_siji(hwnd, content, chose_siji, chose_dashou,frequency)
    elif chose_mode.get()=="单人御魂1~10":
        yuhun_one(hwnd,content,frequency)
    elif chose_mode.get()=="业原火":
        yyh_one(hwnd,content,frequency)
    elif chose_mode.get()=="组队觉醒/御魂/魂土(打手)":
        zudui_siji(hwnd,content,chose_siji,chose_dashou,frequency)
    main_thread_exist=False

class InvateThread(threading.Thread): #查看是否有协同邀请任务的线程
    def __init__(self):
        pass
        threading.Thread.__init__(self)
    def run(self):
        main_thread_exist=True
        wait_invate()
def wait_invate():
    hwnd=tools.get_hwnd(yys_name)
    while main_thread_exist:
        tools.if_exist_lclick(hwnd,invate_chose,0.8)
        time.sleep(2)
def testi(): #测试用
    src=tools.fetch_image()
    search=cv.imread(r"D:\PyCharm Community Edition 2021.1.1\pythonProject\venv\image\jxbegin.PNG")
    pos=ac.find_template(src,search,0.5)

def change_relation(cmb1,cmb2,cmb3): #combobox select操作触发的回调函数
    cmb1_text=cmb1.get()
    if cmb1_text=="组队觉醒/御魂/魂土(司机)" or cmb1_text=="组队觉醒/御魂/魂土(打手)" :
        cmb2["value"]=yys_choose #settings.py
        cmb3["value"]=yys_choose
        cmb2.set(yys_choose[0])
        cmb3.set(yys_choose[0])
    elif cmb1_text=="单人觉醒":
        cmb2["value"]=ql_type
        cmb3["value"] = ()
        cmb2.set(ql_type[0])
        cmb3.set("")
    else:
        cmb2["value"]=()
        cmb3["value"]=()
        cmb2.set("")
        cmb3.set("")

def selection(radio):
    global invate_chose
    if(radio.get()=="yes"):
        invate_chose=invate_yes
    else:
        invate_chose=invate_no



