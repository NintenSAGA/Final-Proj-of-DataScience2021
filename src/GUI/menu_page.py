from tkinter import Frame, Button, Canvas, Tk
from src.GUI import anno_page, crawler_page
from src.GUI.common import get_ft
# -*- coding: utf-8 -*-

app = None


def launch():
    global app
    root = Tk()
    app = Application(master=root)
    root.mainloop()


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.obj_anno_page = None
        self.obj_crawler_page = None
        self.frame = None
        self.build()

    def build(self):
        self.master.resizable(False, False)
        self.master.geometry("400x500+300+300")
        self.master.title("自动化爬取和标注")
        self.frame = Frame(self.master)
        self.create_bt()
        self.obj_anno_page = None
        self.obj_crawler_page = None
        self.frame.pack()

    def create_bt(self):
        ft0 = get_ft(14)
        Button(self.frame, text="  爬取文书 ", bg="cadetblue", command=self.show_crawler_page, fg='black', font=ft0)\
            .pack()
        Button(self.frame, text="自动化标注", bg="cadetblue", command=self.show_anno_page, fg='black', font=ft0)\
            .pack()

    def show_anno_page(self):
        self.frame.destroy()
        self.obj_anno_page = anno_page.Panel(self.master, self)

    def show_crawler_page(self):
        self.frame.destroy()
        self.obj_crawler_page = crawler_page.Panel(self.master, self)
