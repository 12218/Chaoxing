import tkinter
from tkinter import ttk
from tkinter import scrolledtext
import requests
import re
from bs4 import BeautifulSoup
import json
import os
import time
import sys
import threading
import webbrowser


def multi_find():
    args = []
    source = input_entry.get()
    soup = BeautifulSoup(source, features='lxml')
    questions = soup.find_all('div', {'class': 'clearfix', 'style': 'line-height: 35px; font-size: 14px;padding-right:15px;'})
    try:
        for question in questions:
            if '(' in question.text:
                if '.' in question.text:
                    final_operate_question = re.findall(
                        r'\.(.+)\(', question.text)
                    args.append(final_operate_question[0])
                elif '】' in question.text:
                    final_operate_question = re.findall(
                        r'】(.+)\(', question.text)
                    args.append(final_operate_question[0])
                else:
                    final_operate_question = re.findall(
                        r'(.+)\(', question.text)
                    args.append(final_operate_question[0])
            else:
                if '.' in question.text:
                    final_operate_question = re.findall(
                        r'\.(.+)\。', question.text)
                    args.append(final_operate_question[0])
                elif '】' in question.text:
                    final_operate_question = re.findall(
                        r'】(.+)\。', question.text)
                    args.append(final_operate_question[0])
                else:
                    final_operate_question = re.findall(
                        r'(.+)\。', question.text)
                    args.append(final_operate_question[0])
    except:
        print('  Error:正则表达式匹配发生错误!')
    return(args)


def single_find():
    args = []
    source = input_entry.get()
    args.append(source)
    return args


def find_answers(a_args):
    i = 0
    count = 0
    url = 'https://cx.icodef.com/v2/answer'
    data = {}
    if len(a_args) != 0:
        for i in range(len(a_args)):
            data['topic[0]'] = a_args[i]
            # print(data)
            try:
                html = requests.post(url, data=data, timeout=5)
                time.sleep(1)
                json_data = html.json()[0]['result']
                count += 1
                output_text.insert('end', '第%d题:' % (count) + '\n', a_args[i])
                if len(json_data) == 0:
                    output_text.insert('end', '  Warning:未在题库中找到匹配题目!\n')
                for answer in json_data:
                    output_text.insert('end', 'Q: ' + answer['topic'] + '\n')
                    for muti_answer in answer['correct']:
                        output_text.insert(
                            'end', '    A: ' + muti_answer['content'] + '\n')
            except:
                output_text.insert('end', 'Error:请求错误!\n')
            output_text.insert(
                'end', '----------------------------------------\n')
            data.clear()


def search_function():
    if cmb.get() == '多题搜索模式':
        results = multi_find()

        def find_answers_thread():  # threading的timer里面函数不能带参数,原因不明
            find_answers(results)
        timer = threading.Timer(1, find_answers_thread)
        timer.start()
    elif cmb.get() == '单题搜索模式':
        results = single_find()
        find_answers(results)


def clear_function():
    input_entry.delete(0, 'end')
    output_text.delete(1.0, 'end')

def open_browser(self):
    url = 'https://github.com/12218/Chaoxing'
    webbrowser.open(url) 

def keep_front(self):
    if pin_label['image'] == 'pyimage1':
        pin_label['image'] = off_pic
        root.wm_attributes('-topmost', 0)
    elif pin_label['image'] == 'pyimage2':
        pin_label['image'] = on_pic
        root.wm_attributes('-topmost', 1)


root = tkinter.Tk()
root.title('超星学习通助手')
root.geometry('600x600+660+290')

# 导入图钉图片
on_pic = tkinter.PhotoImage(file='resources/on.png')
off_pic = tkinter.PhotoImage(file='resources/off.png')
icon = tkinter.PhotoImage(file='resources/icon.png')

# 输入提示label以及输入框
input_label = tkinter.Label(root, text='输入框', font=('微软雅黑', 12))  # 输入提示label
input_label.place(x=20, y=50)
input_entry = tkinter.Entry(root, width=55, font=('微软雅黑', 12))  # 输入框
input_entry.place(x=90, y=50)

# 答案框的框架
answer_frame = ttk.LabelFrame(root, text=" 答案框 ")  # 创建一个容器，其父容器为root
#answer_frame.grid(row=5, column=1, padx=10, pady=10)
answer_frame.place(x=30, y=100)

# 答案框
output_text = scrolledtext.ScrolledText(
    answer_frame, font=('微软雅黑', 12), height=20, width=40)
output_text.grid(row=5, column=2, padx=10, pady=10)

# 搜题模式选择
cmb = ttk.Combobox(root, width=13)
cmb.place(x=460, y=200)
cmb['value'] = ('多题搜索模式', '单题搜索模式')
cmb.current(0)

# button
search_button = ttk.Button(root, text='搜题', command=search_function)
search_button.place(x=470, y=350)

clear_button = ttk.Button(root, text='清空', command=clear_function)
clear_button.place(x=470, y=420)

#icon
icon_label = tkinter.Label(root, image=icon, cursor='hand2')
icon_label.place(x=440, y=500)
icon_label.bind('<Button-1>', open_browser)

# 保持窗口最前端
pin_label = tkinter.Label(root, image=off_pic, cursor='hand2')
pin_label.place(x=565, y=565)
pin_label.bind('<Button-1>', keep_front)

root.mainloop()
