import tkinter.font
from tkinter import *
from tkinter.font import *


class Windows:
    def __init__(self, parent):
        self.root = Toplevel()
        self.parent = parent
        self.root.geometry("%dx%d" % (1000, 700))  # 窗体尺寸
        self.root.title("自动化爬取和标注")  # 窗体标题
        self.root.resizable(False, False)  # 窗口大小不可变
        self.canvas = None
        self.create_canvas()
        self.create_label()

    def create_canvas(self):
        self.canvas = Canvas(self.root, width=1000, height=700, highlightcolor='pink', bg='white')
        self.canvas.pack()

    def create_label(self):
        ft0 = Font(family="微软雅黑", size=20, weight=tkinter.font.BOLD)
        Label(self.canvas, text='文书源', font=ft0, bg='white').place(x=50, y=25)
