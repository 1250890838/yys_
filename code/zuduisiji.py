from mycode.tools import *
def zudui_siji(hwnd,content,chose_siji,chose_dashou,strict): #组队司机模式
    frequency=0
    content.insert(tk.END, "已选择组队觉醒\n")
    ret=judge_team(chose_siji, chose_dashou)
    if ret==NOSUIT:
        return
    backgroundone=ret[0]
    backgroundtwo=ret[1]
    first = True
    match(content,backgroundone)
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
            src = fetch_image()
            pos_over = ac.find_template(src, play_over, 0.5)
            if pos_over != None:
                pos_over['result']=(50,150)
                if first != True:
                    LCLICK_UNTIL_TWO(hwnd,pos_over,backgroundone, backgroundtwo)
                else: #第一次
                    while True:
                        src=fetch_image()
                        pos = ac.find_template(src, zd_first, 0.6)
                        yes = cap.howdiffer(src,backgroundone) <= 5 \
                                or cap.howdiffer(src, backgroundtwo) <= 5
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