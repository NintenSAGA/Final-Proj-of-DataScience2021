import time
import tkinter.font
import tkinter
from tkinter import Toplevel, Canvas, Label, BooleanVar, Checkbutton, Entry, Button, StringVar, Radiobutton, IntVar
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter.font import Font
from src.crawling import crawl, check_html_list, check_url_list
from src.GUI import common
from threading import Thread

font_type = '微软雅黑'
font_sizes = [20, 15, 14, 10]


def write_text(output):
    common.write_text(output)


def wait_for_its_end(bt: Button, thread: Thread):
    while thread.is_alive():
        time.sleep(0.5)
    enable_bt(bt)
    bt.update()


def disable_bt(bt: Button):
    bt.config(state=tkinter.DISABLED)


def enable_bt(bt: Button):
    bt.config(state=tkinter.NORMAL)


class Windows:
    def __init__(self, parent):
        self.root = Toplevel()
        self.parent = parent
        self.root.geometry("%dx%d" % (800, 700))  # 窗体尺寸
        self.root.title("自动化爬取和标注")  # 窗体标题
        self.root.resizable(False, False)  # 窗口大小不可变
        self.canvas = Canvas(self.root, width=1000, height=700, highlightcolor='pink', bg='white')
        self.canvas.pack()
        self.ft = [Font(family=font_type, size=size, weight=tkinter.font.BOLD) for size in font_sizes]

        self.src_site = None  # IntVal 对应三个网站
        self.crawler_option = {}  # dict: name -> [Button, BooleanVar, Label]
        self.text_pad = None

        self.entry_begin_n, self.entry_delta_n = None, None
        self.var_begin_n, self.var_delta_n = None, None

        self.launch_bt = None

        self.create_src_option()
        self.create_crawler_option()
        self.create_entry()
        self.create_launch_bt()
        self.create_text_pad()

    def create_src_option(self):
        Label(self.canvas, text='文书源', font=self.ft[0], bg='white').place(x=50, y=25)

        self.src_site = IntVar(value=1)
        st_x, st_y = 70, 65

        src_sites = [[1, '北大法宝'],
                     [0, '中华人民共和国最高人民法院公报'],
                     [2, '裁判文书网']]
        for i, site_pack in enumerate(src_sites):
            var, site = site_pack
            bt = Radiobutton(self.canvas, text=site, variable=self.src_site, value=var, font=self.ft[2],
                             state=tkinter.NORMAL if var == 1 else tkinter.DISABLED)
            bt.place(x=st_x, y=st_y + i * 40)

    def create_text_pad(self):
        self.text_pad = ScrolledText(self.canvas, width=100, height=20, bg='white', highlightcolor='black',
                                     highlightbackground='black')
        self.text_pad.place(x=50, y=400)
        self.text_pad.config(state=tkinter.DISABLED)
        common.text_pad = self.text_pad

    def create_entry(self):
        self.var_begin_n = StringVar(value='0')
        self.var_delta_n = StringVar(value='100')

        for var in [self.var_begin_n, self.var_delta_n]:
            var.trace('w', lambda *args: self.label_update(self.var_begin_n.get(), self.var_delta_n.get()))

        lst_x, lst_y = 50, 360
        est_x, est_y = 120, 365
        entries = [['开始条目', self.var_begin_n, self.entry_begin_n],
                   ['文书数量', self.var_delta_n, self.entry_delta_n]]
        for i, pack in enumerate(entries):
            text, var, entry = pack
            Label(self.canvas, text=text, font=self.ft[1], bg='white').place(x=lst_x + 150 * i, y=lst_y)
            entry = Entry(self.canvas, width=5, borderwidth=4, textvariable=var)
            entry.place(x=est_x + i * 170, y=est_y)

    def create_launch_bt(self):
        self.launch_bt = Button(self.canvas, text='开始爬取', font=self.ft[2], bg='grey', command=self.begin, pady=0)
        self.launch_bt.place(x=675, y=350)

    def begin(self):
        disable_bt(self.launch_bt)

        thread = Thread(target=lambda: crawl(
            n=int(self.var_delta_n.get()),
            src=self.src_site.get(),
            from_n=int(self.var_begin_n.get()),
            skip_fu=not self.crawler_option['url_list'][1].get(),
            skip_rhf=not self.crawler_option['html_list'][1].get(),
            launched_by_gui=True))

        thread.start()
        Thread(target=lambda: wait_for_its_end(self.launch_bt, thread)).start()

    def create_crawler_option(self):
        Label(self.canvas, text='爬取选项', font=self.ft[0], bg='white').place(x=50, y=200)

        st_x, st_y = 70, 240
        lst_x, lst_y = 250, 240
        choices = [["url_list", BooleanVar(value=False), lambda: self.url_list_action()],
                   ['html_list', BooleanVar(value=False), None]]
        for i, pack in enumerate(choices):
            text, var, cmd = pack
            bt = Checkbutton(self.canvas, text='爬取' + text, variable=var, font=self.ft[2])
            bt.place(x=st_x, y=st_y + 40 * i)
            var.trace('w', lambda *args: self.url_list_action())
            label = Label(self.canvas, text='', font=self.ft[3], bg='white', fg='blue')
            label.place(x=lst_x, y=lst_y + i*40)
            self.crawler_option[text] = [bt, var, label]

    def url_list_action(self):
        var = self.crawler_option['url_list'][1]  # type: BooleanVar
        html_bt, html_var, label = self.crawler_option['html_list']

        html_bt.config(state=tkinter.DISABLED if var.get() else tkinter.NORMAL)
        html_var.set(value=var.get())

    def label_update(self, from_n, delta_n):
        try:
            from_n = int(from_n)
            delta_n = int(delta_n)
            if from_n > delta_n or delta_n > 2500:
                raise ValueError
            url_var, url_msg = check_url_list(from_n, delta_n)
            html_var, html_msg = check_html_list(from_n, delta_n)
            enable_bt(self.launch_bt)
        except (ValueError, TypeError):
            disable_bt(self.launch_bt)
            url_var, url_msg = False, '参数错误'
            html_var, html_msg = False, '参数错误'

        for keys in [['url_list', url_var, url_msg], ['html_list', html_var, html_msg]]:
            pack = self.crawler_option[keys[0]]
            pack[1].set(value=keys[1])
            max_len = 50
            if len(keys[2]) < max_len:
                pack[2].config(text=keys[2])
            else:
                pack[2].config(text=keys[2][:max_len]+'...')
            if keys[1]:
                pack[2].config(fg='blue')
            else:
                pack[2].config(fg='red')





