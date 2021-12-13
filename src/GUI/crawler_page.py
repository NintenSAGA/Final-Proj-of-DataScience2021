import tkinter.font
import tkinter
from tkinter import Toplevel, Canvas, Label, BooleanVar, Checkbutton, Entry, Button, StringVar, Radiobutton, IntVar
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter.font import Font
from src.crawling import crawl
from src.GUI import common
from threading import Thread

font_type = '微软雅黑'


def write_text(output):
    common.write_text(output)


def begin():
    thread = Thread(target=lambda: crawl(100, skip_fu=True, skip_rhf=True, launched_by_GUI=True))
    thread.start()


class Windows:
    def __init__(self, parent):
        self.ft0 = Font(family=font_type, size=20, weight=tkinter.font.BOLD)
        self.ft1 = Font(family=font_type, size=15, weight=tkinter.font.BOLD)
        self.ft2 = Font(family=font_type, size=14, weight=tkinter.font.BOLD)
        self.src_site = None
        self.check_url_list, self.check_html_list = None, None

        self.root = Toplevel()
        self.parent = parent
        self.root.geometry("%dx%d" % (800, 700))  # 窗体尺寸
        self.root.title("自动化爬取和标注")  # 窗体标题
        self.root.resizable(False, False)  # 窗口大小不可变

        self.canvas = None
        self.text_pad = None

        self.entry_begin_n, self.entry_delta_n = None, None
        self.var_begin_n, self.var_delta_n = None, None

        self.create_canvas()
        self.create_label()
        self.create_check_button()
        self.create_get_choice()
        self.create_entry()
        self.create_button()

        self.create_text_pad()
        common.text_pad = self.text_pad

    def create_canvas(self):
        self.canvas = Canvas(self.root, width=1000, height=700, highlightcolor='pink', bg='white')
        self.canvas.pack()

    def create_label(self):
        Label(self.canvas, text='文书源', font=self.ft0, bg='white').place(x=50, y=25)
        Label(self.canvas, text='爬取选项', font=self.ft0, bg='white').place(x=50, y=200)

        Label(self.canvas, text='url_list：本地已有缓存，可重新获取', font=self.ft1, bg='white', fg='blue').place(x=250, y=240)
        Label(self.canvas, text='html_list：本地已有缓存，可重新获取', font=self.ft1, bg='white', fg='blue').place(x=250, y=280)

    def create_check_button(self):
        self.src_site = IntVar(value=1)

        check_button1 = Radiobutton(self.canvas, text="北大法宝", variable=self.src_site, value=1, font=self.ft2)
        check_button1.place(x=70, y=65)

        check_button2 = Radiobutton(self.canvas, text="中华人民共和国最高人民法院公报", variable=self.src_site, value=0, font=self.ft2, state=tkinter.DISABLED)
        check_button2.place(x=70, y=105)

        check_button3 = Radiobutton(self.canvas, text='裁判文书网', variable=self.src_site, value=2, font=self.ft2, state=tkinter.DISABLED)
        check_button3.place(x=70, y=145)

    def create_get_choice(self):
        self.check_url_list = BooleanVar()
        check_button1 = Checkbutton(self.canvas, text="爬取url_list", variable=self.check_url_list, font=self.ft2)

        self.check_html_list = BooleanVar()
        check_button2 = Checkbutton(self.canvas, text="爬取html_list", variable=self.check_html_list, font=self.ft2)
        check_button1.place(x=70, y=240)
        check_button2.place(x=70, y=280)

    def create_text_pad(self):
        self.text_pad = ScrolledText(self.canvas, width=100, height=20, bg='white', highlightcolor='black',
                                     highlightbackground='black')
        self.text_pad.place(x=50, y=400)
        self.text_pad.config(state=tkinter.DISABLED)

    def create_entry(self):
        self.var_begin_n = StringVar(value='0')
        Label(self.canvas, text='开始条目', font=self.ft1, bg='white').place(x=50, y=360)
        self.entry_begin_n = Entry(self.canvas, width=5, borderwidth=4, textvariable=self.var_begin_n)
        self.entry_begin_n.place(x=120, y=365)

        self.var_delta_n = StringVar(value='100')
        Label(self.canvas, text='文书数量', font=self.ft1, bg='white').place(x=200, y=360)
        self.entry_delta_n = Entry(self.canvas, width=5, borderwidth=4, textvariable=self.var_delta_n)
        self.entry_delta_n.place(x=290, y=365)

    def create_button(self):
        Button(self.canvas, text='开始爬取', font=self.ft2, bg='grey', command=begin,
               anchor='w', pady=0).place(x=675, y=350)
