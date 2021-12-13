from tkinter import Frame, Button, Canvas, Tk
from tkinter.font import Font, BOLD
from src.GUI import anno_page, crawler_page

app = None


def launch():
    global app
    root = Tk()
    root.resizable(False, False)
    root.geometry("500x500+300+300")
    root.title("自动化爬取和标注")
    app = Application(master=root)
    root.mainloop()


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.canvas = None
        self.create_widget()
        self.obj_anno_page = None
        self.obj_crawler_page = None

    def create_widget(self):
        self.canvas = Canvas(self.master, bg='white', width=750, height=750, highlightcolor='pink')
        self.canvas.pack()
        ft0 = Font(family="微软雅黑", size=14, weight=BOLD)
        Button(self.canvas, text="  爬取文书 ", bg="cadetblue", command=self.show_crawler_page, fg='black',
               font=ft0, anchor='w').place(x=185, y=125)
        Button(self.canvas, text="自动化标注", bg="cadetblue", command=self.show_anno_page, fg='black',
               font=ft0, anchor='w').place(x=185, y=275)

    def show_anno_page(self):
        self.obj_anno_page = anno_page.Windows(self.master)

    def show_crawler_page(self):
        self.obj_crawler_page = crawler_page.Windows(self.master)
