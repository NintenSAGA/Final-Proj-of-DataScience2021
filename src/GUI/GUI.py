from tkinter import *
# from tkinter import messagebox
import another_paper


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.text_pad = None
        self.pack()
        self.create_widget()
        self.file_name = None
        root.resizable(False, False)

    def create_widget(self):
        # 实现多选，还没写完
        self.check_var1 = BooleanVar()
        self.check_var2 = BooleanVar()
        self.check_var1.set(True)  # 预设为勾选
        c1 = Checkbutton(self.master, text="RUN", variable=self.check_var1, height=2, width=8, anchor='w')
        c2 = Checkbutton(self.master, text="GOOGLE", variable=self.check_var2, height=2, width=8, anchor='w')
        c1.place(x=0, y=400)
        c2.place(x=0, y=450)

        Button(text="go", bg="cadetblue", command=self.show_single).pack()
        # n = tkinter.StringVar()
        # month_choose = tkinter.ttk.Combobox(root, width=27, textvariable=n)
        # month_choose['values'] = ('January', 'February', 'March', 'April')
        # month_choose.pack()
        # month_choose.current()
        # month_choose.bind('<<ComboboxSelected>>', self.open_file)

    def show_single(self):
        another_paper.Windows(self.master)


if __name__ == '__main__':
    root = Tk()
    root.geometry("1000x700+500+500")
    root.title("自动化爬取和标注")
    app = Application(master=root)
    root.mainloop()
