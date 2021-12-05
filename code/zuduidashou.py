from mycode.tools import *
def zudui_dashou(hwnd,content,chose_siji,chose_dashou,strict): #组队-打手模式
    frequency = 0
    content.insert(tk.END, "已选择组队模式（打手）\n")
    ret = judge_team(chose_siji, chose_dashou)
    if ret == NOSUIT:
        return
    backgroundone = ret[0]
    backgroundtwo = ret[1]
    first = True
    match(content,backgroundone)
    state = recognize_state(state, content)
    if state == YERROR:
        return
    pos=WAIT_SEARCH(play_over)
    pos["result"]=(50,150)
    while True:
        src=fetch_image()
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
            src=fetch_image()
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
                src = fetch_image()
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
