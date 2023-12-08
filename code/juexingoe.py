from mycode.tools import *
def juexing_one(hwnd,content,chose_siji,strict): #单人觉醒模式
    frequency = 0  # 统计刷副本次数
    content.insert(tk.END, "已选择单人觉醒\n")
    type = judge_juexing_type(chose_siji)  # 选择麒麟类型
    state = match(content,type)
    state = recognize_state(state, content)
    if state == YERROR:
        return
    while (frequency!=strict):  # 开始刷
        src = fetch_image()
        pos = ac.find_template(src, jx_bg, 0.5)  # 识别挑战按钮
        if pos == None:
            continue
        confirm_left_click(hwnd,pos,type)
        while True:
            src = fetch_image()
            pos = ac.find_template(src, play_over)  # 识别结束按钮
            if pos != None:
                LCLICK_UNTIL(hwnd,type,pos) #不断进行这个函数直到第二个参数type出现
                break
        frequency += 1
        content.insert(tk.END, "第" + str(frequency) + "次\n")
        if app.ifstop: #检测是否按下了停止键
            content.insert(tk.END, "已停止\n")
            return
