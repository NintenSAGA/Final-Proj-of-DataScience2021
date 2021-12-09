import tkinter


class Windows:
    def __init__(self, parent):
        self.root = tkinter.Toplevel()
        self.parent = parent
        self.root.geometry("%dx%d" % (1000, 700))  # 窗体尺寸
        self.root.title("单组件的pack布局演示")  # 窗体标题
        self.root.grab_set()
        self.root.resizable(False, False)