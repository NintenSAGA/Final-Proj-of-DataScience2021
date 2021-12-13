import tkinter.font
import tkinter
from tkinter import Toplevel, Canvas, Label, BooleanVar, Checkbutton, Entry, Button, Text
from tkinter.scrolledtext import ScrolledText
from tkinter.font import Font


class Windows:
    def __init__(self, parent):
        self.ft0 = Font(family="微软雅黑", size=20, weight=tkinter.font.BOLD)
        self.ft1 = Font(family="微软雅黑", size=15, weight=tkinter.font.BOLD)
        self.ft2 = Font(family="微软雅黑", size=14, weight=tkinter.font.BOLD)
        self.check_pkulaw = BooleanVar()
        self.check_gb = BooleanVar()
        self.check_ws = BooleanVar()
        self.check_url_list = BooleanVar()
        self.check_html_list = BooleanVar()
        self.root = Toplevel()
        self.parent = parent
        self.root.geometry("%dx%d" % (800, 700))  # 窗体尺寸
        self.root.title("自动化爬取和标注")  # 窗体标题
        self.root.resizable(False, False)  # 窗口大小不可变
        self.canvas = None
        self.text_pad = None
        self.entry_begin_page = None
        self.entry_page_n = None
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
        Label(self.canvas, text='文书源', font=self.ft0, bg='white').place(x=50, y=25)
        Label(self.canvas, text='爬取选项', font=self.ft0, bg='white').place(x=50, y=200)

        Label(self.canvas, text='url_list：本地已有缓存，可重新获取', font=self.ft1, bg='white', fg='blue').place(x=250, y=240)
        Label(self.canvas, text='html_list：本地已有缓存，可重新获取', font=self.ft1, bg='white', fg='blue').place(x=250, y=280)

    def create_check_button(self):
        check_button1 = Checkbutton(self.canvas, text="北大法宝", variable=self.check_pkulaw,
                                    anchor='w', bg='white', font=self.ft2)
        check_button2 = Checkbutton(self.canvas, text="中华人民共和国最高人民法院公报", variable=self.check_gb
                                    , anchor='w', bg='white', font=self.ft2, state=tkinter.DISABLED)
        check_button3 = Checkbutton(self.canvas, text='裁判文书网', variable=self.check_ws,
                                    anchor='w', bg='white', font=self.ft2, state=tkinter.DISABLED)
        check_button1.place(x=70, y=65)
        check_button2.place(x=70, y=105)
        check_button3.place(x=70, y=145)

    def create_get_choice(self):
        check_button1 = Checkbutton(self.canvas, text="爬取url_list", variable=self.check_url_list,
                                    anchor='w', bg='white', font=self.ft2)
        check_button2 = Checkbutton(self.canvas, text="爬取html_list", variable=self.check_html_list
                                    , anchor='w', bg='white', font=self.ft2)
        check_button1.place(x=70, y=240)
        check_button2.place(x=70, y=280)

    def create_text_pad(self):
        self.text_pad = ScrolledText(self.canvas, width=100, height=20, bg='white', highlightcolor='black', highlightbackground='black')
        self.text_pad.insert(tkinter.INSERT, 'dwd\n'*100)
        self.text_pad.see(tkinter.END)
        self.text_pad.config(state=tkinter.DISABLED)
        self.text_pad.place(x=50, y=400)

    def create_entry(self):
        Label(self.canvas, text='开始页', font=self.ft1, bg='white').place(x=50, y=360)
        Label(self.canvas, text='文书数量', font=self.ft1, bg='white').place(x=200, y=360)

        self.entry_begin_page = Entry(self.canvas, width=5, borderwidth=4)
        self.entry_begin_page.place(x=120, y=365)
        self.entry_page_n = Entry(self.canvas, width=5, borderwidth=4)
        self.entry_page_n.place(x=290, y=365)

    def create_button(self):
        Button(self.canvas, text=' 开始爬取', font=self.ft2, bg='grey', command=self.begin,
               anchor='w', pady=0).place(x=675, y=350)

    def begin(self):
        pass
