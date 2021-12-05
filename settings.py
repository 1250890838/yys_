import cv2.cv2 as cv
#主线程是否还活着
main_thread_exist=True
#是否停止
ifstop=False
#选择
yys_choose=("晴明","神乐")
ql_type=("火","风","水","雷")
#名字
yys_name="阴阳师-网易游戏"
#统一结束按钮
play_over = cv.imread(r"D:\PyCharm Community Edition 2021.1.1\pythonProject\venv\image\jxover.PNG") #单人觉醒结束按钮
#t
invate=cv.imread(r"D:\PyCharm Community Edition 2021.1.1\pythonProject\venv\image\first.PNG")
#单人觉醒
jx_backh=cv.imread(r"D:\PyCharm Community Edition 2021.1.1\pythonProject\venv\image\jx_backh.PNG")  #单人觉醒背景
jx_backf=cv.imread(r"D:\PyCharm Community Edition 2021.1.1\pythonProject\venv\image\jx_backf.PNG")
jx_backs=cv.imread(r"D:\PyCharm Community Edition 2021.1.1\pythonProject\venv\image\jx_backs.PNG")
jx_backl=cv.imread(r"D:\PyCharm Community Edition 2021.1.1\pythonProject\venv\image\jx_backl.PNG")
jx_bg = cv.imread(r"D:\PyCharm Community Edition 2021.1.1\pythonProject\venv\image\jxbegin.PNG") #单人觉醒挑战按钮
"""
HQL=1 #火麒麟
FQL=2 #风麒麟
SQL=3 #水麒麟
LQL=4 #雷麒麟
"""
#组队
invate_yes=cv.imread(r"D:\PyCharm Community Edition 2021.1.1\pythonProject\venv\image\invate_yes.PNG")
invate_no=cv.imread(r"D:\PyCharm Community Edition 2021.1.1\pythonProject\venv\image\invate_no.PNG")
invate_chose=invate_yes
zd_bg=cv.imread(r"D:\PyCharm Community Edition 2021.1.1\pythonProject\venv\image\jxsbegin.PNG") #组队觉醒挑战按钮
zd_first=cv.imread(r"D:\PyCharm Community Edition 2021.1.1\pythonProject\venv\image\jxfirst.PNG") #第一次觉醒识别图片
zd_backqs=cv.imread(r"D:\PyCharm Community Edition 2021.1.1\pythonProject\venv\image\jxsbackqs.PNG") #晴明+神乐-觉醒
zd_backqq=cv.imread(r"D:\PyCharm Community Edition 2021.1.1\pythonProject\venv\image\jxsbackqq.PNG") #晴明+晴明-觉醒
zd_backss=cv.imread(r"D:\PyCharm Community Edition 2021.1.1\pythonProject\venv\image\jxsbackss.PNG") #神乐＋神乐-觉醒
zd_backsq=cv.imread(r"D:\PyCharm Community Edition 2021.1.1\pythonProject\venv\image\jxsbacksq.PNG") #神乐+晴明-觉醒
zd_backq=cv.imread(r"D:\PyCharm Community Edition 2021.1.1\pythonProject\venv\image\jxsbackq.PNG") #晴明单人
zd_backs=cv.imread(r"D:\PyCharm Community Edition 2021.1.1\pythonProject\venv\image\jxsbacks.PNG") #神乐单人
zd_auto=cv.imread(r"D:\PyCharm Community Edition 2021.1.1\pythonProject\venv\image\autoplay.PNG")
zd_confirm=cv.imread(r"D:\PyCharm Community Edition 2021.1.1\pythonProject\venv\image\conplay.PNG")
choose=cv.imread(r"D:\PyCharm Community Edition 2021.1.1\pythonProject\venv\image\choose.PNG")
#御魂
yh_back=cv.imread(r"D:\PyCharm Community Edition 2021.1.1\pythonProject\venv\image\yhback.PNG")
yh_begin=cv.imread(r"D:\PyCharm Community Edition 2021.1.1\pythonProject\venv\image\yhbegin.PNG")
#业原火
yyh_back=cv.imread(r"D:\PyCharm Community Edition 2021.1.1\pythonProject\venv\image\yyhback.PNG")
yyh_bg=cv.imread(r"D:\PyCharm Community Edition 2021.1.1\pythonProject\venv\image\yyhchibg.PNG")






#测试
test1=cv.imread(r"D:\PyCharm Community Edition 2021.1.1\pythonProject\venv\image\htsbackqq.PNG")
test2=cv.imread(r"D:\PyCharm Community Edition 2021.1.1\pythonProject\venv\image\htsbacksq.PNG")
test3=cv.imread(r"D:\PyCharm Community Edition 2021.1.1\pythonProject\venv\image\test3.PNG")
jxthread=None #觉醒线程

#状态码
NOTFOUND=-1 #没有找到阴阳师窗口
INCON=-2 #将阴阳师设为前台失败3
FETCH_ERROR=-3
YERROR=-4
NOSUIT=-5
# 窗口最好是1200*700左右



