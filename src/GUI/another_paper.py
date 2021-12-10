from tkinter import *
from tkinter.filedialog import *
from tkinter.scrolledtext import *
import tkinter.ttk


class Windows:
    def __init__(self, parent):
        self.root = Toplevel()
        self.parent = parent
        self.root.geometry("%dx%d" % (1200, 700))  # 窗体尺寸
        self.root.title("自动化爬取和标注")  # 窗体标题
        self.root.grab_set()
        self.root.resizable(False, False)
        self.text_pad = None
        self.create_menu()
        self.file_name = None
        self.create_text_pad()
        self.create_dire_label_and_entry()
        self.create_tab_basic_information()

    def create_menu(self):
        # 建立一个菜单
        menu_bar = Menu(self.root)
        # 建立一级菜单
        menu_file = Menu(menu_bar)
        menu_edit = Menu(menu_bar)
        menu_help = Menu(menu_bar)
        # 将一级菜单加入菜单中
        menu_bar.add_cascade(label="文件(F)", menu=menu_file)
        menu_bar.add_cascade(label="编辑(E)", menu=menu_edit)
        menu_bar.add_cascade(label="帮助(H)", menu=menu_help)
        # 给一级菜单加入实现、功能
        menu_file.add_command(label="新建", accelerator="ctrl+n", command=self.new_file)
        menu_file.add_command(label="打开", accelerator="ctrl+o", command=self.open_file)
        menu_file.add_command(label="保存", accelerator="ctrl+s", command=self.save_file)
        menu_file.add_separator()
        menu_file.add_command(label="退出", accelerator="ctrl+q", command=self.root.quit)
        # 向root中加入menu
        self.root["menu"] = menu_bar
        # 快捷键设置
        self.root.bind("<Control-n>", lambda event: self.new_file())
        self.root.bind("<Control-o>", lambda event: self.open_file())
        self.root.bind("<Control-s>", lambda event: self.save_file())
        self.root.bind("<Control-q>", lambda event: self.root.quit())
        # 右键跟随菜单设置
        self.context_menu = Menu(self.root)
        self.context_menu.add_command(label="别点了，没用的", command=self.test)
        self.root.bind("<Button-3>", self.create_context_menu)

        # 文本框设置
    def create_text_pad(self):
        self.text_pad = ScrolledText(self.root, width=70, height=40)
        self.text_pad.place(x=50, y=80)

        # 显示文件夹的当前位置
    def create_dire_label_and_entry(self):
        pass

    def create_tab_basic_information(self):
        tab_control = tkinter.ttk.Notebook(self.root)
        first_tab = tkinter.ttk.Frame(tab_control)
        tab_control.add(first_tab, text='姓名')
        second_tab = tkinter.ttk.Frame(tab_control)
        tab_control.add(second_tab, text='法院')
        tab_control.place(x=700, y=50)
        mighty = tkinter.ttk.Labelframe(first_tab, text='Mighty')
        mighty.grid(column=0, row=0, padx=8, pady=4)
        self.create_tab1_information(mighty)

    def create_tab1_information(self, mighty):
        self.check_var3 = BooleanVar()
        self.check_var4 = BooleanVar()
        self.check_var3.set(True)  # 预设为勾选
        check_button1 = Checkbutton(mighty, text="RUN", variable=self.check_var3, anchor='w')
        check_button2 = Checkbutton(mighty, text="google", variable=self.check_var4, anchor='w')
        check_button1.pack()
        check_button2.pack()

    def create_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def open_file(self):
        self.text_pad.delete('1.0', 'end')
        # 避免编码错误，所以偶尔会需要打开两次
        try:
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
