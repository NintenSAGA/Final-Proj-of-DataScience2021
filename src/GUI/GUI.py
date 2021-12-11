import tkinter.font
from tkinter import *
import another_paper
import reptile
from tkinter.font import *


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.canvas = None
        self.create_widget()

    def create_widget(self):
        self.canvas = Canvas(self.master, bg='white', width=750, height=750, highlightcolor='pink')
        self.canvas.pack()
        ft0 = Font(family="微软雅黑", size=14, weight=tkinter.font.BOLD)
        Button(self.canvas, text="  爬取文书 ", bg="cadetblue", command=self.show_reptile, fg='white',
               font=ft0, anchor='w').place(x=300, y=250)
        Button(self.canvas, text="自动化标注", bg="cadetblue", command=self.show_another_paper, fg='white',
               font=ft0, anchor='w').place(x=300, y=450)

    def show_another_paper(self):
        another_paper.Windows(self.master)

    def show_reptile(self):
        reptile.Windows(self.master)


if __name__ == '__main__':
    root = Tk()
    root.resizable(False, False)
    root.geometry("750x750+300+300")
    root.title("自动化爬取和标注")
    app = Application(master=root)
    root.mainloop()
