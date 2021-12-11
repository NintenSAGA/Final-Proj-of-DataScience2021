from tkinter import *
# from tkinter import messagebox
import another_paper


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widget()

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

    def show_single(self):
        another_paper.Windows(self.master)


if __name__ == '__main__':
    root = Tk()
    root.geometry("500x500+200+300")
    root.title("一个经典的GUI程序类的测试")
    app = Application(master=root)
    root.mainloop()
