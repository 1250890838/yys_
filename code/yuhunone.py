from mycode.tools import *
def yuhun_one(hwnd,content,strict): #单人御魂模式
    frequency = 0  # 统计刷副本次数
    content.insert(tk.END, "已选择单人御魂\n")
    state = match(content,yh_back)
    state = recognize_state(state, content)
    if state == YERROR:
        return
    while (frequency!=strict):  # 开始刷
        src = fetch_image()
        pos = ac.find_template(src, yh_begin, 0.5)  # 识别挑战按钮
        if pos == None:
            continue
        confirm_left_click(hwnd,pos,yh_back)
        while True:
            src = fetch_image()
            pos = ac.find_template(src, play_over)  # 识别结束按钮
            if pos != None:
                LCLICK_UNTIL(hwnd,yh_back, pos)  # 不断进行这个函数直到第二个参数type出现
                break
        frequency += 1
        content.insert(tk.END, "第" + str(frequency) + "次\n")
        if app.ifstop:  # 检测是否按下了停止键
            content.insert(tk.END, "已停止\n")
            return