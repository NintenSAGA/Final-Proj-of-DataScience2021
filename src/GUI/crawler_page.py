import time
import tkinter.font
import tkinter
from tkinter import Toplevel, Label, BooleanVar, Checkbutton, Entry, Button, StringVar, Radiobutton, IntVar
from tkinter import Frame, messagebox
from tkinter.scrolledtext import ScrolledText
from src.crawling import crawl, check_html_list, check_url_list
from src.GUI import common
from src.GUI.common import get_ft
from threading import Thread


def write_text(output):
    common.write_text(output)


def wait_for_its_end(bt: Button, thread: Thread):
    while thread.is_alive():
        time.sleep(0.5)
    enable_bt(bt)
    bt.update()
    messagebox.showinfo('完成', '全部文件扒取完毕')


def disable_bt(bt: Button):
    bt.config(state=tkinter.DISABLED)


def enable_bt(bt: Button):
    bt.config(state=tkinter.NORMAL)


class Panel:
    def __init__(self, parent, from_panel):
        self.debug_mode = False

        self.from_panel = from_panel
        self.root = parent
        self.parent = parent
        self.root.geometry("%dx%d" % (400, 500))  # 窗体尺寸
        self.root.title("自动化爬取和标注")  # 窗体标题
        self.root.resizable(False, False)  # 窗口大小不可变

        self.src_site = None  # IntVal 对应三个网站
        self.crawler_option = {}  # dict: name -> [Button, BooleanVar, Label]
        self.text_pad = None

        self.var_begin_n, self.var_delta_n, self.var_year = StringVar(), StringVar(), StringVar()

        self.launch_bt = None

        self.frame = Frame(self.root)

        self.middle_zone = Frame(self.frame)
        self.create_entry()
        self.create_launch_bt()
        self.middle_zone.grid(row=2, column=0, sticky='w')

        self.upper_zone = Frame(self.frame)
        self.create_src_option()
        self.create_crawler_option()
        self.upper_zone.grid(row=1, column=0, sticky='w')

        self.lower_zone = Frame(self.frame)
        self.create_text_pad()
        self.lower_zone.grid(row=3, column=0, sticky='w')

        Button(self.frame, text='返回', command=lambda: self.exit()).grid(row=0, column=0, sticky='w')

        self.frame.pack()
        
    def exit(self):
        self.frame.destroy()
        self.from_panel.build()

    def create_src_option(self):
        src_opt_frame = Frame(self.upper_zone)

        Label(src_opt_frame, text='文书源', font=get_ft(15), bg='white').grid(row=0, column=0, sticky='w')

        self.src_site = IntVar(value=1)

        src_sites = [[1, '北大法宝'],
                     [0, '中华人民共和国最高人民法院公报'],
                     [2, '裁判文书网']]
        for i, site_pack in enumerate(src_sites):
            val, site = site_pack
            bt = Radiobutton(src_opt_frame, text=site, variable=self.src_site, value=val, font=get_ft(14),
                             state=tkinter.NORMAL if val == 1 else tkinter.DISABLED)
            bt.grid(row=i+1, column=0, sticky='w')

        src_opt_frame.grid(row=0, column=0, sticky='w')

    def create_text_pad(self):
        self.text_pad = ScrolledText(self.lower_zone, width=55, height=20, bg='white', highlightcolor='black',
                                     highlightbackground='black')
        self.text_pad.config(state=tkinter.DISABLED)
        common.text_pad = self.text_pad
        self.text_pad.pack(side=tkinter.TOP)

    def create_entry(self):
        entry_frame = Frame(self.middle_zone)

        # entries = [['开始条目', self.var_begin_n, self.entry_begin_n],
        #            ['文书数量', self.var_delta_n, self.entry_delta_n]]

        entries = [['年份', self.var_year],
                   ['文书数量', self.var_delta_n]]

        for i, pack in enumerate(entries):
            single_entry_frame = Frame(entry_frame)
            text, var = pack

            var.trace('w', lambda *args: self.label_update(self.var_year.get(), self.var_delta_n.get()))   # 设定跟踪动作

            Label(single_entry_frame, text=text, font=get_ft(15), bg='white').pack(side=tkinter.LEFT)
            entry = Entry(single_entry_frame, width=5, borderwidth=4, textvariable=var)
            entry.pack(side=tkinter.LEFT)
            single_entry_frame.grid(row=0, column=i)

        entry_frame.pack(side=tkinter.LEFT)

    def create_launch_bt(self):
        self.launch_bt = Button(self.middle_zone, text='开始爬取', font=get_ft(14), bg='grey', command=self.begin, pady=0)
        self.launch_bt.pack(side=tkinter.LEFT)

    def begin(self):
        disable_bt(self.launch_bt)

        thread = Thread(target=lambda: crawl(
            n=int(self.var_delta_n.get()),
            src=self.src_site.get(),
            from_n=0,
            skip_fu=not self.crawler_option['url_list'][1].get(),
            skip_rhf=not self.crawler_option['html_list'][1].get(),
            year=int(self.var_year.get()),
            launched_by_gui=True,
            debug_mode=self.debug_mode))

        thread.start()
        Thread(target=lambda: wait_for_its_end(self.launch_bt, thread)).start()

    def create_crawler_option(self):
        crawler_opt_frame = Frame(self.upper_zone)

        Label(crawler_opt_frame, text='爬取选项', font=get_ft(15), bg='white').grid(column=0, row=0, sticky='w')

        choices = [["url_list", BooleanVar(value=False), lambda: self.url_list_action()],
                   ['html_list', BooleanVar(value=False), None]]
        for i, pack in enumerate(choices):
            text, var, cmd = pack
            opt_frame = Frame(crawler_opt_frame)
            bt = Checkbutton(opt_frame, text='爬取' + text, variable=var, font=get_ft(14))
            bt.pack(side=tkinter.LEFT)
            label = Label(opt_frame, text='', font=get_ft(10), bg='white', fg='blue')
            label.pack(side=tkinter.LEFT)
            self.crawler_option[text] = [bt, var, label]
            opt_frame.grid(column=0, row=i+1, sticky='w')

        self.crawler_option['url_list'][1].trace('w', lambda *args: self.url_list_action())
        self.var_delta_n.set(value='100')
        self.var_year.set(value='2021')

        crawler_opt_frame.grid(row=2, column=0, sticky='w')

    def url_list_action(self):
        var = self.crawler_option['url_list'][1]  # type: BooleanVar
        html_bt, html_var, label = self.crawler_option['html_list']

        html_bt.config(state=tkinter.DISABLED if var.get() else tkinter.NORMAL)
        html_var.set(value=var.get())

    def label_update(self, year: str, delta_n: str):
        try:
            year = int(year)
            delta_n = int(delta_n)
            if year > 2021 or year < 2000 or delta_n > 15000:
                raise ValueError
            url_var, url_msg = check_url_list(0, delta_n, year)
            html_var, html_msg = check_html_list(0, delta_n, year)
            enable_bt(self.launch_bt)
        except (ValueError, TypeError):
            disable_bt(self.launch_bt)
            url_var, url_msg = False, '参数错误'
            html_var, html_msg = False, '参数错误'

        for keys in [['url_list', url_var, url_msg],
                     ['html_list', html_var, html_msg]]:
            pack = self.crawler_option[keys[0]]
            if not keys[1]:
                pack[1].set(value=keys[1])
            max_len = 50
            # 防止过长
            if len(keys[2]) < max_len:
                pack[2].config(text=keys[2])
            else:
                pack[2].config(text=keys[2][:max_len]+'...')
            # 颜色
            if keys[1]:
                pack[2].config(fg='blue')
            else:
                pack[2].config(fg='red')

