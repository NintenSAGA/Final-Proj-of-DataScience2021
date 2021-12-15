import math
import tkinter

from src.crawling.common import refined_text_folder, result_folder, json_folder
from src.GUI.common import get_ft, write_text
from src.GUI import common
from tkinter import Button, Frame, Label, Entry, OptionMenu, IntVar, Radiobutton
from tkinter import StringVar
from tkinter.filedialog import askdirectory
from tkinter.scrolledtext import ScrolledText
import os
from tkinter.ttk import Notebook
from collections import OrderedDict

OM_WRAP_LEN = 30


class Panel:
    def __init__(self, parent, from_panel):
        self.from_panel = from_panel
        self.root = parent
        self.parent = parent
        self.root.geometry("%dx%d" % (800, 500))  # 窗体尺寸
        self.root.title("自动化爬取和标注")  # 窗体标题
        self.root.resizable(False, False)  # 窗口大小不可变

        self.frame = Frame(self.root)

        self.left_frame = Frame(self.frame)
        self.folder_path = StringVar()  # 文件夹目录, StrVal
        self.folder_check_label = None  # 文件夹监测信息，Label
        self.dropdown = None  # 下拉菜单, OptionMenu
        self.file_list = ['']  # 文书列表
        self.idx = 0  # 当前位置
        self.file_name = None  # 文件名，StrVal
        self.text_area = None  # 划动文本框，ScrolledText
        self.cur_text = ''  # 当前文本框内文字
        self.info_label = None  # 底部显示文字信息的Label
        self.build_left_frame(self.left_frame)
        self.left_frame.grid(row=1, column=0, sticky='w')

        self.right_frame = Frame(self.frame)
        self.tabs = None    # 切换标签页, Notebook
        self.build_right_frame(self.right_frame)
        self.tags = OrderedDict()  # type: OrderedDict[str, (IntVar, list[str])]  # 存放tag数据结构
        self.right_frame.grid(row=1, column=1, sticky='w')

        self.folder_path.set(value=refined_text_folder)

        Button(self.frame, text='返回', command=lambda: self.exit()).grid(row=0, column=0, sticky='w')

        self.frame.pack()

    def exit(self):
        self.frame.destroy()
        self.from_panel.build()

    # ==================构建左侧页面==================================== #
    def build_left_frame(self, frame):
        self.build_src_folder_opt(frame)
        self.build_text_area(frame)
        self.build_drop_down_opt(frame)
        self.build_info_area(frame)

    # -----------------第一层，文件夹信息, row = 0---------------------- #
    def build_src_folder_opt(self, frame):
        upper_frame = Frame(frame)

        self.folder_path = StringVar()
        self.folder_check_label = Label(upper_frame)

        Label(upper_frame, text='文件夹：', font=get_ft(14), background='white').pack(side=tkinter.LEFT)

        entry = Entry(upper_frame, width=10, textvariable=self.folder_path)
        entry.pack(side=tkinter.LEFT)

        bt = Button(upper_frame, text='选择文件夹', command=lambda: self.select_folder(entry))
        bt.pack(side=tkinter.LEFT)

        self.folder_check_label.pack(side=tkinter.LEFT)

        self.folder_path.trace('w', lambda *arg: self.folder_check())

        entry.xview('end')
        upper_frame.grid(row=0, column=0, sticky='w')

    def folder_check(self):
        """
        检查文件夹的可读情况并更新界面，由folder_path变量更改触发
        :return:
        """
        n = check_file_num(self.folder_path.get())
        msg: str
        color: str

        if n == -1:
            msg = '该目录不含可读文件'
            color = 'red'
            self.update_om([''])
        else:
            msg = '该目录下共有文书{}份'.format(n)
            color = 'blue'
            self.update_om(get_files_in_folder(self.folder_path.get()))

        self.folder_check_label.config(text=msg, fg=color)

    def select_folder(self, entry):
        self.folder_path.set(askdirectory(initialdir=result_folder))
        entry.xview('end')

    # -----------------第二层，下拉窗口, row = 1---------------------- #
    def build_drop_down_opt(self, frame):
        middle_frame = Frame(frame)

        self.file_name = StringVar(value='')
        self.dropdown = OptionMenu(middle_frame, self.file_name, *self.file_list)
        self.dropdown.config(width=OM_WRAP_LEN + 5)
        self.dropdown.pack()

        self.file_name.trace('w', lambda *args: self.update_text())

        middle_frame.grid(row=1, column=0, sticky='w')

    def update_text(self):
        if self.file_name.get() == '':
            text = ''
        else:
            full_path = self.folder_path.get() + '/' + self.file_list[self.idx]
            with open(full_path, 'r') as f:
                text = f.read()

        self.cur_text = text
        write_text(text)
        self.text_area.yview('0.0')

    def update_om(self, file_list: []):
        self.file_list = file_list
        menu = self.dropdown['menu']
        menu.delete(0, "end")
        for i, file in enumerate(self.file_list):
            menu.add_command(label=file[:OM_WRAP_LEN], command=lambda value=i: self.update_idx(value))

        self.update_idx(0)

    def update_idx(self, idx):
        """
        选择文书列表中的第 idx 项，核心触发点
        :param idx:
        :return:
        """
        self.idx = idx % len(self.file_list)
        self.file_name.set(self.file_list[self.idx][:OM_WRAP_LEN])
        self.info_label.config(text="第{}份，共{}份".format(self.idx + 1, len(self.file_list)))
        self.update_tabs()

    # -----------------第三层，划动文本框, row = 2---------------------- #
    def build_text_area(self, frame):
        self.text_area = ScrolledText(frame, width=60, height=30, bg='white',
                                      highlightcolor='black', highlightbackground='black')
        self.text_area.grid(row=2, column=0, sticky='w')
        common.text_pad = self.text_area

    # -----------------第四层，信息行, row = 3---------------------- #
    def build_info_area(self, frame):
        bottom_frame = Frame(frame)

        # 左侧上一份按钮
        bt_left = Button(bottom_frame, text='上一份', command=lambda: self.update_idx(self.idx - 1))
        bt_left.grid(column=0, row=0, sticky='w')

        # 中央文字信息
        self.info_label = Label(bottom_frame, text='', fg='blue')
        self.info_label.place(relx=.5, rely=.5, anchor='center')

        bottom_frame.grid(row=3, column=0, sticky='nsew')

    # ==================构建右侧页面==================================== #
    def build_right_frame(self, frame):
        self.build_tabs(frame)
        self.build_nxt_bt(frame)

    def build_tabs(self, frame):
        tab_frame = Frame(frame, width=350, height=450)

        self.tabs = Notebook(frame, name='标注信息', width=300, height=380)
        self.tabs.grid(row=0, column=0)

        tab_frame.grid(row=0, column=0)

    def update_tabs(self):
        """
        更新标签页信息并保存到self.tags
        :return:
        """
        tags = self.grab_tags()
        self.tabs = self.tabs  # type: Notebook

        for child in self.tabs.winfo_children():
            child.destroy()

        for category in tags.keys():
            tab_frame = Frame(self.tabs)                                # 子框架
            tab_var = IntVar()                                          # 变量
            self.tags.update({category: (tab_var, tags[category])})     # 更新域
            self.tabs.add(tab_frame, text=category)                     # 添加标签
            for i, tag in enumerate(tags[category]):
                rbt = Radiobutton(tab_frame, text=tag, variable=tab_var, value=i)
                rbt.grid(column=math.floor(i/17), row=i % 17, sticky='w')
            tab_var.set(value=0)

    def grab_tags(self) -> OrderedDict[str, list[str]]:
        text = self.cur_text
        if text == '':
            return OrderedDict()

        # TODO: 填补api
        data = OrderedDict()

        # fake_data
        for key1 in ['姓名', '省份', '罪由']:
            val1 = []
            for i in range(1, 50):
                name = '{}测试{}'.format(key1, i)
                val1.append(name)
            data[key1] = val1

        return data

    def build_nxt_bt(self, frame):
        bt_frame = Frame(frame)

        # 右侧下一份按钮
        # TODO: 更改成 保存，下一份
        bt_right = Button(bt_frame, text='保存，下一份', command=lambda: self.save_and_nxt())
        bt_right.grid(column=0, row=0, sticky='e')

        bt_frame.grid(row=1, column=0, sticky='nsew')

    def save_and_nxt(self):
        self.yield_json()
        self.update_idx(self.idx + 1)

    def yield_json(self):
        """
        生成Json文件
        :return:
        """
        json_file = json_folder + self.file_name.get() + '.json'
        if not os.path.exists(json_folder):
            os.mkdir(json_folder)

        # {
        #     "Criminals": "周永华",
        #     "Gender": "男",
        #     "Ethnicity": "汉族",
        #     "Birthplace": "贵州省威宁彝族回族苗族自治县",
        #     "Accusation": "抢劫",
        #     "Courts": "云南省红河哈..."
        # }

        with open(json_file, 'w') as f:
            f.write('{' + os.linesep)
            entries = []
            for category in self.tags.keys():
                sel, tag_list = self.tags[category]
                tag = tag_list[sel.get()]
                entries.append('\t"{}": "{}"'.format(category, tag))
            f.write(',{}'.format(os.linesep).join(entries))
            f.write(os.linesep + '}')


def get_files_in_folder(folder: str) -> list:
    """
    获得文件夹内文件列表并排序

    :param folder: 文件夹路径
    :return:
    """
    try:
        return sorted(filter(lambda x: x.endswith('.txt'), os.listdir(folder)), key=lambda x: date_sort(x))
    except (ValueError, TypeError):
        return sorted(filter(lambda x: x.endswith('.txt'), os.listdir(folder)))


def date_sort(s: str):
    """
    对诸如 yyyy.mm.dd_nn.[name].txt 格式的字符串拆解key供sorted函数使用

    :param s: 字符串
    :return:
    """
    date_and_n = s.split('_')
    date_vals = date_and_n[0].split('.')

    return date_vals[0], date_vals[1], date_vals[2], date_and_n[1].split('.')[0]


def check_file_num(folder_path) -> int:
    if not os.path.exists(folder_path):
        return -1
    count = 0
    for file in os.listdir(folder_path):
        if file.endswith('.txt'):
            count += 1
    return -1 if count == 0 else count
