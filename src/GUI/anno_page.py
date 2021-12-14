import tkinter

from src.crawling.common import refined_text_folder, result_folder
from src.GUI.common import get_ft, write_text
from src.GUI import common
from tkinter import Toplevel, BooleanVar, Button, Frame, Label, Entry, Menubutton, OptionMenu
from tkinter import StringVar
from tkinter.filedialog import askdirectory
from tkinter.scrolledtext import ScrolledText
import os
from tkinter.ttk import Notebook, Separator


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
        self.folder_path = None                             # 文件夹目录, StrVal
        self.folder_check_label = None                      # 文件夹监测信息，Label
        self.dropdown = None                                # 下拉菜单, OptionMenu
        self.file_list = ['']                               # 文书列表
        self.idx = 0                                        # 当前位置
        self.file_name = None                               # 文件名，StrVal
        self.text_area = None                               # 划动文本框，ScrolledText
        self.cur_text = ''                                  # 当前文本框内文字
        self.build_left_frame(self.left_frame)
        self.left_frame.grid(row=0, column=0, sticky='w')

        self.right_frame = Frame(self.frame)
        self.build_right_frame(self.right_frame)
        self.right_frame.grid(row=0, column=1, sticky='e')

        Button(self.frame, text='返回', command=lambda: self.exit()).grid(row=1, column=0, sticky='w')

        self.frame.pack()

    def exit(self):
        self.frame.destroy()
        self.from_panel.build()

    def build_left_frame(self, frame):
        self.build_text_area(frame)
        self.build_drop_down_opt(frame)
        self.build_src_folder_opt(frame)
        Label(frame, text=' ').grid(row=2, column=0, sticky='w')

    def build_src_folder_opt(self, frame):
        upper_frame = Frame(frame)

        self.folder_path = StringVar()
        self.folder_check_label = Label(upper_frame)

        Label(upper_frame, text='文件夹目录：', font=get_ft(14), background='white').pack(side=tkinter.LEFT)

        entry = Entry(upper_frame, width=10, textvariable=self.folder_path)
        entry.pack(side=tkinter.LEFT)

        bt = Button(upper_frame, text='选择文件夹', command=lambda: self.select_folder(entry))
        bt.pack(side=tkinter.LEFT)

        self.folder_check_label.pack(side=tkinter.LEFT)

        self.folder_path.trace('w', lambda *arg: self.folder_check())
        self.folder_path.set(value=refined_text_folder)

        entry.xview('end')
        upper_frame.grid(row=0, column=0, sticky='w')

    def folder_check(self):
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

    def build_drop_down_opt(self, frame):
        middle_frame = Frame(frame)

        self.file_name = StringVar(value='')
        self.dropdown = OptionMenu(middle_frame, self.file_name, *self.file_list)
        self.dropdown.pack()

        self.file_name.trace('w', lambda *args: self.show_text())

        middle_frame.grid(row=1, column=0, sticky='w')

    def show_text(self):
        if self.file_name.get() == '':
            return
        full_path = self.folder_path.get() + self.file_name.get()

        with open(full_path, 'r') as f:
            self.cur_text = f.read()

        write_text(self.cur_text)
        self.text_area.yview('0.0')

    def update_om(self, file_list: []):
        self.file_list = file_list
        menu = self.dropdown['menu']
        menu.delete(0, "end")
        for i, file in enumerate(self.file_list):
            menu.add_command(label=file, command=lambda value=i: self.menu_cmd(value))

        self.menu_cmd(0)
        
    def menu_cmd(self, idx):
        self.idx = idx
        self.file_name.set(self.file_list[self.idx])

    def build_text_area(self, frame):
        self.text_area = ScrolledText(frame, width=60, height=20, bg='white',
                                      highlightcolor='black', highlightbackground='black')
        self.text_area.grid(row=3, column=0, sticky='w')
        common.text_pad = self.text_area




    def build_right_frame(self, frame):
        pass


def get_files_in_folder(folder: str) -> list:
    try:
        return sorted(filter(lambda x: x.endswith('.txt'), os.listdir(folder)), key=lambda x: int(x.split('.')[0]))
    except (ValueError, TypeError):
        return sorted(filter(lambda x: x.endswith('.txt'), os.listdir(folder)))


def check_file_num(folder_path) -> int:
    if not os.path.exists(folder_path):
        return -1
    count = 0
    for file in os.listdir(folder_path):
        if file.endswith('.txt'):
            count += 1
    return count

