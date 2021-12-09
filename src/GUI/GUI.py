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
        self.file_name = None

    def create_widget(self):
        # 建立一个菜单
        menu_bar = Menu(root)
        # 建立一级菜单
        menu_file = Menu(menu_bar)
        menu_edit = Menu(menu_bar)
        menu_help = Menu(menu_bar)
        # 将一级菜单加入菜单中
        menu_bar.add_cascade(label="文件", menu=menu_file)
        menu_bar.add_cascade(label="编辑（但是没写）", menu=menu_edit)
        menu_bar.add_cascade(label="帮助（但是依旧没写）", menu=menu_help)
        # 给一级菜单加入实现、功能
        menu_file.add_command(label="新建", accelerator="ctrl+n", command=self.new_file)
        menu_file.add_command(label="打开", accelerator="ctrl+o", command=self.open_file)
        menu_file.add_command(label="保存", accelerator="ctrl+s", command=self.save_file)
        menu_file.add_separator()
        menu_file.add_command(label="退出", accelerator="ctrl+q", command=root.quit)
        # 向root中加入menu
        root["menu"] = menu_bar
        # 快捷键设置
        root.bind("<Control-n>", lambda event: self.new_file())
        root.bind("<Control-o>", lambda event: self.open_file())
        root.bind("<Control-s>", lambda event: self.save_file())
        root.bind("<Control-q>", lambda event: root.quit())
        # 文本框设置
        self.text_pad = Text(root, width=50, height=30)
        self.text_pad.place(x=0, y=0)
        # 右键跟随菜单设置
        self.context_menu = Menu(root)
        self.context_menu.add_command(label="别点了，没用的", command=self.test)
        root.bind("<Button-3>", self.create_context_menu)
        # 实现多选，还没写完
        self.CheckVar1 = BooleanVar()
        self.CheckVar2 = BooleanVar()
        self.CheckVar1.set(True)  # 预设为勾选
        self.C1 = Checkbutton(self.master, text="RUN", variable=self.CheckVar1, height=2,
                              width=8, anchor='w')
        self.C2 = Checkbutton(self.master, text="GOOGLE", variable=self.CheckVar2, height=2,
                              width=8, anchor='w')
        self.C1.place(x=0, y=400)
        self.C2.place(x=0, y=450)

    def create_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def open_file(self):
        self.text_pad.delete("1.0", "end")
        try:  # 避免编码错误，所以偶尔会需要打开两次
            with open(askopenfilename()) as f:
                self.text_pad.insert(INSERT, f.read())
                self.file_name = f.name
        except UnicodeDecodeError:
            with open(askopenfilename(), encoding='utf-8') as f:
                self.text_pad.insert(INSERT, f.read())
                self.file_name = f.name

    def new_file(self):
        self.file_name = asksaveasfilename(title="另存为", initialfile="未命名.txt", filetypes=[("文本文档", "*.txt")],
                                           defaultextension=".txt")
        self.save_file()

    def save_file(self):
        with open(self.file_name, "w") as f:
            c = self.text_pad.get(1.0, END)
            f.write(c)

    def test(self):  # 占位置用的
        pass


root = Tk()
root.geometry("500x500+200+300")
root.title("一个经典的GUI程序类的测试")
app = Application(master=root)
root.mainloop()
