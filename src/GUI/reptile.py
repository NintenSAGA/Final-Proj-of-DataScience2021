import tkinter.font
from tkinter import *
from tkinter.scrolledtext import *
from tkinter.font import *


class Windows:
    def __init__(self, parent):
        self.root = Toplevel()
        self.parent = parent
        self.root.geometry("%dx%d" % (800, 700))  # 窗体尺寸
        self.root.title("自动化爬取和标注")  # 窗体标题
        self.root.resizable(False, False)  # 窗口大小不可变
        self.canvas = None
        self.text_pad = None
        self.entry_start = None
        self.entry_number = None
        self.create_canvas()
        self.create_label()
        self.create_check_button()
        self.create_get_choice()
        self.create_text_pad()
        self.create_entry()
        self.create_button()

    def create_canvas(self):
        self.canvas = Canvas(self.root, width=1000, height=700, highlightcolor='pink', bg='white')
        self.canvas.pack()

    def create_label(self):
        ft0 = Font(family="微软雅黑", size=20, weight=tkinter.font.BOLD)
        ft1 = Font(family="微软雅黑", size=15, weight=tkinter.font.BOLD)

        Label(self.canvas, text='文书源', font=ft0, bg='white').place(x=50, y=25)
        Label(self.canvas, text='爬取选项', font=ft0, bg='white').place(x=50, y=200)

        Label(self.canvas, text='url_list：本地已有缓存，可重新获取', font=ft1, bg='white', fg='blue').place(x=250, y=240)
        Label(self.canvas, text='html_list：本地已有缓存，可重新获取', font=ft1, bg='white', fg='blue').place(x=250, y=280)

        Label(self.canvas, text='开始页', font=ft1, bg='white').place(x=50, y=360)
        Label(self.canvas, text='文书数量', font=ft1, bg='white').place(x=200, y=360)

    def create_check_button(self):
        self.check_bei_da = BooleanVar()
        self.check_gong_bao = BooleanVar()
        self.check_wen_shu = BooleanVar()
        ft0 = Font(family="微软雅黑", size=14, weight=tkinter.font.BOLD)
        check_button1 = Checkbutton(self.canvas, text="北大法宝", variable=self.check_bei_da,
                                    anchor='w', bg='white', font=ft0)
        check_button2 = Checkbutton(self.canvas, text="中华人民共和国最高人民法院公报", variable=self.check_gong_bao
                                    , anchor='w', bg='white', font=ft0)
        check_button3 = Checkbutton(self.canvas, text='裁判文书网', variable=self.check_wen_shu,
                                    anchor='w', bg='white', font=ft0)
        check_button1.place(x=70, y=65)
        check_button2.place(x=70, y=105)
        check_button3.place(x=70, y=145)

    def create_get_choice(self):
        self.check_url_list = BooleanVar()
        self.check_html_list = BooleanVar()
        ft0 = Font(family="微软雅黑", size=14, weight=tkinter.font.BOLD)
        check_button1 = Checkbutton(self.canvas, text="爬取url_list", variable=self.check_url_list,
                                    anchor='w', bg='white', font=ft0)
        check_button2 = Checkbutton(self.canvas, text="爬取html_list", variable=self.check_html_list
                                    , anchor='w', bg='white', font=ft0)
        check_button1.place(x=70, y=240)
        check_button2.place(x=70, y=280)

    def create_text_pad(self):
        self.text_pad = ScrolledText(self.canvas, width=100, height=20, bg='white', highlightcolor='black')
        self.text_pad.place(x=50, y=400)

    def create_entry(self):
        self.entry_start = Entry(self.canvas, width=5, borderwidth=4)
        self.entry_start.place(x=120, y=365)
        self.entry_number = Entry(self.canvas, width=5, borderwidth=4)
        self.entry_number.place(x=290, y=365)

    def create_button(self):
        ft0 = Font(family="微软雅黑", size=14, weight=tkinter.font.BOLD)
        Button(self.canvas, text=' 开始爬取', font=ft0, bg='grey', command=self.begin,
               anchor='w', pady=0).place(x=675, y=350)

    def begin(self):
        pass
