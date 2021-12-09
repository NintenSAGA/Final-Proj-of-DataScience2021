from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import *


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.text_pad = None
        self.pack()
        self.create_widget()

    def create_widget(self):
        menu_bar = Menu(root)

        menu_file = Menu(menu_bar)
        menu_edit = Menu(menu_bar)
        menu_help = Menu(menu_bar)

        menu_bar.add_cascade(label="文件", menu=menu_file)
        menu_bar.add_cascade(label="编辑", menu=menu_edit)
        menu_bar.add_cascade(label="帮助", menu=menu_help)

        menu_file.add_command(label="新建", accelerator="ctrl+n", command=self.test)
        menu_file.add_command(label="打开", accelerator="ctrl+o", command=self.open_file)
        menu_file.add_command(label="保存", accelerator="ctrl+s", command=self.test)
        menu_file.add_separator()
        menu_file.add_command(label="退出", accelerator="ctrl+q", command=self.test)

        root["menu"] = menu_bar

        self.text_pad = Text(root, width=50, height=30)
        self.text_pad.place(x=0, y=0)

        self.context_menu = Menu(root)
        self.context_menu.add_command(label="背景颜色", command=self.test)

        root.bind("<Button-3>", self.create_context_menu)

        self.CheckVar1 = BooleanVar()
        self.CheckVar2 = BooleanVar()
        self.CheckVar1.set(True)
        self.C1 = Checkbutton(self.master, text="RUN", variable=self.CheckVar1, height=2,
                              width=8, anchor='w')
        self.C2 = Checkbutton(self.master, text="GOOGLE", variable=self.CheckVar2, height=2,
                              width=8, anchor='w')

        self.C1.place(x=0, y=400)
        self.C2.place(x=0, y=450)

    def create_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def open_file(self):
        with open(askopenfilename(), encoding='utf-8') as f:
            self.text_pad.insert(INSERT, f.read())

    def test(self):
        pass


root = Tk()
root.geometry("500x500+200+300")
root.title("一个经典的GUI程序类的测试")
app = Application(master=root)

root.mainloop()