from tkinter import *
from tkinter.filedialog import *
from tkinter.scrolledtext import *
from tkinter.font import *
from src.GUI.common import get_ft
import tkinter.ttk


class Panel:
    def __init__(self, parent):
        self.root = Toplevel()
        self.parent = parent
        self.root.geometry("%dx%d" % (1200, 700))  # 窗体尺寸
        self.root.title("自动化爬取和标注")  # 窗体标题
        self.root.resizable(False, False)  # 窗口大小不可变
        self.big_canvas = None
        self.text_pad = None
        self.create_menu()
        self.create_canvas()
        self.file_name = None
        self.create_text_pad()
        self.create_dire_label_and_entry()
        self.create_tab_basic_information()
        self.create_special_information()

    def create_menu(self):
        # 建立一个菜单
        menu_bar = Menu(self.root)
        # 建立一级菜单
        menu_file = Menu(menu_bar)
        menu_edit = Menu(menu_bar)
        menu_help = Menu(menu_bar)
        # 加入一级菜单
        menu_bar.add_cascade(label="文件(F)", menu=menu_file)
        menu_bar.add_cascade(label="编辑(E)", menu=menu_edit)
        menu_bar.add_cascade(label="帮助(H)", menu=menu_help)
        # 加入二级菜单
        menu_file.add_command(label="新建", accelerator="ctrl+n", command=self.new_file)
        menu_file.add_command(label="打开", accelerator="ctrl+o", command=self.open_file)
        menu_file.add_command(label="保存", accelerator="ctrl+s", command=self.save_file)
        # menu_file.add_separator()
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

        # 画布填充（其实是为了实现分割线）
    def create_canvas(self):
        self.big_canvas = Canvas(self.root, bg='white', width=1200, height=700, highlightcolor='pink')
        self.big_canvas.create_line(600, 25, 600, 675)
        self.big_canvas.pack()

        # 文本框设置，带滚动条的那种
    def create_text_pad(self):
        self.text_pad = ScrolledText(self.big_canvas, width=65, height=35, bg='white',
                                     highlightcolor='black', highlightbackground='black')
        self.text_pad.place(x=50, y=135)

        # 显示文件夹的当前位置
    def create_dire_label_and_entry(self):
        ft1 = get_ft(14)
        ft2 = get_ft(12)
        Label(self.big_canvas, text='文件夹：', font=ft1, bg='white').place(x=50, y=30)
        Entry(self.big_canvas, borderwidth=4, width=20).place(x=125, y=30)
        Label(self.big_canvas, text='已找到文书共xx份', font=ft2, bg='white', fg='blue').place(x=390, y=28)

        # 显示基本信息
    def create_tab_basic_information(self):
        tab_control = tkinter.ttk.Notebook(self.big_canvas, height=200, width=400)

        label_basic_information = Label(tab_control, text='基本信息', fg='blue')
        label_basic_information.place(x=325, y=0)

        first_tab = tkinter.ttk.Frame(tab_control)
        tab_control.add(first_tab, text='姓名')

        second_tab = tkinter.ttk.Frame(tab_control)
        tab_control.add(second_tab, text='法院')

        tab_control.place(x=700, y=50)
        self.create_basic_tab_information(first_tab)

        # 给基本信息中的tab进行信息填入
    def create_basic_tab_information(self, first_tabel):
        self.check_var3 = BooleanVar()
        self.check_var4 = BooleanVar()
        self.check_var3.set(True)  # 预设为勾选
        check_button1 = Checkbutton(first_tabel, text="run", variable=self.check_var3, anchor='w', padx=10, pady=10)
        check_button2 = Checkbutton(first_tabel, text="google", variable=self.check_var4, anchor='w', padx=10, pady=10)
        check_button1.place(x=0, y=0)
        check_button2.place(x=0, y=40)

        # 特殊信息
    def create_special_information(self):
        tab_control_special = tkinter.ttk.Notebook(self.big_canvas, height=200, width=400)

        label_special_information = Label(tab_control_special, text='特殊信息', fg='blue')
        label_special_information.place(x=325, y=0)

        first_tab = tkinter.ttk.Frame(tab_control_special)
        tab_control_special.add(first_tab, text='血液酒精浓度')

        tab_control_special.place(x=700, y=350)
        self.create_special_tab_information(first_tab)

        # 特殊信息tab填充
    def create_special_tab_information(self, first_tabel):
        self.check_var5 = BooleanVar()
        self.check_var6 = BooleanVar()
        self.check_var5.set(True)  # 预设为勾选
        check_button1 = Checkbutton(first_tabel, text="run", variable=self.check_var5, anchor='w', padx=10, pady=10)
        check_button2 = Checkbutton(first_tabel, text="google", variable=self.check_var6, anchor='w', padx=10, pady=10)
        check_button1.place(x=0, y=0)
        check_button2.place(x=0, y=40)

        # 实现右键菜单的跟随
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

    def test(self):  # 占位置用
        pass
